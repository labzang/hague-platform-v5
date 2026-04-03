import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// 도메인별 플레이스홀더 화면 — 가운데 [홈] + 공통 사이드 메뉴.
class DomainHomeScaffold extends StatelessWidget {
  const DomainHomeScaffold({
    super.key,
    required this.navTitle,
  });

  final String navTitle;

  @override
  Widget build(BuildContext context) {
    return AppDrawerLayout(
      title: navTitle,
      child: const Center(
        child: Text(
          '홈',
          style: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );
  }
}
