# -*- coding: utf-8 -*-
"""Player reader output adapter — SQLAlchemy ORM 기반 `PlayerReader` 구현.

애플리케이션에서는 `PlayerQueryImpl(player_reader)`처럼 이 구현체를 주입해 조회 유스케이스를 구성한다.
"""

from typing import Any, List, Optional

from sqlalchemy import select

from labzang.apps.biz.soccer.player.application.dtos.player_dto import PlayerDTO
from labzang.apps.biz.soccer.player.adapter.outbound.orm.player_orm import PlayerORM
from labzang.apps.biz.soccer.player.application.ports.output.player_reader import (
    PlayerReader,
)
from labzang.core.database import AsyncSessionLocal


def _player_orm_to_dto(row: PlayerORM) -> PlayerDTO:
    return PlayerDTO(
        id=int(row.id),
        team_id=int(row.team_id) if row.team_id is not None else None,
        player_name=row.player_name,
        e_player_name=row.e_player_name,
        nickname=row.nickname,
        join_yyyy=row.join_yyyy,
        position=row.position,
        back_no=row.back_no,
        nation=row.nation,
        birth_date=row.birth_date,
        solar=row.solar,
        height=row.height,
        weight=row.weight,
    )


class PlayerReaderImpl(PlayerReader):
    """PlayerReader 포트 구현. AsyncSession으로 ORM 조회 후 DTO로 변환."""

    async def find_by_id(self, player_id: int) -> Optional[Any]:
        async with AsyncSessionLocal() as session:
            stmt = select(PlayerORM).where(PlayerORM.id == player_id)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return _player_orm_to_dto(row)

    async def find_all(self) -> List[Any]:
        async with AsyncSessionLocal() as session:
            stmt = select(PlayerORM)
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [ _player_orm_to_dto(row) for row in rows ]
