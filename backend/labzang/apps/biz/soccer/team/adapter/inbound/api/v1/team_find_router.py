# -*- coding: utf-8 -*-
"""Team read API — `TeamQuery` (find_all / find_by_id)."""

from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path

from labzang.apps.biz.soccer.team.adapter.inbound.schemas.team_response import TeamResponse
from labzang.apps.biz.soccer.team.adapter.outbound.impl.team_reader_impl import (
    TeamReaderImpl,
)
from labzang.apps.biz.soccer.team.application.ports.input.team_query import TeamQuery
from labzang.apps.biz.soccer.team.application.use_cases.team_query_impl import TeamQueryImpl

router = APIRouter()


def get_team_query() -> TeamQuery:
    """FastAPI Depends: wires output adapter into the query use case."""
    return TeamQueryImpl(TeamReaderImpl())


TeamQueryDep = Annotated[TeamQuery, Depends(get_team_query)]


@router.get(
    "",
    response_model=List[TeamResponse],
    summary="List all teams",
)
async def list_teams(
    query: TeamQueryDep,
) -> List[TeamResponse]:
    rows = await query.find_all()
    return [TeamResponse.from_team_dto(dto) for dto in rows]


@router.get(
    "/{team_id}",
    response_model=TeamResponse,
    summary="Get team by id",
)
async def get_team_by_id(
    query: TeamQueryDep,
    team_id: int = Path(..., gt=0, description="Team primary key"),
) -> TeamResponse:
    dto = await query.find_by_id(team_id)
    if dto is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamResponse.from_team_dto(dto)
