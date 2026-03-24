"""
도메인 값 객체 (순수: 외부 라이브러리 미참조)
- 비즈니스 의미가 있는 불변 값만. 데이터셋/결과 DTO는 application/dto.
"""
from labzang.apps.geospatial.domain.value_objects.seoul_crime_vo import (
    MurderArrested,
    MurderOccurred,
    PoliceStationName,
    RapeArrested,
    RapeOccurred,
    RobberyArrested,
    RobberyOccurred,
    SeoulDistrictName,
    SeoulPreprocessResult,
    TheftArrested,
    TheftOccurred,
    ViolenceArrested,
    ViolenceOccurred,
)
from labzang.apps.kaggle.domain.value_objects.titanic_vo import (
    Age,
    Embarked,
    Fare,
    Gender,
    Parch,
    Pclass,
    SibSp,
    Survived,
)

__all__ = [
    "Age",
    "Embarked",
    "Fare",
    "Gender",
    "MurderArrested",
    "MurderOccurred",
    "Parch",
    "Pclass",
    "PoliceStationName",
    "RapeArrested",
    "RapeOccurred",
    "RobberyArrested",
    "RobberyOccurred",
    "SeoulDistrictName",
    "SeoulPreprocessResult",
    "SibSp",
    "Survived",
    "TheftArrested",
    "TheftOccurred",
    "ViolenceArrested",
    "ViolenceOccurred",
]
