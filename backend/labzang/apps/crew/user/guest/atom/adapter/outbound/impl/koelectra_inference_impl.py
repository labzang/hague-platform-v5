"""Inference adapter backed by KoELECTRA service."""

from typing import Any, Dict, List

from labzang.apps.ai.sentiment.application.inference.sentiment_inference_service import (
    get_sentiment_service,
)
from labzang.apps.ai.sentiment.application.ports.output import SentimentInferencePort


class KoELECTRAInferenceImpl(SentimentInferencePort):
    def __init__(self):
        self._service = get_sentiment_service()

    def predict(self, text: str) -> Dict[str, Any]:
        return self._service.predict_sentiment(text)

    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        return self._service.predict_batch(texts)

    def health(self) -> Dict[str, Any]:
        return self._service.health_check()

    def model_info(self) -> Dict[str, Any]:
        return self._service.get_model_info()
