# 타이타닉 헥사고날 구조 (수업용 · 엄격 기준)

**의존성 방향**: `Adapter(외곽) → Application(중심) → Domain(핵심)`. 안쪽은 외부에 의존하지 않음.

---

## 1. Domain (의존성 0, 순수만)

| 위치 | 역할 |
|------|------|
| `domain/entities/` | **순수 파이썬** 엔티티만 (TitanicModels 등). pandas/sklearn/SQL/프레임워크 미사용. |
| `domain/value_objects.py` | 구조화된 데이터(PreprocessResult, EvaluationResult, TitanicDataSet). 타입은 Any/기본형만. |
| `domain/ports/` | **Output Port(아웃바운드)** 인터페이스만. repository_port(CRUD), vector_db_port(RAG), llm_port(LLM), 타이타닉 포트 등. 구현은 Adapter에 둠. |

- Domain에는 비즈니스 규칙·엔티티·값 객체·포트(인터페이스)만 있음.
- 외부 라이브러리 의존이 있으면 Adapter로 빼야 함.

---

## 2. Application (비즈니스 흐름 제어)

| 위치 | 역할 |
|------|------|
| `application/orchestrator/` | **중앙 제어소**. 요청 분류 → **CRUD 경로** vs **AI 경로** 결정. |
| `application/hub/` | Star 허브. AI 경로 내부에서 RAG/타이타닉 등 Spoke 라우팅. |
| `application/spokes/` | **crud_spoke**(규칙 기반 CRUD), **rag_spoke**, **titanic_spoke**. |
| `application/use_cases/` | **Use Case = Application Service**. Port를 호출해 흐름만 제어. |

- `flow_manager`: CRUD vs AI 분리로 단순 DB 작업과 복합 AI 로직이 엉키지 않도록 보호.
- `titanic_use_cases.py`: PreprocessTitanicUseCase, EvaluateTitanicUseCase, SubmitTitanicUseCase.

---

## 3. Adapter (외부 기술 결합)

| 위치 | 역할 |
|------|------|
| `adapter/input/` | FastAPI 라우터만. Port 구현체 조립 후 Use Case 호출. |
| `adapter/output/` | Output Port 구현: persistence(SQLAlchemy CRUD), vector_db(RAG), ai_clients(LLM), 타이타닉(CSV/전처리/Sklearn). |

- `/titanic`·`/hex/titanic` 모두 같은 Use Case + 같은 Output Adapter 사용.

---

## 위반 정리 (수정 완료)

1. **Domain 오염** → `domain/titanic/`(pandas/sklearn 사용) 제거. 순수 엔티티만 `domain/entities/`에 둠.
2. **Application/Use Case 이원화** → `titanic_service.py` 제거. Use Case만 `application/use_cases/`에 둠.
3. **Port 위치** → Output Port는 `domain/ports.py`에만. Input은 라우터가 Use Case를 직접 호출하는 방식으로 통일.

---

## 디렉터리 구조 (엄격 기준 + CRUD/AI 분리)

- **온톨로지 스키마** → `domain/ontology/` (Core, 규격만).
- **오케스트레이터** → `application/orchestrator/flow_manager`: CRUD 경로 vs AI 경로 결정.
- **허브·스포크** → `application/hub/`, `application/spokes/` (crud_spoke, rag_spoke, titanic_spoke).

```text
learning/
├── domain/                  # [Core] 순수 영역 (의존성 0)
│   ├── entities/            # Pure Python 엔티티
│   ├── ontology/            # 온톨로지 스키마 (KG 규격)
│   ├── value_objects.py     # 값 객체
│   └── ports/               # repository_port(CRUD), vector_db_port, llm_port, 타이타닉 등
├── application/             # [Orchestration] 제어 흐름
│   ├── orchestrator/        # flow_manager: CRUD vs AI 경로 분기
│   ├── hub/                 # policy_engine (AI 경로 내부 라우팅)
│   ├── spokes/              # crud_spoke, rag_spoke, titanic_spoke
│   ├── use_cases/           # Use Case = Application Service
│   └── common/              # 공통 유틸
└── adapter/                 # [Infrastructure]
    ├── input/               # FastAPI Router, chatbot_router 등
    └── output/              # persistence, vector_db, ai_clients, 타이타닉 어댑터
```

**규칙 기반 CRUD vs 오케스트레이터(AI) 흐름도**는 `ARCHITECTURE.md` 참고. **application과 ontology를 분리했던 이유**는 `docs/WHY_APPLICATION_AND_ONTOLOGY_WERE_SEPARATED.md` 참고.
