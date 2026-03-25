"""출력 포트: 주소 ↔ 좌표 변환(지오코딩 / 역지오코딩)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List


class GeocodingPort(ABC):
    """Google Maps 등 외부 지오코딩 제공자 뒤에 두는 추상 포트."""

    @abstractmethod
    def geocode(self, address: str, *, language: str = "ko") -> List[dict[str, Any]]:
        """주소 문자열을 지오코딩한다. 결과는 제공자 API 원본 dict 리스트."""
        ...

    @abstractmethod
    def reverse_geocode(
        self, latitude: float, longitude: float, *, language: str = "ko"
    ) -> str:
        """좌표에 대응하는 대표 포맷 주소 문자열(없으면 빈 문자열)."""
        ...

    @abstractmethod
    def batch_geocode(
        self, addresses: List[str], *, language: str = "ko"
    ) -> List[dict[str, Any]]:
        """주소별로 첫 번째 지오코딩 결과 dict를 모은다(실패 시 빈 dict)."""
        ...

    @abstractmethod
    def batch_reverse_geocode(
        self,
        latitudes: List[float],
        longitudes: List[float],
        *,
        language: str = "ko",
    ) -> List[str]:
        """위도·경도 리스트(동일 길이)에 대한 포맷 주소 문자열."""
        ...

    @abstractmethod
    def batch_geocode_and_reverse_geocode(
        self, addresses: List[str], *, language: str = "ko"
    ) -> List[dict[str, Any]]:
        """주소별 지오코딩 후, 첫 좌표로 역지오코딩한 문자열을 함께 담는다.

        각 원소 예:
        ``{"address", "geocode_results", "reverse_formatted_address"}``
        """
        ...
