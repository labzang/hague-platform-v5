# -*- coding: utf-8 -*-
"""PlayerQuery — 출력 포트 `PlayerReader`에 위임."""

from __future__ import annotations

from typing import Any, List, Optional

from labzang.apps.soccer.player.application.ports.input.player_query import PlayerQuery
from labzang.apps.soccer.player.application.ports.output.player_reader import (
    PlayerReader,
)


class PlayerQueryImpl(PlayerQuery):
    def __init__(self, player_reader: PlayerReader) -> None:
        self._player_reader = player_reader

    async def find_by_id(self, player_id: int) -> Optional[Any]:
        return await self._player_reader.find_by_id(player_id)

    async def find_all(self) -> List[Any]:
        return await self._player_reader.find_all()
