# -*- coding: utf-8 -*-
"""PlayerCommand — 출력 포트(PlayerRepository)를 통해 구현."""

from __future__ import annotations

from typing import Any, Dict, List

from labzang.apps.biz.soccer.player.application.ports.input.player_command import (
    PlayerCommand,
)
from labzang.apps.biz.soccer.player.application.ports.output.player_repository import (
    PlayerRepository,
)


class PlayerCommandImpl(PlayerCommand):
    def __init__(self, player_repository: PlayerRepository) -> None:
        self._player_repository = player_repository

    async def upload_players_batch(
        self, players_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return await self._player_repository.upsert_batch(players_data)
