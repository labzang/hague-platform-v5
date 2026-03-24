# 아웃바운드 어댑터 (Application 포트 구현)
from labzang.apps.geospatial.adapter.outbound.persistence.seoul_crime_repo import (
    KakaoGeocodeAdapter,
    SeoulCrimeRepo,
    SeoulPreprocessorAdapter,
)
from labzang.apps.kaggle.adapter.outbound.file_adapters import (
    FileImageStorageAdapter,
    FileTextSourceAdapter,
    GutenbergTextSourceAdapter,
)
from labzang.apps.kaggle.adapter.outbound.repositories.titanic_repo import (
    CsvTitanicDataAdapter,
    SklearnTitanicModelAdapter,
    TitanicPreprocessorAdapter,
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
