"""공통 로깅/응답 유틸리티."""

from datetime import datetime
import logging
from typing import Any, Dict


def setup_logging(service_name: str, level: str = "INFO") -> logging.Logger:
    """서비스 로거를 구성하고 반환한다."""
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
    """표준 성공 응답 형식을 생성한다."""
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
    """표준 에러 응답 형식을 생성한다."""
    return {
        "status": "error",
        "message": message,
        "error_code": error_code,
        "timestamp": datetime.utcnow().isoformat(),
    }

