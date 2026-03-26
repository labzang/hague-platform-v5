from sqlalchemy import BigInteger, Column, Integer, String

from labzang.core.database import Base


class TitanicFeatureORM(Base):
    """전처리 후 수치 특성만 저장 (원본 SibSp, Name, Fare 등은 포함하지 않음)."""

    __tablename__ = "titanic_passenger_features"

    passenger_id = Column(BigInteger, primary_key=True, comment="PassengerId")
    dataset_split = Column(String(10), nullable=False, comment="DatasetSplit")
    pclass = Column(Integer, nullable=False, comment="Pclass")
    embarked = Column(Integer, nullable=False, comment="Embarked (인코딩)")
    title = Column(Integer, nullable=False, comment="Title (인코딩)")
    gender = Column(Integer, nullable=False, comment="Gender 0/1")
    age_group = Column(Integer, nullable=False, comment="AgeGroup")
    fare_band = Column(Integer, nullable=False, comment="FareBand")
