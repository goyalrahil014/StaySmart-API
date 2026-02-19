"""
Pytest configuration file for test setup and fixtures.
"""

import sys
from pathlib import Path
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base

# Force use of .env.test for test DB
os.environ['ENV_FILE'] = '.env.test'
from app.core.config import settings

# Import all models so Base.metadata knows about them
from app.models.user import User
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.booking import Booking

# Add the project root to Python path so tests can import from app
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Create test database engine
engine = create_engine(settings.DATABASE_URL)

@pytest.fixture(scope="function", autouse=True)
def reset_database():
    """Reset database before each test by dropping and recreating all tables."""
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Create all tables fresh
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup after test if needed

