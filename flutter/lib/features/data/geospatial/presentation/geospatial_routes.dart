import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import 'package:labzang_app/features/data/geospatial/presentation/pages/data_geospatial_home_page.dart';
import 'package:labzang_app/features/data/geospatial/seoul_crime/presentation/pages/seoul_crime_landing_page.dart';

/// Geospatial feature 라우트 경로.
abstract final class GeospatialRoutePaths {
  static const home = '/home/geospatial';
  static const seoulCrime = '/home/geospatial/seoul-crime';
}

/// Geospatial 도메인 하위 [GoRoute] — [app_router]에서 조합만 한다.
///
/// 하위 경로를 먼저 등록한다.
List<RouteBase> buildGeospatialRoutes() {
  return <RouteBase>[
    GoRoute(
      path: GeospatialRoutePaths.seoulCrime,
      builder: (BuildContext context, GoRouterState state) =>
          const SeoulCrimeLandingPage(),
    ),
    GoRoute(
      path: GeospatialRoutePaths.home,
      builder: (BuildContext context, GoRouterState state) =>
          const DataGeospatialHomePage(),
    ),
  ];
}
