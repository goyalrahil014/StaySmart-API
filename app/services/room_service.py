"""
Service layer for room-related business logic.
"""
from sqlalchemy.orm import Session
from app.models.room import Room
from app.models.hotel import Hotel
from app.schemas.room import RoomCreate

def create_room(db: Session, hotel_id: int, room_in: RoomCreate, owner_id: int) -> Room:
    """
    Create a new room for a hotel, ensuring only the hotel owner can add rooms.
    """
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise ValueError("Hotel not found")
    if hotel.owner_id != owner_id:
        raise PermissionError("Only the hotel owner can add rooms")
    room = Room(**room_in.model_dump(), hotel_id=hotel_id)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def list_rooms(db: Session, hotel_id: int):
    """
    List all rooms for a given hotel.
    """
    return db.query(Room).filter(Room.hotel_id == hotel_id).all()
