import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import 'package:labzang_app/features/data/wordcloud/presentation/pages/data_wordcloud_home_page.dart';
import 'package:labzang_app/features/data/wordcloud/samsung_report/presentation/pages/samsung_report_home_page.dart';

/// Wordcloud feature 라우트 경로.
abstract final class WordcloudRoutePaths {
  static const home = '/home/wordcloud';
  static const samsungReport = '/home/wordcloud/samsung-report';
}

/// Wordcloud 도메인 하위 [GoRoute] — [app_router]에서 조합만 한다.
///
/// 더 구체적인 경로를 먼저 등록한다.
List<RouteBase> buildWordcloudRoutes() {
  return <RouteBase>[
    GoRoute(
      path: WordcloudRoutePaths.samsungReport,
      builder: (BuildContext context, GoRouterState state) =>
          const SamsungReportHomePage(),
    ),
    GoRoute(
      path: WordcloudRoutePaths.home,
      builder: (BuildContext context, GoRouterState state) =>
          const DataWordcloudHomePage(),
    ),
  ];
}
