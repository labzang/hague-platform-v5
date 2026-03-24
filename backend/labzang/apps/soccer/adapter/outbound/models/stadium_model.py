"""경기장(Stadium) SQLAlchemy 모델."""

from sqlalchemy import Column, Integer, BigInteger, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.core.database import Base


class StadiumModel(Base):
    """경기장 정보를 저장하는 SQLAlchemy 모델.

    Attributes:
        id: 경기장 고유 식별자 (PK, BigInt)
        stadium_code: 경기장 코드
        stadium_name: 경기장 이름
        hometeam_code: 홈팀 코드
        seat_count: 좌석 수
        address: 주소
        ddd: 지역번호
        tel: 전화번호
        embedding_text: 임베딩 생성에 사용된 원본 텍스트
        embedding: KoElectra 기반 768차원 벡터
        embedding_at: 임베딩 생성 시각
    """

    __tablename__ = "stadiums"

    # 기본 키
    id = Column(
        BigInteger,
        primary_key=True,
        comment="경기장 고유 식별자"
    )

    # 경기장 정보
    stadium_code = Column(
        String(10),
        nullable=True,
        comment="경기장 코드"
    )

    stadium_name = Column(
        String(40),
        nullable=True,
        comment="경기장 이름"
    )

    hometeam_code = Column(
        String(10),
        nullable=True,
        comment="홈팀 코드"
    )

    seat_count = Column(
        Integer,
        nullable=True,
        comment="좌석 수"
    )

    address = Column(
        String(60),
        nullable=True,
        comment="주소"
    )

    ddd = Column(
        String(10),
        nullable=True,
        comment="지역번호"
    )

    tel = Column(
        String(20),
        nullable=True,
        comment="전화번호"
    )

    # 임베딩 (기존 stadium_embeddings 테이블 컬럼 통합)
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
    teams = relationship(
        "TeamModel",
        back_populates="stadium"
    )

    schedules = relationship(
        "ScheduleModel",
        back_populates="stadium"
    )
