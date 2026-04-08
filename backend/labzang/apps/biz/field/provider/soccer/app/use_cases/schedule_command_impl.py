# -*- coding: utf-8 -*-
"""ScheduleCommand — 출력 포트(ScheduleRepositoryPort)를 통해 구현."""

from __future__ import annotations

from typing import Any, Dict, List

from labzang.apps.biz.field.provider.soccer.app.ports.input.schedule_command_port import (
    ScheduleCommandPort,
)
from labzang.apps.biz.field.provider.soccer.app.ports.output.schedule_repository_port import (
    ScheduleRepositoryPort,
)


class ScheduleCommandImpl(ScheduleCommandPort):
    def __init__(self, schedule_repository: ScheduleRepositoryPort) -> None:
        self._schedule_repository = schedule_repository

    async def upload_schedules_batch(
        self, schedules_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._schedule_repository.upsert_batch(schedules_data)
