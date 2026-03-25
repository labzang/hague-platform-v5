# -*- coding: utf-8 -*-
"""인바운드 API 요청 스키마 — 경기장 검색."""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, Query
from pydantic import BaseModel, ConfigDict, Field


class StadiumSearchRequest(BaseModel):
    """경기장 목록/검색 요청. 필터는 `StadiumDTO` 제약과 맞추며 모두 생략 가능."""

    model_config = ConfigDict(str_strip_whitespace=True)

    stadium_code: Optional[str] = Field(default=None, max_length=10)
    stadium_name: Optional[str] = Field(
        default=None,
        max_length=60,
        description="경기장명 (부분 일치 등은 유스케이스 정책)",
    )
    hometeam_code: Optional[str] = Field(default=None, max_length=10)
    seat_count_min: Optional[int] = Field(default=None, ge=0)
    seat_count_max: Optional[int] = Field(default=None, ge=0)
    address: Optional[str] = Field(default=None, max_length=80)
    ddd: Optional[str] = Field(default=None, max_length=10)
    tel: Optional[str] = Field(default=None, max_length=20)

    limit: int = Field(default=20, ge=1, le=200, description="최대 반환 건수")
    offset: int = Field(default=0, ge=0, description="건너뛸 건수")


def get_stadium_search_params(
    stadium_code: Optional[str] = Query(None, max_length=10),
    stadium_name: Optional[str] = Query(None, max_length=60),
    hometeam_code: Optional[str] = Query(None, max_length=10),
    seat_count_min: Optional[int] = Query(None, ge=0),
    seat_count_max: Optional[int] = Query(None, ge=0),
    address: Optional[str] = Query(None, max_length=80),
    ddd: Optional[str] = Query(None, max_length=10),
    tel: Optional[str] = Query(None, max_length=20),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> StadiumSearchRequest:
    return StadiumSearchRequest(
        stadium_code=stadium_code,
        stadium_name=stadium_name,
        hometeam_code=hometeam_code,
        seat_count_min=seat_count_min,
        seat_count_max=seat_count_max,
        address=address,
        ddd=ddd,
        tel=tel,
        limit=limit,
        offset=offset,
    )


StadiumSearchQuery = Annotated[StadiumSearchRequest, Depends(get_stadium_search_params)]

__all__ = [
    "StadiumSearchQuery",
    "StadiumSearchRequest",
    "get_stadium_search_params",
]
