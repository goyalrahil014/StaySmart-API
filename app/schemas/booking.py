from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from datetime import date, datetime
from typing import Optional

class BookingBase(BaseModel):
    """Base schema for Booking."""
    from_date: date = Field(
        ...,
        description="Check-in date (YYYY-MM-DD)",
        examples=["2024-03-01"]
    )
    to_date: date = Field(
        ...,
        description="Check-out date (YYYY-MM-DD)",
        examples=["2024-03-05"]
    )

class BookingCreate(BookingBase):
    """Schema for creating a new booking."""
    room_id: int = Field(
        ...,
        gt=0,
        description="Room ID to book",
        examples=[1]
    )

class BookingOut(BookingBase):
    """Schema for booking response."""
    id: int = Field(..., description="Booking ID", gt=0)
    user_id: int = Field(..., description="User ID who made the booking", gt=0)
    room_id: int = Field(
        ...,
        gt=0,
        description="Room ID to book",
        examples=[1]
    )
    status: str = Field(
        ...,
        description="Booking status",
        examples=["confirmed", "cancelled", "completed"]
    )
    created_at: datetime = Field(..., description="Booking creation timestamp")

    model_config = ConfigDict(from_attributes=True)