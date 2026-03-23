"""
ChatLLMPort 구현: 설정에 따라 OpenAI / Midm / Korean Local LLM 생성
"""
from typing import Any, Optional

from labzang.apps.chat.application.ports.output import ChatLLMPort
from labzang.apps.chat.domain.value_objects import LlmConfig
from labzang.apps.chat.adapter.outbound.llm.providers.openai import create_openai_chat_llm
from labzang.apps.chat.adapter.outbound.llm.providers.korean_hf_local import create_local_korean_llm
from labzang.apps.chat.adapter.outbound.llm.providers.midm_local import create_midm_local_llm


class ChatLLMAdapter(ChatLLMPort):
    """설정(provider 등)에 따라 LLM 인스턴스를 생성하는 아웃바운드 어댑터."""

    def create_llm(self, config: LlmConfig) -> Optional[Any]:
        provider = (config.provider or "").strip().lower()
        if not provider:
            return None

        if provider == "openai":
            if not config.openai_api_key:
                print("⚠️ OpenAI API 키가 설정되지 않았습니다.")
                return None
            print("🤖 OpenAI LLM을 사용합니다.")
            return create_openai_chat_llm()

        if provider == "korean_local":
            if not config.local_model_dir:
                print("⚠️ LOCAL_MODEL_DIR이 설정되지 않았습니다.")
                return None
            print(f"🏠 로컬 한국어 모델을 사용합니다: {config.local_model_dir}")
            return create_local_korean_llm(config.local_model_dir)

        if provider == "midm":
            print("🤖 Midm-2.0-Mini-Instruct 모델을 사용합니다.")
            model_dir = config.local_model_dir if config.local_model_dir else None
            return create_midm_local_llm(model_dir)

        raise ValueError(f"지원하지 않는 LLM provider: {config.provider}")
