# -*- coding: utf-8 -*-
"""경기장 도메인 엔티티 — 식별자(StadiumId)와 값 객체로 구성."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from labzang.apps.biz.field.provider.soccer.domain.value_objects.stadium_vo import (
    HometeamCode,
    SeatCount,
    StadiumAddress,
    StadiumCode,
    StadiumDdd,
    StadiumId,
    StadiumName,
    StadiumTel,
)


def _stadium_name_from_row(row: Mapping[str, Any]) -> object:
    """JSONL 오타 `statdium_name`과 정상 키 `stadium_name` 모두 수용."""
    sn = row.get("stadium_name")
    if sn is not None:
        return sn
    return row.get("statdium_name")


@dataclass(slots=True)
class Stadium:
    """경기장 엔티티. 동등성은 `stadium_id`만 기준으로 한다."""

    stadium_id: StadiumId
    stadium_code: Optional[StadiumCode] = None
    stadium_name: Optional[StadiumName] = None
    hometeam_code: Optional[HometeamCode] = None
    seat_count: Optional[SeatCount] = None
    address: Optional[StadiumAddress] = None
    ddd: Optional[StadiumDdd] = None
    tel: Optional[StadiumTel] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stadium):
            return NotImplemented
        return self.stadium_id == other.stadium_id

    def __hash__(self) -> int:
        return hash(self.stadium_id)

    @classmethod
    def from_json_dict(cls, row: Mapping[str, Any]) -> Stadium:
        return cls(
            stadium_id=StadiumId.from_json(row.get("id")),
            stadium_code=StadiumCode.from_json(row.get("stadium_code")),
            stadium_name=StadiumName.from_json(_stadium_name_from_row(row)),
            hometeam_code=HometeamCode.from_json(row.get("hometeam_code")),
            seat_count=SeatCount.from_json(row.get("seat_count")),
            address=StadiumAddress.from_json(row.get("address")),
            ddd=StadiumDdd.from_json(row.get("ddd")),
            tel=StadiumTel.from_json(row.get("tel")),
        )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "id": self.stadium_id.value,
            "stadium_code": None if self.stadium_code is None else self.stadium_code.value,
            "stadium_name": None if self.stadium_name is None else self.stadium_name.value,
            "hometeam_code": None
            if self.hometeam_code is None
            else self.hometeam_code.value,
            "seat_count": None if self.seat_count is None else self.seat_count.value,
            "address": None if self.address is None else self.address.value,
            "ddd": None if self.ddd is None else self.ddd.value,
            "tel": None if self.tel is None else self.tel.value,
        }
