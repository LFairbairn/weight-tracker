from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, func, Date
from datetime import datetime, date


class MedicationDose(Base):
    __tablename__ = "medication_doses"

    id: Mapped[int] = mapped_column(primary_key=True)
    medication_id: Mapped[int] = mapped_column(ForeignKey("medications.id"))
    dose: Mapped[float] = mapped_column()
    unit: Mapped[str] = mapped_column(String(10))
    date_changed: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
