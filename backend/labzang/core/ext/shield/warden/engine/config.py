"""Re-export: canonical settings live in `labzang.core.config`."""

from labzang.core.config import (  # noqa: F401
    BaseServiceConfig,
    ChatbotServiceConfig,
    DatabaseConfig,
    RedisConfig,
)

__all__ = [
    "BaseServiceConfig",
    "ChatbotServiceConfig",
    "DatabaseConfig",
    "RedisConfig",
]
