# -*- coding: utf-8 -*-
"""인바운드 API 요청 스키마 — 일정 검색."""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, Query
from pydantic import BaseModel, ConfigDict, Field


class ScheduleSearchRequest(BaseModel):
    """일정 목록/검색 요청. 필터는 `ScheduleDTO` 제약과 맞추며 모두 생략 가능."""

    model_config = ConfigDict(str_strip_whitespace=True)

    stadium_id: Optional[int] = Field(default=None, gt=0)
    hometeam_id: Optional[int] = Field(default=None, gt=0)
    awayteam_id: Optional[int] = Field(default=None, gt=0)
    stadium_code: Optional[str] = Field(default=None, max_length=10)
    sche_date: Optional[str] = Field(
        default=None,
        max_length=10,
        description="경기 일자 YYYYMMDD (유스케이스에서 범위/부분 일치 정책 적용 가능)",
    )
    gubun: Optional[str] = Field(default=None, max_length=5)
    hometeam_code: Optional[str] = Field(default=None, max_length=10)
    awayteam_code: Optional[str] = Field(default=None, max_length=10)
    home_score_min: Optional[int] = Field(default=None, ge=0)
    home_score_max: Optional[int] = Field(default=None, ge=0)
    away_score_min: Optional[int] = Field(default=None, ge=0)
    away_score_max: Optional[int] = Field(default=None, ge=0)

    limit: int = Field(default=20, ge=1, le=200, description="최대 반환 건수")
    offset: int = Field(default=0, ge=0, description="건너뛸 건수")


def get_schedule_search_params(
    stadium_id: Optional[int] = Query(None, gt=0),
    hometeam_id: Optional[int] = Query(None, gt=0),
    awayteam_id: Optional[int] = Query(None, gt=0),
    stadium_code: Optional[str] = Query(None, max_length=10),
    sche_date: Optional[str] = Query(None, max_length=10),
    gubun: Optional[str] = Query(None, max_length=5),
    hometeam_code: Optional[str] = Query(None, max_length=10),
    awayteam_code: Optional[str] = Query(None, max_length=10),
    home_score_min: Optional[int] = Query(None, ge=0),
    home_score_max: Optional[int] = Query(None, ge=0),
    away_score_min: Optional[int] = Query(None, ge=0),
    away_score_max: Optional[int] = Query(None, ge=0),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> ScheduleSearchRequest:
    return ScheduleSearchRequest(
        stadium_id=stadium_id,
        hometeam_id=hometeam_id,
        awayteam_id=awayteam_id,
        stadium_code=stadium_code,
        sche_date=sche_date,
        gubun=gubun,
        hometeam_code=hometeam_code,
        awayteam_code=awayteam_code,
        home_score_min=home_score_min,
        home_score_max=home_score_max,
        away_score_min=away_score_min,
        away_score_max=away_score_max,
        limit=limit,
        offset=offset,
    )


ScheduleSearchQuery = Annotated[
    ScheduleSearchRequest, Depends(get_schedule_search_params)
]

__all__ = [
    "ScheduleSearchQuery",
    "ScheduleSearchRequest",
    "get_schedule_search_params",
]
