"""
도메인 엔티티 (순수 파이썬만)
- 외부 라이브러리(pandas, sklearn, DB 등) 의존 없음
"""
from .seoul_crime import SeoulCrime
from .titanic import Passenger, TitanicModels

__all__ = ["Passenger", "SeoulCrime", "TitanicModels"]
