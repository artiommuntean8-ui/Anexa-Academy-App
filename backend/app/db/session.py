import os
import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings

logger = logging.getLogger("app.db")

db_url = settings.DATABASE_URL

def create_db_engine(url: str):
    try:
        if url.startswith("sqlite"):
            return create_engine(url, connect_args={"check_same_thread": False})
        else:
            return create_engine(url, pool_pre_ping=True)
    except (ModuleNotFoundError, Exception) as e:
        logger.warning(f"Could not initialize DB with URL '{url}': {e}. Falling back to SQLite.")
        sqlite_url = "sqlite:///./arkitech_dashboard.db"
        return create_engine(sqlite_url, connect_args={"check_same_thread": False})

engine = create_db_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator for database sessions.
    Ensures the session is always closed after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
