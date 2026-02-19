"""
Custom exception classes and handlers for clean error responses.
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.main import app

class OverlappingBookingException(HTTPException):
    def __init__(self, detail="Room already booked for these dates"):
        super().__init__(status_code=400, detail=detail)

@app.exception_handler(OverlappingBookingException)
async def overlapping_booking_exception_handler(request: Request, exc: OverlappingBookingException):
    return JSONResponse(status_code=400, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )
