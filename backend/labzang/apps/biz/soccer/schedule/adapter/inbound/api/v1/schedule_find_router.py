# -*- coding: utf-8 -*-
"""Schedule read API — `ScheduleQuery` (find_all / find_by_id)."""

from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path

from labzang.apps.soccer.schedule.adapter.inbound.schemas.schedule_response import (
    ScheduleResponse,
)
from labzang.apps.soccer.schedule.adapter.outbound.impl.schedule_reader_impl import (
    ScheduleReaderImpl,
)
from labzang.apps.soccer.schedule.application.ports.input.schedule_query import (
    ScheduleQuery,
)
from labzang.apps.soccer.schedule.application.use_cases.schedule_query_impl import (
    ScheduleQueryImpl,
)

router = APIRouter()


def get_schedule_query() -> ScheduleQuery:
    """FastAPI Depends: wires output adapter into the query use case."""
    return ScheduleQueryImpl(ScheduleReaderImpl())


ScheduleQueryDep = Annotated[ScheduleQuery, Depends(get_schedule_query)]


@router.get(
    "",
    response_model=List[ScheduleResponse],
    summary="List all schedules",
)
async def list_schedules(
    query: ScheduleQueryDep,
) -> List[ScheduleResponse]:
    rows = await query.find_all()
    return [ScheduleResponse.from_schedule_dto(dto) for dto in rows]


@router.get(
    "/{schedule_id}",
    response_model=ScheduleResponse,
    summary="Get schedule by id",
)
async def get_schedule_by_id(
    query: ScheduleQueryDep,
    schedule_id: int = Path(..., gt=0, description="Schedule primary key"),
) -> ScheduleResponse:
    dto = await query.find_by_id(schedule_id)
    if dto is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return ScheduleResponse.from_schedule_dto(dto)
