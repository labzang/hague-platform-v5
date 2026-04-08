# -*- coding: utf-8 -*-
"""ScheduleRepository port — domain `Schedule` -> `ScheduleORM` upsert into `schedules`."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from sqlalchemy import select

from labzang.apps.biz.asset.content.soccer.adapter.outbound.orm.schedule_orm import ScheduleORM
from labzang.apps.biz.asset.content.soccer.application.ports.output.schedule_repository import (
    ScheduleRepository,
)
from labzang.apps.biz.asset.content.soccer.domain.entities.schedule import Schedule
from labzang.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


def _apply_entity_to_orm(orm_row: ScheduleORM, entity: Schedule) -> None:
    """Copy domain entity fields onto a SQLAlchemy row (excluding PK)."""
    orm_row.stadium_id = entity.stadium_id.value if entity.stadium_id else None
    orm_row.hometeam_id = entity.hometeam_id.value if entity.hometeam_id else None
    orm_row.awayteam_id = entity.awayteam_id.value if entity.awayteam_id else None
    orm_row.stadium_code = entity.stadium_code.value if entity.stadium_code else None
    orm_row.sche_date = entity.sche_date.value if entity.sche_date else None
    orm_row.gubun = entity.gubun.value if entity.gubun else None
    orm_row.hometeam_code = entity.hometeam_code.value if entity.hometeam_code else None
    orm_row.awayteam_code = entity.awayteam_code.value if entity.awayteam_code else None
    orm_row.home_score = entity.home_score.value if entity.home_score else None
    orm_row.away_score = entity.away_score.value if entity.away_score else None


class ScheduleRepositoryImpl(ScheduleRepository):
    async def upsert_batch(self, schedules_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        inserted = 0
        updated = 0
        errors = 0
        for raw in schedules_data:
            async with AsyncSessionLocal() as session:
                try:
                    entity = Schedule.from_json_dict(raw)
                except (TypeError, ValueError) as e:
                    logger.warning(
                        "invalid schedule row (domain): %s keys=%s", e, raw.keys()
                    )
                    errors += 1
                    continue
                try:
                    sid = entity.schedule_id.value
                    res = await session.execute(
                        select(ScheduleORM).where(ScheduleORM.id == sid)
                    )
                    existing = res.scalar_one_or_none()
                    if existing:
                        _apply_entity_to_orm(existing, entity)
                        updated += 1
                    else:
                        newbie = ScheduleORM(id=sid)
                        _apply_entity_to_orm(newbie, entity)
                        session.add(newbie)
                        inserted += 1
                    await session.commit()
                except Exception:
                    logger.exception(
                        "schedule upsert failed for id=%s", raw.get("id")
                    )
                    await session.rollback()
                    errors += 1
        return {
            "inserted_count": inserted,
            "updated_count": updated,
            "error_count": errors,
        }

    async def commit(self) -> None:
        pass
