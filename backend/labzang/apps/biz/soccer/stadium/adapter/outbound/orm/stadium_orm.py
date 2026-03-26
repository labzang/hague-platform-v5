# -*- coding: utf-8 -*-
"""`stadiums` 테이블 SQLAlchemy 매핑.

`stadiums.jsonl` / `domain.entities.stadium.Stadium` 스키마와 문자열 길이를 맞춘다.
"""

from sqlalchemy import BigInteger, Column, Integer, String

from labzang.shared.bases import Base


class StadiumORM(Base):
    """경기장 행 — 테이블명 `stadiums`."""

    __tablename__ = "stadiums"

    id = Column(BigInteger, primary_key=True, comment="경기장 PK")

    stadium_code = Column(String(10), nullable=True, comment="경기장 코드")
    stadium_name = Column(String(60), nullable=True, comment="경기장명")
    hometeam_code = Column(String(10), nullable=True, comment="홈팀 코드")
    seat_count = Column(Integer, nullable=True, comment="좌석 수")
    address = Column(String(80), nullable=True, comment="주소")
    ddd = Column(String(10), nullable=True, comment="지역번호")
    tel = Column(String(20), nullable=True, comment="전화")
