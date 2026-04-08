# -*- coding: utf-8 -*-
"""TeamCommand — 출력 포트(TeamRepositoryPort)를 통해 구현."""

from __future__ import annotations

from typing import Any, Dict, List

from labzang.apps.biz.field.provider.soccer.app.ports.input.team_command_port import (
    TeamCommandPort,
)
from labzang.apps.biz.field.provider.soccer.app.ports.output.team_repository_port import (
    TeamRepositoryPort,
)


class TeamCommandImpl(TeamCommandPort):
    def __init__(self, team_repository: TeamRepositoryPort) -> None:
        self._team_repository = team_repository

    async def upload_teams_batch(
        self, teams_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._team_repository.upsert_batch(teams_data)
