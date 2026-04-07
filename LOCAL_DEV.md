# TaskFlow Version 1 - Local Development Setup

## Why this approach?
Docker builds fail in your network due to PyPI timeouts. Running backend locally avoids this.

## Setup Instructions

### 1. Install Python Dependencies Locally

```bash
# Create virtual environment
cd se-toolkit-hackathon-Berezhnoy-Sergey
python -m venv .venv

# Activate it
# On Windows (Git Bash):
source .venv/Scripts/activate

# Install packages
pip install fastapi uvicorn sqlmodel psycopg2-binary pydantic pydantic-settings python-dotenv
```

### 2. Start PostgreSQL in Docker

```bash
# Only run postgres (no build needed!)
docker compose -f docker-compose.services.yml up -d
```

### 3. Run the Backend

```bash
# Make sure .venv is activated
source .venv/Scripts/activate

# Set environment variable
export DATABASE_URL="postgresql://taskflow:taskflow_password@localhost:5432/taskflow"

# Run backend
cd backend/src
python -m uvicorn lms_backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Open the Frontend

Just open `web-client/index.html` in your browser, OR:

```bash
# Serve with any HTTP server
cd web-client
python -m http.server 8080
```

Then open: http://localhost:8080

### 5. Test It!

In the chat interface:
- "Add task: Buy groceries"
- "Show my tasks"
- "Mark Buy groceries as done"

## Stopping

```bash
# Stop PostgreSQL
docker compose -f docker-compose.services.yml down
```

## API Documentation

When backend is running, visit: http://localhost:8000/docs
