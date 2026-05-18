from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class MedicationCreate(BaseModel):
    name: str
    start_date: date


class MedicationUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None


class MedicationResponse(BaseModel):
    id: int
    user_id: int
    name: str
    start_date: date
    created_at: datetime

    model_config = {"from_attributes": True}
