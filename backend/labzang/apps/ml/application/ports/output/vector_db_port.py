"""
Outbound: RAG 검색을 위한 벡터 DB 인터페이스
- 구현: adapter/outbound/vector_db (ChromaDB, Pinecone 등)
"""
from abc import ABC, abstractmethod
from typing import Any, List


class VectorDbPort(ABC):
    """RAG 검색용 벡터 DB 포트."""

    @abstractmethod
    def search(self, query: str, top_k: int = 5, **kwargs: Any) -> List[Any]:
        """쿼리로 유사 문서 검색."""
        ...

    @abstractmethod
    def add_documents(self, documents: List[Any], **kwargs: Any) -> None:
        """문서 추가 (임베딩 후 저장)."""
        ...
