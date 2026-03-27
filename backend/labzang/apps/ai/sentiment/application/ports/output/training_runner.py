"""Output port for model training orchestration."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class TrainingRunnerPort(ABC):
    @abstractmethod
    async def trigger_training(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ...

    @abstractmethod
    async def training_status(self) -> Dict[str, Any]:
        ...
