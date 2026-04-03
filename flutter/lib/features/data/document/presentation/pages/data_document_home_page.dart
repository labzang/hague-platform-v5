import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/domain_home_scaffold.dart';

/// `labzang.apps.data.document` 홈
class DataDocumentHomePage extends StatelessWidget {
  const DataDocumentHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DomainHomeScaffold(navTitle: 'Data · 문서');
  }
}
