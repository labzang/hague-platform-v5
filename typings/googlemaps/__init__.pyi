"""Minimal stubs for googlemaps (Pyright; optional runtime dep via pip install googlemaps)."""
from typing import Any, List, Optional

class Client:
    def __init__(
        self,
        key: Optional[str] = None,
        timeout: Optional[int] = None,
        **kwargs: Any,
    ) -> None: ...
    def geocode(
        self,
        address: Optional[str] = None,
        *,
        language: Optional[str] = None,
        **kwargs: Any,
    ) -> List[dict[str, Any]]: ...
