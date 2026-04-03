import 'package:flutter/cupertino.dart';
import 'package:labzang_app/core/theme/app_theme.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';
import 'package:labzang_app/shared/widgets/labzang_home_dashboard.dart';

/// 게스트 로그인 후 홈 화면 — Kroaddy 스타일 메인 대시보드.
/// Backend: `labzang.apps.ext.auth`
class GuestPage extends StatelessWidget {
  const GuestPage({super.key});

  @override
  Widget build(BuildContext context) {
    return AppDrawerLayout(
      title: 'Labzang',
      titleWidget: const Text(
        'Labzang',
        style: TextStyle(
          fontWeight: FontWeight.w800,
          fontSize: 20,
          letterSpacing: -0.4,
          color: AppBrand.purple,
        ),
      ),
      backgroundColor: CupertinoColors.systemGroupedBackground.resolveFrom(
        context,
      ),
      child: const LabzangHomeDashboard(),
    );
  }
}
