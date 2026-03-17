# Learning 앱 - 헥사고날 아키텍처 샘플

이 디렉터리는 **헥사고날(Hexagonal, Ports & Adapters)** 아키텍처로 구성된 샘플입니다.

## 구조

```
learning/
├── domain/                    # 도메인 계층 (핵심 비즈니스)
│   ├── value_objects.py       # TitanicDataSet, PreprocessResult, EvaluationResult
│   └── ports/                 # 아웃바운드 포트(인터페이스)
│       ├── titanic_data.py    # ITitanicDataPort
│       ├── preprocessor.py    # IPreprocessorPort
│       └── model_runner.py    # IModelRunnerPort
│
├── application/               # 애플리케이션 계층
│   └── use_cases/             # 유스케이스
│       ├── preprocess_titanic.py
│       ├── evaluate_titanic.py
│       └── submit_titanic.py
│
├── adapter/
│   ├── input/                 # 인바운드 어댑터 (드라이빙)
│   │   └── api/v1/
│   │       └── titanic_router.py   # FastAPI 라우터
│   │
│   └── output/                # 아웃바운드 어댑터 (드리븐)
│       ├── persistence/       # CsvTitanicDataAdapter (ITitanicDataPort)
│       ├── preprocessing/     # TitanicPreprocessorAdapter (IPreprocessorPort)
│       └── ml/                # SklearnTitanicModelAdapter (IModelRunnerPort)
│
├── main_hex.py                # 헥사고날 전용 진입점
└── application/main.py       # 기존 진입점 (헥사고날 라우터는 /hex 하위에 포함)
```

## 의존성 방향

- **도메인**: 외부 의존 없음 (순수 비즈니스·값 객체·포트 인터페이스)
- **애플리케이션**: 도메인 포트에만 의존, 유스케이스가 포트를 통해 외부 접근
- **어댑터**: 도메인 포트 구현
  - **input**: API가 유스케이스를 호출
  - **output**: CSV/전처리/Sklearn 등 구체 구현

## 실행 방법

### 1) 기존 main (application/main.py) 사용 시

- `sys.path`에 `learning/` 루트가 포함된 상태로 실행합니다.
- 헥사고날 타이타닉 API는 **`/hex/titanic/`** 아래에 붙습니다.
  - `GET /hex/titanic/` — 상태
  - `GET /hex/titanic/preprocess` — 전처리
  - `GET /hex/titanic/evaluate` — 모델 평가
  - `GET /hex/titanic/submit` — 제출 파일 생성

### 2) 헥사고날 전용 진입점 (main_hex.py) 사용 시

```bash
# learning 디렉터리를 루트로 두고
cd backend/labzang/apps/learning
python main_hex.py
# 또는
uvicorn main_hex:app --host 0.0.0.0 --port 9010
```

- 위와 동일하게 `/hex/titanic/` 경로로 접근합니다.

## 확장 방법

- **새 유스케이스**: `application/use_cases/`에 추가하고, 필요한 포트는 `domain/ports/`에 정의.
- **새 데이터 소스**: `ITitanicDataPort`를 구현한 어댑터를 `adapter/output/persistence/` 등에 추가.
- **새 ML 엔진**: `IModelRunnerPort`를 구현한 어댑터를 `adapter/output/ml/`에 추가.
- **새 API**: `adapter/input/api/v1/`에 라우터 추가 후 `main.py` 또는 `main_hex.py`에서 등록.
