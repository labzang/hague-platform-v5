"""
오케스트레이터: 중앙 제어소 (Flow Manager)
1. 요청 분류
2. CRUD(규칙 기반) 경로 vs AI(복합 추론) 경로 결정
- 의뢰인 변덕·ERD 불확실 시, 단순 데이터 관리와 AI 로직이 엉키지 않도록 분리
"""
from enum import Enum
from typing import Any, Optional


class FlowType(str, Enum):
    """흐름 유형: 규칙 기반 CRUD vs AI 오케스트레이션."""
    CRUD = "crud"       # 규칙 기반 CRUD (전형적인 DB 작업)
    AI = "ai"           # 복합 AI 로직 (RAG, 타이타닉 등)


def classify(request: dict) -> FlowType:
    """
    요청을 분류해 CRUD 경로 vs AI 경로 결정.
    - CRUD: REST 리소스 패턴, 메서드(GET/POST/PUT/DELETE), 엔티티 경로 등
    - AI: 챗봇/질의, 정책 기반, 복합 추론 요청
    """
    path = (request.get("path") or request.get("url") or "").strip("/")
    method = (request.get("method") or "GET").upper()
    # 예: /api/v1/users, /api/v1/knowledge → CRUD
    if path.startswith("api/") or path.startswith("v1/"):
        if any(x in path.lower() for x in ("users", "knowledge", "entities", "admin")):
            if method in ("GET", "POST", "PUT", "PATCH", "DELETE"):
                return FlowType.CRUD
    # 챗뷰/질의/정책 플래그 → AI
    if request.get("is_chat") or request.get("policy_based") or request.get("query"):
        return FlowType.AI
    # 기본: 단순 리소스 접근은 CRUD, 나머지는 AI
    if method == "GET" and path.count("/") <= 1:
        return FlowType.CRUD
    return FlowType.AI


def route_to_flow(request: dict) -> tuple[FlowType, Optional[str]]:
    """
    분류 후 어느 Spoke로 보낼지 결정.
    Returns:
        (FlowType.CRUD or FlowType.AI, spoke_hint)
    """
    flow = classify(request)
    if flow == FlowType.CRUD:
        return flow, "crud_spoke"
    # AI 경로: policy_engine으로 세부 Spoke 결정 (rag / titanic 등)
    return flow, None  # None이면 hub/policy_engine에서 추가 라우팅
