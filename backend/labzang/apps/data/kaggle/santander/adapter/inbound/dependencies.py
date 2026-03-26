"""
Kaggle/Geospatial/Wordcloud composition root for inbound adapters.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Optional

from labzang.apps.data.geospatial.adapter.outbound.persistence.seoul_crime_repo import (
    KakaoGeocodeAdapter,
    SeoulCrimeRepositoryImpl,
    SeoulPreprocessorAdapter,
)
from labzang.apps.data.geospatial.application.ports.seoul_crime_port import (
    GeocodePort,
    SeoulCrimePort,
    SeoulPreprocessorPort,
)
from labzang.apps.data.geospatial.application.use_cases.seoul_crime_uc import (
    PreprocessSeoulCrimeUC,
)
from labzang.apps.data.kaggle.santander.adapter.outbound.file_adapters.file_image_storage import (
    FileImageStorageAdapter,
)
from labzang.apps.data.kaggle.santander.adapter.outbound.file_adapters.file_text_source import (
    FileTextSourceAdapter,
)
from labzang.apps.data.kaggle.santander.adapter.outbound.file_adapters.gutenberg_text_source import (
    GutenbergTextSourceAdapter,
)
from labzang.apps.data.kaggle.santander.adapter.outbound.repositories.titanic_repo import (
    CsvTitanicDataAdapter,
    SklearnTitanicModelAdapter,
    TitanicPreprocessorAdapter,
)
from labzang.apps.data.kaggle.santander.application.ports.output.titanic_repo_port import (
    ModelRunnerPort,
    PreprocessorPort,
    TitanicDataPort,
)
from labzang.apps.data.kaggle.santander.application.use_cases.titanic_uc import (
    EvaluateTitanicUC,
    PreprocessTitanicUC,
    SubmitTitanicUC,
)
from labzang.apps.data.wordcloud.samsung_report.application.ports.output.wordcloud_ports import (
    ImageStoragePort,
    TextSourcePort,
)
from labzang.core.paths import LEARNING_ROOT, ML_ROOT

if TYPE_CHECKING:
    from labzang.apps.data.wordcloud.samsung_report.application.use_cases.emma_wordcloud_uc import (
        GenerateEmmaWordcloudUC,
    )
    from labzang.apps.data.wordcloud.samsung_report.application.use_cases.samsung_wordcloud_uc import (
        GenerateSamsungWordcloudUC,
    )


_titanic_resources_dir: Optional[Path] = None


def _get_titanic_resources_dir() -> Path:
    global _titanic_resources_dir
    if _titanic_resources_dir is not None:
        return _titanic_resources_dir
    _titanic_resources_dir = (ML_ROOT / "data" / "titanic").resolve()
    return _titanic_resources_dir


_seoul_base_dir: Optional[Path] = None


def _get_seoul_base_dir() -> Path:
    global _seoul_base_dir
    if _seoul_base_dir is not None:
        return _seoul_base_dir
    _seoul_base_dir = (LEARNING_ROOT / "application" / "seoul_crime").resolve()
    return _seoul_base_dir


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


def get_seoul_data_port() -> SeoulCrimePort:
    base = _get_seoul_base_dir()
    return SeoulCrimeRepositoryImpl(base / "data", base / "save")


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


_nlp_data_root: Optional[Path] = None


def _get_nlp_data_root() -> Path:
    global _nlp_data_root
    if _nlp_data_root is not None:
        return _nlp_data_root
    _nlp_data_root = (Path("app") / "nlp").resolve()
    return _nlp_data_root


def get_samsung_text_source_port() -> TextSourcePort:
    return FileTextSourceAdapter(_get_nlp_data_root())


def get_samsung_image_storage_port() -> ImageStoragePort:
    return FileImageStorageAdapter(_get_nlp_data_root())


def get_samsung_wordcloud_use_case() -> "GenerateSamsungWordcloudUC":
    from labzang.apps.data.wordcloud.samsung_report.application.services.samsung_wordcloud_service import (
        SamsungWordcloudService,
    )
    from labzang.apps.data.wordcloud.samsung_report.application.use_cases.samsung_wordcloud_uc import (
        GenerateSamsungWordcloudUC,
    )

    return GenerateSamsungWordcloudUC(
        get_samsung_text_source_port(),
        get_samsung_image_storage_port(),
        SamsungWordcloudService(),
    )


def _get_emma_nlp_root() -> Path:
    return (LEARNING_ROOT / "application" / "nlp").resolve()


def get_emma_text_source_port() -> TextSourcePort:
    return GutenbergTextSourceAdapter(_get_nlp_data_root())


def get_emma_image_storage_port() -> ImageStoragePort:
    return FileImageStorageAdapter(_get_emma_nlp_root())


def get_emma_wordcloud_use_case() -> "GenerateEmmaWordcloudUC":
    from labzang.apps.data.wordcloud.samsung_report.application.services.emma_wordcloud_service import (
        EmmaWordcloudService,
    )
    from labzang.apps.data.wordcloud.samsung_report.application.use_cases.emma_wordcloud_uc import (
        GenerateEmmaWordcloudUC,
    )

    return GenerateEmmaWordcloudUC(
        get_emma_text_source_port(),
        get_emma_image_storage_port(),
        EmmaWordcloudService(),
    )


def get_wordcloud_resp_dep():
    """Wordcloud router response builder dependency."""
    from labzang.apps.data.wordcloud.adapter.inbound.api.schemas.wordcloud_resp import (
        get_wordcloud_resp,
    )

    return get_wordcloud_resp
