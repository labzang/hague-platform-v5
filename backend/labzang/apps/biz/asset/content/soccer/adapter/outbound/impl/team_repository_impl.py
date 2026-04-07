# -*- coding: utf-8 -*-
"""TeamRepository port — domain `Team` -> `TeamORM` upsert into `teams`."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from sqlalchemy import select

from labzang.apps.biz.asset.content.soccer.adapter.outbound.orm.team_orm import TeamORM
from labzang.apps.biz.asset.content.soccer.application.ports.output.team_repository import (
    TeamRepository,
)
from labzang.apps.biz.asset.content.soccer.domain.entities.team import Team
from labzang.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


def _apply_entity_to_orm(orm_row: TeamORM, entity: Team) -> None:
    """Copy domain entity fields onto a SQLAlchemy row (excluding PK)."""
    orm_row.stadium_id = entity.stadium_id.value if entity.stadium_id else None
    orm_row.team_code = entity.team_code.value if entity.team_code else None
    orm_row.region_name = entity.region_name.value if entity.region_name else None
    orm_row.team_name = entity.team_name.value if entity.team_name else None
    orm_row.e_team_name = entity.e_team_name.value if entity.e_team_name else None
    orm_row.orig_yyyy = entity.orig_yyyy.value if entity.orig_yyyy else None
    orm_row.zip_code1 = entity.zip_code1.value if entity.zip_code1 else None
    orm_row.zip_code2 = entity.zip_code2.value if entity.zip_code2 else None
    orm_row.address = entity.address.value if entity.address else None
    orm_row.ddd = entity.ddd.value if entity.ddd else None
    orm_row.tel = entity.tel.value if entity.tel else None
    orm_row.fax = entity.fax.value if entity.fax else None
    orm_row.homepage = entity.homepage.value if entity.homepage else None
    orm_row.owner = entity.owner.value if entity.owner else None


class TeamRepositoryImpl(TeamRepository):
    async def upsert_batch(self, teams_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        inserted = 0
        updated = 0
        errors = 0
        for raw in teams_data:
            async with AsyncSessionLocal() as session:
                try:
                    entity = Team.from_json_dict(raw)
                except (TypeError, ValueError) as e:
                    logger.warning("invalid team row (domain): %s keys=%s", e, raw.keys())
                    errors += 1
                    continue
                try:
                    tid = entity.team_id.value
                    res = await session.execute(select(TeamORM).where(TeamORM.id == tid))
                    existing = res.scalar_one_or_none()
                    if existing:
                        _apply_entity_to_orm(existing, entity)
                        updated += 1
                    else:
                        newbie = TeamORM(id=tid)
                        _apply_entity_to_orm(newbie, entity)
                        session.add(newbie)
                        inserted += 1
                    await session.commit()
                except Exception:
                    logger.exception("team upsert failed for id=%s", raw.get("id"))
                    await session.rollback()
                    errors += 1
        return {
            "inserted_count": inserted,
            "updated_count": updated,
            "error_count": errors,
        }

    async def commit(self) -> None:
        pass
