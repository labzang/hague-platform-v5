# -*- coding: utf-8 -*-
"""Stadium read API — `StadiumQuery` (find_all / find_by_id)."""

from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path

from labzang.apps.biz.asset.content.soccer.adapter.inbound.schemas.stadium_response import (
    StadiumResponse,
)
from labzang.apps.biz.asset.content.soccer.adapter.outbound.impl.stadium_reader_impl import (
    StadiumReaderImpl,
)
from labzang.apps.biz.asset.content.soccer.application.ports.input.stadium_query import (
    StadiumQuery,
)
from labzang.apps.biz.asset.content.soccer.application.use_cases.stadium_query_impl import (
    StadiumQueryImpl,
)

router = APIRouter()


def get_stadium_query() -> StadiumQuery:
    """FastAPI Depends: wires output adapter into the query use case."""
    return StadiumQueryImpl(StadiumReaderImpl())


StadiumQueryDep = Annotated[StadiumQuery, Depends(get_stadium_query)]


@router.get(
    "",
    response_model=List[StadiumResponse],
    summary="List all stadiums",
)
async def list_stadiums(
    query: StadiumQueryDep,
) -> List[StadiumResponse]:
    rows = await query.find_all()
    return [StadiumResponse.from_stadium_dto(dto) for dto in rows]


@router.get(
    "/{stadium_id}",
    response_model=StadiumResponse,
    summary="Get stadium by id",
)
async def get_stadium_by_id(
    query: StadiumQueryDep,
    stadium_id: int = Path(..., gt=0, description="Stadium primary key"),
) -> StadiumResponse:
    dto = await query.find_by_id(stadium_id)
    if dto is None:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return StadiumResponse.from_stadium_dto(dto)
