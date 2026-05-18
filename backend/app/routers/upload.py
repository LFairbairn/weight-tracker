import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.medication import Medication
from app.models.medication_dose import MedicationDose
from app.models.user import User
from app.models.weight_log import WeightLog

router = APIRouter(prefix="/upload", tags=["uploads"])

@router.post("/weight-logs")
async def upload_weight_logs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = get_current_user(db)
    contents = await file.read()
    text = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    db.query(WeightLog).filter(WeightLog.user_id == user.id).delete()

    inserted = 0
    for row in reader:
        if not row.get("date") or not row.get("weight_kg"):
            continue
        log = WeightLog(
            user_id=user.id,
            date=datetime.strptime(row["date"].strip(), "%Y-%m-%d").date(),
            weight_kg=float(row["weight_kg"]),
            notes=row.get("notes", "").strip() or None,
        )
        db.add(log)
        inserted += 1

    db.commit()
    return {"inserted": inserted}

@router.post("/medication-doses")
async def upload_medication_doses(file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = get_current_user(db)
    contents = await file.read()
    text = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    rows = list(reader)
    if not rows:
        return {"inserted": 0}

    db.query(MedicationDose).filter(
        MedicationDose.medication_id.in_(
            db.query(Medication.id).filter(Medication.user_id == user.id)
        )
    ).delete(synchronize_session=False)
    db.query(Medication).filter(Medication.user_id == user.id).delete()

    medications = {}
    inserted = 0
    for row in rows:
        name = row["medication_name"].strip()
        if name not in medications:
            start_date = datetime.strptime(row["date_changed"].strip(), "%Y-%m-%d").date()
            med = Medication(user_id=user.id, name=name, start_date=start_date)
            db.add(med)
            db.flush()
            medications[name] = med.id
        dose = MedicationDose(
            medication_id=medications[name],
            dose=float(row["dose"]),
            unit=row["unit"].strip(),
            date_changed=datetime.strptime(row["date_changed"].strip(), "%Y-%m-%d").date(),
        )
        db.add(dose)
        inserted += 1

    db.commit()
    return {"inserted": inserted}

@router.post("/user")
async def upload_user(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    text = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    rows = list(reader)
    if not rows:
        return {"error": "empty file"}

    row = rows[0]
    existing = db.query(User).first()
    if existing:
        db.query(MedicationDose).filter(
            MedicationDose.medication_id.in_(
                db.query(Medication.id).filter(Medication.user_id == existing.id)
            )
        ).delete(synchronize_session=False)
        db.query(Medication).filter(Medication.user_id == existing.id).delete()
        db.query(WeightLog).filter(WeightLog.user_id == existing.id).delete()
        db.query(User).filter(User.id == existing.id).delete()
    user = User(
        name=row["name"].strip(),
        height=float(row["height_cm"]),
        target_weight=float(row["target_weight_kg"]),
        weight_unit="kg",
        measurement_unit="cm",
    )
    db.add(user)
    db.commit()
    return {"created": user.name}

@router.post("/reset")
def reset_data(db: Session = Depends(get_db)):
    existing = db.query(User).first()
    if existing:
        db.query(MedicationDose).filter(
            MedicationDose.medication_id.in_(
                db.query(Medication.id).filter(Medication.user_id == existing.id)
            )
        ).delete(synchronize_session=False)
        db.query(Medication).filter(Medication.user_id == existing.id).delete()
        db.query(WeightLog).filter(WeightLog.user_id == existing.id).delete()
        db.query(User).filter(User.id == existing.id).delete()
    db.commit()
    return {"reset": True}

