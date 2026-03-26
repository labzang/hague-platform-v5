"""Shared common values compatibility package."""

from labzang.shared.common_values.utils import (
    create_error_response,
    create_response,
    setup_logging,
)

__all__ = [
    "setup_logging",
    "create_response",
    "create_error_response",
]
