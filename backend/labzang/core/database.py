"""SQLAlchemy engine, sessions, and declarative Base (canonical)."""

from __future__ import annotations

from collections.abc import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from labzang.core.config import DatabaseConfig

_cfg = DatabaseConfig()

DB_HOST = _cfg.db_host
DB_PORT = _cfg.db_port
DB_NAME = _cfg.db_name
DB_USER = _cfg.db_user
DB_PASSWORD = _cfg.db_password


def _sync_url() -> str:
    if _cfg.database_url:
        return _cfg.database_url
    return (
        f"postgresql://{_cfg.db_user}:{_cfg.db_password}"
        f"@{_cfg.db_host}:{_cfg.db_port}/{_cfg.db_name}"
    )


def _async_url() -> str:
    u = _sync_url()
    if u.startswith("postgresql://"):
        return u.replace("postgresql://", "postgresql+asyncpg://", 1)
    if u.startswith("postgresql+asyncpg://"):
        return u
    return u


Base = declarative_base()

engine = create_engine(_sync_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_async_engine = create_async_engine(_async_url(), pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(
    _async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


__all__ = [
    "AsyncSessionLocal",
    "Base",
    "DB_HOST",
    "DB_NAME",
    "DB_PASSWORD",
    "DB_PORT",
    "DB_USER",
    "SessionLocal",
    "engine",
    "get_async_db",
    "get_db",
]
