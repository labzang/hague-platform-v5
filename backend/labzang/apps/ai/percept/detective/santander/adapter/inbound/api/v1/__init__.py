# 헥사고날: 모든 HTTP 라우터는 adapter에만 위치 (레거시 라우터 없음)
from labzang.apps.ai.percept.detective.titanic.adapter.inbound.api.v1.titanic_router import (
    router as titanic_router,
)
from labzang.apps.dash.council.illustrator.cloud.adapter.inbound.api.v1.samsung_router import (
    router as wordcloud_router,
)
from labzang.apps.dash.council.illustrator.folium.adapter.inbound.api.v1.us_unemployment_router import (
    router as us_unemployment_router,
)
from labzang.apps.dash.council.illustrator.folium.adapter.inbound.api.v2.seoul_crime_router import (
    router as seoul_crime_router,
)

__all__ = [
    "seoul_crime_router",
    "titanic_router",
    "us_unemployment_router",
    "wordcloud_router",
]
