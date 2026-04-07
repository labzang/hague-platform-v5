"""Composition root for sentiment inbound adapters."""

from pathlib import Path

from labzang.apps.ai.sentiment.adapter.outbound.impl import (
    KoELECTRAInferenceImpl,
    KoELECTRATrainingRunnerImpl,
    SentimentRepositoryImpl,
)
from labzang.apps.ai.sentiment.application.ports.input import (
    SentimentCommand,
    SentimentQuery,
    TrainingEventCommand,
)
from labzang.apps.ai.sentiment.application.use_cases import (
    SentimentCommandImpl,
    SentimentQueryImpl,
    TrainingEventCommandImpl,
)


def _resources_data_dir() -> Path:
    # sentiment/adapter/inbound/dependencies.py -> sentiment/resources/data
    return Path(__file__).resolve().parents[2] / "resources" / "data"


def get_sentiment_query() -> SentimentQuery:
    return SentimentQueryImpl(KoELECTRAInferenceImpl())


def get_sentiment_command() -> SentimentCommand:
    return SentimentCommandImpl(SentimentRepositoryImpl(), _resources_data_dir())


def get_training_event_command() -> TrainingEventCommand:
    return TrainingEventCommandImpl(KoELECTRATrainingRunnerImpl())
