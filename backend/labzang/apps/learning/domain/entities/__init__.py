"""
도메인 엔티티 (순수 파이썬만)
- 외부 라이브러리(pandas, sklearn, DB 등) 의존 없음
"""
from domain.entities.titanic import TitanicModels
from domain.entities.seoul_crime import SeoulCrime

__all__ = ["TitanicModels", "SeoulCrime"]
