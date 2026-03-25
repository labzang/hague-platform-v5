"""Application use cases (wired from composition root)."""

from labzang.apps.kaggle.application.use_cases.titanic_uc import (
    EvaluateTitanicUC,
    PreprocessTitanicUC,
    SubmitTitanicUC,
)

__all__ = ["EvaluateTitanicUC", "PreprocessTitanicUC", "SubmitTitanicUC"]
