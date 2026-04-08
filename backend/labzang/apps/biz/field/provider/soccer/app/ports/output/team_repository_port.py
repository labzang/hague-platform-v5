"""팀 쓰기 저장소 출력 포트 (헥사고날 드리븐 포트)."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class TeamRepositoryPort(ABC):
    """팀 저장소 포트."""

    @abstractmethod
    async def upsert_batch(self, teams_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """여러 팀 일괄 upsert."""
        ...

    @abstractmethod
    async def commit(self) -> None:
        """변경사항 커밋."""
        ...
