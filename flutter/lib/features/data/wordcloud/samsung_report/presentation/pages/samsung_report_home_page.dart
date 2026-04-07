import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// `labzang.apps.dash.wordcloud.samsung_report` 홈
class SamsungReportHomePage extends StatelessWidget {
  const SamsungReportHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return AppDrawerLayout(
      title: 'Samsung Report',
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
