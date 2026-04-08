from __future__ import annotations

from typing import Protocol

from labzang.apps.ai.percept.detective.santander.app.dtos.titanic_dto import (
    PreprocessResult,
)
from labzang.apps.ai.percept.detective.titanic.app.dtos.titanic_row_dto import (
    TitanicPreprocessPipelineResultDTO,
    TitanicRowDTO,
)


class TitanicCommandPort(Protocol):
    """train/test 배치 수신 → DTO 정합 → 전처리 → (Neon/Postgres) 저장."""

    def ingest_train_batch(
        self,
        train_rows: list[TitanicRowDTO],
        test_rows: list[TitanicRowDTO] | None = None,
    ) -> TitanicPreprocessPipelineResultDTO: ...

    def ingest_test_batch(
        self, test_rows: list[TitanicRowDTO]
    ) -> TitanicPreprocessPipelineResultDTO: ...


class TitanicPreprocessPort(Protocol):
    """타이타닉 전처리 인바운드 포트."""

    def execute(self) -> PreprocessResult: ...


class TitanicSubmitPort(Protocol):
    """타이타닉 제출 파일 생성 인바운드 포트."""

    def execute(self) -> dict: ...
