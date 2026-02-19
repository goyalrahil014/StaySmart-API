"""
Comprehensive API tests for StaySmart FastAPI project.
Tests all endpoints: authentication, hotels, rooms, and bookings.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

client = TestClient(app)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def register_and_login(email: str, password: str):
    """Helper to create a user and return auth headers."""
    # Register user (ignore if already exists, status 400 means duplicate)
    register_response = client.post("/auth/register", json={"email": email, "password": password})
    # Allow either successful registration (200/201) or duplicate email (400)
    if register_response.status_code not in (200, 201, 400):
        raise AssertionError(f"Registration failed with unexpected status {register_response.status_code}: {register_response.json()}")

    # Login and get token
    login_response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    if login_response.status_code != 200:
        raise AssertionError(f"Login failed for {email}: {login_response.json()}")
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ============================================================
# HEALTH CHECK TESTS
# ============================================================

def test_health_check():
    """Test the root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ============================================================
# AUTHENTICATION TESTS
# ============================================================

def test_register_new_user():
    """Test user registration with a new email."""
    email = f"newuser_{id(object())}@example.com"  # Generate unique email
    password = "securepass123"

    response = client.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code in (200, 201)
    body = response.json()
    assert "id" in body
    assert body["email"] == email
    assert "role" in body
    assert body["role"] == "user"


def test_register_duplicate_email():
    """Test registration with an already registered email."""
    email = "duplicate@example.com"
    password = "testpass"

    # Register first time
    client.post("/auth/register", json={"email": email, "password": password})
    
    # Try to register again with same email
    response = client.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_valid_credentials():
    """Test login with valid credentials."""
    email = "validuser@example.com"
    password = "validpass"

    # Register user first
    client.post("/auth/register", json={"email": email, "password": password})

    # Login
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid password."""
    email = "testuser@example.com"
    password = "correctpass"

    # Register user
    client.post("/auth/register", json={"email": email, "password": password})

    # Try login with wrong password
    response = client.post("/auth/login", data={"username": email, "password": "wrongpass"})
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_nonexistent_user():
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent@example.com", "password": "anypass"}
    )
    assert response.status_code == 401


# ============================================================
# HOTEL TESTS
# ============================================================

def test_create_hotel():
    """Test creating a new hotel."""
    headers = register_and_login("hotelowner@example.com", "hotelpass")

    hotel_data = {"name": "Grand Hotel", "location": "New York"}
    response = client.post("/hotels/", json=hotel_data, headers=headers)
    
    assert response.status_code in (200, 201)
    hotel = response.json()
    assert "id" in hotel
    assert hotel["name"] == "Grand Hotel"
    assert hotel["location"] == "New York"
    assert "owner_id" in hotel


def test_create_hotel_unauthorized():
    """Test creating a hotel without authentication."""
    hotel_data = {"name": "Unauthorized Hotel", "location": "Unknown"}
    response = client.post("/hotels/", json=hotel_data)
    assert response.status_code == 401


def test_list_hotels():
    """Test listing all hotels."""
    headers = register_and_login("listuser@example.com", "listpass")

    # Create a hotel first
    client.post("/hotels/", json={"name": "List Hotel", "location": "Boston"}, headers=headers)

    # List all hotels
    response = client.get("/hotels/")
    assert response.status_code == 200
    hotels = response.json()
    assert isinstance(hotels, list)
    assert len(hotels) > 0


def test_get_hotel_by_id():
    """Test retrieving a specific hotel by ID."""
    headers = register_and_login("gethotel@example.com", "getpass")

    # Create hotel
    create_response = client.post(
        "/hotels/",
        json={"name": "Specific Hotel", "location": "Chicago"},
        headers=headers
    )
    hotel_id = create_response.json()["id"]

    # Get hotel by ID
    response = client.get(f"/hotels/{hotel_id}")
    assert response.status_code == 200
    hotel = response.json()
    assert hotel["id"] == hotel_id
    assert hotel["name"] == "Specific Hotel"


def test_get_nonexistent_hotel():
    """Test retrieving a hotel that doesn't exist."""
    response = client.get("/hotels/999999")
    assert response.status_code == 404


