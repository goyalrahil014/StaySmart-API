"""
Service layer for user-related business logic.
"""
from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Retrieve a user by their ID.
    """
    return db.query(User).filter(User.id == user_id).first()
