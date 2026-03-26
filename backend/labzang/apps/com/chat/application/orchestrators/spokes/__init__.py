"""Spokes package: small single-purpose units used by orchestrators."""
from labzang.apps.com.chat.application.orchestrators.spokes.generate_answer_spoke import (
    GenerateAnswerSpoke,
)
from labzang.apps.com.chat.application.orchestrators.spokes.search_spoke import SearchSpoke

__all__ = ["GenerateAnswerSpoke", "SearchSpoke"]