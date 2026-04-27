from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    height: float
    target_weight: float
    weight_unit: str
    measurement_unit: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    height: Optional[float] = None
    target_weight: Optional[float] = None
    weight_unit: Optional[str] = None
    measurement_unit: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    height: float
    target_weight: float
    weight_unit: str
    measurement_unit: str
    created_at: datetime

    model_config = {"from_attributes": True}
