# 시각화 Use Case 연결
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


def crud_get(repository: Any, id: Any) -> Optional[Any]:
    """단건 조회."""
    return repository.get(id)


def crud_list(repository: Any, **filters: Any) -> List[Any]:
    """목록 조회."""
    return repository.list_(**filters)


def crud_create(repository: Any, entity: Any) -> Any:
    """생성."""
    return repository.add(entity)


def crud_update(repository: Any, entity: Any) -> Any:
    """수정."""
    return repository.update(entity)


def crud_delete(repository: Any, id: Any) -> bool:
    """삭제."""
    return repository.delete(id)
