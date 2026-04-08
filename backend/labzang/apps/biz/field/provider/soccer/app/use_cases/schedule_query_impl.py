# -*- coding: utf-8 -*-
"""ScheduleQuery — 출력 포트 `ScheduleReaderPort`에 위임."""

from __future__ import annotations

from typing import Any, List, Optional

from labzang.apps.biz.field.provider.soccer.app.ports.input.schedule_query_port import (
    ScheduleQueryPort,
)
from labzang.apps.biz.field.provider.soccer.app.ports.output.schedule_reader_port import (
    ScheduleReaderPort,
)


class ScheduleQueryImpl(ScheduleQueryPort):
    def __init__(self, schedule_reader: ScheduleReaderPort) -> None:
        self._schedule_reader = schedule_reader

    async def find_by_id(self, schedule_id: int) -> Optional[Any]:
        return await self._schedule_reader.find_by_id(schedule_id)

    async def find_all(self) -> List[Any]:
        return await self._schedule_reader.find_all()
