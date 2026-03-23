"""로컬 Hugging Face 한국어 LLM provider."""
from pathlib import Path

from labzang.apps.chat.adapter.outbound.llm.llm_types import LLMType


def create_local_korean_llm(model_dir: str | Path) -> LLMType:
    """로컬 Hugging Face 한국어 LLM 인스턴스를 생성합니다."""
    try:
        from langchain_community.llms import HuggingFacePipeline
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            pipeline,
            BitsAndBytesConfig,
        )
        import torch
    except ImportError as e:
        raise ImportError(
            f"로컬 HF 모델 사용을 위해 필요한 패키지가 설치되지 않았습니다: {e}\n"
            "pip install transformers torch langchain-community 를 실행하세요."
        )

    model_path = Path(model_dir)
    if not model_path.exists():
        raise FileNotFoundError(f"모델 디렉터리를 찾을 수 없습니다: {model_path}")

    print(f"🔧 로컬 한국어 모델 로딩 중: {model_path}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️ 사용 디바이스: {device}")

    tokenizer = AutoTokenizer.from_pretrained(str(model_path))

    if device == "cuda":
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.float16,
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch.float32,
        )
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True,
        return_full_text=False,
        device=0 if device == "cuda" else -1,
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    print("✅ 로컬 한국어 모델 로딩 완료!")
    return llm
