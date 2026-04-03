import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/app_side_menu_panel.dart';

/// 햄버거 → [AppSideMenuPanel] (도메인 링크 공통).
class AppDrawerLayout extends StatefulWidget {
  const AppDrawerLayout({
    super.key,
    required this.title,
    required this.child,
    this.titleWidget,
    this.backgroundColor,
    this.trailing,
  });

  final String title;
  /// 지정 시 내비 중앙에 [title] 대신 표시 (브랜드 타이틀 등).
  final Widget? titleWidget;
  final Widget child;
  final Color? backgroundColor;
  final Widget? trailing;

  @override
  State<AppDrawerLayout> createState() => _AppDrawerLayoutState();
}

class _AppDrawerLayoutState extends State<AppDrawerLayout> {
  bool _open = false;

  void _toggle() => setState(() => _open = !_open);

  void _close() {
    if (!_open) return;
    setState(() => _open = false);
  }

  @override
  Widget build(BuildContext context) {
    final bg = widget.backgroundColor ??
        CupertinoColors.systemGrey6.resolveFrom(context);
    final double panelW =
        (MediaQuery.sizeOf(context).width * 0.72).clamp(260.0, 320.0);

    return CupertinoPageScaffold(
      backgroundColor: bg,
      navigationBar: CupertinoNavigationBar(
        border: null,
        middle: widget.titleWidget ?? Text(widget.title),
        trailing: widget.trailing,
        leading: CupertinoButton(
          padding: EdgeInsets.zero,
          onPressed: _toggle,
          child: Icon(
            CupertinoIcons.bars,
            color: CupertinoTheme.of(context).primaryColor,
          ),
        ),
      ),
      child: SafeArea(
        child: Stack(
          children: [
            GestureDetector(
              behavior: HitTestBehavior.opaque,
              onTap: _close,
              child: widget.child,
            ),
            if (_open)
              Positioned.fill(
                child: GestureDetector(
                  onTap: _close,
                  child: Container(
                    color: CupertinoColors.black.withValues(alpha: 0.22),
                  ),
                ),
              ),
            AnimatedPositioned(
              duration: const Duration(milliseconds: 220),
              curve: Curves.easeOutCubic,
              left: _open ? 0 : -panelW,
              top: 0,
              bottom: 0,
              child: AppSideMenuPanel(
                onClose: _close,
                panelWidth: panelW,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
