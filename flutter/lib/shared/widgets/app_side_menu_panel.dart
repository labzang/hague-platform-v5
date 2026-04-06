import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:labzang_app/core/theme/app_theme.dart';
import 'package:labzang_app/shared/navigation/app_domain_links.dart';

/// Kroaddy 스타일 슬라이드 패널 — 브랜드 헤더, 섹션, 아이콘+라벨, 선택 하이라이트, 로그아웃.
class AppSideMenuPanel extends StatelessWidget {
  const AppSideMenuPanel({
    super.key,
    required this.onClose,
    required this.panelWidth,
  });

  final VoidCallback onClose;

  /// 부모에서 화면 비율 등으로 계산한 폭.
  final double panelWidth;

  static const List<IconData> _linkIcons = <IconData>[
    CupertinoIcons.bubble_left_bubble_right_fill,
    CupertinoIcons.star_fill,
    CupertinoIcons.sportscourt,
    CupertinoIcons.map_fill,
    CupertinoIcons.chart_bar_alt_fill,
    CupertinoIcons.cloud_fill,
    CupertinoIcons.arrow_down_circle_fill,
  ];

  static const Color _logoutCoral = Color(0xFFE85D5D);

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).uri.path;

    return SizedBox(
      width: panelWidth,
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: CupertinoColors.white,
          border: Border(
            right: BorderSide(
              color: CupertinoColors.separator.resolveFrom(context),
              width: 0.5,
            ),
          ),
        ),
        child: SafeArea(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 10, 8, 12),
                child: Row(
                  children: [
                    CupertinoButton(
                      padding: EdgeInsets.zero,
                      minimumSize: Size.zero,
                      onPressed: () {
                        onClose();
                        context.go('/guest');
                      },
                      child: Container(
                        width: 44,
                        height: 44,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(12),
                          gradient: const LinearGradient(
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                            colors: <Color>[
                              Color(0xFF8B6CF0),
                              AppBrand.purple,
                            ],
                          ),
                        ),
                        alignment: Alignment.center,
                        child: const Text(
                          'L',
                          style: TextStyle(
                            color: CupertinoColors.white,
                            fontSize: 22,
                            fontWeight: FontWeight.w800,
                            height: 1,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    const Expanded(
                      child: Text(
                        'Labzang',
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w800,
                          letterSpacing: -0.3,
                          color: AppBrand.purple,
                        ),
                      ),
                    ),
                    CupertinoButton(
                      padding: const EdgeInsets.all(8),
                      minimumSize: Size.zero,
                      onPressed: onClose,
                      child: const Icon(
                        CupertinoIcons.xmark,
                        size: 22,
                        color: AppBrand.purple,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                height: 0.5,
                color: CupertinoColors.separator.resolveFrom(context),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(20, 14, 16, 8),
                child: Text(
                  '카테고리',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    letterSpacing: 0.2,
                    color: CupertinoColors.secondaryLabel.resolveFrom(context),
                  ),
                ),
              ),
              Expanded(
                child: ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  itemCount: kAppDomainLinks.length,
                  itemBuilder: (BuildContext context, int index) {
                    final AppDomainLink e = kAppDomainLinks[index];
                    final bool selected = appDomainLinkMatches(location, e.path);
                    final IconData icon = _linkIcons[index % _linkIcons.length];
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: _SideMenuTile(
                        icon: icon,
                        label: e.label,
                        selected: selected,
                        onTap: () {
                          onClose();
                          context.push(e.path);
                        },
                      ),
                    );
                  },
                ),
              ),
              Container(
                height: 0.5,
                color: CupertinoColors.separator.resolveFrom(context),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(8, 6, 8, 12),
                child: CupertinoButton(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
                  alignment: Alignment.centerLeft,
                  onPressed: () {
                    onClose();
                    context.go('/');
                  },
                  child: Row(
                    children: [
                      const Icon(
                        CupertinoIcons.square_arrow_right,
                        size: 22,
                        color: _logoutCoral,
                      ),
                      const SizedBox(width: 12),
                      const Text(
                        '로그아웃',
                        style: TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.w500,
                          color: _logoutCoral,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _SideMenuTile extends StatelessWidget {
  const _SideMenuTile({
    required this.icon,
    required this.label,
    required this.selected,
    required this.onTap,
  });

  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final Color purple = AppBrand.purple;
    final Color iconColor = selected
        ? purple
        : CupertinoColors.systemGrey.resolveFrom(context);
    final Color textColor = selected
        ? purple
        : CupertinoColors.label.resolveFrom(context);

    return CupertinoButton(
      padding: EdgeInsets.zero,
      onPressed: onTap,
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: selected ? AppBrand.purpleMuted : CupertinoColors.white,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
          child: Row(
            children: [
              Icon(icon, size: 22, color: iconColor),
              const SizedBox(width: 14),
              Expanded(
                child: Text(
                  label,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                    color: textColor,
                    height: 1.2,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
