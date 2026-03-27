# -*- coding: utf-8 -*-
"""Player read API — `PlayerQuery` (find_all / find_by_id)."""

from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path
from labzang.apps.biz.soccer.player.application.use_cases.player_query_impl import PlayerQueryImpl
from labzang.apps.biz.soccer.player.application.ports.input.player_query import PlayerQuery
from labzang.apps.biz.soccer.player.adapter.outbound.impl.player_reader_impl import PlayerReaderImpl
from labzang.apps.biz.soccer.player.adapter.inbound.schemas.player_response import PlayerResponse
router = APIRouter()


def get_player_query() -> PlayerQuery:
    """FastAPI Depends: wires output adapter into the query use case."""
    return PlayerQueryImpl(PlayerReaderImpl())


PlayerQueryDep = Annotated[PlayerQuery, Depends(get_player_query)]


@router.get(
    "",
    response_model=List[PlayerResponse],
    summary="List all players",
)
async def list_players(
    query: PlayerQueryDep,
) -> List[PlayerResponse]:
    rows = await query.find_all()
    return [PlayerResponse.from_player_dto(dto) for dto in rows]


@router.get(
    "/{player_id}",
    response_model=PlayerResponse,
    summary="Get player by id",
)
async def get_player_by_id(
    query: PlayerQueryDep,
    player_id: int = Path(..., gt=0, description="Player primary key"),
) -> PlayerResponse:
    dto = await query.find_by_id(player_id)
    if dto is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return PlayerResponse.from_player_dto(dto)
