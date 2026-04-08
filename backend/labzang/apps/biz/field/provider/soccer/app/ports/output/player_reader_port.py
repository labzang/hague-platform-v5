"""선수 저장소 출력 포트 (헥사고날 드리븐 포트)."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class PlayerReaderPort(ABC):
    """선수 저장소 포트."""

    @abstractmethod
    async def find_by_id(self, player_id: int) -> Optional[Any]:
        """ID로 선수 조회."""
        ...

    @abstractmethod
    async def find_all(self) -> List[Any]:
        """모든 선수 조회."""
        ...
