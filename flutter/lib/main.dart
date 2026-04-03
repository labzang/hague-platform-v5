import 'package:flutter/cupertino.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';

/// Labzang 앱 엔트리. 전역 테마는 [AppTheme]; 게스트 홈은 Kroaddy 스타일 메인 대시보드로 연결된다.
void main() {
  runApp(
    const ProviderScope(
      child: LabzangApp(),
    ),
  );
}

class LabzangApp extends ConsumerWidget {
  const LabzangApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);
    return CupertinoApp.router(
      debugShowCheckedModeBanner: false,
      title: 'Labzang',
      theme: AppTheme.cupertino,
      routerConfig: router,
      locale: const Locale('ko', 'KR'),
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('ko', 'KR'),
        Locale('en', 'US'),
      ],
    );
  }
}
