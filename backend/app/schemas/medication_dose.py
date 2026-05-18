from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class MedicationDoseCreate(BaseModel):
    dose: float
    unit: str
    date_changed: date


class MedicationDoseUpdate(BaseModel):
    dose: Optional[float] = None
    unit: Optional[str] = None
    date_changed: Optional[date] = None


class MedicationDoseResponse(BaseModel):
    id: int
    medication_id: int
    dose: float
    unit: str
    date_changed: date
    created_at: datetime

    model_config = {"from_attributes": True}
