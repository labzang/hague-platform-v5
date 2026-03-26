# -*- coding: utf-8 -*-
"""`players` 테이블 SQLAlchemy 매핑.

`players.jsonl` 컬럼과 `player_vo` 문자열 길이 상한을 맞춘다.
(동일 DB의 `players`를 이미 `domain.entities.players.Player`로 매핑 중이면
프로세스에서 둘 중 하나만 메타데이터에 등록하는 것이 안전하다.)
"""

from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer, String

from labzang.shared.bases import Base


class PlayerORM(Base):
    """선수 행 — 테이블명 `players`."""

    __tablename__ = "players"

    id = Column(BigInteger, primary_key=True, comment="선수 PK")

    team_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="팀 FK",
    )

    player_name = Column(String(20), nullable=True, comment="선수명")
    e_player_name = Column(String(40), nullable=True, comment="영문 선수명")
    nickname = Column(String(30), nullable=True, comment="닉네임")
    join_yyyy = Column(String(10), nullable=True, comment="입단 연도")
    position = Column(String(10), nullable=True, comment="포지션")
    back_no = Column(Integer, nullable=True, comment="등번호")
    nation = Column(String(20), nullable=True, comment="국적")
    birth_date = Column(Date, nullable=True, comment="생년월일")
    solar = Column(String(10), nullable=True, comment="양력/음력 구분")
    height = Column(Integer, nullable=True, comment="키(cm)")
    weight = Column(Integer, nullable=True, comment="몸무게(kg)")
