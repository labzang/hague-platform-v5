"""Use case handling external training trigger events."""

from typing import Any, Dict

from labzang.apps.ai.sentiment.application.ports.input.training_event_command import (
    TrainingEventCommand,
)
from labzang.apps.ai.sentiment.application.ports.output.training_runner import (
    TrainingRunnerPort,
)


class TrainingEventCommandImpl(TrainingEventCommand):
    def __init__(self, runner: TrainingRunnerPort):
        self._runner = runner

    async def on_train_click(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._runner.trigger_training(payload)

    async def get_training_status(self) -> Dict[str, Any]:
        return await self._runner.training_status()
