# Balance API

FastAPI backend for balance tracking application.

## Prerequisites

- Docker & Docker Compose
- PostgreSQL (included in Docker setup)

---

## Local Development

### Using Docker (Recommended)

1. Start the services:
   ```bash
   docker compose up --build
   ```

2. The API will be available at `http://localhost:8000`
3. API documentation: `http://localhost:8000/docs`

### Using Local Environment

1. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL locally and update `DATABASE_URL` in `.env`

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Production Deployment

### 1. Environment Setup

Create a `.env.production` file:
```bash
cp .env.example .env.production
```

Edit `.env.production` with production values:
```env
DATABASE_URL=postgresql://postgres:your-secure-password@db:5432/balance_app_db
SECRET_KEY=your-very-secure-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=60
DB_PASSWORD=your-secure-password
```

### 2. Build & Deploy

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### 3. View Logs

```bash
docker compose -f docker-compose.prod.yml logs -f
```

### 4. Stop Services

```bash
docker compose -f docker-compose.prod.yml down
```

---

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `docker compose up --build` | Build and start dev services |
| `docker compose down` | Stop dev services |
| `docker compose -f docker-compose.prod.yml up --build -d` | Production deploy |
| `docker compose logs -f` | View logs |
| `docker compose exec api sh` | Shell into API container |
| `docker compose exec db psql -U postgres` | Connect to database |