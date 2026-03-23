"""스포크 — 단일 책임 유스케이스 조각. 오케스트레이터가 조합해 사용."""
from labzang.apps.chat.application.use_cases.spokes.generate_answer_spoke import GenerateAnswerSpoke
from labzang.apps.chat.application.use_cases.spokes.search_spoke import SearchSpoke

__all__ = ["GenerateAnswerSpoke", "SearchSpoke"]
