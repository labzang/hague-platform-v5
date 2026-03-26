from sqlalchemy import BigInteger, Column, Float, Integer, String

from labzang.core.database import Base


class TitanicORM(Base):
    """SQLAlchemy mapping for normalized Titanic rows."""

    __tablename__ = "titanic_passengers"

    passenger_id = Column(BigInteger, primary_key=True, comment="PassengerId")
    dataset_split = Column(String(10), nullable=False, default="train", comment="DatasetSplit")
    survived = Column(Integer, nullable=True, comment="Survived")
    pclass = Column(Integer, nullable=False, comment="Pclass")
    name = Column(String(255), nullable=False, comment="Name")
    gender = Column(String(10), nullable=False, comment="Gender")
    age = Column(Float, nullable=True, comment="Age")
    sibsp = Column(Integer, nullable=False, comment="SibSp")
    parch = Column(Integer, nullable=False, comment="Parch")
    ticket = Column(String(50), nullable=False, comment="Ticket")
    fare = Column(Float, nullable=True, comment="Fare")
    cabin = Column(String(50), nullable=True, comment="Cabin")
    embarked = Column(String(1), nullable=True, comment="Embarked")
