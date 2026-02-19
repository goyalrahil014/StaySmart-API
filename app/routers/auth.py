"""
Authentication router: register, login endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserOut
from app.core.security import get_password_hash, verify_password, create_access_token
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    except ValueError:
        raise HTTPException(status_code=400, detail="Password must be at most 72 bytes when encoded as UTF-8. Please use a shorter password.")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Password must be at most 72 bytes when encoded as UTF-8. Please use a shorter password.")
