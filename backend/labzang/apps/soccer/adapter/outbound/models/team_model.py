"""팀(Team) SQLAlchemy 모델."""

from sqlalchemy import Column, String, BigInteger, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.core.database import Base


class TeamModel(Base):
    """팀 정보를 저장하는 SQLAlchemy 모델.

    Attributes:
        id: 팀 고유 식별자 (PK, BigInt)
        stadium_id: 경기장 ID (FK -> stadiums.id)
        team_code: 팀 코드
        region_name: 지역명
        team_name: 팀명
        e_team_name: 영문 팀명
        orig_yyyy: 창단년도
        zip_code1: 우편번호1
        zip_code2: 우편번호2
        address: 주소
        ddd: 지역번호
        tel: 전화번호
        fax: 팩스번호
        homepage: 홈페이지
        owner: 구단주
        embedding_text: 임베딩 생성에 사용된 원본 텍스트
        embedding: KoElectra 기반 768차원 벡터
        embedding_at: 임베딩 생성 시각
    """

    __tablename__ = "teams"

    # 기본 키
    id = Column(
        BigInteger,
        primary_key=True,
        comment="팀 고유 식별자"
    )

    # 외래 키
    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id"),
        nullable=True,
        comment="경기장 ID"
    )

    # 팀 정보
    team_code = Column(
        String(10),
        nullable=True,
        comment="팀 코드"
    )

    region_name = Column(
        String(10),
        nullable=True,
        comment="지역명"
    )

    team_name = Column(
        String(40),
        nullable=True,
        comment="팀명"
    )

    e_team_name = Column(
        String(50),
        nullable=True,
        comment="영문 팀명"
    )

    orig_yyyy = Column(
        String(10),
        nullable=True,
        comment="창단년도"
    )

    zip_code1 = Column(
        String(10),
        nullable=True,
        comment="우편번호1"
    )

    zip_code2 = Column(
        String(10),
        nullable=True,
        comment="우편번호2"
    )

    address = Column(
        String(80),
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

    fax = Column(
        String(20),
        nullable=True,
        comment="팩스번호"
    )

    homepage = Column(
        String(100),
        nullable=True,
        comment="홈페이지"
    )

    owner = Column(
        String(50),
        nullable=True,
        comment="구단주"
    )

    # 임베딩 (기존 team_embeddings 테이블 컬럼 통합)
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
        back_populates="teams"
    )

    players = relationship(
        "PlayerModel",
        back_populates="team",
        cascade="all, delete-orphan"
    )
