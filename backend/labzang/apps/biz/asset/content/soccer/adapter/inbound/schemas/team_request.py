# -*- coding: utf-8 -*-
"""인바운드 API 요청 스키마 — 팀 검색."""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, Query
from pydantic import BaseModel, ConfigDict, Field


class TeamSearchRequest(BaseModel):
    """팀 목록/검색 요청. 필터는 `TeamDTO` 제약과 맞추며 모두 생략 가능."""

    model_config = ConfigDict(str_strip_whitespace=True)

    stadium_id: Optional[int] = Field(default=None, gt=0)
    team_code: Optional[str] = Field(default=None, max_length=10)
    region_name: Optional[str] = Field(default=None, max_length=10)
    team_name: Optional[str] = Field(
        default=None,
        max_length=40,
        description="팀명 (부분 일치 등은 유스케이스 정책)",
    )
    e_team_name: Optional[str] = Field(default=None, max_length=50)
    orig_yyyy: Optional[str] = Field(default=None, max_length=10)
    zip_code1: Optional[str] = Field(default=None, max_length=10)
    zip_code2: Optional[str] = Field(default=None, max_length=10)
    address: Optional[str] = Field(default=None, max_length=80)
    ddd: Optional[str] = Field(default=None, max_length=10)
    tel: Optional[str] = Field(default=None, max_length=20)
    fax: Optional[str] = Field(default=None, max_length=20)
    homepage: Optional[str] = Field(default=None, max_length=100)
    owner: Optional[str] = Field(default=None, max_length=50)

    limit: int = Field(default=20, ge=1, le=200, description="최대 반환 건수")
    offset: int = Field(default=0, ge=0, description="건너뛸 건수")


def get_team_search_params(
    stadium_id: Optional[int] = Query(None, gt=0),
    team_code: Optional[str] = Query(None, max_length=10),
    region_name: Optional[str] = Query(None, max_length=10),
    team_name: Optional[str] = Query(None, max_length=40),
    e_team_name: Optional[str] = Query(None, max_length=50),
    orig_yyyy: Optional[str] = Query(None, max_length=10),
    zip_code1: Optional[str] = Query(None, max_length=10),
    zip_code2: Optional[str] = Query(None, max_length=10),
    address: Optional[str] = Query(None, max_length=80),
    ddd: Optional[str] = Query(None, max_length=10),
    tel: Optional[str] = Query(None, max_length=20),
    fax: Optional[str] = Query(None, max_length=20),
    homepage: Optional[str] = Query(None, max_length=100),
    owner: Optional[str] = Query(None, max_length=50),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> TeamSearchRequest:
    return TeamSearchRequest(
        stadium_id=stadium_id,
        team_code=team_code,
        region_name=region_name,
        team_name=team_name,
        e_team_name=e_team_name,
        orig_yyyy=orig_yyyy,
        zip_code1=zip_code1,
        zip_code2=zip_code2,
        address=address,
        ddd=ddd,
        tel=tel,
        fax=fax,
        homepage=homepage,
        owner=owner,
        limit=limit,
        offset=offset,
    )


TeamSearchQuery = Annotated[TeamSearchRequest, Depends(get_team_search_params)]

__all__ = [
    "TeamSearchQuery",
    "TeamSearchRequest",
    "get_team_search_params",
]
