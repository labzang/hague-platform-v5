# -*- coding: utf-8 -*-
"""Stadium reader output adapter — SQLAlchemy ORM 기반 `StadiumReader` 구현.

애플리케이션에서는 `StadiumQueryImpl(stadium_reader)`처럼 이 구현체를 주입해 조회 유스케이스를 구성한다.
"""

from typing import Any, List, Optional

from sqlalchemy import select

from labzang.apps.biz.soccer.stadium.application.dtos.stadium_dto import StadiumDTO
from labzang.apps.biz.soccer.stadium.adapter.outbound.orm.stadium_orm import StadiumORM
from labzang.apps.biz.soccer.stadium.application.ports.output.stadium_reader import (
    StadiumReader,
)
from labzang.core.database import AsyncSessionLocal


def _stadium_orm_to_dto(row: StadiumORM) -> StadiumDTO:
    return StadiumDTO(
        id=int(row.id),
        stadium_code=row.stadium_code,
        stadium_name=row.stadium_name,
        hometeam_code=row.hometeam_code,
        seat_count=row.seat_count,
        address=row.address,
        ddd=row.ddd,
        tel=row.tel,
        embedding_content=None,
        embedding=None,
        embedding_created_at=None,
    )


class StadiumReaderImpl(StadiumReader):
    """StadiumReader 포트 구현. AsyncSession으로 ORM 조회 후 DTO로 변환."""

    async def find_by_id(self, stadium_id: int) -> Optional[Any]:
        async with AsyncSessionLocal() as session:
            stmt = select(StadiumORM).where(StadiumORM.id == stadium_id)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return _stadium_orm_to_dto(row)

    async def find_all(self) -> List[Any]:
        async with AsyncSessionLocal() as session:
            stmt = select(StadiumORM)
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [_stadium_orm_to_dto(row) for row in rows]
