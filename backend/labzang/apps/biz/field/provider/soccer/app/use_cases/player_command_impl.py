# -*- coding: utf-8 -*-
"""PlayerCommand — 출력 포트(PlayerRepositoryPort)를 통해 구현."""

from __future__ import annotations

from typing import Any, Dict, List

from labzang.apps.biz.field.provider.soccer.app.ports.input.player_command_port import (
    PlayerCommandPort,
)
from labzang.apps.biz.field.provider.soccer.app.ports.output.player_repository_port import (
    PlayerRepositoryPort,
)


class PlayerCommandImpl(PlayerCommandPort):
    def __init__(self, player_repository: PlayerRepositoryPort) -> None:
        self._player_repository = player_repository

    async def upload_players_batch(
        self, players_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._player_repository.upsert_batch(players_data)
