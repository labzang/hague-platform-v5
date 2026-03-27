"""Sentiment inference output port."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SentimentInferencePort(ABC):
    @abstractmethod
    def predict(self, text: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def model_info(self) -> Dict[str, Any]:
        ...
