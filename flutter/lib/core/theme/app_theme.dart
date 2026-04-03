import 'package:flutter/cupertino.dart';

/// Kroaddy 느낌의 보라·에메랄드 포인트 ([LabzangHomeDashboard], 내비 등).
abstract final class AppBrand {
  const AppBrand._();

  static const Color purple = Color(0xFF6B4EE6);
  static const Color purpleMuted = Color(0xFFE8E4FB);
  static const Color green = Color(0xFF1FA37A);
  static const Color greenMuted = Color(0xFFE8F5F0);
  static const Color greenBorder = Color(0xFF7BC9A8);
}

/// Global Cupertino theme (iOS-first). Presentation may override per screen.
abstract final class AppTheme {
  static const CupertinoThemeData cupertino = CupertinoThemeData(
    brightness: Brightness.light,
    primaryColor: AppBrand.purple,
    applyThemeToAll: true,
  );
}
