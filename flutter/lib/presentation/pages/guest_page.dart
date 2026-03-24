import 'package:flutter/material.dart';

/// 게스트 모드 진입 시 이동하는 페이지
class GuestPage extends StatelessWidget {
  const GuestPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('게스트 모드'),
        centerTitle: true,
      ),
      body: const Center(
        child: Text('게스트로 이용 중입니다.'),
      ),
    );
  }
}
