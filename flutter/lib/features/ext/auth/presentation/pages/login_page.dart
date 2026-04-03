import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

/// 앱 기본 진입 로그인 화면 (구글 / 네이버 / 게스트) — 유지 대상.
/// Backend: `labzang.apps.ext.auth`
class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    final titleStyle = CupertinoTheme.of(context)
        .textTheme
        .navLargeTitleTextStyle
        .copyWith(fontWeight: FontWeight.w600);

    return CupertinoPageScaffold(
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const SizedBox(height: 48),
              Text(
                '로그인',
                style: titleStyle,
              ),
              const SizedBox(height: 48),
              _SocialButton(label: '구글', onPressed: () {}),
              const SizedBox(height: 16),
              _SocialButton(label: '네이버', onPressed: () {}),
              const SizedBox(height: 16),
              _SocialButton(
                label: '게스트',
                onPressed: () => context.push('/guest'),
              ),
            ],
          ),
        ),
      ),
    );
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
    return MouseRegion(
      cursor: SystemMouseCursors.click,
      child: SizedBox(
        width: double.infinity,
        height: 52,
        child: CupertinoButton.filled(
          padding: EdgeInsets.zero,
          onPressed: onPressed,
          child: Text(
            label,
            style: const TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    );
  }
}
