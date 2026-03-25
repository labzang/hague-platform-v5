# -*- coding: utf-8 -*-
"""`teams` 테이블 SQLAlchemy 매핑.

`teams.jsonl` / 기존 `domain.entities.teams.Team` 스키마와 문자열 길이를 맞춘다.
"""

from sqlalchemy import BigInteger, Column, ForeignKey, String

from labzang.shared.bases import Base


class TeamORM(Base):
    """팀 행 — 테이블명 `teams`."""

    __tablename__ = "teams"

    id = Column(BigInteger, primary_key=True, comment="팀 PK")

    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id"),
        nullable=True,
        comment="경기장 FK",
    )

    team_code = Column(String(10), nullable=True, comment="팀 코드")
    region_name = Column(String(10), nullable=True, comment="지역명")
    team_name = Column(String(40), nullable=True, comment="팀명")
    e_team_name = Column(String(50), nullable=True, comment="영문 팀명")
    orig_yyyy = Column(String(10), nullable=True, comment="창단 연도")
    zip_code1 = Column(String(10), nullable=True, comment="우편번호 앞")
    zip_code2 = Column(String(10), nullable=True, comment="우편번호 뒤")
    address = Column(String(80), nullable=True, comment="주소")
    ddd = Column(String(10), nullable=True, comment="지역번호")
    tel = Column(String(20), nullable=True, comment="전화")
    fax = Column(String(20), nullable=True, comment="팩스")
    homepage = Column(String(100), nullable=True, comment="홈페이지")
    owner = Column(String(50), nullable=True, comment="오너")
