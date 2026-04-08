"""Google Maps Geocoding API 어댑터 (`GeocodingPort` 구현)."""

from __future__ import annotations

import os
from typing import Any, List, Optional

import googlemaps

from labzang.apps.dash.geospatial.seoul_crime.application.ports.output.geocoding_port import (
    GeocodingPort,
)


class GoogleMapsGeocoder(GeocodingPort):
    """환경변수 ``GOOGLE_MAPS_API_KEY`` 또는 생성자 ``api_key``로 클라이언트를 만든다."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        client: Optional[googlemaps.Client] = None,
    ) -> None:
        if client is not None:
            self._client = client
            self._api_key: Optional[str] = api_key
            return
        key = api_key or os.environ.get("GOOGLE_MAPS_API_KEY")
        if not key:
            raise ValueError(
                "Google Maps API 키가 없습니다. api_key 인자를 넘기거나 "
                "환경변수 GOOGLE_MAPS_API_KEY를 설정하세요."
            )
        self._api_key = key
        self._client = googlemaps.Client(key=key)

    @property
    def api_key(self) -> Optional[str]:
        """테스트·로깅용. 운영에서는 노출하지 않는 것이 좋다."""
        return self._api_key

    def geocode(self, address: str, *, language: str = "ko") -> List[dict[str, Any]]:
        return list(self._client.geocode(address, language=language))

    def reverse_geocode(
        self, latitude: float, longitude: float, *, language: str = "ko"
    ) -> str:
        results = self._client.reverse_geocode(
            (latitude, longitude), language=language
        )
        if not results:
            return ""
        return str(results[0].get("formatted_address", ""))

    def batch_geocode(
        self, addresses: List[str], *, language: str = "ko"
    ) -> List[dict[str, Any]]:
        out: List[dict[str, Any]] = []
        for addr in addresses:
            batch = self._client.geocode(addr, language=language)
            out.append(dict(batch[0]) if batch else {})
        return out

    def batch_reverse_geocode(
        self,
        latitudes: List[float],
        longitudes: List[float],
        *,
        language: str = "ko",
    ) -> List[str]:
        if len(latitudes) != len(longitudes):
            raise ValueError(
                "latitudes와 longitudes 길이가 같아야 합니다: "
                f"{len(latitudes)} != {len(longitudes)}"
            )
        return [
            self.reverse_geocode(lat, lng, language=language)
            for lat, lng in zip(latitudes, longitudes, strict=True)
        ]

    def batch_geocode_and_reverse_geocode(
        self, addresses: List[str], *, language: str = "ko"
    ) -> List[dict[str, Any]]:
        rows: List[dict[str, Any]] = []
        for addr in addresses:
            gc = self._client.geocode(addr, language=language)
            if not gc:
                rows.append(
                    {
                        "address": addr,
                        "geocode_results": [],
                        "reverse_formatted_address": "",
                    }
                )
                continue
            first = gc[0]
            loc = first.get("geometry", {}).get("location", {})
            lat = float(loc.get("lat", 0.0))
            lng = float(loc.get("lng", 0.0))
            rev = (
                self.reverse_geocode(lat, lng, language=language)
                if loc
                else ""
            )
            rows.append(
                {
                    "address": addr,
                    "geocode_results": [dict(x) for x in gc],
                    "reverse_formatted_address": rev,
                }
            )
        return rows
