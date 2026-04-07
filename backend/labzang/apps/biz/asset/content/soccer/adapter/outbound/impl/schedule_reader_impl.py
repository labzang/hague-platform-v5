# -*- coding: utf-8 -*-
"""Schedule reader output adapter — SQLAlchemy ORM 기반 `ScheduleReader` 구현.

애플리케이션에서는 `ScheduleQueryImpl(schedule_reader)`처럼 이 구현체를 주입해 조회 유스케이스를 구성한다.
"""

from typing import Any, List, Optional

from sqlalchemy import select

from labzang.apps.biz.asset.content.soccer.application.dtos.schedule_dto import ScheduleDTO
from labzang.apps.biz.asset.content.soccer.adapter.outbound.orm.schedule_orm import ScheduleORM
from labzang.apps.biz.asset.content.soccer.application.ports.output.schedule_reader import (
    ScheduleReader,
)
from labzang.core.database import AsyncSessionLocal


def _schedule_orm_to_dto(row: ScheduleORM) -> ScheduleDTO:
    return ScheduleDTO(
        id=int(row.id),
        stadium_id=int(row.stadium_id) if row.stadium_id is not None else None,
        hometeam_id=int(row.hometeam_id) if row.hometeam_id is not None else None,
        awayteam_id=int(row.awayteam_id) if row.awayteam_id is not None else None,
        stadium_code=row.stadium_code,
        sche_date=row.sche_date,
        gubun=row.gubun,
        hometeam_code=row.hometeam_code,
        awayteam_code=row.awayteam_code,
        home_score=row.home_score,
        away_score=row.away_score,
        embedding_content=None,
        embedding=None,
        embedding_created_at=None,
    )


class ScheduleReaderImpl(ScheduleReader):
    """ScheduleReader 포트 구현. AsyncSession으로 ORM 조회 후 DTO로 변환."""

    async def find_by_id(self, schedule_id: int) -> Optional[Any]:
        async with AsyncSessionLocal() as session:
            stmt = select(ScheduleORM).where(ScheduleORM.id == schedule_id)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return _schedule_orm_to_dto(row)

    async def find_all(self) -> List[Any]:
        async with AsyncSessionLocal() as session:
            stmt = select(ScheduleORM)
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [_schedule_orm_to_dto(row) for row in rows]
