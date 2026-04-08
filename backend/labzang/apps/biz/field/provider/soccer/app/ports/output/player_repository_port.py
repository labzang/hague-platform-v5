"""선수 저장소 출력 포트 (헥사고날 드리븐 포트)."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class PlayerRepositoryPort(ABC):
    """선수 저장소 포트."""


    @abstractmethod
    async def upsert_batch(self, players_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """여러 선수 일괄 upsert."""
        ...

    @abstractmethod
    async def commit(self) -> None:
        """변경사항 커밋."""
        ...
