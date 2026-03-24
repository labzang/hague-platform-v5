"""LangGraph 처리 상태 공통 베이스 (TypedDict)."""
from typing import TypedDict


class BaseProcessingState(TypedDict, total=False):
    """도메인별 State가 상속하는 마커 베이스."""

    pass
