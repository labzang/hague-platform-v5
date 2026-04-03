import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/domain_home_scaffold.dart';

/// `labzang.apps.ext.crawler.naver_news` 홈
class ExtCrawlerNaverNewsHomePage extends StatelessWidget {
  const ExtCrawlerNaverNewsHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DomainHomeScaffold(navTitle: 'Crawler · 네이버뉴스');
  }
}
