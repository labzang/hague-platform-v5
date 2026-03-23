"""
도메인 엔티티 (순수 파이썬만)
- 외부 라이브러리(pandas, sklearn, DB 등) 의존 없음
"""

from labzang.apps.ml.domain.entities.geospatial.seoul_crime import (
    SeoulCrime,
    SeoulCrime,
    SeoulCrimeModels,
)
from labzang.apps.ml.domain.entities.kaggle.titanic import Passenger, TitanicModels

__all__ = [
    "SeoulCrime",
    "Passenger",
    "SeoulCrime",
    "SeoulCrimeModels",
    "TitanicModels",
]
