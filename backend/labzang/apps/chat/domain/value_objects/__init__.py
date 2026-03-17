"""
Chat/LLM 도메인 값 객체 (설정 주입용, 순수)
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class LlmConfig:
    """LLM 생성에 필요한 설정 (포트/유스케이스는 이 타입만 의존)."""
    provider: str
    openai_api_key: Optional[str] = None
    local_model_dir: Optional[str] = None
