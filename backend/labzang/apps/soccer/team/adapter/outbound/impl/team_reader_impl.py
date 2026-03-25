# -*- coding: utf-8 -*-
"""Team reader output adapter — SQLAlchemy ORM 기반 `TeamReader` 구현.

애플리케이션에서는 `TeamQueryImpl(team_reader)`처럼 이 구현체를 주입해 조회 유스케이스를 구성한다.
"""

from typing import Any, List, Optional

from sqlalchemy import select

from labzang.apps.soccer.application.dtos.team_dto import TeamDTO
from labzang.apps.soccer.team.adapter.outbound.orm.team_orm import TeamORM
from labzang.apps.soccer.team.application.ports.output.team_reader import TeamReader
from labzang.core.database import AsyncSessionLocal


def _team_orm_to_dto(row: TeamORM) -> TeamDTO:
    return TeamDTO(
        id=int(row.id),
        stadium_id=int(row.stadium_id) if row.stadium_id is not None else None,
        team_code=row.team_code,
        region_name=row.region_name,
        team_name=row.team_name,
        e_team_name=row.e_team_name,
        orig_yyyy=row.orig_yyyy,
        zip_code1=row.zip_code1,
        zip_code2=row.zip_code2,
        address=row.address,
        ddd=row.ddd,
        tel=row.tel,
        fax=row.fax,
        homepage=row.homepage,
        owner=row.owner,
        embedding_content=None,
        embedding=None,
        embedding_created_at=None,
    )


class TeamReaderImpl(TeamReader):
    """TeamReader 포트 구현. AsyncSession으로 ORM 조회 후 DTO로 변환."""

    async def find_by_id(self, team_id: int) -> Optional[Any]:
        async with AsyncSessionLocal() as session:
            stmt = select(TeamORM).where(TeamORM.id == team_id)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()
            if row is None:
                return None
            return _team_orm_to_dto(row)

    async def find_all(self) -> List[Any]:
        async with AsyncSessionLocal() as session:
            stmt = select(TeamORM)
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [_team_orm_to_dto(row) for row in rows]
