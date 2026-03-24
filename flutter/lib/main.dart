import 'package:flutter/material.dart';
import 'presentation/pages/guest_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Labzang',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const LoginScreen(),
        '/guest': (context) => const GuestPage(),
      },
    );
  }
}

/// 첫 화면: 구글 / 카카오 / 게스트 로그인 버튼
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const SizedBox(height: 48),
              Text(
                '로그인',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ) ??
                    const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 48),
              // 구글 OAuth (버튼만, 연동 없음)
              _SocialButton(label: '구글', onPressed: () {}),
              const SizedBox(height: 16),
              // 카카오 OAuth (버튼만, 연동 없음)
              _SocialButton(label: '카카오', onPressed: () {}),
              const SizedBox(height: 16),
              // 게스트 모드 진입 → 전용 페이지로 이동
              _SocialButton(
                label: '게스트',
                onPressed: () => _onGuestLogin(context),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _onGuestLogin(BuildContext context) {
    Navigator.of(context).pushNamed('/guest');
  }
}

class _SocialButton extends StatelessWidget {
  const _SocialButton({
    required this.label,
    required this.onPressed,
  });

  final String label;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 52,
      child: FilledButton(
        onPressed: onPressed,
        child: Text(label, style: const TextStyle(fontSize: 16)),
      ),
    );
  }
}

