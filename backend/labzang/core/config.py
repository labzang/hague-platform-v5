"""Core configuration models (canonical)."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class BaseServiceConfig(BaseSettings):
    service_name: str = "labzang"
    service_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


class DatabaseConfig(BaseSettings):
    database_url: str = Field(default="", alias="DATABASE_URL")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="railway", alias="DB_NAME")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="", alias="DB_PASSWORD")

    class Config:
        env_file = ".env"
        case_sensitive = False


class RedisConfig(BaseSettings):
    redis_url: str = Field(default="", alias="REDIS_URL")

    class Config:
        env_file = ".env"
        case_sensitive = False


class ChatbotServiceConfig(BaseServiceConfig):
    service_name: str = "labzang-monolith"


__all__ = [
    "BaseServiceConfig",
    "ChatbotServiceConfig",
    "DatabaseConfig",
    "RedisConfig",
]
