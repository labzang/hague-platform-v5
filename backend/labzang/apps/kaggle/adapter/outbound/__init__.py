# 아웃바운드 어댑터 (Application 포트 구현)
from labzang.apps.ml.adapter.outbound.persistence.titanic_repo import (
    CsvTitanicDataAdapter,
    TitanicPreprocessorAdapter,
    SklearnTitanicModelAdapter,
)
from labzang.apps.ml.adapter.outbound.persistence.seoul_crime_repo import (
    SeoulCrimeRepo,
    SeoulPreprocessorAdapter,
    KakaoGeocodeAdapter,
)
from labzang.apps.ml.adapter.outbound.file_adapters import (
    FileTextSourceAdapter,
    FileImageStorageAdapter,
    GutenbergTextSourceAdapter,
)

__all__ = [
    "CsvTitanicDataAdapter",
    "TitanicPreprocessorAdapter",
    "SklearnTitanicModelAdapter",
    "SeoulCrimeRepo",
    "SeoulPreprocessorAdapter",
    "KakaoGeocodeAdapter",
    "FileTextSourceAdapter",
    "FileImageStorageAdapter",
    "GutenbergTextSourceAdapter",
]
