"""Backward-compatible shared exports."""

from datetime import datetime
import logging
from typing import Any, Dict

from labzang.core.exceptions import (
    NotFoundException,
    ServiceException,
    ValidationException,
)

def setup_logging(service_name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.upper()))
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def create_response(
    data: Any,
    message: str = "Success",
    status: str = "success",
) -> Dict:
    return {
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }


def create_error_response(
    message: str,
    error_code: str = "UNKNOWN_ERROR",
) -> Dict:
    return {
        "status": "error",
        "message": message,
        "error_code": error_code,
        "timestamp": datetime.utcnow().isoformat(),
    }

__all__ = [
    "setup_logging",
    "create_response",
    "create_error_response",
    "ServiceException",
    "NotFoundException",
    "ValidationException",
]
