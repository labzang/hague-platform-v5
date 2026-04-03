import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/domain_home_scaffold.dart';

/// `labzang.apps.ai.sentiment` 홈
class AiSentimentHomePage extends StatelessWidget {
  const AiSentimentHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DomainHomeScaffold(navTitle: 'AI · 감성');
  }
}
