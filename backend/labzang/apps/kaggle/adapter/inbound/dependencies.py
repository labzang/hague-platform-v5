"""
조립 루트(Composition Root): 포트 구현체 생성 후 유스케이스 주입.
- 인바운드 라우터는 이 모듈의 의존성만 사용하며, output 어댑터를 직접 import하지 않음.
"""
from pathlib import Path
from typing import Optional

from labzang.core.paths import KAGGLE_ROOT, LEARNING_ROOT
from labzang.apps.kaggle.application.ports import (
    ITitanicDataPort,
    IPreprocessorPort,
    IModelRunnerPort,
    ISeoulDataPort,
    ISeoulPreprocessorPort,
    IGeocodePort,
)
from labzang.apps.kaggle.application.use_cases import (
    PreprocessTitanicUseCase,
    EvaluateTitanicUseCase,
    SubmitTitanicUseCase,
)
from labzang.apps.kaggle.application.use_cases.seoul_crime_use_cases import (
    PreprocessSeoulCrimeUseCase,
)
from labzang.apps.kaggle.adapter.outbound import (
    CsvTitanicDataAdapter,
    TitanicPreprocessorAdapter,
    SklearnTitanicModelAdapter,
    SeoulDataAdapter,
    SeoulPreprocessorAdapter,
    KakaoGeocodeAdapter,
)

# ---------- 타이타닉 리소스 경로 ----------
_titanic_resources_dir: Optional[Path] = None


def _get_titanic_resources_dir() -> Path:
    global _titanic_resources_dir
    if _titanic_resources_dir is not None:
        return _titanic_resources_dir
    _titanic_resources_dir = (KAGGLE_ROOT / "data" / "titanic").resolve()
    return _titanic_resources_dir


# ---------- 서울 범죄 경로 ----------
_seoul_base_dir: Optional[Path] = None


def _get_seoul_base_dir() -> Path:
    global _seoul_base_dir
    if _seoul_base_dir is not None:
        return _seoul_base_dir
    _seoul_base_dir = (LEARNING_ROOT / "application" / "seoul_crime").resolve()
    return _seoul_base_dir


# ---------- 타이타닉 포트 팩토리 (조립은 여기서만) ----------


def get_titanic_data_port() -> ITitanicDataPort:
    return CsvTitanicDataAdapter(_get_titanic_resources_dir())


def get_titanic_preprocessor_port() -> IPreprocessorPort:
    return TitanicPreprocessorAdapter()


def get_titanic_model_port() -> IModelRunnerPort:
    return SklearnTitanicModelAdapter()


def get_preprocess_titanic_use_case() -> PreprocessTitanicUseCase:
    return PreprocessTitanicUseCase(
        get_titanic_data_port(),
        get_titanic_preprocessor_port(),
    )


def get_evaluate_titanic_use_case() -> EvaluateTitanicUseCase:
    return EvaluateTitanicUseCase(
        get_titanic_data_port(),
        get_titanic_preprocessor_port(),
        get_titanic_model_port(),
    )


def get_submit_titanic_use_case() -> SubmitTitanicUseCase:
    return SubmitTitanicUseCase(
        get_titanic_data_port(),
        get_titanic_preprocessor_port(),
        get_titanic_model_port(),
    )


# ---------- 서울 범죄 포트·유스케이스 (조립은 여기서만) ----------


def get_seoul_data_port() -> ISeoulDataPort:
    d = _get_seoul_base_dir()
    return SeoulDataAdapter(d / "data", d / "save")


def get_seoul_preprocessor_port() -> ISeoulPreprocessorPort:
    return SeoulPreprocessorAdapter()


def get_seoul_geocode_port() -> IGeocodePort:
    return KakaoGeocodeAdapter()


def get_preprocess_seoul_use_case() -> PreprocessSeoulCrimeUseCase:
    return PreprocessSeoulCrimeUseCase(
        get_seoul_data_port(),
        get_seoul_preprocessor_port(),
        get_seoul_geocode_port(),
    )
