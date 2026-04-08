"""일정 조회 출력 포트 (헥사고날 드리븐 포트)."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class ScheduleReaderPort(ABC):
    """일정 읽기 저장소 포트."""

    @abstractmethod
    async def find_by_id(self, schedule_id: int) -> Optional[Any]:
        """ID로 일정 조회."""
        ...

    @abstractmethod
    async def find_all(self) -> List[Any]:
        """모든 일정 조회."""
        ...
