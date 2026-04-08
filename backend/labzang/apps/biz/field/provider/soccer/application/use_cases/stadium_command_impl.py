# -*- coding: utf-8 -*-
"""StadiumCommand — 출력 포트(StadiumRepository)를 통해 구현."""

from __future__ import annotations

from typing import Any, Dict, List

from labzang.apps.biz.asset.content.soccer.application.ports.input.stadium_command import (
    StadiumCommand,
)
from labzang.apps.biz.asset.content.soccer.application.ports.output.stadium_repository import (
    StadiumRepository,
)


class StadiumCommandImpl(StadiumCommand):
    def __init__(self, stadium_repository: StadiumRepository) -> None:
        self._stadium_repository = stadium_repository

    async def upload_stadiums_batch(
        self, stadiums_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._stadium_repository.upsert_batch(stadiums_data)
