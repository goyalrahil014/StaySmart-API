from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base schema for User with email validation."""
    email: EmailStr = Field(
        ...,
        description="Valid email address",
        examples=["user@example.com"]
    )

class UserCreate(UserBase):
    """Schema for creating a new user with password validation."""
    password: str = Field(
        ...,
        min_length=4,
        max_length=72,
        description="Password must be 8-72 characters",
        examples=["securepass123"]
    )
class UserOut(UserBase):
    """Schema for user response (without password)."""
    id: int = Field(..., description="User ID", gt=0)
    role: str = Field(..., description="User role")
    created_at: datetime = Field(..., description="Account creation timestamp")

    model_config = ConfigDict(from_attributes=True)

