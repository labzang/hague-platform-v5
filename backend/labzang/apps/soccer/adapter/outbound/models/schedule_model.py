"""경기 일정(Schedule) SQLAlchemy 모델."""

from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.core.database import Base


class ScheduleModel(Base):
    """경기 일정 정보를 저장하는 SQLAlchemy 모델.

    Attributes:
        id: 경기 일정 고유 식별자 (PK, BigInt)
        stadium_id: 경기장 ID (FK -> stadiums.id)
        hometeam_id: 홈팀 ID (FK -> teams.id)
        awayteam_id: 원정팀 ID (FK -> teams.id)
        stadium_code: 경기장 코드
        sche_date: 경기 일자
        gubun: 구분
        hometeam_code: 홈팀 코드
        awayteam_code: 원정팀 코드
        home_score: 홈팀 점수
        away_score: 원정팀 점수
        embedding_text: 임베딩 생성에 사용된 원본 텍스트
        embedding: KoElectra 기반 768차원 벡터
        embedding_at: 임베딩 생성 시각
    """

    __tablename__ = "schedules"

    # 기본 키
    id = Column(
        BigInteger,
        primary_key=True,
        comment="경기 일정 고유 식별자"
    )

    # 외래 키
    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id"),
        nullable=True,
        comment="경기장 ID"
    )

    hometeam_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="홈팀 ID"
    )

    awayteam_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="원정팀 ID"
    )

    # 경기 정보
    stadium_code = Column(
        String(10),
        nullable=True,
        comment="경기장 코드"
    )

    sche_date = Column(
        String(10),
        nullable=True,
        comment="경기 일자"
    )

    gubun = Column(
        String(10),
        nullable=True,
        comment="구분"
    )

    hometeam_code = Column(
        String(10),
        nullable=True,
        comment="홈팀 코드"
    )

    awayteam_code = Column(
        String(10),
        nullable=True,
        comment="원정팀 코드"
    )

    home_score = Column(
        Integer,
        nullable=True,
        comment="홈팀 점수"
    )

    away_score = Column(
        Integer,
        nullable=True,
        comment="원정팀 점수"
    )

    # 임베딩 (기존 schedule_embeddings 테이블 컬럼 통합)
    embedding_text = Column(
        Text,
        nullable=True,
        comment="임베딩 생성에 사용된 원본 텍스트",
    )
    embedding = Column(
        Vector(768),
        nullable=True,
        comment="768차원 KoElectra 임베딩 벡터",
    )
    embedding_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
        comment="임베딩 생성 시각",
    )

    # 관계
    stadium = relationship(
        "StadiumModel",
        back_populates="schedules"
    )

    hometeam = relationship(
        "TeamModel",
        foreign_keys=[hometeam_id],
        backref="home_schedules"
    )

    awayteam = relationship(
        "TeamModel",
        foreign_keys=[awayteam_id],
        backref="away_schedules"
    )
