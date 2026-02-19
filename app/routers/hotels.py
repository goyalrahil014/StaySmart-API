"""
Hotel endpoints: create, list, retrieve, delete (admin only).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.hotel import Hotel
from app.models.user import User, UserRole
from app.schemas.hotel import HotelCreate, HotelOut
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.post("/", response_model=HotelOut)
def create_hotel(hotel_in: HotelCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    hotel = Hotel(**hotel_in.model_dump(), owner_id=user.id)
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return hotel

@router.get("/", response_model=List[HotelOut])
def list_hotels(db: Session = Depends(get_db)):
    return db.query(Hotel).all()

@router.get("/{hotel_id}", response_model=HotelOut)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@router.delete("/{hotel_id}", status_code=204)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(hotel)
    db.commit()
    return None
