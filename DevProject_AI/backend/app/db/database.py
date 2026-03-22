# SQLAlchemy database engine and session setup.
# All database operations use the SessionLocal context via the get_db dependency.
# DATABASE_URL is validated at startup in config.py — no need to re-check here.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_size=5,        # max persistent connections
    max_overflow=10,    # extra connections allowed under load
    pool_timeout=30,    # seconds to wait for a connection before raising
    pool_pre_ping=True, # test connections before use to handle stale ones
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
