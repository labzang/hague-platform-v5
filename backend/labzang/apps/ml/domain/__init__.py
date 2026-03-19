"""
도메인 계층 (Hexagonal - 의존성 0, 순수만)
- entities: 순수 파이썬 엔티티 (Passenger, TitanicModels, SeoulCrime)
- value_objects: 도메인 값 객체 (Survived, Pclass, Embarked, Fare, Age 등)
- 데이터셋/전처리·평가 결과 DTO는 application/dto
"""
from .entities import Passenger, SeoulCrime, TitanicModels
from .value_objects import (
    Age,
    Embarked,
    Fare,
    Pclass,
    SeoulPreprocessResult,
    Survived,
)

__all__ = [
    "Age",
    "Embarked",
    "Fare",
    "Passenger",
    "Pclass",
    "SeoulCrime",
    "SeoulPreprocessResult",
    "Survived",
    "TitanicModels",
]
