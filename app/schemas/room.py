from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

class RoomBase(BaseModel):
    """Base schema for Room."""
    number: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Room number/identifier",
        examples=["101", "A-201", "Presidential Suite"]
    )
    type: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Room type",
        examples=["Single", "Double", "Suite", "Deluxe"]
    )
    price: float = Field(
        ...,
        gt=0,
        le=100000,
        description="Room price per night (must be positive)",
        examples=[99.99, 150.00, 500.00]
    )
class RoomCreate(RoomBase):
    """Schema for creating a new room."""
    pass


class RoomOut(RoomBase):
    """Schema for room response."""
    id: int = Field(..., description="Room ID", gt=0)
    hotel_id: int = Field(..., description="Hotel ID", gt=0)

    model_config = ConfigDict(from_attributes=True)