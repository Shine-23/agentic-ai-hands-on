# Entry point for the DevProject AI backend.
# Initialises the FastAPI app, configures CORS, and registers the /plan and /history routers.
#
# NOTE: create_all() creates missing tables but does NOT apply column changes to existing ones.
# If you add a new column to a model, run ALTER TABLE manually in psql or via a one-off script.

from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.routes_plan import router as plan_router
from app.api.routes_history import router as history_router
from app.core.config import ALLOW_ORIGINS
from app.db.database import engine, SessionLocal
from app.db import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create any missing tables on startup (does not alter existing columns)
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise RuntimeError(f"Database unavailable on startup: {e}") from e
    yield
    # No teardown needed — connection pool closes automatically


app = FastAPI(title="DevProject AI API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,   # set ALLOW_ORIGINS in .env for prod; defaults to "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan_router)
app.include_router(history_router)


@app.get("/")
def health_check(response: Response):
    """Health check — verifies the API is running and the database is reachable."""
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e}"
    finally:
        db.close()

    healthy = db_status == "ok"
    if not healthy:
        response.status_code = 503

    return {
        "status": "ok" if healthy else "degraded",
        "api": "DevProject AI backend is running",
        "database": db_status,
    }
