# -*- coding: utf-8 -*-
"""Inbound response schemas — JSON for clients (e.g. Vercel) from `find_by_id` results."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from labzang.apps.biz.soccer.player.application.dtos.player_dto import PlayerDTO as HubPlayerDTO


class PlayerResponse(BaseModel):
    """Single player payload suitable for `JSONResponse` / Vercel `Response.json()`.

    Maps from application `PlayerDTO` (dataclass) after `find_by_id`.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 2009175,
                "team_id": 1011,
                "player_name": "홍길동",
                "position": "MF",
                "birth_date": "1990-01-15",
            }
        }
    )

    id: int = Field(..., gt=0, description="Player primary key")
    team_id: Optional[int] = Field(default=None, description="Team FK")
    player_name: Optional[str] = Field(default=None, max_length=20)
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
    embedding_content: Optional[str] = None
    embedding: Optional[List[float]] = None
    embedding_created_at: Optional[datetime] = None

    @classmethod
    def from_player_dto(cls, dto: HubPlayerDTO) -> PlayerResponse:
        """Build from hub `PlayerDTO` returned by `PlayerReader.find_by_id`."""
        return cls(
            id=dto.id,
            team_id=dto.team_id,
            player_name=dto.player_name,
            e_player_name=dto.e_player_name,
            nickname=dto.nickname,
            join_yyyy=dto.join_yyyy,
            position=dto.position,
            back_no=dto.back_no,
            nation=dto.nation,
            birth_date=dto.birth_date,
            solar=dto.solar,
            height=dto.height,
            weight=dto.weight,
            embedding_content=dto.embedding_content,
            embedding=dto.embedding,
            embedding_created_at=dto.embedding_created_at,
        )

    def to_json_dict(self) -> dict[str, Any]:
        """JSON-serializable dict (`date`/`datetime` → ISO strings) for fetch/Next.js."""
        return self.model_dump(mode="json")


__all__ = ["PlayerResponse"]
