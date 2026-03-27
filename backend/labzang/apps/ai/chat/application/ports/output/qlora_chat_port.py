"""
아웃바운드 포트: QLoRA 기반 대화·학습 (구현: adapter/outbound/qlora)
- Application은 이 인터페이스만 의존. torch/transformers/peft 등은 Adapter에만 둠.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class QLoRAChatPort(ABC):
    """QLoRA(4-bit LoRA) 대화 생성 및 학습 포트."""

    @abstractmethod
    def chat(
        self,
        message: str,
        *,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """대화 응답 생성. conversation_history: [{"role":"user"|"assistant","content":"..."}]"""
        ...

    @abstractmethod
    def train(
        self,
        dataset: Any,
        *,
        output_dir: str = "./checkpoints",
        num_train_epochs: int = 3,
        per_device_train_batch_size: int = 4,
        gradient_accumulation_steps: int = 4,
        learning_rate: float = 2e-4,
        warmup_steps: int = 100,
        logging_steps: int = 10,
        save_steps: int = 500,
        save_total_limit: int = 3,
        fp16: bool = True,
        dataset_text_field: str = "text",
    ) -> None:
        """QLoRA SFT 학습. dataset은 Adapter에서 Hugging Face Dataset 등으로 해석."""
        ...

    @abstractmethod
    def save_adapter(self, output_path: str) -> None:
        """LoRA 어댑터 저장."""
        ...
