"""
타이타닉 train.csv 매퍼 모델 — Alembic insert / ORM 매핑용.
테이블: titanic_train (resources/titanic/train.csv 컬럼과 1:1)
"""
import math
from typing import Any, Optional

from sqlalchemy import Column, Float, Integer, String

try:
    from labzang.core.database import Base
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()


class TitanicTrain(Base):
    """타이타닉 학습 데이터 테이블. train.csv 컬럼과 매핑."""

    __tablename__ = "titanic_train"

    passenger_id = Column("passenger_id", Integer, primary_key=True, autoincrement=False)
    survived = Column("survived", Integer, nullable=False)  # 0=사망, 1=생존
    pclass = Column("pclass", Integer, nullable=False)  # 1, 2, 3
    name = Column("name", String(256), nullable=True)
    # 원본 DB 컬럼명 "sex" 유지, Python에서는 gender로 도입
    gender = Column("sex", String(16), nullable=True)
    age = Column("age", Float, nullable=True)
    sib_sp = Column("sib_sp", Integer, nullable=True)  # SibSp
    parch = Column("parch", Integer, nullable=True)
    ticket = Column("ticket", String(64), nullable=True)
    fare = Column("fare", Float, nullable=True)
    cabin = Column("cabin", String(32), nullable=True)
    embarked = Column("embarked", String(1), nullable=True)  # S, C, Q

    def __repr__(self) -> str:
        return f"<TitanicTrain(passenger_id={self.passenger_id}, survived={self.survived})>"

    @classmethod
    def csv_row_to_kwargs(cls, row: dict) -> dict:
        """CSV 행(키: PassengerId, Name, SibSp 등)을 ORM kwargs로 변환. Alembic/insert 시 사용."""
        def _int(v: Any) -> Optional[int]:
            if v is None or v == "" or (isinstance(v, float) and math.isnan(v)):
                return None
            try:
                return int(float(v))
            except (ValueError, TypeError):
                return None

        def _float(v: Any) -> Optional[float]:
            if v is None or v == "" or (isinstance(v, float) and math.isnan(v)):
                return None
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        # 원본 키 "Sex" 수신 → 도입 시점에서 gender로 순화
        gender_val = row.get("Gender") or row.get("Sex") or None
        return {
            "passenger_id": _int(row.get("PassengerId")),
            "survived": _int(row.get("Survived")),
            "pclass": _int(row.get("Pclass")),
            "name": row.get("Name") or None,
            "gender": gender_val,
            "age": _float(row.get("Age")),
            "sib_sp": _int(row.get("SibSp")),
            "parch": _int(row.get("Parch")),
            "ticket": row.get("Ticket") or None,
            "fare": _float(row.get("Fare")),
            "cabin": row.get("Cabin") or None,
            "embarked": row.get("Embarked") or None,
        }
