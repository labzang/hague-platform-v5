"""
서빙용 문서 저장/관리 — DocumentRepository 구현.
원본 문서를 파일/DB/Blob Storage에서 가져오고 저장하는 기능.
"""

from typing import Any, Dict, List, Optional

from labzang.apps.com.chat.application.ports.output import DocumentRepository


class DocumentRepositoryAdapter(DocumentRepository):
    """문서 저장소 아웃바운드 어댑터 (파일/DB/Blob 등으로 구현 가능)."""

    def load(self, document_id: str) -> Optional[Dict[str, Any]]:
        """문서 ID로 단건 로드."""
        raise NotImplementedError(
            "DocumentRepositoryAdapter.load: persistence 구현 필요"
        )

    def save(
        self,
        document_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """문서 저장. 반환: 저장된 식별자."""
        raise NotImplementedError(
            "DocumentRepositoryAdapter.save: persistence 구현 필요"
        )

    def list_(self, **filters: Any) -> List[Dict[str, Any]]:
        """목록 조회 (필터 옵션)."""
        raise NotImplementedError(
            "DocumentRepositoryAdapter.list_: persistence 구현 필요"
        )

    def delete(self, document_id: str) -> bool:
        """문서 삭제."""
        raise NotImplementedError(
            "DocumentRepositoryAdapter.delete: persistence 구현 필요"
        )
