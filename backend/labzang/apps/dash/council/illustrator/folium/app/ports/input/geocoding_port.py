"""Geocoding output port (Google/Kakao 등 어댑터가 구현)."""

from __future__ import annotations

from typing import Any, List, Protocol, runtime_checkable


@runtime_checkable
class GeocodingPort(Protocol):
    def geocode(self, address: str, *, language: str = "ko") -> List[dict[str, Any]]: ...

    def reverse_geocode(
        self, latitude: float, longitude: float, *, language: str = "ko"
    ) -> str: ...

    def batch_geocode(
        self, addresses: List[str], *, language: str = "ko"
    ) -> List[dict[str, Any]]: ...

    def batch_reverse_geocode(
        self,
        latitudes: List[float],
        longitudes: List[float],
        *,
        language: str = "ko",
    ) -> List[str]: ...

    def batch_geocode_and_reverse_geocode(
        self, addresses: List[str], *, language: str = "ko"
    ) -> List[dict[str, Any]]: ...
