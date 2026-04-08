"""HTTP middleware (canonical)."""

from __future__ import annotations

import logging
from time import perf_counter

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """Minimal request logging middleware."""

    logger = logging.getLogger("labzang.request")

    async def dispatch(self, request: Request, call_next):
        start = perf_counter()
        response = await call_next(request)
        elapsed_ms = (perf_counter() - start) * 1000
        self.logger.info(
            "%s %s -> %s (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response


__all__ = ["LoggingMiddleware", "CORSMiddleware"]
