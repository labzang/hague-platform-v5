import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:labzang_app/main.dart';

void main() {
  testWidgets('Labzang app loads login title', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: LabzangApp(),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('로그인'), findsOneWidget);
  });
}
