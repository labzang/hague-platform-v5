"""
벅스 차트 도메인 값 객체 (순수: 외부 라이브러리 미참조)
- 차트 한 행 컬럼 기준: rank, artist, title
- 도메인 의미·검증이 있는 값만 VO로 정의.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ChartRank:
    """차트 순위. 1 이상 (상한은 서비스 정책)."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError("ChartRank must be >= 1")
        if self.value > 500:
            raise ValueError("ChartRank must be <= 500")


@dataclass(frozen=True)
class ArtistName:
    """아티스트명. 비어 있지 않은 문자열."""

    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if not v:
            raise ValueError("ArtistName must be non-empty")
        object.__setattr__(self, "value", v)


@dataclass(frozen=True)
class SongTitle:
    """곡 제목. 비어 있지 않은 문자열."""

    value: str

    def __post_init__(self) -> None:
        v = (self.value or "").strip()
        if not v:
            raise ValueError("SongTitle must be non-empty")
        object.__setattr__(self, "value", v)


__all__ = ["ArtistName", "ChartRank", "SongTitle"]
