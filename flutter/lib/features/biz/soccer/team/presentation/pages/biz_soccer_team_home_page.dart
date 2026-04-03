import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/domain_home_scaffold.dart';

/// `labzang.apps.biz.soccer.team` 홈
class BizSoccerTeamHomePage extends StatelessWidget {
  const BizSoccerTeamHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DomainHomeScaffold(navTitle: 'Soccer · 팀');
  }
}
