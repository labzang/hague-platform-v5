"""
서빙용 벡터 저장소 CRUD — VectorRepositoryPort 구현.
vectorstore와 연결되는 CRUD 래퍼.
"""
from typing import Any, Dict, List, Optional

from labzang.apps.chat.application.ports.output import VectorRepositoryPort


class VectorRepositoryAdapter(VectorRepositoryPort):
    """벡터 저장소 아웃바운드 어댑터 (vectorstore 래퍼)."""

    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """문서 임베딩 후 저장. 반환: 저장된 ID 목록."""
        raise NotImplementedError(
            "VectorRepositoryAdapter.add_documents: persistence 구현 필요"
        )

    def search(
        self,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """유사도 검색. 반환: 문서 목록(content, metadata, score)."""
        raise NotImplementedError(
            "VectorRepositoryAdapter.search: persistence 구현 필요"
        )

    def delete(self, ids: List[str]) -> bool:
        """ID 목록에 해당하는 벡터 삭제."""
        raise NotImplementedError(
            "VectorRepositoryAdapter.delete: persistence 구현 필요"
        )
