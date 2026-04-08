# -*- coding: utf-8 -*-
"""팀 도메인 엔티티 — 식별자(TeamId)와 값 객체로 구성."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from labzang.apps.biz.asset.content.soccer.domain.value_objects.team_vo import (
    Address,
    Ddd,
    ETeamName,
    Fax,
    Homepage,
    OrigYyyy,
    Owner,
    RegionName,
    StadiumId,
    TeamCode,
    TeamId,
    TeamName,
    Tel,
    ZipCode1,
    ZipCode2,
)


@dataclass(slots=True)
class Team:
    """팀 엔티티. 동등성은 `team_id`만 기준으로 한다."""

    team_id: TeamId
    stadium_id: Optional[StadiumId] = None
    team_code: Optional[TeamCode] = None
    region_name: Optional[RegionName] = None
    team_name: Optional[TeamName] = None
    e_team_name: Optional[ETeamName] = None
    orig_yyyy: Optional[OrigYyyy] = None
    zip_code1: Optional[ZipCode1] = None
    zip_code2: Optional[ZipCode2] = None
    address: Optional[Address] = None
    ddd: Optional[Ddd] = None
    tel: Optional[Tel] = None
    fax: Optional[Fax] = None
    homepage: Optional[Homepage] = None
    owner: Optional[Owner] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Team):
            return NotImplemented
        return self.team_id == other.team_id

    def __hash__(self) -> int:
        return hash(self.team_id)

    @classmethod
    def from_json_dict(cls, row: Mapping[str, Any]) -> Team:
        return cls(
            team_id=TeamId.from_json(row.get("id")),
            stadium_id=StadiumId.from_json(row.get("stadium_id")),
            team_code=TeamCode.from_json(row.get("team_code")),
            region_name=RegionName.from_json(row.get("region_name")),
            team_name=TeamName.from_json(row.get("team_name")),
            e_team_name=ETeamName.from_json(row.get("e_team_name")),
            orig_yyyy=OrigYyyy.from_json(row.get("orig_yyyy")),
            zip_code1=ZipCode1.from_json(row.get("zip_code1")),
            zip_code2=ZipCode2.from_json(row.get("zip_code2")),
            address=Address.from_json(row.get("address")),
            ddd=Ddd.from_json(row.get("ddd")),
            tel=Tel.from_json(row.get("tel")),
            fax=Fax.from_json(row.get("fax")),
            homepage=Homepage.from_json(row.get("homepage")),
            owner=Owner.from_json(row.get("owner")),
        )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "id": self.team_id.value,
            "stadium_id": None if self.stadium_id is None else self.stadium_id.value,
            "team_code": None if self.team_code is None else self.team_code.value,
            "region_name": None if self.region_name is None else self.region_name.value,
            "team_name": None if self.team_name is None else self.team_name.value,
            "e_team_name": None if self.e_team_name is None else self.e_team_name.value,
            "orig_yyyy": None if self.orig_yyyy is None else self.orig_yyyy.value,
            "zip_code1": None if self.zip_code1 is None else self.zip_code1.value,
            "zip_code2": None if self.zip_code2 is None else self.zip_code2.value,
            "address": None if self.address is None else self.address.value,
            "ddd": None if self.ddd is None else self.ddd.value,
            "tel": None if self.tel is None else self.tel.value,
            "fax": None if self.fax is None else self.fax.value,
            "homepage": None if self.homepage is None else self.homepage.value,
            "owner": None if self.owner is None else self.owner.value,
        }
