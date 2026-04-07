"""Sentiment command input port."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SentimentCommand(ABC):
    @abstractmethod
    async def ingest_reviews(self, rows: List[Dict[str, Any]]) -> Dict[str, int]:
        ...

    @abstractmethod
    async def ingest_resources_data(self) -> Dict[str, int]:
        ...