# ============================================================
# ROOM TESTS
# ============================================================

def test_create_room():
    """Test creating a room for a hotel."""
    headers = register_and_login("roomcreator@example.com", "roompass")

    # Create hotel first
    hotel_response = client.post(
        "/hotels/",
        json={"name": "Room Hotel", "location": "Miami"},
        headers=headers
    )
    hotel_id = hotel_response.json()["id"]

    # Create room with correct schema field 'number' (not 'room_number')
    room_data = {
        "number": "101",
        "type": "Deluxe",
        "price": 150.0
    }
    response = client.post(f"/hotels/{hotel_id}/rooms/", json=room_data, headers=headers)
    
    assert response.status_code in (200, 201), f"Failed to create room: {response.json()}"
    room = response.json()
    assert "id" in room
    assert room["hotel_id"] == hotel_id


def test_create_room_unauthorized():
    """Test creating a room without authentication."""
    room_data = {"number": "102", "type": "Standard", "price": 100.0}
    response = client.post("/hotels/1/rooms/", json=room_data)
    assert response.status_code == 401


def test_list_rooms_for_hotel():
    """Test listing all rooms for a specific hotel."""
    headers = register_and_login("roomlister@example.com", "listroom")

    # Create hotel
    hotel_response = client.post(
        "/hotels/",
        json={"name": "List Rooms Hotel", "location": "Seattle"},
        headers=headers
    )
    hotel_id = hotel_response.json()["id"]

    # Create multiple rooms
    for i in range(3):
        client.post(
            f"/hotels/{hotel_id}/rooms/",
            json={"number": f"10{i}", "type": "Standard", "price": 100.0 + i * 10},
            headers=headers
        )

    # List rooms
    response = client.get(f"/hotels/{hotel_id}/rooms/")
    assert response.status_code == 200
    rooms = response.json()
    assert isinstance(rooms, list)
    assert len(rooms) >= 3


def test_list_rooms_for_nonexistent_hotel():
    """Test listing rooms for a hotel that doesn't exist."""
    response = client.get("/hotels/999999/rooms/")
    assert response.status_code == 200
    rooms = response.json()
    assert isinstance(rooms, list)
    assert len(rooms) == 0


# ============================================================
# BOOKING TESTS
# ============================================================

def test_create_booking():
    """Test creating a booking for a room."""
    headers = register_and_login("booker@example.com", "bookpass")

    # Create hotel
    hotel_response = client.post(
        "/hotels/",
        json={"name": "Booking Hotel", "location": "LA"},
        headers=headers
    )
    hotel_id = hotel_response.json()["id"]

    # Create room
    room_response = client.post(
        f"/hotels/{hotel_id}/rooms/",
        json={"number": "201", "type": "Suite", "price": 250.0},
        headers=headers
    )
    room_id = room_response.json()["id"]

    # Create booking
    today = date.today()
    booking_data = {
        "room_id": room_id,
        "from_date": str(today + timedelta(days=1)),
        "to_date": str(today + timedelta(days=3))
    }
    response = client.post("/bookings/", json=booking_data, headers=headers)
    
    assert response.status_code in (200, 201)
    booking = response.json()
    assert "id" in booking
    assert booking["room_id"] == room_id
    assert booking["status"] == "confirmed"


def test_create_booking_unauthorized():
    """Test creating a booking without authentication."""
    booking_data = {
        "room_id": 1,
        "from_date": "2026-03-01",
        "to_date": "2026-03-03"
    }
    response = client.post("/bookings/", json=booking_data)
    assert response.status_code == 401


