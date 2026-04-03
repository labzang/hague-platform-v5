import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import 'package:labzang_app/features/data/kaggle/presentation/pages/data_kaggle_home_page.dart';
import 'package:labzang_app/features/data/kaggle/titanic/presentation/pages/titanic_chat_page.dart';

/// Kaggle feature 라우트 경로 (푸시/고 등에서 재사용).
abstract final class KaggleRoutePaths {
  static const home = '/home/kaggle';
  static const titanic = '/home/kaggle/titanic';
}

/// Kaggle 도메인 하위 [GoRoute] 목록 — [app_router]에서는 조합만 한다.
///
/// 더 구체적인 경로를 먼저 등록한다 (`/home/kaggle/titanic` vs `/home/kaggle`).
List<RouteBase> buildKaggleRoutes() {
  return <RouteBase>[
    GoRoute(
      path: KaggleRoutePaths.titanic,
      builder: (BuildContext context, GoRouterState state) =>
          const TitanicChatPage(),
    ),
    GoRoute(
      path: KaggleRoutePaths.home,
      builder: (BuildContext context, GoRouterState state) =>
          const DataKaggleHomePage(),
    ),
  ];
}
