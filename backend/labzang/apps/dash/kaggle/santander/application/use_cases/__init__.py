"""Application use cases (wired from composition root)."""

from labzang.apps.data.kaggle.santander.application.use_cases.titanic_uc import (
    EvaluateTitanicUC,
    PreprocessTitanicUC,
    SubmitTitanicUC,
)

__all__ = ["EvaluateTitanicUC", "PreprocessTitanicUC", "SubmitTitanicUC"]
