"""
Star Topology Hub: 정책 기반 라우팅 (RAG 정책 및 온톨로지 매핑)
- Orchestrator가 AI 경로로 보낸 요청만 여기서 세부 Spoke 결정
"""
from enum import Enum
from typing import Any, Optional


class RoutePolicy(str, Enum):
    RAG = "rag"         # 정책/지식 기반 → RAG Spoke
    TITANIC = "titanic" # 타이타닉 분석 → Titanic Spoke


def route(query: str, context: Optional[dict] = None) -> RoutePolicy:
    """쿼리·컨텍스트에 따라 라우팅 정책 반환 (AI 경로 내부용)."""
    if context and context.get("policy_based"):
        return RoutePolicy.RAG
    if "타이타닉" in query or "titanic" in query.lower():
        return RoutePolicy.TITANIC
    return RoutePolicy.RAG
