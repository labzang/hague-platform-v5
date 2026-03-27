# -*- coding: utf-8 -*-
"""ScheduleCommand — 출력 포트(ScheduleRepository)를 통해 구현."""

from __future__ import annotations

from typing import Any, Dict, List

from labzang.apps.biz.soccer.schedule.application.ports.input.schedule_command import (
    ScheduleCommand,
)
from labzang.apps.biz.soccer.schedule.application.ports.output.schedule_repository import (
    ScheduleRepository,
)


class ScheduleCommandImpl(ScheduleCommand):
    def __init__(self, schedule_repository: ScheduleRepository) -> None:
        self._schedule_repository = schedule_repository

    async def upload_schedules_batch(
        self, schedules_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._schedule_repository.upsert_batch(schedules_data)
