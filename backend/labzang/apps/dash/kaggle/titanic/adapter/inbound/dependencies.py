"""타이타닉(kaggle/titanic) 인바운드 어댑터용 조립 루트."""

from __future__ import annotations

from labzang.apps.data.kaggle.titanic.adapter.outbound.impl.titanic_feature_repository_impl import (
    TitanicFeatureRepositoryImpl,
)
from labzang.apps.data.kaggle.titanic.adapter.outbound.impl.titanic_repository_impl import (
    TitanicPassengerRepositoryImpl,
)
from labzang.apps.data.kaggle.titanic.application.services.titanic_preprocess_service import (
    TitanicPreprocessService,
)
from labzang.apps.data.kaggle.titanic.application.use_cases.titanic_command_impl import (
    TitanicCommandImpl,
)
from labzang.apps.data.kaggle.titanic.application.use_cases.titanic_query_impl import (
    TitanicQueryImpl,
)


def get_titanic_command_impl() -> TitanicCommandImpl:
    return TitanicCommandImpl(
        repository=TitanicPassengerRepositoryImpl(),
        feature_repository=TitanicFeatureRepositoryImpl(),
        preprocess_service=TitanicPreprocessService(),
    )


def get_titanic_query_impl() -> TitanicQueryImpl:
    return TitanicQueryImpl()
