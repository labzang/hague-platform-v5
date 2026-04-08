"""
Inbound ports (application layer) for entrypoint/use-case contracts.
"""

from labzang.apps.ai.percept.detective.titanic.app.ports.input.titanic_command import (
    TitanicPreprocessPort,
    TitanicSubmitPort,
)
from labzang.apps.ai.percept.detective.titanic.app.ports.input.titanic_query import (
    TitanicEvaluatePort,
)

__all__ = [
    "TitanicPreprocessPort",
    "TitanicEvaluatePort",
    "TitanicSubmitPort",
]
