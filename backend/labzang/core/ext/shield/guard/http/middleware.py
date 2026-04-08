"""Re-export: canonical middleware lives in `labzang.core.middleware`."""

from labzang.core.middleware import CORSMiddleware, LoggingMiddleware  # noqa: F401

__all__ = ["LoggingMiddleware", "CORSMiddleware"]
