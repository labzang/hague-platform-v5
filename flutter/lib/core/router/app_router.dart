import 'package:flutter/cupertino.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/ai/chat/presentation/pages/ai_chat_home_page.dart';
import '../../features/ai/chat/presentation/pages/chat_room_list_page.dart';
import '../../features/ai/sentiment/presentation/pages/ai_sentiment_home_page.dart';
import '../../features/biz/item/presentation/pages/biz_item_home_page.dart';
import '../../features/biz/soccer/presentation/pages/biz_soccer_home_page.dart';
import '../../features/biz/soccer/presentation/pages/seoul_team_detail_page.dart';
import '../../features/biz/soccer/presentation/soccer_routes.dart';
import '../../features/com/presentation/pages/com_apps_home_page.dart';
import '../../features/data/document/presentation/pages/data_document_home_page.dart';
import '../../features/data/geospatial/presentation/geospatial_routes.dart';
import '../../features/data/kaggle/presentation/kaggle_routes.dart';
import '../../features/data/wordcloud/presentation/wordcloud_routes.dart';
import '../../features/ext/guard/presentation/auth_routes.dart';
import '../../features/ext/guard/presentation/pages/guest_page.dart';
import '../../features/ext/guard/presentation/pages/login_page.dart';
import '../../features/ext/guard/presentation/pages/signup_page.dart';
import '../../features/ext/crawler/presentation/crawler_routes.dart';

/// 기본 라우트: `/` 로그인(구글·네이버·게스트), `/guest` 게스트 홈 — 제거하지 말 것.
/// `/home/*` — 각 백엔드 도메인 플레이스홀더 홈.
final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    routes: <RouteBase>[
      GoRoute(
        path: '/',
        builder: (BuildContext context, GoRouterState state) =>
            const LoginPage(),
      ),
      GoRoute(
        path: '/guest',
        builder: (BuildContext context, GoRouterState state) =>
            const GuestPage(),
      ),
      GoRoute(
        path: AuthRoutePaths.signup,
        builder: (BuildContext context, GoRouterState state) =>
            const SignupPage(),
      ),
      GoRoute(
        path: '/chat/rooms',
        builder: (BuildContext context, GoRouterState state) =>
            const ChatRoomListPage(),
      ),
      GoRoute(
        path: '/home/chat',
        builder: (BuildContext context, GoRouterState state) =>
            const AiChatHomePage(),
      ),
      GoRoute(
        path: '/home/sentiment',
        builder: (BuildContext context, GoRouterState state) =>
            const AiSentimentHomePage(),
      ),
      GoRoute(
        path: '/home/biz-item',
        builder: (BuildContext context, GoRouterState state) =>
            const BizItemHomePage(),
      ),
      GoRoute(
        path: SoccerRoutePaths.seoulDetail,
        builder: (BuildContext context, GoRouterState state) =>
            const SeoulTeamDetailPage(),
      ),
      GoRoute(
        path: SoccerRoutePaths.home,
        builder: (BuildContext context, GoRouterState state) =>
            const BizSoccerHomePage(),
      ),
      GoRoute(
        path: '/home/com',
        builder: (BuildContext context, GoRouterState state) =>
            const ComAppsHomePage(),
      ),
      GoRoute(
        path: '/home/data-document',
        builder: (BuildContext context, GoRouterState state) =>
            const DataDocumentHomePage(),
      ),
      ...buildGeospatialRoutes(),
      ...buildKaggleRoutes(),
      ...buildWordcloudRoutes(),
      ...buildCrawlerRoutes(),
    ],
  );
});
