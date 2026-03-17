"""
AI 서비스용 데이터베이스 연결 설정
Railway PostgreSQL 연동
"""
import os
from typing import Generator

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

try:
    import redis
except ImportError:
    redis = None  # type: ignore[assignment]

# 환경 변수에서 데이터베이스 설정 읽기
DATABASE_URL = os.getenv("DATABASE_URL")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "railway")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
REDIS_URL = os.getenv("REDIS_URL")

# PostgreSQL 연결 엔진 생성
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=True,
    )
else:
    database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=True,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

# Upstash Redis 연결 (TLS 필수, redis 패키지 선택)
redis_client = None
REDIS_SSL_ENABLED = os.getenv("REDIS_SSL_ENABLED", "true").lower() == "true"

if REDIS_URL and redis is not None:
    try:
        if REDIS_SSL_ENABLED:
            import ssl
            redis_client = redis.from_url(
                REDIS_URL,
                decode_responses=True,
                ssl_cert_reqs=ssl.CERT_REQUIRED,
                ssl=True,
            )
        else:
            redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        redis_client.ping()
        print("Upstash Redis 연결 성공")
    except Exception as e:
        print(f"Upstash Redis 연결 실패: {e}")
        redis_client = None


def get_db() -> Generator:
    """데이터베이스 세션 의존성 (FastAPI Depends용)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """Redis 클라이언트 반환."""
    return redis_client


def create_tables():
    """테이블 생성."""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """테이블 삭제 (개발용)."""
    Base.metadata.drop_all(bind=engine)


SCHEMAS = {
    "auth": "labzang_ai_auth",
    "chatbot": "labzang_chatbot",
    "crawler": "labzang_crawler",
}


def get_schema(service_name: str) -> str:
    """서비스명으로 스키마명 반환."""
    return SCHEMAS.get(service_name, "public")


def create_schema_if_not_exists(schema_name: str):
    """스키마가 존재하지 않으면 생성."""
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        conn.commit()


def init_schemas():
    """모든 AI 서비스 스키마 초기화."""
    for schema in SCHEMAS.values():
        create_schema_if_not_exists(schema)
    print("AI 서비스 스키마 초기화 완료")


__all__ = [
    "engine",
    "SessionLocal",
    "Base",
    "metadata",
    "redis_client",
    "get_db",
    "get_redis",
    "create_tables",
    "drop_tables",
    "SCHEMAS",
    "get_schema",
    "create_schema_if_not_exists",
    "init_schemas",
]
