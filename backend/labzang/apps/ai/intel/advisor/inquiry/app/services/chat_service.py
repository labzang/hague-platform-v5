"""
😎😎 chat_service.py 서빙 관련 서비스

단순 채팅/대화형 LLM 인터페이스.

세션별 히스토리 관리, 요약, 토큰 절약 전략 등.

QLoRA (4-bit Quantized LoRA)를 사용한 대화 및 학습 기능을 제공합니다.
"""
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

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
from datasets import Dataset, load_dataset


class QLoRAChatService:
    """QLoRA를 사용한 대화 및 학습 서비스."""

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
        """QLoRA 채팅 서비스를 초기화합니다.

        Args:
            model_name_or_path: 모델 이름 또는 경로 (Hugging Face 모델 ID 또는 로컬 경로).
            adapter_path: 기존 LoRA 어댑터 경로 (선택사항).
            device_map: 디바이스 매핑 ("auto", "cuda", "cpu").
            use_4bit: 4-bit 양자화 사용 여부.
            lora_r: LoRA rank.
            lora_alpha: LoRA alpha.
            lora_dropout: LoRA dropout.
            target_modules: LoRA를 적용할 모듈 목록 (None이면 자동 감지).
        """
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
        """모델과 토크나이저를 로드합니다."""
        print(f"🔧 QLoRA 모델 로딩 중: {self.model_name_or_path}")

        # GPU 사용 가능 여부 확인
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🖥️ 사용 디바이스: {device}")

        # 토크나이저 로드
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        # 4-bit 양자화 설정
        quantization_config = None
        if self.use_4bit and device == "cuda":
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

        # 모델 로드
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

        # 기존 어댑터가 있으면 로드
        if self.adapter_path and Path(self.adapter_path).exists():
            print(f"📦 기존 LoRA 어댑터 로딩: {self.adapter_path}")
            self.peft_model = PeftModel.from_pretrained(
                self.model, self.adapter_path
            )
            self.model = self.peft_model
        else:
            # 새 LoRA 설정
            if self.target_modules is None:
                # 일반적인 한국어 모델의 타겟 모듈 (자동 감지 시도)
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

            # 학습 준비 (4-bit 모델인 경우)
            if self.use_4bit:
                self.model = prepare_model_for_kbit_training(self.model)

            self.peft_model = get_peft_model(self.model, lora_config)
            self.model = self.peft_model
        print("😎😎😎😎😎😎😎😎😎😎")
        print("✅ QLoRA 모델 로딩 완료!")
        print("😎😎😎😎😎😎😎😎😎😎")

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
        """대화를 생성합니다.

        Args:
            message: 사용자 메시지.
            max_new_tokens: 최대 생성 토큰 수.
            temperature: 생성 온도.
            top_p: Top-p 샘플링.
            do_sample: 샘플링 사용 여부.
            conversation_history: 대화 히스토리 (선택사항).
                형식: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

        Returns:
            생성된 응답 텍스트.
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("모델이 로드되지 않았습니다.")

        # 대화 히스토리와 현재 메시지를 결합
        if conversation_history:
            # 히스토리를 텍스트로 변환
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

        # 토크나이징
        inputs = self.tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048
        ).to(self.model.device)

        # 생성
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

        # 디코딩
        generated_text = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True
        )

        return generated_text.strip()

    def train(
        self,
        dataset: Dataset,
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
        """QLoRA를 사용하여 모델을 학습합니다.

        Args:
            dataset: 학습 데이터셋 (Hugging Face Dataset).
                형식: {"text": "instruction: ...\ninput: ...\noutput: ..."} 또는
                      {"instruction": "...", "input": "...", "output": "..."}
            output_dir: 체크포인트 저장 디렉터리.
            num_train_epochs: 학습 에포크 수.
            per_device_train_batch_size: 디바이스당 배치 크기.
            gradient_accumulation_steps: 그래디언트 누적 스텝 수.
            learning_rate: 학습률.
            warmup_steps: 워밍업 스텝 수.
            logging_steps: 로깅 스텝 간격.
            save_steps: 저장 스텝 간격.
            save_total_limit: 유지할 체크포인트 수.
            fp16: FP16 사용 여부.
            dataset_text_field: 데이터셋의 텍스트 필드 이름.
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("모델이 로드되지 않았습니다.")

        print("🚀 QLoRA 학습 시작...")

        # 데이터셋 전처리 (필요한 경우)
        if "text" not in dataset.column_names:
            # instruction-input-output 형식을 text로 변환
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

        # 학습 인자 설정
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

        # 데이터 콜레이터
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer, mlm=False
        )

        # SFT Trainer 생성
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

        # 학습 실행
        trainer.train()

        # 최종 모델 저장
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)

        print(f"✅ 학습 완료! 체크포인트 저장 위치: {output_dir}")

    def save_adapter(self, output_path: str) -> None:
        """LoRA 어댑터를 저장합니다.

        Args:
            output_path: 저장 경로.
        """
        if self.peft_model is None:
            raise RuntimeError("PEFT 모델이 없습니다.")

        self.peft_model.save_pretrained(output_path)
        print(f"✅ 어댑터 저장 완료: {output_path}")


def create_qlora_chat_service(
    model_name_or_path: str,
    *,
    adapter_path: Optional[str] = None,
    **kwargs: Any,
) -> QLoRAChatService:
    """QLoRA 채팅 서비스를 생성하는 팩토리 함수.

    Args:
        model_name_or_path: 모델 이름 또는 경로.
        adapter_path: 기존 LoRA 어댑터 경로 (선택사항).
        **kwargs: 추가 인자 (QLoRAChatService.__init__에 전달).

    Returns:
        QLoRAChatService 인스턴스.
    """
    return QLoRAChatService(model_name_or_path, adapter_path=adapter_path, **kwargs)