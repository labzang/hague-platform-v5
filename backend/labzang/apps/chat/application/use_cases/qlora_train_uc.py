"""
QLoRA 학습 유스케이스 — QLoRAChatPort만 의존
"""

from typing import Any

from labzang.apps.chat.application.ports.output import QLoRAChatPort


class QLoRATrainUC:
    """QLoRA 포트를 사용한 SFT 학습 오케스트레이션."""

    def __init__(self, qlora_port: QLoRAChatPort):
        self._port = qlora_port

    def execute(
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
        """QLoRA SFT 학습 실행."""
        self._port.train(
            dataset,
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            warmup_steps=warmup_steps,
            logging_steps=logging_steps,
            save_steps=save_steps,
            save_total_limit=save_total_limit,
            fp16=fp16,
            dataset_text_field=dataset_text_field,
        )
