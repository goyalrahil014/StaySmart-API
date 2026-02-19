"""
Database setup for SQLAlchemy.

Provides:
- `engine` : SQLAlchemy Engine
- `SessionLocal` : sessionmaker
- `Base` : declarative base for models
- `get_db` : FastAPI dependency generator that yields a DB session

This file is intentionally minimal and reads the database URL from app.core.config.settings.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL

# SQLite needs check_same_thread; only set when using sqlite URL
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
