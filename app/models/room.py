"""
SQLAlchemy Room model with relationships.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)

    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")
