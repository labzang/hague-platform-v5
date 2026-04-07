"""
Inbound ports for Titanic use cases.

인바운드 어댑터(HTTP/CLI)는 아래 입력 포트 인터페이스를 통해
Application 유스케이스를 호출할 수 있다.
"""

from abc import ABC, abstractmethod

from labzang.apps.dash.kaggle.santander.application.dtos.titanic_dto import (
    EvaluationResult,
    PreprocessResult,
)


class PreprocessTitanicUCPort(ABC):
    """타이타닉 전처리 인바운드 포트."""

    @abstractmethod
    def execute(self) -> PreprocessResult: ...


class EvaluateTitanicUCPort(ABC):
    """타이타닉 평가 인바운드 포트."""

    @abstractmethod
    def execute(self) -> EvaluationResult: ...


class SubmitTitanicUCPort(ABC):
    """타이타닉 제출 파일 생성 인바운드 포트."""

    @abstractmethod
    def execute(self) -> dict: ...


__all__ = [
    "PreprocessTitanicUCPort",
    "EvaluateTitanicUCPort",
    "SubmitTitanicUCPort",
]
