# -*- coding: utf-8 -*-
"""StadiumRepository port — domain `Stadium` -> `StadiumORM` upsert into `stadiums`."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from sqlalchemy import select

from labzang.apps.biz.soccer.stadium.adapter.outbound.orm.stadium_orm import StadiumORM
from labzang.apps.biz.soccer.stadium.application.ports.output.stadium_repository import (
    StadiumRepository,
)
from labzang.apps.biz.soccer.stadium.domain.entities.stadium import Stadium
from labzang.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


def _apply_entity_to_orm(orm_row: StadiumORM, entity: Stadium) -> None:
    """Copy domain entity fields onto a SQLAlchemy row (excluding PK)."""
    orm_row.stadium_code = entity.stadium_code.value if entity.stadium_code else None
    orm_row.stadium_name = entity.stadium_name.value if entity.stadium_name else None
    orm_row.hometeam_code = entity.hometeam_code.value if entity.hometeam_code else None
    orm_row.seat_count = entity.seat_count.value if entity.seat_count else None
    orm_row.address = entity.address.value if entity.address else None
    orm_row.ddd = entity.ddd.value if entity.ddd else None
    orm_row.tel = entity.tel.value if entity.tel else None


class StadiumRepositoryImpl(StadiumRepository):
    async def upsert_batch(self, stadiums_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        inserted = 0
        updated = 0
        errors = 0
        for raw in stadiums_data:
            async with AsyncSessionLocal() as session:
                try:
                    entity = Stadium.from_json_dict(raw)
                except (TypeError, ValueError) as e:
                    logger.warning(
                        "invalid stadium row (domain): %s keys=%s", e, raw.keys()
                    )
                    errors += 1
                    continue
                try:
                    sid = entity.stadium_id.value
                    res = await session.execute(
                        select(StadiumORM).where(StadiumORM.id == sid)
                    )
                    existing = res.scalar_one_or_none()
                    if existing:
                        _apply_entity_to_orm(existing, entity)
                        updated += 1
                    else:
                        newbie = StadiumORM(id=sid)
                        _apply_entity_to_orm(newbie, entity)
                        session.add(newbie)
                        inserted += 1
                    await session.commit()
                except Exception:
                    logger.exception("stadium upsert failed for id=%s", raw.get("id"))
                    await session.rollback()
                    errors += 1
        return {
            "inserted_count": inserted,
            "updated_count": updated,
            "error_count": errors,
        }

    async def commit(self) -> None:
        pass
