# 인바운드: LLM 진입점은 create_llm_from_config만 (헥사고날 경계 준수)
from .factory import create_llm_from_config

__all__ = ["create_llm_from_config"]
