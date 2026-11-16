"""SQLAlchemy engine, session factory, and declarative base."""

import os
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy backend\\.env.example to backend\\.env "
        "and configure the PostgreSQL connection."
    )

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and always close it after the request."""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
