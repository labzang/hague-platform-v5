"""Input port for external training events."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class TrainingEventCommand(ABC):
    @abstractmethod
    async def on_train_click(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ...

    @abstractmethod
    async def get_training_status(self) -> Dict[str, Any]:
        ...
