# Balance API

FastAPI backend for balance tracking application.

## Setup

1. Copy `.env.example` to `.env` and configure your database
2. Set up PostgreSQL locally
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `alembic upgrade head`
5. Start server: `uvicorn app.main:app --reload`

## API Documentation

Visit `http://localhost:8000/docs` for Swagger UI