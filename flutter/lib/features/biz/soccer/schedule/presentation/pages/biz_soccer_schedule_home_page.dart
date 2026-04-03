import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/domain_home_scaffold.dart';

/// `labzang.apps.biz.soccer.schedule` 홈
class BizSoccerScheduleHomePage extends StatelessWidget {
  const BizSoccerScheduleHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DomainHomeScaffold(navTitle: 'Soccer · 일정');
  }
}
