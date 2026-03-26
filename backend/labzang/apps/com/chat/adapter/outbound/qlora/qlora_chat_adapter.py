"""
QLoRAChatPort 구현 — QLoRA(4-bit LoRA) 대화·학습 아웃바운드 어댑터.
torch, transformers, peft, trl, datasets 등 인프라 의존은 이 계층에만 둠.
"""
from pathlib import Path
from typing import Any, Dict, List, Optional

from labzang.apps.com.chat.application.ports.output import QLoRAChatPort

# 인프라 의존 (Adapter 전용)
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel,
    TaskType,
)
from trl import SFTTrainer
from datasets import Dataset


class QLoRAChatAdapter(QLoRAChatPort):
    """QLoRA를 사용한 대화 및 학습 — 포트 구현체."""

    def __init__(
        self,
        model_name_or_path: str,
        *,
        adapter_path: Optional[str] = None,
        device_map: str = "auto",
        use_4bit: bool = True,
        lora_r: int = 64,
        lora_alpha: int = 16,
        lora_dropout: float = 0.1,
        target_modules: Optional[List[str]] = None,
    ):
        self.model_name_or_path = model_name_or_path
        self.adapter_path = adapter_path
        self.device_map = device_map
        self.use_4bit = use_4bit
        self.lora_r = lora_r
        self.lora_alpha = lora_alpha
        self.lora_dropout = lora_dropout
        self.target_modules = target_modules

        self.model: Optional[AutoModelForCausalLM] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.peft_model: Optional[PeftModel] = None

        self._load_model()

    def _load_model(self) -> None:
        """모델과 토크나이저 로드."""
        print(f"🔧 QLoRA 모델 로딩 중: {self.model_name_or_path}")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🖥️ 사용 디바이스: {device}")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        quantization_config = None
        if self.use_4bit and device == "cuda":
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

        model_kwargs = {
            "device_map": self.device_map,
            "torch_dtype": torch.float16 if device == "cuda" else torch.float32,
            "trust_remote_code": True,
        }
        if quantization_config:
            model_kwargs["quantization_config"] = quantization_config

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name_or_path, **model_kwargs
        )

        if self.adapter_path and Path(self.adapter_path).exists():
            print(f"📦 기존 LoRA 어댑터 로딩: {self.adapter_path}")
            self.peft_model = PeftModel.from_pretrained(
                self.model, self.adapter_path
            )
            self.model = self.peft_model
        else:
            if self.target_modules is None:
                self.target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]
                if hasattr(self.model, "config"):
                    config = self.model.config
                    if hasattr(config, "model_type"):
                        model_type = config.model_type.lower()
                        if "llama" in model_type or "mistral" in model_type:
                            self.target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]
                        elif "gpt" in model_type:
                            self.target_modules = ["c_attn", "c_proj"]

            lora_config = LoraConfig(
                r=self.lora_r,
                lora_alpha=self.lora_alpha,
                target_modules=self.target_modules,
                lora_dropout=self.lora_dropout,
                bias="none",
                task_type=TaskType.CAUSAL_LM,
            )
            if self.use_4bit:
                self.model = prepare_model_for_kbit_training(self.model)
            self.peft_model = get_peft_model(self.model, lora_config)
            self.model = self.peft_model

        print("✅ QLoRA 모델 로딩 완료!")

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
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("모델이 로드되지 않았습니다.")

        if conversation_history:
            formatted_messages = []
            for msg in conversation_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    formatted_messages.append(f"사용자: {content}")
                elif role == "assistant":
                    formatted_messages.append(f"어시스턴트: {content}")
            formatted_messages.append(f"사용자: {message}")
            formatted_messages.append("어시스턴트:")
            prompt = "\n".join(formatted_messages)
        else:
            prompt = f"사용자: {message}\n어시스턴트:"

        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        generated_text = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True
        )
        return generated_text.strip()

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
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("모델이 로드되지 않았습니다.")

        # Port는 Any를 받음; 구현체에서는 Hugging Face Dataset 기대
        if not isinstance(dataset, Dataset):
            raise TypeError("QLoRAChatAdapter.train expects a Hugging Face datasets.Dataset.")

        print("🚀 QLoRA 학습 시작...")

        if "text" not in dataset.column_names:
            def format_text(example: Dict[str, Any]) -> Dict[str, str]:
                instruction = example.get("instruction", "")
                input_text = example.get("input", "")
                output = example.get("output", "")
                if input_text:
                    text = f"### Instruction:\n{instruction}\n### Input:\n{input_text}\n### Response:\n{output}"
                else:
                    text = f"### Instruction:\n{instruction}\n### Response:\n{output}"
                return {"text": text}
            dataset = dataset.map(format_text)

        training_args = TrainingArguments(
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
            optim="paged_adamw_32bit",
            lr_scheduler_type="cosine",
            report_to="none",
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer, mlm=False
        )

        trainer = SFTTrainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            tokenizer=self.tokenizer,
            data_collator=data_collator,
            dataset_text_field=dataset_text_field,
            max_seq_length=2048,
            packing=False,
        )

        trainer.train()
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        print(f"✅ 학습 완료! 체크포인트 저장 위치: {output_dir}")

    def save_adapter(self, output_path: str) -> None:
        if self.peft_model is None:
            raise RuntimeError("PEFT 모델이 없습니다.")
        self.peft_model.save_pretrained(output_path)
        print(f"✅ 어댑터 저장 완료: {output_path}")


def create_qlora_chat_adapter(
    model_name_or_path: str,
    *,
    adapter_path: Optional[str] = None,
    **kwargs: Any,
) -> QLoRAChatAdapter:
    """QLoRAChatPort 구현체 생성 (조립 시 사용)."""
    return QLoRAChatAdapter(
        model_name_or_path, adapter_path=adapter_path, **kwargs
    )
