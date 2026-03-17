"""
labzang 인프라 기반 (core).
- config: 설정 베이스 (BaseServiceConfig, DatabaseConfig, RedisConfig)
- database: DB/Redis 연결, 세션, 스키마
- paths: LABZANG_ROOT, APPS_ROOT 등 절대 경로
- middleware: LoggingMiddleware, CORSMiddleware
- llm: init_korean_llm, init_korean_embeddings
- rag: get_vectorstore, create_rag_chain 등
공통 예외·유틸은 labzang.shared 사용.
"""

from labzang.core.config import (
    BaseServiceConfig,
    DatabaseConfig,
    RedisConfig,
    ChatbotServiceConfig,
)
from labzang.core.paths import (
    LABZANG_ROOT,
    APPS_ROOT,
    LEARNING_ROOT,
    CRAWLER_ROOT,
    TRANSFORMER_ROOT,
    CHAT_ROOT,
    SHARED_ROOT,
)
from .middleware import LoggingMiddleware, CORSMiddleware
from . import database
from . import llm
from . import rag

__all__ = [
    "BaseServiceConfig",
    "DatabaseConfig",
    "RedisConfig",
    "ChatbotServiceConfig",
    "LABZANG_ROOT",
    "APPS_ROOT",
    "LEARNING_ROOT",
    "CRAWLER_ROOT",
    "TRANSFORMER_ROOT",
    "CHAT_ROOT",
    "SHARED_ROOT",
    "LoggingMiddleware",
    "CORSMiddleware",
    "database",
    "llm",
    "rag",
]
