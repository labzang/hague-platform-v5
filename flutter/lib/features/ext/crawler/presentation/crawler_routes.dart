import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import 'package:labzang_app/features/ext/crawler/bugsmusic/presentation/pages/ext_crawler_bugsmusic_home_page.dart';
import 'package:labzang_app/features/ext/crawler/naver_news/presentation/pages/ext_crawler_naver_news_home_page.dart';
import 'package:labzang_app/features/ext/crawler/presentation/pages/ext_crawler_home_page.dart';

/// Crawler feature 라우트 경로.
abstract final class CrawlerRoutePaths {
  static const home = '/home/crawler';
  static const bugsmusic = '/home/crawler/bugsmusic';
  static const naverNews = '/home/crawler/naver-news';
}

/// Crawler 도메인 하위 [GoRoute] — [app_router]에서 조합만 한다.
///
/// 더 구체적인 경로를 먼저 등록한다.
List<RouteBase> buildCrawlerRoutes() {
  return <RouteBase>[
    GoRoute(
      path: CrawlerRoutePaths.bugsmusic,
      builder: (BuildContext context, GoRouterState state) =>
          const ExtCrawlerBugsmusicHomePage(),
    ),
    GoRoute(
      path: CrawlerRoutePaths.naverNews,
      builder: (BuildContext context, GoRouterState state) =>
          const ExtCrawlerNaverNewsHomePage(),
    ),
    GoRoute(
      path: CrawlerRoutePaths.home,
      builder: (BuildContext context, GoRouterState state) =>
          const ExtCrawlerHomePage(),
    ),
  ];
}
