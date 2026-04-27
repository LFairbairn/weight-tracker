from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.weight_log import WeightLog
from app.schemas.weight_log import WeightLogCreate, WeightLogUpdate, WeightLogResponse

router = APIRouter(prefix="/weight-logs", tags=["weight-logs"])

# Stage 1: single-user app, user id is always 1
CURRENT_USER_ID = 1


@router.get("", response_model=List[WeightLogResponse])
def list_weight_logs(db: Session = Depends(get_db)):
    return db.query(WeightLog).filter(WeightLog.user_id == CURRENT_USER_ID).order_by(WeightLog.date).all()


@router.post("", response_model=WeightLogResponse, status_code=201)
def create_weight_log(log_in: WeightLogCreate, db: Session = Depends(get_db)):
    log = WeightLog(user_id=CURRENT_USER_ID, **log_in.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/{log_id}", response_model=WeightLogResponse)
def get_weight_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(WeightLog).filter(WeightLog.id == log_id, WeightLog.user_id == CURRENT_USER_ID).first()
    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")
    return log


@router.patch("/{log_id}", response_model=WeightLogResponse)
def update_weight_log(log_id: int, log_in: WeightLogUpdate, db: Session = Depends(get_db)):
    log = db.query(WeightLog).filter(WeightLog.id == log_id, WeightLog.user_id == CURRENT_USER_ID).first()
    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")
    for field, value in log_in.model_dump(exclude_unset=True).items():
        setattr(log, field, value)
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=204)
def delete_weight_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(WeightLog).filter(WeightLog.id == log_id, WeightLog.user_id == CURRENT_USER_ID).first()
    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")
    db.delete(log)
    db.commit()
