# Centralised configuration for the backend.
# Loads environment variables from backend/.env and exposes ANTHROPIC_API_KEY.

import os
from pathlib import Path
from dotenv import load_dotenv

# Always load from backend/.env regardless of where uvicorn is launched from
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
