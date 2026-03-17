# 헥사고날: 모든 HTTP 라우터는 adapter에만 위치
from labzang.apps.kaggle.adapter.input.api.v1.titanic_router import router as titanic_router
from labzang.apps.kaggle.adapter.input.api.v1.legacy_titanic_router import router as legacy_titanic_router
from labzang.apps.kaggle.adapter.input.api.v1.seoul_crime_router import router as seoul_crime_router

__all__ = ["titanic_router", "legacy_titanic_router", "seoul_crime_router"]
