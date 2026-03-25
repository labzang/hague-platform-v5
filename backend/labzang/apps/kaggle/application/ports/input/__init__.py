"""
Inbound ports (application layer) for entrypoint/use-case contracts.
"""

from labzang.apps.kaggle.application.ports.input.titanic_uc_port import (
    EvaluateTitanicUCPort,
    PreprocessTitanicUCPort,
    SubmitTitanicUCPort,
)

__all__ = [
    "PreprocessTitanicUCPort",
    "EvaluateTitanicUCPort",
    "SubmitTitanicUCPort",
]
