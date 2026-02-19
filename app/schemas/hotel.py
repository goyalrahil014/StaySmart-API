from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

class HotelBase(BaseModel):
    """Base schema for Hotel."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Hotel name",
        examples=["Grand Plaza Hotel"]
    )
    location: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Hotel location/address",
        examples=["123 Main St, New York, NY 10001"]
    )
class HotelCreate(HotelBase):
    """Schema for creating a new hotel."""
    pass

class HotelOut(HotelBase):
    """Schema for hotel response."""
    id: int = Field(..., description="Hotel ID", gt=0)
    owner_id: int = Field(..., description="Owner user ID", gt=0)

    model_config = ConfigDict(from_attributes=True)