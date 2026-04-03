import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/domain_home_scaffold.dart';

/// `labzang.apps.biz.item` 홈
class BizItemHomePage extends StatelessWidget {
  const BizItemHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DomainHomeScaffold(navTitle: 'Biz · 아이템');
  }
}
