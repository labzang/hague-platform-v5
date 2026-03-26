"""Midm-2.0-Mini-Instruct 로컬 모델 provider."""
from pathlib import Path
from typing import Optional

from labzang.apps.com.chat.adapter.outbound.llm.llm_types import LLMType


def create_midm_local_llm(model_dir: Optional[str] = None) -> LLMType:
    """Midm-2.0-Mini-Instruct 로컬 모델을 로드합니다."""
    try:
        from langchain_community.llms import HuggingFacePipeline
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        import torch
    except ImportError as e:
        raise ImportError(
            f"Midm 모델 사용을 위해 필요한 패키지가 설치되지 않았습니다: {e}\n"
            "pip install transformers torch langchain-community 를 실행하세요."
        )

    model_path: Path
    if model_dir is None:
        from labzang.core.paths import CHAT_ROOT

        model_path = (CHAT_ROOT / "model" / "midm").resolve()
    else:
        model_path = Path(model_dir).resolve()

    if not model_path.exists():
        raise FileNotFoundError(f"Midm 모델 디렉터리를 찾을 수 없습니다: {model_path}")

    print(f"🤖 Midm-2.0-Mini-Instruct 모델 로딩 중: {model_path}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️ 사용 디바이스: {device}")

    try:
        print("📝 토크나이저 로딩 중...")
        tokenizer = AutoTokenizer.from_pretrained(str(model_path))
        print("🧠 모델 로딩 중...")
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto",
            trust_remote_code=True,
        )
        print("⚙️ 파이프라인 생성 중...")
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True,
            return_full_text=False,
            pad_token_id=tokenizer.eos_token_id,
            device=0 if device == "cuda" else -1,
        )
        llm = HuggingFacePipeline(pipeline=pipe)
        print("✅ Midm-2.0-Mini-Instruct 모델 로딩 완료!")
        return llm
    except Exception as e:
        print(f"❌ Midm 모델 로딩 중 오류 발생: {e}")
        raise


def create_midm_instruct_llm(model_dir: Optional[str] = None) -> LLMType:
    """Midm-2.0-Mini-Instruct 모델을 Instruct 형태로 로드합니다."""
    return create_midm_local_llm(model_dir)
