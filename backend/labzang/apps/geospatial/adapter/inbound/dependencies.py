from pathlib import Path

from labzang.apps.geospatial.adapter.outbound.persistence.seoul_crime_repo import (
    KakaoGeocodeAdapter,
    SeoulCrimeRepo,
    SeoulPreprocessorAdapter,
)
from labzang.apps.geospatial.application.ports.seoul_crime_port import (
    GeocodePort,
    SeoulCrimePort,
    SeoulPreprocessorPort,
)
from labzang.apps.geospatial.application.use_cases.seoul_crime_uc import (
    PreprocessSeoulCrimeUC,
)
from labzang.core.paths import LABZANG_ROOT


def _get_seoul_base_dir() -> Path:
    return (LABZANG_ROOT / "apps" / "geospatial" / "seoul_crime" / "resources").resolve()


def get_seoul_data_port() -> SeoulCrimePort:
    base = _get_seoul_base_dir()
    return SeoulCrimeRepo(base / "processed", base / "processed")


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