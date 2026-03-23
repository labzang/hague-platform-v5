"""
도메인 계층 (Hexagonal - 의존성 0, 순수만)
- entities: 순수 파이썬 엔티티 (Passenger, TitanicModels, SeoulCrime, SeoulCrimeModels)
- value_objects: 도메인 값 객체 (Survived, Pclass, Embarked, Fare, Age 등)
- 데이터셋/전처리·평가 결과 DTO는 application/dto
"""

from labzang.apps.ml.domain.entities import (
    SeoulCrime,
    Passenger,
    SeoulCrime,
    SeoulCrimeModels,
    TitanicModels,
)
from labzang.apps.ml.domain.value_objects import (
    Age,
    Embarked,
    Fare,
    Pclass,
    SeoulPreprocessResult,
    Survived,
)

__all__ = [
    "Age",
    "SeoulCrime",
    "Embarked",
    "Fare",
    "Passenger",
    "Pclass",
    "SeoulCrime",
    "SeoulCrimeModels",
    "SeoulPreprocessResult",
    "Survived",
    "TitanicModels",
]
