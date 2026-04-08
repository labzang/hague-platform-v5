"""Sentiment query input port."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SentimentQuery(ABC):
    @abstractmethod
    async def analyze(self, text: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    async def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    async def health(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    async def model_info(self) -> Dict[str, Any]:
        ...
