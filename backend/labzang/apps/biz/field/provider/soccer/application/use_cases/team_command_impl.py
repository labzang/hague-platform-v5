# -*- coding: utf-8 -*-
"""TeamCommand — 출력 포트(TeamRepository)를 통해 구현."""

from __future__ import annotations

from typing import Any, Dict, List

from labzang.apps.biz.asset.content.soccer.application.ports.input.team_command import TeamCommand
from labzang.apps.biz.asset.content.soccer.application.ports.output.team_repository import (
    TeamRepository,
)


class TeamCommandImpl(TeamCommand):
    def __init__(self, team_repository: TeamRepository) -> None:
        self._team_repository = team_repository

    async def upload_teams_batch(
        self, teams_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._team_repository.upsert_batch(teams_data)
