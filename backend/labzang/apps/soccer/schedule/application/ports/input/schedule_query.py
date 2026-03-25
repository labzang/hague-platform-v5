# -*- coding: utf-8 -*-
"""일정 조회 입력 포트 (애플리케이션 경계)."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class ScheduleQuery(ABC):
    """일정 조회 유스케이스 진입점."""

    @abstractmethod
    async def find_by_id(self, schedule_id: int) -> Optional[Any]:
        """ID로 일정 한 건 조회. 없으면 None."""
        ...

    @abstractmethod
    async def find_all(self) -> List[Any]:
        """일정 전체 목록 조회."""
        ...
