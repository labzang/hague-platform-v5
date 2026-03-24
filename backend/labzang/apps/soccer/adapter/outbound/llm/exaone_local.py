"""ExaOne 로컬 Causal LM provider (축구 MCP / 에이전트 공용)."""
import logging
from pathlib import Path
from typing import Any, Optional

from labzang.core.paths import BACKEND_ROOT

logger = logging.getLogger(__name__)


def create_exaone_local_llm(model_dir: Optional[Path | str] = None) -> Any:
    """로컬 ExaOne 모델을 LangChain 호환 LLM으로 로드합니다."""
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

        try:
            from langchain_huggingface import HuggingFacePipeline
        except ImportError:
            from langchain_community.llms import HuggingFacePipeline
    except ImportError as e:
        raise ImportError(
            "ExaOne 로컬 모델에 필요한 패키지가 없습니다: "
            f"{e}\n pip install torch transformers langchain-community"
        ) from e

    if model_dir is None:
        model_dir = BACKEND_ROOT / "artifacts" / "base-models" / "exaone-2.4b"
    path = Path(model_dir).resolve()
    if not path.exists():
        raise FileNotFoundError(f"ExaOne 모델 디렉터리를 찾을 수 없습니다: {path}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("[exaone_local] ExaOne 로딩: %s (device=%s)", path, device)

    tokenizer = AutoTokenizer.from_pretrained(
        str(path), trust_remote_code=True, local_files_only=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model_kwargs: dict[str, Any] = {
        "torch_dtype": torch.float16 if device == "cuda" else torch.float32,
        "device_map": "auto" if device == "cuda" else None,
        "trust_remote_code": True,
        "local_files_only": True,
    }
    model = AutoModelForCausalLM.from_pretrained(str(path), **model_kwargs)

    text_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
        device=0 if device == "cuda" else -1,
    )
    return HuggingFacePipeline(
        pipeline=text_pipeline,
        model_kwargs={
            "temperature": 0.7,
            "max_new_tokens": 512,
            "do_sample": True,
            "top_p": 0.9,
        },
    )
