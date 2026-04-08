"""
도메인 엔티티 (순수 파이썬만)
- 외부 라이브러리(pandas, sklearn, DB 등) 의존 없음
"""

from labzang.apps.dash.geospatial.domain.entities.seoul_crime import SeoulCrime
from labzang.apps.ai.percept.detective.santander.domain.entities.titanic import Passenger

__all__ = [
    "SeoulCrime",
    "Passenger",
]
