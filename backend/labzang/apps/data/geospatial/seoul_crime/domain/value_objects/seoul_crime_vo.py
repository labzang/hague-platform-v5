"""
서울 범죄 도메인 값 객체 (순수: 외부 라이브러리 미참조)
- crime.csv / DB 저장 컬럼 기준: 관서명, 5대 범죄 발생·검거, 자치구
- 도메인 의미·검증이 있는 값만 VO로 정의. SeoulPreprocessResult는 전처리 응답 DTO.
"""
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class PoliceStationName:
    """경찰서 관서명. CSV/DB: 관서명 (예: 중부서, 종로서)."""
    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if not v:
            raise ValueError("PoliceStationName must be non-empty")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True)
class MurderOccurred:
    """살인 발생 건수. CSV/DB: 살인 발생 (비음수 정수)."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("MurderOccurred must be non-negative")


@dataclass(frozen=True)
class MurderArrested:
    """살인 검거 건수. CSV/DB: 살인 검거 (비음수 정수)."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("MurderArrested must be non-negative")


@dataclass(frozen=True)
class RobberyOccurred:
    """강도 발생 건수. CSV/DB: 강도 발생."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("RobberyOccurred must be non-negative")


@dataclass(frozen=True)
class RobberyArrested:
    """강도 검거 건수. CSV/DB: 강도 검거."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("RobberyArrested must be non-negative")


@dataclass(frozen=True)
class RapeOccurred:
    """강간 발생 건수. CSV/DB: 강간 발생."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("RapeOccurred must be non-negative")


@dataclass(frozen=True)
class RapeArrested:
    """강간 검거 건수. CSV/DB: 강간 검거."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("RapeArrested must be non-negative")


@dataclass(frozen=True)
class TheftOccurred:
    """절도 발생 건수. CSV/DB: 절도 발생."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("TheftOccurred must be non-negative")


@dataclass(frozen=True)
class TheftArrested:
    """절도 검거 건수. CSV/DB: 절도 검거."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("TheftArrested must be non-negative")


@dataclass(frozen=True)
class ViolenceOccurred:
    """폭력 발생 건수. CSV/DB: 폭력 발생."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("ViolenceOccurred must be non-negative")


@dataclass(frozen=True)
class ViolenceArrested:
    """폭력 검거 건수. CSV/DB: 폭력 검거."""
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("ViolenceArrested must be non-negative")


@dataclass(frozen=True)
class SeoulDistrictName:
    """서울 자치구명. CSV/DB: 자치구 (예: 중구, 종로구)."""
    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if not v:
            raise ValueError("SeoulDistrictName must be non-empty")
        if len(v) < 2 or v[-1] != "구":
            raise ValueError("SeoulDistrictName must end with '구'")
        object.__setattr__(self, "value", v)


@dataclass
class SeoulPreprocessResult:
    """서울 범죄 전처리 결과."""

    status: str
    cctv_rows: int
    cctv_columns: List[str]
    crime_rows: int
    crime_columns: List[str]
    pop_rows: int
    pop_columns: List[str]
    cctv_pop_rows: int
    cctv_pop_columns: List[str]
    cctv_preview: List[Dict[str, Any]]
    crime_preview: List[Dict[str, Any]]
    pop_preview: List[Dict[str, Any]]
    cctv_pop_preview: List[Dict[str, Any]]
    message: str


__all__ = [
    "MurderArrested",
    "MurderOccurred",
    "PoliceStationName",
    "RapeArrested",
    "RapeOccurred",
    "RobberyArrested",
    "RobberyOccurred",
    "SeoulDistrictName",
    "SeoulPreprocessResult",
    "TheftArrested",
    "TheftOccurred",
    "ViolenceArrested",
    "ViolenceOccurred",
]