def test_create_overlapping_booking():
    """Test creating overlapping bookings for the same room."""
    headers = register_and_login("overlap@example.com", "overlappass")

    # Create hotel and room
    hotel_response = client.post(
        "/hotels/",
        json={"name": "Overlap Hotel", "location": "Denver"},
        headers=headers
    )
    hotel_id = hotel_response.json()["id"]

    room_response = client.post(
        f"/hotels/{hotel_id}/rooms/",
        json={"number": "301", "type": "Standard", "price": 120.0},
        headers=headers
    )
    room_id = room_response.json()["id"]

    # Create first booking
    today = date.today()
    booking1 = {
        "room_id": room_id,
        "from_date": str(today + timedelta(days=5)),
        "to_date": str(today + timedelta(days=8))
    }
    response1 = client.post("/bookings/", json=booking1, headers=headers)
    assert response1.status_code in (200, 201)

    # Try to create overlapping booking
    booking2 = {
        "room_id": room_id,
        "from_date": str(today + timedelta(days=6)),
        "to_date": str(today + timedelta(days=9))
    }
    response2 = client.post("/bookings/", json=booking2, headers=headers)
    assert response2.status_code == 400
    assert "already booked" in response2.json()["detail"].lower()


def test_list_user_bookings():
    """Test listing all bookings for the current user."""
    headers = register_and_login("mybookings@example.com", "mybookpass")

    # Create hotel and room
    hotel_response = client.post(
        "/hotels/",
        json={"name": "My Bookings Hotel", "location": "Portland"},
        headers=headers
    )
    hotel_id = hotel_response.json()["id"]

    room_response = client.post(
        f"/hotels/{hotel_id}/rooms/",
        json={"number": "401", "type": "Deluxe", "price": 180.0},
        headers=headers
    )
    room_id = room_response.json()["id"]

    # Create booking
    today = date.today()
    booking_data = {
        "room_id": room_id,
        "from_date": str(today + timedelta(days=10)),
        "to_date": str(today + timedelta(days=12))
    }
    client.post("/bookings/", json=booking_data, headers=headers)

    # List user's bookings
    response = client.get("/bookings/users/me/bookings", headers=headers)
    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, list)
    assert len(bookings) >= 1
    assert any(b["room_id"] == room_id for b in bookings)


def test_list_bookings_unauthorized():
    """Test listing bookings without authentication."""
    response = client.get("/bookings/users/me/bookings")
    assert response.status_code == 401


# ============================================================
# INTEGRATION TESTS
# ============================================================

def test_full_booking_workflow():
    """Test complete workflow: register, create hotel, room, and make booking."""
    # Register and login
    headers = register_and_login("fullflow@example.com", "fullflowpass")

    # Create hotel
    hotel_response = client.post(
        "/hotels/",
        json={"name": "Full Flow Hotel", "location": "Austin"},
        headers=headers
    )
    assert hotel_response.status_code in (200, 201)
    hotel = hotel_response.json()
    hotel_id = hotel["id"]

    # Verify hotel exists
    get_hotel_response = client.get(f"/hotels/{hotel_id}")
    assert get_hotel_response.status_code == 200

    # Create room
    room_response = client.post(
        f"/hotels/{hotel_id}/rooms/",
        json={"number": "501", "type": "Presidential Suite", "price": 500.0},
        headers=headers
    )
    assert room_response.status_code in (200, 201)
    room_id = room_response.json()["id"]

    # List rooms for hotel
    rooms_response = client.get(f"/hotels/{hotel_id}/rooms/")
    assert rooms_response.status_code == 200
    assert len(rooms_response.json()) >= 1

    # Create booking
    today = date.today()
    booking_response = client.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "from_date": str(today + timedelta(days=20)),
            "to_date": str(today + timedelta(days=23))
        },
        headers=headers
    )
    assert booking_response.status_code in (200, 201)
    booking = booking_response.json()

    # Verify booking in user's booking list
    my_bookings_response = client.get("/bookings/users/me/bookings", headers=headers)
    assert my_bookings_response.status_code == 200
    bookings = my_bookings_response.json()
    assert any(b["id"] == booking["id"] for b in bookings)
