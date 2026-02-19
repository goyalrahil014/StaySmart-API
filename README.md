deploy:

# StaySmart Backend

StaySmart is a FastAPI backend for hotel, room, and booking management with JWT authentication, PostgreSQL, Alembic migrations, Docker, and CI/CD support.

## Features
- Hotel, room, and booking CRUD
- JWT authentication (user/admin roles)
- PostgreSQL with SQLAlchemy ORM
- Alembic migrations
- Docker & docker-compose support
- Automated tests (pytest)
- API docs (Swagger UI, ReDoc)

## Quick Start
1. **Clone & Setup**
   ```bash
   git clone <repo-url>
   cd Assignment-4(Chat-GPT)
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Edit .env for DB credentials
   ```
2. **Database**
   - Create PostgreSQL DB (see .env.example)
   - Run migrations:
     ```bash
     alembic upgrade head
     ```
3. **Run App**
   ```bash
   uvicorn app.main:app --reload
   # Docs: http://localhost:8000/docs
   ```

## Docker
```bash
docker-compose up --build
# App: http://localhost:8000
```

## Testing
```bash
pytest
```

## API Overview
- `POST /auth/register` — Register user
- `POST /auth/login` — Login, get JWT
- `GET /hotels/` — List hotels
- `POST /hotels/` — Create hotel (auth)
- `GET /hotels/{id}` — Hotel details
- `DELETE /hotels/{id}` — Delete hotel (admin)
- `GET /hotels/{hotel_id}/rooms/` — List rooms
- `POST /hotels/{hotel_id}/rooms/` — Create room (auth)
- `POST /bookings/` — Book room (auth)
- `GET /bookings/users/me/bookings` — My bookings

## Postman Collection
Import `StaySmart.postman_collection.json` in Postman for ready-to-use API requests.

## Deployment
- Docker & Render supported (see `.gitlab-ci.yml` & Dockerfile)
- Set env vars: `DATABASE_URL`, `SECRET_KEY`, etc.

---
**Assignment project. Built with FastAPI.**
