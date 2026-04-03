import 'package:flutter/widgets.dart';

/// Breakpoints for responsive layouts (Android phone / iPhone / tablets).
/// Use only from presentation — domain/data stay layout-agnostic.
enum AppBreakpoint {
  small,
  medium,
  large,
}

abstract final class AppBreakpoints {
  static const double smallMax = 600;
  static const double mediumMax = 900;

  static AppBreakpoint ofWidth(double width) {
    if (width < smallMax) return AppBreakpoint.small;
    if (width < mediumMax) return AppBreakpoint.medium;
    return AppBreakpoint.large;
  }

  static AppBreakpoint of(BuildContext context) =>
      ofWidth(MediaQuery.sizeOf(context).width);
}
