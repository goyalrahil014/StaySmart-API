
"""
StaySmart API - Main FastAPI application entry point.

This file initializes the FastAPI app, includes all routers, and sets up startup/shutdown events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth, hotels, rooms, bookings
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	Lifespan context manager for startup and shutdown events.
	Handles application lifecycle management.
	"""
	# Startup logic
	print("🚀 StaySmart API starting up...")
	yield
	# Shutdown logic
	print("🛑 StaySmart API shutting down...")


# Create the FastAPI application instance with lifespan
app = FastAPI(
	title="StaySmart API",
	description="Backend for managing hotels, rooms, and bookings.",
	version="1.0.0",
	docs_url="/docs",
	redoc_url="/redoc",
	lifespan=lifespan
)


# Register API routers for modular endpoint organization
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(hotels.router, prefix="/hotels", tags=["Hotels"])
app.include_router(rooms.router)
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])

# Health check endpoint for test coverage
@app.get("/")
def health_check():
	"""
	Root endpoint for health check.
	Returns status OK.
	"""
	return {"status": "ok"}
