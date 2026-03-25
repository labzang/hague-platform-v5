# -*- coding: utf-8 -*-
"""`schedules` 테이블 SQLAlchemy 매핑.

`schedules.jsonl` / `domain.entities.schedule.Schedule` 스키마와 문자열 길이를 맞춘다.
"""

from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String

from labzang.shared.bases import Base


class ScheduleORM(Base):
    """일정 행 — 테이블명 `schedules`."""

    __tablename__ = "schedules"

    id = Column(BigInteger, primary_key=True, comment="일정 PK")

    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id"),
        nullable=True,
        comment="경기장 FK",
    )
    hometeam_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="홈팀 FK",
    )
    awayteam_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="원정팀 FK",
    )

    stadium_code = Column(String(10), nullable=True, comment="경기장 코드")
    sche_date = Column(String(10), nullable=True, comment="경기 일자 YYYYMMDD")
    gubun = Column(String(5), nullable=True, comment="구분")
    hometeam_code = Column(String(10), nullable=True, comment="홈팀 코드")
    awayteam_code = Column(String(10), nullable=True, comment="원정팀 코드")
    home_score = Column(Integer, nullable=True, comment="홈 득점")
    away_score = Column(Integer, nullable=True, comment="원정 득점")
