# Learning 앱: 헥사고날 + 규칙 기반 CRUD / 오케스트레이터 분리

## 1. 전체 구조 (CRUD 경로 vs AI 경로 분리)

의뢰인 변덕·ERD 불확실 시 **단순 데이터 관리(CRUD)**와 **복합 AI 로직**이 엉키지 않도록 분리.

```
                         ┌─────────────────────────────────────────────────────────┐
                         │                  adapter (Infrastructure)                 │
                         │  ┌─────────────────┐    ┌─────────────────────────────┐  │
                         │  │  input/api_v1/  │    │  output/                     │  │
                         │  │  FastAPI        │    │  persistence (SQLAlchemy)    │  │
                         │  │  Routers        │    │  vector_db (ChromaDB)        │  │
                         │  └────────┬────────┘    │  ai_clients (OpenAI/Claude)  │  │
                         └───────────┼─────────────┴──────────────▲───────────────┘  │
                                     │                             │                  │
                         ┌───────────▼─────────────────────────────┴───────────────┐  │
                         │              application (Orchestration)                 │  │
                         │  ┌──────────────────────────────────────────────────┐   │  │
                         │  │  orchestrator/flow_manager                        │   │  │
                         │  │  1. 요청 분류  2. CRUD 경로 vs AI 경로 결정        │   │  │
                         │  └─────────────┬──────────────────┬─────────────────┘   │  │
                         │                │                  │                        │  │
                         │     ┌──────────▼──────────┐  ┌────▼────────────┐          │  │
                         │     │  CRUD 경로          │  │  AI 경로        │          │  │
                         │     │  spokes/crud_spoke  │  │  hub/policy_    │          │  │
                         │     │  (규칙 기반 DB)    │  │  engine         │          │  │
                         │     └──────────┬──────────┘  └────┬────────────┘          │  │
                         │                │                  │                        │  │
                         │                │           ┌──────▼──────┐                 │  │
                         │                │           │  spokes/   │                 │  │
                         │                │           │  rag_spoke │                 │  │
                         │                │           │  titanic_  │                 │  │
                         │                │           │  spoke     │                 │  │
                         │                │           └────────────┘                 │  │
                         │  ┌─────────────▼──────────────────────────────────────┐  │  │
                         │  │  use_cases/  (실제 비즈니스 시나리오)                 │  │  │
                         │  └─────────────────────────────────────────────────────┘  │  │
                         └─────────────────────────────┬────────────────────────────┘  │
                                                        │                               │
                         ┌──────────────────────────────▼──────────────────────────────┐  │
                         │                    domain (Core)                             │  │
                         │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │  │
                         │  │  entities/ │  │  ontology/  │  │  ports/              │  │  │
                         │  │  Titanic,  │  │  Rule-set   │  │  repository_port     │  │  │
                         │  │  User, KB  │  │  (정책)     │  │  vector_store_port   │  │  │
                         │  └─────────────┘  └─────────────┘  │  llm_port            │  │  │
                         │                                    └─────────────────────┘  │  │
                         └─────────────────────────────────────────────────────────────┘  │
```

---

## 2. 흐름 요약

```
  [요청]
     │
     ▼
  orchestrator/flow_manager  ── 1. 요청 분류
     │
     ├── CRUD 경로  ──▶ spokes/crud_spoke  ──▶ persistence (Repository Port)
     │                  (규칙 기반 CRUD)
     │
     └── AI 경로    ──▶ hub/policy_engine  ──▶ spokes/rag_spoke     ──▶ vector_db + ai_clients
                                          └──▶ spokes/titanic_spoke ──▶ use_cases
```

---

## 3. 디렉터리 구조 (최종)

```text
learning/
├── domain/                         # [Core] 비즈니스 엔티티 및 정책 규격
│   ├── entities/                   # Titanic, User, KnowledgeBase (Pure Class)
│   ├── ontology/                   # 온톨로지 기반 정책 (Rule-set)
│   ├── value_objects.py            # 값 객체
│   └── ports/                      # Outbound 인터페이스
│       ├── repository_port.py      # CRUD용 DB 인터페이스 (SQLAlchemy용)
│       ├── vector_db_port.py       # RAG 검색용 (vector_store)
│       ├── llm_port.py             # LLM 추론용
│       └── (타이타닉 포트는 __init__.py)
│
├── application/                    # [Orchestration] 제어 흐름
│   ├── orchestrator/               # 중앙 제어소
│   │   └── flow_manager.py        # 1. 요청 분류 → 2. CRUD or AI 경로 결정
│   ├── hub/                        # Star Topology Hub (Policy 기반)
│   │   └── policy_engine.py        # RAG 정책 및 온톨로지 매핑
│   ├── spokes/                     # 전용 기능 (Spokes)
│   │   ├── rag_spoke.py            # AI 기반 지식 반환
│   │   ├── crud_spoke.py           # 규칙 기반 데이터 처리 (Standard CRUD)
│   │   └── titanic_spoke.py        # 타이타닉 분석 전용
│   ├── use_cases/                  # 실제 비즈니스 시나리오
│   └── common/                     # 공통 유틸
│
└── adapter/                        # [Infrastructure] 실제 구현체
    ├── input/                      # Inbound (API)
    │   └── api_v1/                 # FastAPI Routers (기존 v1 등)
    └── output/                     # Outbound (Persistence & External)
        ├── persistence/            # Alembic + SQLAlchemy (MySQL/PostgreSQL, CRUD)
        ├── vector_db/              # LangChain + ChromaDB (RAG)
        └── ai_clients/             # OpenAI/Anthropic SDK 구현 (ILlmPort)
```

---

## 4. 정리

| 구분 | 경로 | 역할 |
|------|------|------|
| **규칙 기반 CRUD** | flow_manager → crud_spoke → persistence | 전형적인 DB 작업만. AI 추론 없음. |
| **오케스트레이터** | flow_manager → (AI 경로) → hub → spokes | 복합 AI 로직(RAG, 타이타닉 등) 분리 보호. |

- **repository_port**: CRUD를 위한 DB 인터페이스 → adapter/output/persistence에서 구현.
- **vector_db_port / llm_port**: RAG·LLM용 → adapter/output/vector_db, ai_clients에서 구현.
