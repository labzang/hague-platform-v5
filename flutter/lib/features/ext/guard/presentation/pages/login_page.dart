import 'package:flutter/cupertino.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:go_router/go_router.dart';
import 'package:labzang_app/core/theme/app_theme.dart';
import 'package:labzang_app/features/ext/guard/data/local_signup_credentials_store.dart';
import 'package:labzang_app/features/ext/guard/presentation/auth_routes.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// 앱 기본 진입 로그인 화면 — ID/비밀번호, 자동 로그인, SNS OAuth(플레이스홀더), 게스트 둘러보기.
/// Backend: `labzang.apps.ext.guard`
class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  static const String _prefAutoLogin = 'auth_auto_login';

  final TextEditingController _idController = TextEditingController();
  final TextEditingController _pwController = TextEditingController();

  bool _autoLogin = false;
  bool _obscurePassword = true;
  bool _prefsLoaded = false;

  @override
  void initState() {
    super.initState();
    _loadAutoLoginPref();
  }

  Future<void> _loadAutoLoginPref() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    if (!mounted) return;
    setState(() {
      _autoLogin = prefs.getBool(_prefAutoLogin) ?? false;
      _prefsLoaded = true;
    });
  }

  Future<void> _setAutoLogin(bool value) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_prefAutoLogin, value);
    if (!mounted) return;
    setState(() => _autoLogin = value);
  }

  @override
  void dispose() {
    _idController.dispose();
    _pwController.dispose();
    super.dispose();
  }

  Future<void> _onLogin() async {
    final String id = _idController.text.trim();
    final String pw = _pwController.text;
    if (id.isEmpty || pw.isEmpty) {
      await _showMessage('아이디와 비밀번호를 입력해 주세요.');
      return;
    }

    final LocalSignupCredentialsStore store =
        await LocalSignupCredentialsStore.open();
    if (store.verifyLogin(id, pw)) {
      if (!mounted) return;
      context.go('/guest');
      return;
    }

    await _showMessage(
      '저장된 회원 정보와 일치하지 않습니다.\n'
      '회원가입으로 임시저장한 아이디·비밀번호를 입력하거나\n'
      '「게스트로 둘러보기」를 이용해 주세요.\n'
      '(자동 로그인 설정: ${_autoLogin ? "켜짐" : "꺼짐"})',
    );
  }

  void _onSignUp() {
    context.push(AuthRoutePaths.signup);
  }

  Future<void> _onOAuthTap(String provider) async {
    await _showMessage('$provider OAuth 연동 전입니다.');
  }

  BoxDecoration _loginFieldDecoration(BuildContext context) {
    final Color border = CupertinoColors.label.resolveFrom(context)
        .withValues(alpha: 0.58);
    return BoxDecoration(
      color: CupertinoColors.systemBackground.resolveFrom(context),
      borderRadius: BorderRadius.circular(12),
      border: Border.all(color: border, width: 2),
    );
  }

  Future<void> _showMessage(String message) async {
    if (!mounted) return;
    await showCupertinoDialog<void>(
      context: context,
      builder: (BuildContext context) => CupertinoAlertDialog(
        content: Text(message),
        actions: [
          CupertinoDialogAction(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final CupertinoThemeData theme = CupertinoTheme.of(context);
    final Color label = CupertinoColors.label.resolveFrom(context);
    final Color secondary = CupertinoColors.secondaryLabel.resolveFrom(context);
    final TextStyle titleStyle = theme.textTheme.navLargeTitleTextStyle
        .copyWith(fontWeight: FontWeight.w700, color: label);

    final double bottomInset = MediaQuery.viewInsetsOf(context).bottom;
    final double safeBottom = MediaQuery.paddingOf(context).bottom;

    return CupertinoPageScaffold(
      backgroundColor: CupertinoColors.systemGroupedBackground.resolveFrom(context),
      child: SafeArea(
        child: LayoutBuilder(
          builder: (BuildContext context, BoxConstraints constraints) {
            return SingleChildScrollView(
              padding: EdgeInsets.fromLTRB(24, 20, 24, 24 + bottomInset),
              keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag,
              child: ConstrainedBox(
                constraints: BoxConstraints(
                  minHeight: constraints.maxHeight - safeBottom - 40,
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const SizedBox(height: 8),
                    Text('랩장 아카데미', style: titleStyle),
                    const SizedBox(height: 8),
                    Text(
                      '아카데미 계정으로 로그인하세요',
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w500,
                        color: secondary,
                      ),
                    ),
                    const SizedBox(height: 28),
                    CupertinoTextField(
                      controller: _idController,
                      placeholder: '아이디를 입력하세요',
                      padding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 14,
                      ),
                      decoration: _loginFieldDecoration(context),
                      autocorrect: false,
                      textInputAction: TextInputAction.next,
                    ),
                    const SizedBox(height: 14),
                    CupertinoTextField(
                      controller: _pwController,
                      placeholder: '비밀번호를 입력하세요',
                      obscureText: _obscurePassword,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 14,
                      ),
                      decoration: _loginFieldDecoration(context),
                      textInputAction: TextInputAction.done,
                      suffix: Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: CupertinoButton(
                          padding: EdgeInsets.zero,
                          minimumSize: Size.zero,
                          onPressed: () {
                            setState(() => _obscurePassword = !_obscurePassword);
                          },
                          child: Icon(
                            _obscurePassword
                                ? CupertinoIcons.eye_slash
                                : CupertinoIcons.eye,
                            size: 22,
                            color: secondary,
                          ),
                        ),
                      ),
                      onSubmitted: (_) => _onLogin(),
                    ),
                    const SizedBox(height: 14),
                    if (_prefsLoaded)
                      GestureDetector(
                        onTap: () => _setAutoLogin(!_autoLogin),
                        behavior: HitTestBehavior.opaque,
                        child: Row(
                          children: [
                            Icon(
                              _autoLogin
                                  ? CupertinoIcons.checkmark_square_fill
                                  : CupertinoIcons.square,
                              size: 24,
                              color: _autoLogin
                                  ? AppBrand.purple
                                  : secondary,
                            ),
                            const SizedBox(width: 10),
                            Text(
                              '자동 로그인',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w500,
                                color: label,
                              ),
                            ),
                          ],
                        ),
                      )
                    else
                      const SizedBox(height: 24),
                    const SizedBox(height: 22),
                    CupertinoButton.filled(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      borderRadius: BorderRadius.circular(12),
                      onPressed: _onLogin,
                      child: const Text(
                        '로그인',
                        style: TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    CupertinoButton(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      onPressed: _onSignUp,
                      child: Container(
                        width: double.infinity,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: AppBrand.purple,
                            width: 1.5,
                          ),
                        ),
                        alignment: Alignment.center,
                        child: const Text(
                          '회원가입',
                          style: TextStyle(
                            fontSize: 17,
                            fontWeight: FontWeight.w600,
                            color: AppBrand.purple,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 28),
                    Row(
                      children: [
                        Expanded(
                          child: Container(
                            height: 0.5,
                            color: CupertinoColors.separator.resolveFrom(
                              context,
                            ),
                          ),
                        ),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                          child: Text(
                            'SNS 계정으로 로그인',
                            style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w500,
                              color: secondary,
                            ),
                          ),
                        ),
                        Expanded(
                          child: Container(
                            height: 0.5,
                            color: CupertinoColors.separator.resolveFrom(
                              context,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        _OAuthCircleButton(
                          backgroundColor: CupertinoColors.white,
                          borderColor: const Color(0xFFE0E0E0),
                          onPressed: () => _onOAuthTap('Google'),
                          child: SvgPicture.asset(
                            'assets/images/oauth/google_logo.svg',
                            width: 26,
                            height: 26,
                            fit: BoxFit.contain,
                          ),
                        ),
                        const SizedBox(width: 20),
                        _OAuthCircleButton(
                          backgroundColor: const Color(0xFF03C75A),
                          onPressed: () => _onOAuthTap('네이버'),
                          child: const Text(
                            'N',
                            style: TextStyle(
                              color: CupertinoColors.white,
                              fontSize: 22,
                              fontWeight: FontWeight.w900,
                              height: 1,
                            ),
                          ),
                        ),
                        const SizedBox(width: 20),
                        _OAuthCircleButton(
                          backgroundColor: const Color(0xFFFEE500),
                          onPressed: () => _onOAuthTap('카카오'),
                          child: const Text(
                            'K',
                            style: TextStyle(
                              color: Color(0xFF191600),
                              fontSize: 20,
                              fontWeight: FontWeight.w900,
                              height: 1,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 36),
                    Center(
                      child: CupertinoButton(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 8,
                        ),
                        minimumSize: Size.zero,
                        onPressed: () => context.push('/guest'),
                        child: Text(
                          '게스트로 둘러보기',
                          style: TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w600,
                            color: AppBrand.purple,
                            decoration: TextDecoration.underline,
                            decorationColor: AppBrand.purple,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _OAuthCircleButton extends StatelessWidget {
  const _OAuthCircleButton({
    required this.backgroundColor,
    required this.onPressed,
    required this.child,
    this.borderColor,
  });

  final Color backgroundColor;
  final Color? borderColor;
  final VoidCallback onPressed;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      cursor: SystemMouseCursors.click,
      child: CupertinoButton(
        padding: EdgeInsets.zero,
        minimumSize: Size.zero,
        onPressed: onPressed,
        child: Container(
          width: 56,
          height: 56,
          decoration: BoxDecoration(
            color: backgroundColor,
            shape: BoxShape.circle,
            border: borderColor != null
                ? Border.all(color: borderColor!, width: 1)
                : null,
            boxShadow: [
              BoxShadow(
                color: CupertinoColors.black.withValues(alpha: 0.06),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          alignment: Alignment.center,
          child: child,
        ),
      ),
    );
  }
}
