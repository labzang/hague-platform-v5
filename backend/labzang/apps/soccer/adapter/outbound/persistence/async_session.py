"""비동기 SQLAlchemy 세션 (soccer 앱, asyncpg). 엔진은 첫 사용 시 생성됩니다."""
import os
from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def _to_async_pg_url(url: str) -> str:
    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    raise ValueError("DATABASE_URL must be a postgresql:// URL for async soccer repos")


def _build_async_url() -> str:
    DATABASE_URL = os.getenv("DATABASE_URL")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "railway")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    if DATABASE_URL:
        return _to_async_pg_url(DATABASE_URL)
    sync_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return _to_async_pg_url(sync_url)


_maker: Any = None


def _get_sessionmaker() -> Callable[..., Any]:
    global _maker
    if _maker is None:
        async_engine = create_async_engine(
            _build_async_url(),
            pool_pre_ping=True,
            echo=os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true",
        )
        _maker = async_sessionmaker(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
    return _maker


class _AsyncSessionLocalProxy:
    """async_sessionmaker와 동일하게 `async with AsyncSessionLocal() as s:` 지원."""

    def __call__(self) -> Any:
        return _get_sessionmaker()()


AsyncSessionLocal = _AsyncSessionLocalProxy()

__all__ = ["AsyncSessionLocal"]
