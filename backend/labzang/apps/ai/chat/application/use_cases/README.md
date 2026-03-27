# Use Cases — 역할과 호출 위치

유스케이스는 **애플리케이션 로직**이다.  
**output 포트(인터페이스)**만 의존하고, 실제 구현(어댑터)은 인바운드에서 주입받는다.

---

## 1. 각 유스케이스가 하는 일

| 유스케이스 | 하는 일 | 의존하는 output 포트 |
|-----------|--------|----------------------|
| **CreateLlmFromConfigUC** | 설정(LlmConfig)으로 LLM 인스턴스 하나 생성 | ChatLLMPort |
| **QLoRAChatUC** | 메시지 → QLoRA 포트로 답변 생성 (원시 파라미터) | QLoRAChatPort |
| **QLoRATrainUC** | 데이터셋으로 QLoRA SFT 학습 실행 | QLoRAChatPort |
| **ChatQueryUC** | ChatRequestDto → ChatResponseDto (단순 채팅, DTO 기반) | QLoRAChatPort |
| **SearchUC** | SearchQueryDto → SearchResultDto (벡터 검색만) | (내부에서 SearchSpoke → VectorRepositoryPort) |
| **RAGOrchestrator** (hub) | RAGQueryDto → RAGResultDto (검색 + 컨텍스트 + 답변 생성) | SearchSpoke, GenerateAnswerSpoke → VectorRepositoryPort, QLoRAChatPort |

---

## 2. 어디서 가져다 쓰는가 (호출 위치)

**호출하는 쪽 = 인바운드 어댑터** (API 라우터, CLI, 배치 진입점 등).

| 유스케이스 | 현재 호출 위치 | 비고 |
|-----------|----------------|------|
| **CreateLlmFromConfigUC** | `adapter/inbound/factory.py` → `create_llm_from_config()` | ✅ 앱 기동 시 LLM 생성에 사용 중 |
| **QLoRAChatUC** | (없음) | API에서 직접 QLoRA 쓰는 곳에서 이 유스케이스로 대체 가능 |
| **QLoRATrainUC** | (없음) | 학습 API/CLI 진입점에서 주입해 호출하면 됨 |
| **ChatQueryUC** | (없음) | POST /chat 같은 단순 채팅 엔드포인트에서 주입해 호출 |
| **SearchUC** | (없음) | `search_router`에서 벡터스토어 직접 호출 대신 이 유스케이스 호출로 연결 가능 |
| **RAGOrchestrator** | (없음) | `chat_router`의 RAG 플로우를 이 오케스트레이터 호출로 교체 가능 |

정리하면, **지금 실제로 쓰이는 건 CreateLlmFromConfigUC 하나**이고,  
나머지는 “인바운드에서 유스케이스를 주입하고 호출하도록” 연결만 하면 된다.

---

## 3. 호출 흐름 (헥사고날)

```
[인바운드]  API/CLI 등
     │
     │  유스케이스 생성 시 output 포트 구현체(어댑터) 주입
     ▼
[유스케이스]  execute(dto) → output 포트 호출
     │
     │  예: chat_port.chat(...), vector_repo.search(...)
     ▼
[아웃바운드 어댑터]  QLoRAChatAdapter, VectorRepositoryImpl 등
     │
     ▼
  실제 기술 (QLoRA, DB, 벡터스토어 등)
```

유스케이스는 **포트 인터페이스만** 알 고, **어떤 어댑터가 붙을지는 인바운드(조립하는 쪽)**에서 결정한다.
