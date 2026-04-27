# URL Shortener API
A REST API built with FastAPI that shortens URLs, tracks clicks, and automatically expires links after 30 days.

**Live Demo:** https://url-shortner-api-one.vercel.app

---

## Features
- Generate short URLs from long ones
- Redirect users to the original URL
- Track click count per short URL
- Automatically expire links after 30 days
- Reject duplicate URLs (returns existing short code)
- Validate URLs before saving

---

## Tech Stack
- **FastAPI** — Python web framework
- **SQLAlchemy** — ORM for database access
- **PostgreSQL** — Database (hosted on Neon)
- **Pydantic** — Request validation
- **Vercel** — Deployment

---

## API Endpoints

### POST `/shorten`
Create a short URL.

**Request body:**
```json
{
  "url": "https://www.example.com"
}
```

**Response:**
```json
{
  "short_code": "abc12",
  "short_url": "https://url-shortner-api-one.vercel.app/abc12"
}
```

---

### GET `/shorten/{code}`
Redirects to the original URL. Returns 404 if the link has expired (older than 30 days) or does not exist.

---

### GET `/shorten/stats/{code}`
Get statistics for a short URL.

**Response:**
```json
{
  "short_code": "abc12",
  "original_url": "https://www.example.com",
  "clicks": 5,
  "created_at": "2026-04-24T10:00:00"
}
```

---

## Running Locally

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Create a `.env` file:**
```
DATABASE_URL=postgresql://your-connection-string
```

**4. Run the server:**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs available at `http://localhost:8000/docs`.

---

## Running with Docker / Podman

**1. Create a `.env` file:**
```
DATABASE_URL=postgresql://your-connection-string@host/dbname?sslmode=require
```

**2. Build and start the containers:**
```bash
# Docker
docker compose up --build

# Podman
podman-compose up --build
```

**3. Run in the background:**
```bash
# Docker
docker compose up -d --build

# Podman
podman-compose up -d --build
```

The API will be available at `http://localhost:8000`.  
Interactive docs available at `http://localhost:8000/docs`.

**Other useful commands:**
```bash
# View logs
docker compose logs -f api

# Restart the API
docker compose restart api

# Stop all containers
docker compose down
```

---

## Project Structure
```
url-shortener/
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Multi-container setup
├── api/
│   ├── main.py          # API routes
│   └── requirements.txt
├── models.py            # Database models
├── database.py          # Database connection
├── vercel.json          # Vercel deployment config
└── .env                 # Environment variables (not committed)
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
