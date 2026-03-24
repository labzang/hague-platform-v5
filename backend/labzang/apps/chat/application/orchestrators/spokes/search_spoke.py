"""
스포크: 벡터 검색 — VectorRepositoryPort만 사용.
"""
from labzang.apps.chat.application.dtos import DocumentDto, SearchQueryDto, SearchResultDto
from labzang.apps.chat.application.ports.output import VectorRepositoryPort


class SearchSpoke:
    """벡터 검색만 담당. RAG 오케스트레이터 또는 SearchInputPort 구현에서 사용."""

    def __init__(self, vector_repo: VectorRepositoryPort):
        self._vector = vector_repo

    def run(self, query: SearchQueryDto) -> SearchResultDto:
        """검색 실행 후 SearchResultDto 반환."""
        raw = self._vector.search(
            query=query.query,
            k=query.k,
        )
        documents = []
        for d in raw:
            if not isinstance(d, dict):
                continue
            content = d.get("content") or d.get("page_content", "")
            documents.append(
                DocumentDto(
                    content=content,
                    metadata=d.get("metadata") or {},
                    score=d.get("score"),
                    document_id=d.get("id"),
                )
            )
        return SearchResultDto(
            query=query.query,
            documents=documents,
            count=len(documents),
        )
