"""
도메인 계층 (Hexagonal - 의존성 0, 순수만)
- entities: 순수 파이썬 엔티티 (Passenger, SeoulCrime 등)
- value_objects: 도메인 값 객체 (Survived, Pclass, Embarked, Fare, Age 등)
- 데이터셋/전처리·평가 결과 DTO는 application/dto
"""

from labzang.apps.dash.kaggle.santander.domain.entities import Passenger, SeoulCrime
from labzang.apps.dash.kaggle.santander.domain.value_objects import (
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
    "SeoulPreprocessResult",
    "Survived",
]
