# -*- coding: utf-8 -*-
"""PlayerRepository port — domain `Player` -> `PlayerORM` upsert into `players`."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from sqlalchemy import select

from labzang.apps.soccer.player.adapter.outbound.orm.player_orm import PlayerORM
from labzang.apps.soccer.player.application.ports.output.player_repository import (
    PlayerRepository,
)
from labzang.apps.soccer.player.domain.entities.player import Player
from labzang.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


def _apply_entity_to_orm(orm_row: PlayerORM, entity: Player) -> None:
    """Copy domain entity fields onto a SQLAlchemy row (excluding PK)."""
    orm_row.team_id = entity.team_id.value if entity.team_id else None
    orm_row.player_name = entity.player_name.value if entity.player_name else None
    orm_row.e_player_name = entity.e_player_name.value if entity.e_player_name else None
    orm_row.nickname = entity.nickname.value if entity.nickname else None
    orm_row.join_yyyy = entity.join_year.value if entity.join_year else None
    orm_row.position = entity.position.value if entity.position else None
    orm_row.back_no = entity.back_number.value if entity.back_number else None
    orm_row.nation = entity.nation.value if entity.nation else None
    orm_row.birth_date = entity.birth_date.value if entity.birth_date else None
    orm_row.solar = entity.solar.value if entity.solar else None
    orm_row.height = entity.height.value if entity.height else None
    orm_row.weight = entity.weight.value if entity.weight else None


class PlayerRepositoryImpl(PlayerRepository):
    async def upsert_batch(self, players_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        inserted = 0
        updated = 0
        errors = 0
        for raw in players_data:
            async with AsyncSessionLocal() as session:
                try:
                    entity = Player.from_json_dict(raw)
                except (TypeError, ValueError) as e:
                    logger.warning("invalid player row (domain): %s keys=%s", e, raw.keys())
                    errors += 1
                    continue
                try:
                    pid = entity.player_id.value
                    res = await session.execute(
                        select(PlayerORM).where(PlayerORM.id == pid)
                    )
                    existing = res.scalar_one_or_none()
                    if existing:
                        _apply_entity_to_orm(existing, entity)
                        updated += 1
                    else:
                        newbie = PlayerORM(id=pid)
                        _apply_entity_to_orm(newbie, entity)
                        session.add(newbie)
                        inserted += 1
                    await session.commit()
                except Exception:
                    logger.exception("player upsert failed for id=%s", raw.get("id"))
                    await session.rollback()
                    errors += 1
        return {
            "inserted_count": inserted,
            "updated_count": updated,
            "error_count": errors,
        }

    async def commit(self) -> None:
        pass
