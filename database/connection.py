"""Database connection and session factory with graceful fallback."""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import config

Base = declarative_base()

def get_engine():
    db_url = config.DATABASE_URL
    connect_args = {}
    if db_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    try:
        engine = create_engine(db_url, connect_args=connect_args)
        # Test connection
        with engine.connect() as conn:
            pass
        return engine
    except Exception as e:
        # If remote or local PostgreSQL is unreachable, fall back to SQLite for local reliability
        fallback_url = "sqlite:///./knowlix.db"
        print(f"[Knowlix DB Warning] Could not connect to {db_url} ({e}). Falling back to {fallback_url}", file=sys.stderr)
        return create_engine(fallback_url, connect_args={"check_same_thread": False})

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables defined in models."""
    import database.models  # noqa: F401
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

