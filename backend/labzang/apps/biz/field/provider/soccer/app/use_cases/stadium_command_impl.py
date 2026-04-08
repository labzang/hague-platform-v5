# -*- coding: utf-8 -*-
"""StadiumCommand — 출력 포트(StadiumRepositoryPort)를 통해 구현."""

from __future__ import annotations

from typing import Any, Dict, List

from labzang.apps.biz.field.provider.soccer.app.ports.input.stadium_command_port import (
    StadiumCommandPort,
)
from labzang.apps.biz.field.provider.soccer.app.ports.output.stadium_repository_port import (
    StadiumRepositoryPort,
)


class StadiumCommandImpl(StadiumCommandPort):
    def __init__(self, stadium_repository: StadiumRepositoryPort) -> None:
        self._stadium_repository = stadium_repository

    async def upload_stadiums_batch(
        self, stadiums_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._stadium_repository.upsert_batch(stadiums_data)
