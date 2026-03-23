# 인바운드: API(api/), 팩토리(factories/), hub_sink 등
from labzang.apps.chat.adapter.inbound.factories import create_llm_from_config

__all__ = ["create_llm_from_config"]
