"""
도메인 값 객체 (순수: 외부 라이브러리 미참조)
- 비즈니스 의미가 있는 불변 값만. 데이터셋/결과 DTO는 application/dto.
"""
from .titanic import Age, Embarked, Fare, Gender, Parch, Pclass, SibSp, Survived
from .seoul_crime import SeoulPreprocessResult

__all__ = [
    "Age",
    "Embarked",
    "Fare",
    "Gender",
    "Parch",
    "Pclass",
    "SeoulPreprocessResult",
    "SibSp",
    "Survived",
]
