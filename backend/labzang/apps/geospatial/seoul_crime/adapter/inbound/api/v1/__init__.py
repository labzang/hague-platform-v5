from labzang.apps.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_cctv_uploader import (
    router as seoul_cctv_uploader_router,
)
from labzang.apps.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_map_router import (
    router as seoul_map_router,
)
from labzang.apps.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_population_uploader import (
    router as seoul_population_uploader_router,
)

__all__ = [
    "seoul_cctv_uploader_router",
    "seoul_population_uploader_router",
    "seoul_map_router",
]
