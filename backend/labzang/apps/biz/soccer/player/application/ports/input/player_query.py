# -*- coding: utf-8 -*-
"""선수 조회 입력 포트 (애플리케이션 경계)."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class PlayerQuery(ABC):
    """선수 조회 유스케이스 진입점."""

    @abstractmethod
    async def find_by_id(self, player_id: int) -> Optional[Any]:
        """ID로 선수 한 건 조회. 없으면 None."""
        ...

    @abstractmethod
    async def find_all(self) -> List[Any]:
        """선수 전체 목록 조회."""
        ...
