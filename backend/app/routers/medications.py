from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.deps import get_current_user
from app.models.medication import Medication
from app.models.medication_dose import MedicationDose
from app.schemas.medication import MedicationCreate, MedicationUpdate, MedicationResponse
from app.schemas.medication_dose import MedicationDoseCreate, MedicationDoseUpdate, MedicationDoseResponse

router = APIRouter(prefix="/medications", tags=["medications"])


@router.get("", response_model=List[MedicationResponse])
def list_medications(db: Session = Depends(get_db)):
    user = get_current_user(db)
    return db.query(Medication).filter(Medication.user_id == user.id).all()


@router.post("", response_model=MedicationResponse, status_code=201)
def create_medication(med_in: MedicationCreate, db: Session = Depends(get_db)):
    user = get_current_user(db)
    med = Medication(user_id=user.id, **med_in.model_dump())
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


@router.get("/{medication_id}", response_model=MedicationResponse)
def get_medication(medication_id: int, db: Session = Depends(get_db)):
    user = get_current_user(db)
    med = db.query(Medication).filter(Medication.id == medication_id, Medication.user_id == user.id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return med


@router.patch("/{medication_id}", response_model=MedicationResponse)
def update_medication(medication_id: int, med_in: MedicationUpdate, db: Session = Depends(get_db)):
    user = get_current_user(db)
    med = db.query(Medication).filter(Medication.id == medication_id, Medication.user_id == user.id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    for field, value in med_in.model_dump(exclude_unset=True).items():
        setattr(med, field, value)
    db.commit()
    db.refresh(med)
    return med


# --- Doses (nested under a medication) ---

@router.get("/{medication_id}/doses", response_model=List[MedicationDoseResponse])
def list_doses(medication_id: int, db: Session = Depends(get_db)):
    user = get_current_user(db)
    med = db.query(Medication).filter(Medication.id == medication_id, Medication.user_id == user.id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return db.query(MedicationDose).filter(MedicationDose.medication_id == medication_id).order_by(MedicationDose.date_changed).all()


@router.post("/{medication_id}/doses", response_model=MedicationDoseResponse, status_code=201)
def create_dose(medication_id: int, dose_in: MedicationDoseCreate, db: Session = Depends(get_db)):
    user = get_current_user(db)
    med = db.query(Medication).filter(Medication.id == medication_id, Medication.user_id == user.id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    dose = MedicationDose(medication_id=medication_id, **dose_in.model_dump())
    db.add(dose)
    db.commit()
    db.refresh(dose)
    return dose


@router.patch("/{medication_id}/doses/{dose_id}", response_model=MedicationDoseResponse)
def update_dose(medication_id: int, dose_id: int, dose_in: MedicationDoseUpdate, db: Session = Depends(get_db)):
    dose = db.query(MedicationDose).filter(MedicationDose.id == dose_id, MedicationDose.medication_id == medication_id).first()
    if not dose:
        raise HTTPException(status_code=404, detail="Dose not found")
    for field, value in dose_in.model_dump(exclude_unset=True).items():
        setattr(dose, field, value)
    db.commit()
    db.refresh(dose)
    return dose


@router.delete("/{medication_id}/doses/{dose_id}", status_code=204)
def delete_dose(medication_id: int, dose_id: int, db: Session = Depends(get_db)):
    dose = db.query(MedicationDose).filter(MedicationDose.id == dose_id, MedicationDose.medication_id == medication_id).first()
    if not dose:
        raise HTTPException(status_code=404, detail="Dose not found")
    db.delete(dose)
    db.commit()
