from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User


def get_current_user(db: Session) -> User:
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
