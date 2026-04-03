import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/domain_home_scaffold.dart';

/// `labzang.apps.biz.soccer.stadium` 홈
class BizSoccerStadiumHomePage extends StatelessWidget {
  const BizSoccerStadiumHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DomainHomeScaffold(navTitle: 'Soccer · 경기장');
  }
}
