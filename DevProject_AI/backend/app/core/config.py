# Centralised configuration for the backend.
# Loads environment variables from backend/.env and exposes:
#   ANTHROPIC_API_KEY — required, Claude API key
#   DATABASE_URL      — required, PostgreSQL connection string
#   ALLOW_ORIGINS     — optional, comma-separated CORS origins (default "*")

import os
from pathlib import Path
from dotenv import load_dotenv

# Always load from backend/.env regardless of where uvicorn is launched from
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DATABASE_URL      = os.getenv("DATABASE_URL")
ALLOW_ORIGINS     = [o.strip() for o in os.getenv("ALLOW_ORIGINS", "*").split(",")]

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is not set in .env")
