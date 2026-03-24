"""선수 데이터 처리 상태 스키마."""
from typing import List, Dict, Any, TypedDict, Optional, Annotated, Literal
from datetime import datetime
import operator

from labzang.apps.soccer.application.orchestrators.states.base_state import (
    BaseProcessingState,
)
from labzang.apps.soccer.application.orchestrators.states.database_result import (
    DatabaseResult,
)


class PlayerEmbeddingState(TypedDict):
    """선수 임베딩 데이터 상태 스키마.

    PlayerEmbedding 모델의 필드를 기반으로 한 TypedDict.
    LangGraph StateGraph에서 임베딩 관련 상태를 관리할 때 사용합니다.
    """

    id: Optional[int]  # 임베딩 레코드 고유 식별자
    player_id: int  # 선수 ID
    content: str  # 원본 텍스트 데이터
    embedding: List[float]  # 768차원 KoElectra 벡터 임베딩
    created_at: Optional[datetime]  # 레코드 생성 시간


class PlayerState(BaseProcessingState):
    """선수 데이터 처리 상태 스키마.

    LangGraph StateGraph에서 사용하는 상태 정의.
    각 노드에서 이 상태를 읽고 업데이트합니다.
    """

    # 입력 데이터 (BaseProcessingState에서 상속)
    items: List[Dict[str, Any]]

    # 검증 결과 (BaseProcessingState에서 상속)
    # 여러 노드에서 발생한 에러를 누적하기 위해 Annotated 사용
    validation_errors: Annotated[List[Dict[str, Any]], operator.add]

    # 전략 판단 결과 (BaseProcessingState에서 상속)
    # Literal을 사용하여 타입 안정성 향상
    strategy_type: Literal["policy", "rule"]

    # 정규화된 데이터 (Rule 기반 처리용)
    normalized_items: List[Dict[str, Any]]

    # 정책 기반 처리 결과
    policy_result: Dict[str, Any]

    # 규칙 기반 처리 결과
    rule_result: Dict[str, Any]

    # 데이터베이스 저장 결과 (구체적인 구조로 정의)
    db_result: DatabaseResult

    # 임베딩 관련 상태
    # 여러 노드에서 생성된 임베딩 객체들을 합치기 위해 Annotated 사용
    embeddings: Annotated[List[PlayerEmbeddingState], operator.add]

    # 최종 결과 (BaseProcessingState에서 상속)
    final_result: Dict[str, Any]


# UC / LangGraph에서 쓰던 이름과 호환
PlayerProcessingState = PlayerState
