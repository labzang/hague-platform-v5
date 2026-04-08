"""
아웃바운드 포트: 문서/벡터/체크포인트/데이터셋 저장소 (구현: adapter/outbound/persistence)
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class DocumentRepository(ABC):
    """문서 저장소 포트."""

    @abstractmethod
    def load(self, document_id: str) -> Optional[Dict[str, Any]]: ...

    @abstractmethod
    def save(
        self,
        document_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str: ...

    @abstractmethod
    def list_(self, **filters: Any) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def delete(self, document_id: str) -> bool: ...


class VectorRepositoryPort(ABC):
    """벡터 저장소 포트."""

    @abstractmethod
    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> List[str]: ...

    @abstractmethod
    def search(
        self,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def delete(self, ids: List[str]) -> bool: ...


class ModelCheckpointRepositoryPort(ABC):
    """체크포인트 저장소 포트."""

    @abstractmethod
    def get_checkpoint_path(
        self, run_id: str, kind: str = "latest"
    ) -> Optional[str]: ...

    @abstractmethod
    def save_checkpoint(
        self,
        run_id: str,
        path: str,
        meta: Optional[Dict[str, Any]] = None,
    ) -> str: ...

    @abstractmethod
    def list_checkpoints(self, run_id: str) -> List[Dict[str, Any]]: ...


class TrainingDatasetRepositoryPort(ABC):
    """학습 데이터셋 저장소 포트."""

    @abstractmethod
    def load_dataset(self, name: str) -> Any: ...

    @abstractmethod
    def save_dataset(
        self,
        name: str,
        data: Any,
        meta: Optional[Dict[str, Any]] = None,
    ) -> str: ...

    @abstractmethod
    def get_meta(self, name: str) -> Optional[Dict[str, Any]]: ...

    @abstractmethod
    def list_datasets(self) -> List[Dict[str, Any]]: ...
