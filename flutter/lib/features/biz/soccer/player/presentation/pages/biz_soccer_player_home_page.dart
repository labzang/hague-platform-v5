import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/domain_home_scaffold.dart';

/// `labzang.apps.biz.soccer.player` 홈
class BizSoccerPlayerHomePage extends StatelessWidget {
  const BizSoccerPlayerHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DomainHomeScaffold(navTitle: 'Soccer · 선수');
  }
}
