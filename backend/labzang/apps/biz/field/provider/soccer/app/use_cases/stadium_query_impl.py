# -*- coding: utf-8 -*-
"""StadiumQuery — 출력 포트 `StadiumReaderPort`에 위임."""

from __future__ import annotations

from typing import Any, List, Optional

from labzang.apps.biz.field.provider.soccer.app.ports.input.stadium_query_port import (
    StadiumQueryPort,
)
from labzang.apps.biz.field.provider.soccer.app.ports.output.stadium_reader_port import (
    StadiumReaderPort,
)


class StadiumQueryImpl(StadiumQueryPort):
    def __init__(self, stadium_reader: StadiumReaderPort) -> None:
        self._stadium_reader = stadium_reader

    async def find_by_id(self, stadium_id: int) -> Optional[Any]:
        return await self._stadium_reader.find_by_id(stadium_id)

    async def find_all(self) -> List[Any]:
        return await self._stadium_reader.find_all()
