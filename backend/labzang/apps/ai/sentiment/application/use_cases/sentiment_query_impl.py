"""Sentiment query use case implementation."""

from typing import Any, Dict, List

from labzang.apps.ai.sentiment.application.ports.input import SentimentQuery
from labzang.apps.ai.sentiment.application.ports.output import SentimentInferencePort


class SentimentQueryImpl(SentimentQuery):
    def __init__(self, inference: SentimentInferencePort):
        self._inference = inference

    async def analyze(self, text: str) -> Dict[str, Any]:
        return self._inference.predict(text)

    async def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        return self._inference.predict_batch(texts)

    async def health(self) -> Dict[str, Any]:
        return self._inference.health()

    async def model_info(self) -> Dict[str, Any]:
        return self._inference.model_info()
