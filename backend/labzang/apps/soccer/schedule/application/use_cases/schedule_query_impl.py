# -*- coding: utf-8 -*-
"""ScheduleQuery — 출력 포트 `ScheduleReader`에 위임."""

from __future__ import annotations

from typing import Any, List, Optional

from labzang.apps.soccer.schedule.application.ports.input.schedule_query import (
    ScheduleQuery,
)
from labzang.apps.soccer.schedule.application.ports.output.schedule_reader import (
    ScheduleReader,
)


class ScheduleQueryImpl(ScheduleQuery):
    def __init__(self, schedule_reader: ScheduleReader) -> None:
        self._schedule_reader = schedule_reader

    async def find_by_id(self, schedule_id: int) -> Optional[Any]:
        return await self._schedule_reader.find_by_id(schedule_id)

    async def find_all(self) -> List[Any]:
        return await self._schedule_reader.find_all()
