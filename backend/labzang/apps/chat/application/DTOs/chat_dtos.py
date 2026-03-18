"""채팅·검색·RAG 유스케이스용 Application DTOs."""
from typing import Any, Dict, List, Optional

from pydantic import Field

from backend.labzang.apps.chat.application.DTOs.base_dto import BaseDto




# ---- 대화 메시지 ----
class ChatMessageDto(BaseDto):
    """대화 메시지 한 건 (role + content)."""

    role: str = Field(..., description="user | assistant | system")
    content: str = Field(..., min_length=1)


class ChatRequestDto(BaseDto):
    """채팅 요청 (유스케이스 입력)."""

    message: str = Field(..., min_length=1, description="사용자 메시지")
    max_new_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    conversation_history: Optional[List[ChatMessageDto]] = Field(default=None)


class ChatResponseDto(BaseDto):
    """채팅 응답 (유스케이스 출력)."""

    answer: str = Field(..., description="생성된 답변")
    model_info: Optional[str] = Field(None, description="모델/엔진 정보")


# ---- 검색 ----
class DocumentDto(BaseDto):
    """검색된 문서 한 건."""

    content: str = Field(..., description="문서 내용")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    score: Optional[float] = Field(None, description="유사도 점수")
    document_id: Optional[str] = Field(None, description="저장소 ID")


class SearchQueryDto(BaseDto):
    """벡터 검색 요청."""

    query: str = Field(..., min_length=1)
    k: int = Field(default=5, ge=1, le=20)


class SearchResultDto(BaseDto):
    """벡터 검색 결과."""

    query: str = Field(...)
    documents: List[DocumentDto] = Field(default_factory=list)
    count: int = Field(..., ge=0)


# ---- RAG ----
class RAGQueryDto(BaseDto):
    """RAG 질의 요청 (검색 + 생성 입력)."""

    question: str = Field(..., min_length=1, description="질문")
    k: int = Field(default=5, ge=1, le=20, description="검색 문서 수")
    max_new_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class RAGResultDto(BaseDto):
    """RAG 질의 결과 (검색된 문서 + 생성된 답변)."""

    question: str = Field(...)
    answer: str = Field(...)
    sources: List[DocumentDto] = Field(default_factory=list, description="참조 문서")
    retrieved_count: int = Field(default=0, ge=0)
