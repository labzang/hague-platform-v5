# -*- coding: utf-8 -*-
"""StadiumQuery — 출력 포트 `StadiumReader`에 위임."""

from __future__ import annotations

from typing import Any, List, Optional

from labzang.apps.biz.asset.content.soccer.application.ports.input.stadium_query import StadiumQuery
from labzang.apps.biz.asset.content.soccer.application.ports.output.stadium_reader import (
    StadiumReader,
)


class StadiumQueryImpl(StadiumQuery):
    def __init__(self, stadium_reader: StadiumReader) -> None:
        self._stadium_reader = stadium_reader

    async def find_by_id(self, stadium_id: int) -> Optional[Any]:
        return await self._stadium_reader.find_by_id(stadium_id)

    async def find_all(self) -> List[Any]:
        return await self._stadium_reader.find_all()
