# -*- coding: utf-8 -*-
"""인바운드 API 요청 스키마 — 선수 검색."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Optional

from fastapi import Depends, Query
from pydantic import BaseModel, ConfigDict, Field


class PlayerSearchRequest(BaseModel):
    """선수 목록/검색 요청.

    필터는 `PlayerDTO` 필드와 동일한 이름·제약을 따르며, 모두 생략 가능하다.
    유스케이스에서 `player_name` 등은 부분 일치(contains)로 해석할 수 있다.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    team_id: Optional[int] = Field(default=None, gt=0)
    player_name: Optional[str] = Field(
        default=None,
        max_length=20,
        description="선수명 (부분 일치 검색 등, 애플리케이션 정책에 따름)",
    )
    e_player_name: Optional[str] = Field(default=None, max_length=40)
    nickname: Optional[str] = Field(default=None, max_length=30)
    join_yyyy: Optional[str] = Field(default=None, max_length=10)
    position: Optional[str] = Field(default=None, max_length=10)
    back_no: Optional[int] = Field(default=None, ge=0, le=99)
    nation: Optional[str] = Field(default=None, max_length=20)
    birth_date: Optional[date] = None
    solar: Optional[str] = Field(default=None, max_length=10)
    height: Optional[int] = Field(default=None, ge=50, le=280)
    weight: Optional[int] = Field(default=None, ge=20, le=200)

    limit: int = Field(default=20, ge=1, le=200, description="최대 반환 건수")
    offset: int = Field(default=0, ge=0, description="건너뛸 건수")


def get_player_search_params(
    team_id: Optional[int] = Query(None, gt=0, description="팀 ID"),
    player_name: Optional[str] = Query(
        None,
        max_length=20,
        description="선수명 (부분 일치)",
    ),
    e_player_name: Optional[str] = Query(None, max_length=40),
    nickname: Optional[str] = Query(None, max_length=30),
    join_yyyy: Optional[str] = Query(None, max_length=10),
    position: Optional[str] = Query(None, max_length=10),
    back_no: Optional[int] = Query(None, ge=0, le=99),
    nation: Optional[str] = Query(None, max_length=20),
    birth_date: Optional[date] = Query(None, description="YYYY-MM-DD"),
    solar: Optional[str] = Query(None, max_length=10),
    height: Optional[int] = Query(None, ge=50, le=280),
    weight: Optional[int] = Query(None, ge=20, le=200),
    limit: int = Query(20, ge=1, le=200, description="최대 반환 건수"),
    offset: int = Query(0, ge=0, description="건너뛸 건수"),
) -> PlayerSearchRequest:
    """GET 쿼리 스트링을 `PlayerSearchRequest`로 묶는 FastAPI 의존성."""
    return PlayerSearchRequest(
        team_id=team_id,
        player_name=player_name,
        e_player_name=e_player_name,
        nickname=nickname,
        join_yyyy=join_yyyy,
        position=position,
        back_no=back_no,
        nation=nation,
        birth_date=birth_date,
        solar=solar,
        height=height,
        weight=weight,
        limit=limit,
        offset=offset,
    )


PlayerSearchQuery = Annotated[PlayerSearchRequest, Depends(get_player_search_params)]

__all__ = [
    "PlayerSearchQuery",
    "PlayerSearchRequest",
    "get_player_search_params",
]
