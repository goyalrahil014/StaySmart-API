"""
Booking endpoints: create booking, list user bookings.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.models.room import Room
from app.models.booking import Booking
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingOut
from app.routers.hotels import get_current_user

router = APIRouter()

def send_booking_email(booking_id: int):
    # Simulate sending an email (background task)
    print(f"Email sent for booking {booking_id}")

@router.post("/", response_model=BookingOut)
def create_booking(booking_in: BookingCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Check for overlapping bookings
    overlaps = db.query(Booking).filter(
        Booking.room_id == booking_in.room_id,
        Booking.from_date < booking_in.to_date,
        Booking.to_date > booking_in.from_date
    ).first()
    if overlaps:
        raise HTTPException(status_code=400, detail="Room already booked for these dates")
    booking = Booking(**booking_in.model_dump(), user_id=user.id, status="confirmed")
    db.add(booking)
    db.commit()
    db.refresh(booking)
    background_tasks.add_task(send_booking_email, booking.id)
    return booking

@router.get("/users/me/bookings", response_model=List[BookingOut])
def list_user_bookings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Booking).filter(Booking.user_id == user.id).all()
