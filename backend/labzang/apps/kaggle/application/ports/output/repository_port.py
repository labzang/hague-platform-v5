"""
Outbound: CRUD를 위한 DB 인터페이스 (Repository)
- 구현: adapter/outbound/persistence (Alembic + SQLAlchemy, MySQL/PostgreSQL 등)
"""
from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class IRepositoryPort(ABC, Generic[T]):
    """규칙 기반 CRUD용 Repository 포트 (엔티티 단위)."""

    @abstractmethod
    def get(self, id: Any) -> Optional[T]:
        """ID로 단건 조회."""
        ...

    @abstractmethod
    def list_(self, **filters: Any) -> List[T]:
        """목록 조회 (필터 옵션)."""
        ...

    @abstractmethod
    def add(self, entity: T) -> T:
        """추가."""
        ...

    @abstractmethod
    def update(self, entity: T) -> T:
        """수정."""
        ...

    @abstractmethod
    def delete(self, id: Any) -> bool:
        """삭제."""
        ...
