"""API 요청/응답 모델 (챗 검색·RAG·헬스 인바운드 계약)."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


class SearchRequest(BaseModel):
    """벡터 검색 요청 모델."""

    query: str = Field(..., description="검색할 질문 또는 키워드")
    k: int = Field(default=5, ge=1, le=20, description="반환할 문서 개수")


class RAGRequest(BaseModel):
    """RAG 질의 요청 모델."""

    question: str = Field(..., description="질문 내용")
    k: int = Field(default=2, ge=1, le=10, description="검색에 사용할 문서 개수")
