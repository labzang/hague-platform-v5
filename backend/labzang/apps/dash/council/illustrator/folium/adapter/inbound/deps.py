"""
Composition root for geospatial inbound adapters (Seoul crime).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from labzang.apps.dash.geospatial.adapter.outbound.persistence.seoul_crime_repo import (
    KakaoGeocodeAdapter,
    SeoulCrimeRepositoryImpl,
    SeoulPreprocessorAdapter,
)
from labzang.apps.dash.geospatial.application.ports.seoul_crime_port import (
    GeocodePort,
    SeoulCrimePort,
    SeoulPreprocessorPort,
)
from labzang.apps.dash.geospatial.application.use_cases.seoul_crime_uc import (
    PreprocessSeoulCrimeUC,
)
from labzang.core.paths import LEARNING_ROOT

_seoul_base_dir: Optional[Path] = None


def _get_seoul_base_dir() -> Path:
    global _seoul_base_dir
    if _seoul_base_dir is not None:
        return _seoul_base_dir
    _seoul_base_dir = (LEARNING_ROOT / "application" / "seoul_crime").resolve()
    return _seoul_base_dir


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
