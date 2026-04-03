import 'package:flutter/cupertino.dart';

import 'package:labzang_app/features/biz/soccer/presentation/widgets/soccer_team_logo_strip.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// K리그 등록 구단 — 이모지 그리드 허브 (채팅 UI 없음).
class BizSoccerHomePage extends StatelessWidget {
  const BizSoccerHomePage({super.key});

  /// 샘플 화면과 유사한 연한 라벤더 톤 (라이트 모드).
  static const Color _lightPageTint = Color(0xFFF5F7FF);

  @override
  Widget build(BuildContext context) {
    final bool dark = CupertinoTheme.of(context).brightness == Brightness.dark;
    return AppDrawerLayout(
      title: '축구 홈',
      backgroundColor: dark
          ? CupertinoColors.systemGroupedBackground.resolveFrom(context)
          : _lightPageTint,
      child: const SoccerTeamLogoStrip(),
    );
  }
}
