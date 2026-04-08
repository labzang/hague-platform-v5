"""
서울 범죄 도메인 엔티티 (순수 파이썬)
- crime.csv / DB 저장 행과 1:1 대응: SeoulCrime (식별: 관서명).
- 전처리·실험 Run 메타: SeoulCrimeModels (TitanicModels와 동일 역할).
"""

from dataclasses import dataclass
from typing import Optional

from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    PoliceStationName,
    SeoulDistrictName,
    ViolenceArrested,
    ViolenceOccurred,
)
from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    MurderOccurred,
)
from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    MurderArrested,
)
from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    RobberyOccurred,
)
from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    RobberyArrested,
)
from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    RapeOccurred,
)
from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    RapeArrested,
)
from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    TheftOccurred,
)
from labzang.apps.dash.council.illustrator.folium.domain.value_objects.seoul_crime_vo import (
    TheftArrested,
)


@dataclass
class SeoulCrime:
    """경찰서 단위 범죄 집계. crime.csv 한 행·ORM 한 레코드와 컬럼 일치. 식별자: station_name."""

    station_name: PoliceStationName
    murder_occurred: Optional[MurderOccurred] = None
    murder_arrested: Optional[MurderArrested] = None
    robbery_occurred: Optional[RobberyOccurred] = None
    robbery_arrested: Optional[RobberyArrested] = None
    rape_occurred: Optional[RapeOccurred] = None
    rape_arrested: Optional[RapeArrested] = None
    theft_occurred: Optional[TheftOccurred] = None
    theft_arrested: Optional[TheftArrested] = None
    violence_occurred: Optional[ViolenceOccurred] = None
    violence_arrested: Optional[ViolenceArrested] = None
    district: Optional[SeoulDistrictName] = None
