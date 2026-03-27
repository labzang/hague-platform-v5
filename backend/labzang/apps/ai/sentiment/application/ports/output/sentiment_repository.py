"""Sentiment repository output port."""

from abc import ABC, abstractmethod
from typing import Dict, List

from labzang.apps.ai.sentiment.domain.entities import SentimentReview


class SentimentRepository(ABC):
    @abstractmethod
    async def upsert_batch(self, reviews: List[SentimentReview]) -> Dict[str, int]:
        ...
