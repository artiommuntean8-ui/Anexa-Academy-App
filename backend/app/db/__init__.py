"""
Database module for Academy Student Dashboard.
"""
from app.db.session import Base, SessionLocal, get_db
from app.db.init_db import init_db, seed_demo_data

__all__ = ["Base", "SessionLocal", "get_db", "init_db", "seed_demo_data"]
