# -*- coding: utf-8 -*-
"""TeamQuery — 출력 포트 `TeamReaderPort`에 위임."""

from __future__ import annotations

from typing import Any, List, Optional

from labzang.apps.biz.field.provider.soccer.app.ports.input.team_query_port import (
    TeamQueryPort,
)
from labzang.apps.biz.field.provider.soccer.app.ports.output.team_reader_port import (
    TeamReaderPort,
)


class TeamQueryImpl(TeamQueryPort):
    def __init__(self, team_reader: TeamReaderPort) -> None:
        self._team_reader = team_reader

    async def find_by_id(self, team_id: int) -> Optional[Any]:
        return await self._team_reader.find_by_id(team_id)

    async def find_all(self) -> List[Any]:
        return await self._team_reader.find_all()
