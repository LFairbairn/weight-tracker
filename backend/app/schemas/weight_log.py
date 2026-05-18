from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class WeightLogCreate(BaseModel):
    date: date
    weight_kg: Optional[float] = None
    waist_cm: Optional[float] = None
    notes: Optional[str] = None


class WeightLogUpdate(BaseModel):
    date: Optional[date] = None
    weight_kg: Optional[float] = None
    waist_cm: Optional[float] = None
    notes: Optional[str] = None


class WeightLogResponse(BaseModel):
    id: int
    user_id: int
    date: date
    weight_kg: Optional[float] = None
    waist_cm: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
