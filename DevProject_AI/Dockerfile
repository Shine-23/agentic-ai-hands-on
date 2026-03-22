FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ backend/

# Copy agent prompt files (required by backend/app/agent_prompt.py)
COPY .claude/agents/ .claude/agents/

# Copy frontend static files (served by FastAPI at runtime)
COPY frontend/ frontend/

# Run uvicorn from the backend directory so imports resolve correctly.
# Railway injects $PORT; fall back to 8000 for local Docker runs.
WORKDIR /app/backend
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
