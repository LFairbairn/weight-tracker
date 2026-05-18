from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.weight_log import WeightLog
from app.schemas.weight_log import WeightLogCreate, WeightLogResponse, WeightLogUpdate

router = APIRouter(prefix="/weight-logs", tags=["weight-logs"])


@router.get("", response_model=List[WeightLogResponse])
def list_weight_logs(db: Session = Depends(get_db)):
    user = get_current_user(db)
    return db.query(WeightLog).filter(WeightLog.user_id == user.id).order_by(WeightLog.date).all()


@router.post("", response_model=WeightLogResponse, status_code=201)
def create_weight_log(log_in: WeightLogCreate, db: Session = Depends(get_db)):
    user = get_current_user(db)
    log = WeightLog(user_id=user.id, **log_in.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/{log_id}", response_model=WeightLogResponse)
def get_weight_log(log_id: int, db: Session = Depends(get_db)):
    user = get_current_user(db)
    log = db.query(WeightLog).filter(WeightLog.id == log_id, WeightLog.user_id == user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")
    return log


@router.patch("/{log_id}", response_model=WeightLogResponse)
def update_weight_log(log_id: int, log_in: WeightLogUpdate, db: Session = Depends(get_db)):
    user = get_current_user(db)
    log = db.query(WeightLog).filter(WeightLog.id == log_id, WeightLog.user_id == user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")
    for field, value in log_in.model_dump(exclude_unset=True).items():
        setattr(log, field, value)
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=204)
def delete_weight_log(log_id: int, db: Session = Depends(get_db)):
    user = get_current_user(db)
    log = db.query(WeightLog).filter(WeightLog.id == log_id, WeightLog.user_id == user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")
    db.delete(log)
    db.commit()
