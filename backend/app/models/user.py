from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func
from datetime import datetime

class User(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    height: Mapped[float] = mapped_column()
    target_weight: Mapped[float] = mapped_column()
    weight_unit: Mapped[str] = mapped_column()
    measurement_unit: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=func.now())

