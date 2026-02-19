# Testing Guide for StaySmart API

## Test Suite Overview

The project now has a comprehensive test suite located in `tests/test_api_fresh.py` with **21 test cases** covering all major API endpoints and workflows.

## Running Tests

### Run All Tests
```bash
pytest tests/test_api_fresh.py -v
```

### Run Specific Test
```bash
pytest tests/test_api_fresh.py::test_create_hotel -v
```

### Run with Coverage
```bash
pytest tests/test_api_fresh.py --cov=app --cov-report=html
```

## Test Coverage

### Authentication Tests (6 tests)
- ✅ `test_register_new_user` - Register a new user successfully
- ✅ `test_register_duplicate_email` - Prevent duplicate email registration
- ✅ `test_login_valid_credentials` - Login with correct credentials
- ✅ `test_login_invalid_credentials` - Reject invalid passwords
- ✅ `test_login_nonexistent_user` - Reject non-existent users
- ✅ `test_health_check` - API health check endpoint

### Hotel Tests (5 tests)
- ✅ `test_create_hotel` - Create a new hotel
- ✅ `test_create_hotel_unauthorized` - Prevent unauthorized hotel creation
- ✅ `test_list_hotels` - List all hotels
- ✅ `test_get_hotel_by_id` - Retrieve specific hotel
- ✅ `test_get_nonexistent_hotel` - Handle non-existent hotel requests

### Room Tests (4 tests)
- ✅ `test_create_room` - Create a room for a hotel
- ✅ `test_create_room_unauthorized` - Prevent unauthorized room creation
- ✅ `test_list_rooms_for_hotel` - List all rooms for a hotel
- ✅ `test_list_rooms_for_nonexistent_hotel` - Handle non-existent hotel

### Booking Tests (5 tests)
- ✅ `test_create_booking` - Create a booking for a room
- ✅ `test_create_booking_unauthorized` - Prevent unauthorized bookings
- ✅ `test_create_overlapping_booking` - Prevent double booking
- ✅ `test_list_user_bookings` - List user's bookings
- ✅ `test_list_bookings_unauthorized` - Prevent unauthorized access

### Integration Test (1 test)
- ✅ `test_full_booking_workflow` - Complete workflow from registration to booking

## Test Features

### Database Cleanup
Tests use a `reset_database` fixture in `conftest.py` that automatically:
- Drops all tables before each test
- Creates fresh tables
- Ensures test isolation

### Authentication Helper
The `register_and_login()` helper function:
- Registers a new user (or skips if already exists)
- Logs in the user
- Returns authentication headers for API calls

### Dynamic Test Data
Tests use dynamic emails and dates to avoid conflicts and ensure relevance.

## Issues Fixed

### 1. Database Schema Mismatch
**Problem**: Database table had `room_number` column but models/schemas used `number`.
**Solution**: Updated all models and schemas to use consistent field name `number`.

### 2. Multiple Base Classes
**Problem**: Two different SQLAlchemy Base classes (`app.db.session.Base` and `app.core.database.Base`).
**Solution**: Unified all models to use `app.core.database.Base`.

### 3. Duplicate Model Definitions
**Problem**: Models defined in both `app/models/hotel.py` (all-in-one) and separate files.
**Solution**: Separated models into individual files with proper imports.

### 4. Missing created_at Field
**Problem**: Booking schema expected `created_at` but model didn't have it.
**Solution**: Added `created_at` field to Booking model.

### 5. Test Database Persistence
**Problem**: Tests failed due to stale data from previous runs.
**Solution**: Added automatic database reset fixture in conftest.py.

## Deprecation Warnings (Non-Critical)

The following warnings appear but don't affect functionality:

1. **Pydantic V2 Config** - `app/core/config.py` uses old `class Config` style
2. **FastAPI on_event** - `app/main.py` uses deprecated `@app.on_event()`
3. **datetime.utcnow()** - Should use `datetime.now(datetime.UTC)`
4. **Pydantic .dict()** - Should use `.model_dump()` instead

These can be addressed in future refactoring without breaking tests.

## Test Results Summary

```
====================== 21 passed, 37 warnings in 22.10s =======================
```

All tests passing! ✅
