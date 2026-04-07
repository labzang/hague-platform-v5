# 헥사고날: 모든 HTTP 라우터는 adapter에만 위치 (레거시 라우터 없음)
from labzang.apps.data.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_crime_router import (
    router as seoul_crime_router,
)
from labzang.apps.data.geospatial.adapter.inbound.api.v1.us_unemployment_router import (
    router as us_unemployment_router,
)
from labzang.apps.data.kaggle.santander.adapter.inbound.api.v1.titanic_router import (
    router as titanic_router,
)
from labzang.apps.data.wordcloud.samsung_report.adapter.inbound.api.v1.samsung_router import (
    router as wordcloud_router,
)

__all__ = [
    "titanic_router",
    "seoul_crime_router",
    "wordcloud_router",
    "us_unemployment_router",
]
