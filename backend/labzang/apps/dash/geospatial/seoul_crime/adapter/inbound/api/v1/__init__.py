from labzang.apps.data.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_cctv_router import (
    router as seoul_cctv_router,
)
from labzang.apps.data.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_map_router import (
    router as seoul_map_router,
)
from labzang.apps.data.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_population_router import (
    router as seoul_population_router,
)
from labzang.apps.data.geospatial.seoul_crime.adapter.inbound.api.v1.seoul_crime_router import (
    router as seoul_crime_router,
)

__all__ = [
    "seoul_cctv_router",
    "seoul_population_router",
    "seoul_map_router",
    "seoul_crime_router",
]
