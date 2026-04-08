# -*- coding: utf-8 -*-
"""PlayerQuery — 출력 포트 `PlayerReaderPort`에 위임."""

from __future__ import annotations

from typing import Any, List, Optional

from labzang.apps.biz.field.provider.soccer.app.ports.input.player_query_port import (
    PlayerQueryPort,
)
from labzang.apps.biz.field.provider.soccer.app.ports.output.player_reader_port import (
    PlayerReaderPort,
)


class PlayerQueryImpl(PlayerQueryPort):
    def __init__(self, player_reader: PlayerReaderPort) -> None:
        self._player_reader = player_reader

    async def find_by_id(self, player_id: int) -> Optional[Any]:
        return await self._player_reader.find_by_id(player_id)

    async def find_all(self) -> List[Any]:
        return await self._player_reader.find_all()
