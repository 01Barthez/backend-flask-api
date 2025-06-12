# Meal Tracker API

## Project Overview

A comprehensive meal tracking application with user authentication, meal management, and allergy tracking.

## Features

- JWT Authentication
- User Management
- Meal CRUD Operations
- Allergy Tracking
- Advanced Querying

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL

### Installation

1. Clone the repository
2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Setup PostgreSQL Database

```bash
createdb meal_tracker_db
```

5. Set environment variables in `.env`

6. Run Migrations

```bash
flask db upgrade
```

7. Start the Application

```bash
flask run
```

## Docker Setup and Deployment

### Prerequisites

- Docker
- Docker Compose

### Environment Configuration

1. Copy `.env.example` to `.env`
2. Modify environment variables as needed

### Build and Run

```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Database Migrations

```bash
# Run migrations inside the app container
docker-compose exec app flask db upgrade
```

### Accessing Services

- API: <http://localhost:5000>
- Swagger UI: <http://localhost:5000/apidocs>
- PgAdmin: <http://localhost:8080>

### Persistent Data

Data is stored in `./data` directory:

- `./data/postgres`: PostgreSQL database files
- `./data/app`: Application data
- `./data/pgadmin`: PgAdmin configuration

### Stopping Services

```bash
docker-compose down
```

## Development

- Use `docker-compose -f docker-compose.dev.yml` for development mode
- Mount local code for live reloading

## Security

- Non-root containers
- HTTPS enforcement
- Content Security Policy
- JWT Authentication

## Testing

```bash
pytest
```

## API Documentation

Access Swagger UI at `/apidocs` after running the application.
