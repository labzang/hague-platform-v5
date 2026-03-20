"""
조립 루트(Composition Root): 포트 구현체 생성 후 유스케이스 주입.
- 인바운드 라우터는 이 모듈의 의존성만 사용하며, output 어댑터를 직접 import하지 않음.
"""

from pathlib import Path
from typing import Optional

from labzang.core.paths import ML_ROOT, LEARNING_ROOT
from labzang.apps.ml.application.ports import (
    TitanicDataPort,
    PreprocessorPort,
    ModelRunnerPort,
    SeoulCrimePort,
    SeoulPreprocessorPort,
    GeocodePort,
    TextSourcePort,
    ImageStoragePort,
)
from labzang.apps.ml.application.use_cases import (
    PreprocessTitanicUC,
    EvaluateTitanicUC,
    SubmitTitanicUC,
)
from labzang.apps.ml.application.use_cases.geospatial.seoul_crime_uc import (
    PreprocessSeoulCrimeUC,
)
from labzang.apps.ml.adapter.outbound import (
    CsvTitanicDataAdapter,
    TitanicPreprocessorAdapter,
    SklearnTitanicModelAdapter,
    SeoulCrimeRepo,
    SeoulPreprocessorAdapter,
    KakaoGeocodeAdapter,
    FileTextSourceAdapter,
    FileImageStorageAdapter,
    GutenbergTextSourceAdapter,
)

# ---------- 타이타닉 리소스 경로 ----------
_titanic_resources_dir: Optional[Path] = None


def _get_titanic_resources_dir() -> Path:
    global _titanic_resources_dir
    if _titanic_resources_dir is not None:
        return _titanic_resources_dir
    _titanic_resources_dir = (ML_ROOT / "data" / "titanic").resolve()
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


def get_titanic_data_port() -> TitanicDataPort:
    return CsvTitanicDataAdapter(_get_titanic_resources_dir())


def get_titanic_preprocessor_port() -> PreprocessorPort:
    return TitanicPreprocessorAdapter()


def get_titanic_model_port() -> ModelRunnerPort:
    return SklearnTitanicModelAdapter()


def get_preprocess_titanic_use_case() -> PreprocessTitanicUC:
    return PreprocessTitanicUC(
        get_titanic_data_port(),
        get_titanic_preprocessor_port(),
    )


def get_evaluate_titanic_use_case() -> EvaluateTitanicUC:
    return EvaluateTitanicUC(
        get_titanic_data_port(),
        get_titanic_preprocessor_port(),
        get_titanic_model_port(),
    )


def get_submit_titanic_use_case() -> SubmitTitanicUC:
    return SubmitTitanicUC(
        get_titanic_data_port(),
        get_titanic_preprocessor_port(),
        get_titanic_model_port(),
    )


# ---------- 서울 범죄 포트·유스케이스 (조립은 여기서만) ----------


def get_seoul_data_port() -> SeoulCrimePort:
    d = _get_seoul_base_dir()
    return SeoulCrimeRepo(d / "data", d / "save")


def get_seoul_preprocessor_port() -> SeoulPreprocessorPort:
    return SeoulPreprocessorAdapter()


def get_seoul_geocode_port() -> GeocodePort:
    return KakaoGeocodeAdapter()


def get_preprocess_seoul_use_case() -> PreprocessSeoulCrimeUC:
    return PreprocessSeoulCrimeUC(
        get_seoul_data_port(),
        get_seoul_preprocessor_port(),
        get_seoul_geocode_port(),
    )


# ---------- 삼성 워드클라우드 (NLP) ----------
_nlp_data_root: Optional[Path] = None


def _get_nlp_data_root() -> Path:
    global _nlp_data_root
    if _nlp_data_root is not None:
        return _nlp_data_root
    # app/wordcloud 기준 (실행 cwd에 app/nlp가 있음을 가정)
    _nlp_data_root = (Path("app") / "nlp").resolve()
    return _nlp_data_root


def get_samsung_text_source_port() -> TextSourcePort:
    return FileTextSourceAdapter(_get_nlp_data_root())


def get_samsung_image_storage_port() -> ImageStoragePort:
    return FileImageStorageAdapter(_get_nlp_data_root())


def get_samsung_wordcloud_use_case() -> "GenerateSamsungWordcloudUC":
    from labzang.apps.ml.application.use_cases.wordcloud.samsung_wordcloud_uc import (
        GenerateSamsungWordcloudUC,
    )
    from labzang.apps.ml.application.services.wordcloud import (
        SamsungWordcloudService,
    )

    return GenerateSamsungWordcloudUC(
        get_samsung_text_source_port(),
        get_samsung_image_storage_port(),
        SamsungWordcloudService(),
    )


# ---------- Emma 워드클라우드 (NLP) ----------
def _get_emma_nlp_root() -> Path:
    return (LEARNING_ROOT / "application" / "nlp").resolve()


def get_emma_text_source_port() -> TextSourcePort:
    # 폰트 경로용으로 nlp 데이터 루트 사용 (app/wordcloud 또는 동일 구조)
    return GutenbergTextSourceAdapter(_get_nlp_data_root())


def get_emma_image_storage_port() -> ImageStoragePort:
    return FileImageStorageAdapter(_get_emma_nlp_root())


def get_emma_wordcloud_use_case() -> "GenerateEmmaWordcloudUC":
    from labzang.apps.ml.application.use_cases.wordcloud.emma_wordcloud_uc import (
        GenerateEmmaWordcloudUC,
    )
    from labzang.apps.ml.application.services.wordcloud import (
        EmmaWordcloudService,
    )

    return GenerateEmmaWordcloudUC(
        get_emma_text_source_port(),
        get_emma_image_storage_port(),
        EmmaWordcloudService(),
    )


# ---------- 워드클라우드 응답 빌더 (주입용) ----------
def get_wordcloud_resp_dep():
    """워드클라우드 라우터에 주입할 응답 빌더 (create_response 대체)."""
    from labzang.apps.ml.adapter.inbound.api.schemas.wordcloud_resp import (
        get_wordcloud_resp,
    )
    return get_wordcloud_resp
