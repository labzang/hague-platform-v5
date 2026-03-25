# Soccer 앱 – 헥사고날 아키텍처 샘플

이 디렉터리는 **헥사고날(포트·어댑터)** 구조로 구성된 샘플입니다.

## 레이어 구조

```
soccer/
├── domain/                    # 도메인 (코어, 외부 의존 없음)
│   └── entities/              # 엔티티, 값 객체
│       └── team_entity.py
├── application/
│   ├── ports/                 # 계약 (인터페이스)
│   │   ├── input/             # 드라이빙: 유스케이스 계약
│   │   │   └── process_team_upload_port.py
│   │   └── output/            # 드리븐: 저장소/외부 서비스 계약
│   │       └── team_repository_port.py
│   └── use_cases/             # 유스케이스 (입력 포트 구현)
│       └── process_team_upload_use_case.py
└── adapter/
    ├── input/                 # 드라이빙 어댑터 (HTTP 등)
    │   └── api/v1/routers/
    │       └── team_router.py  → 유스케이스 호출
    └── outbound/              # 드리븐 어댑터 (DB, 외부 API 등)
        └── persistence/
            └── team_repository_adapter.py  → 출력 포트 구현
```

## 의존성 방향

- **domain**: 어떤 레이어도 의존하지 않음.
- **application**: `domain` + **ports**(인터페이스만) 에만 의존. 구체적인 DB/HTTP는 모름.
- **adapter/input**: `application.use_cases`(입력 포트 구현) 호출.
- **adapter/outbound**: `application.ports.output` **구현** + 인프라(DB 세션 등) 사용.

## 팀 업로드 흐름 (샘플)

1. **라우터** (`adapter/input/.../team_router.py`): JSONL 파싱 후 `ProcessTeamUploadUseCase.execute(items)` 호출.
2. **유스케이스** (`application/use_cases/process_team_upload_use_case.py`): 정규화 후 `TeamRepositoryPort.upsert_batch()` 호출.
3. **출력 어댑터** (`adapter/outbound/persistence/team_repository_adapter.py`): `TeamRepositoryPort` 구현, 기존 `TeamRepository`(hub)로 DB 저장.

기존 `hub.orchestrators`, `hub.repositories`, `spokes` 등은 그대로 두었으며, 팀 업로드만 위 흐름으로 동작합니다.
