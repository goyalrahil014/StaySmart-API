"""
Room router: RESTful endpoints for creating and listing rooms, using service layer and dependencies.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.room import RoomCreate, RoomOut
from app.services.room_service import create_room, list_rooms
from app.models.user import User

router = APIRouter(
    prefix="/hotels/{hotel_id}/rooms",
    tags=["Rooms"]
)

@router.post(
    "/",
    response_model=RoomOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new room for a hotel"
)
def create_room_endpoint(
    hotel_id: int,
    room_in: RoomCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Create a new room for a hotel. Only the hotel owner can add rooms.
    """
    try:
        return create_room(db, hotel_id, room_in, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get(
    "/",
    response_model=List[RoomOut],
    status_code=status.HTTP_200_OK,
    summary="List all rooms for a hotel"
)
def list_rooms_endpoint(
    hotel_id: int,
    db: Session = Depends(get_db)
):
    """
    List all rooms for a given hotel.
    """
    return list_rooms(db, hotel_id)
