import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import 'package:labzang_app/core/theme/app_theme.dart';
import 'package:labzang_app/shared/navigation/app_domain_links.dart';

/// Kroaddy 스타일 메인 허브 — 히어로 캐러셀, 바로가기, 프로모 배너, 파스텀 메뉴 그리드.
class LabzangHomeDashboard extends StatefulWidget {
  const LabzangHomeDashboard({super.key});

  @override
  State<LabzangHomeDashboard> createState() => _LabzangHomeDashboardState();
}

class _LabzangHomeDashboardState extends State<LabzangHomeDashboard> {
  late final PageController _heroController;
  int _heroIndex = 0;

  static const List<_HeroSlide> _slides = <_HeroSlide>[
    _HeroSlide(
      caption: 'Labzang으로 데이터·AI 기능을 한곳에서',
      colors: <Color>[Color(0xFF7C6CF0), Color(0xFF4E3BC4)],
      badgeIcon: CupertinoIcons.star_fill,
    ),
    _HeroSlide(
      caption: 'K리그·캐글·워드클라우드까지 실험해 보세요',
      colors: <Color>[Color(0xFF3D9A7A), Color(0xFF1F6B52)],
      badgeIcon: CupertinoIcons.chart_bar_alt_fill,
    ),
    _HeroSlide(
      caption: '크롤링·지오코딩으로 수집·시각화',
      colors: <Color>[Color(0xFFE85D75), Color(0xFFB83B52)],
      badgeIcon: CupertinoIcons.map_fill,
    ),
    _HeroSlide(
      caption: '채팅·감성 분석으로 대화형 인사이트',
      colors: <Color>[Color(0xFF5BA4E8), Color(0xFF2E7AB8)],
      badgeIcon: CupertinoIcons.bubble_left_bubble_right_fill,
    ),
  ];

  /// 바로가기 한 줄 라벨 (가로 칩용).
  static const List<String> _quickLabels = <String>[
    '채팅',
    '감성',
    '축구',
    '지오',
    '캐글',
    '워클',
    '크롤',
  ];

  static final List<_MenuStyle> _menuStyles = <_MenuStyle>[
    _MenuStyle(
      icon: CupertinoIcons.bubble_left_bubble_right_fill,
      pastel: Color(0xFFFFF0F7),
      accent: Color(0xFFB84D8E),
    ),
    _MenuStyle(
      icon: CupertinoIcons.star_fill,
      pastel: Color(0xFFFFF8E8),
      accent: Color(0xFFC98A00),
    ),
    _MenuStyle(
      icon: CupertinoIcons.sportscourt,
      pastel: Color(0xFFE8F7ED),
      accent: Color(0xFF1FA37A),
    ),
    _MenuStyle(
      icon: CupertinoIcons.map_fill,
      pastel: Color(0xFFE8F0FF),
      accent: Color(0xFF4A6CF5),
    ),
    _MenuStyle(
      icon: CupertinoIcons.chart_bar_alt_fill,
      pastel: Color(0xFFF3EEFF),
      accent: Color(0xFF6B4EE6),
    ),
    _MenuStyle(
      icon: CupertinoIcons.cloud_fill,
      pastel: Color(0xFFE8F8FC),
      accent: Color(0xFF0B8FCC),
    ),
    _MenuStyle(
      icon: CupertinoIcons.arrow_down_circle_fill,
      pastel: Color(0xFFFFF2EC),
      accent: Color(0xFFE85D4A),
    ),
  ];

  @override
  void initState() {
    super.initState();
    _heroController = PageController();
  }

  @override
  void dispose() {
    _heroController.dispose();
    super.dispose();
  }

  void _push(BuildContext context, String path) {
    context.push(path);
  }

  void _showAllMenus(BuildContext context) {
    showCupertinoModalPopup<void>(
      context: context,
      builder: (BuildContext ctx) => CupertinoActionSheet(
        title: const Text('Labzang 메뉴'),
        actions: <Widget>[
          for (final AppDomainLink link in kAppDomainLinks)
            CupertinoActionSheetAction(
              onPressed: () {
                Navigator.pop(ctx);
                context.push(link.path);
              },
              child: Text(link.label),
            ),
        ],
        cancelButton: CupertinoActionSheetAction(
          onPressed: () => Navigator.pop(ctx),
          child: const Text('닫기'),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final labelColor = CupertinoColors.label.resolveFrom(context);
    final secondary = CupertinoColors.secondaryLabel.resolveFrom(context);

    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
            child: _HeroCarousel(
              controller: _heroController,
              slides: _slides,
              index: _heroIndex,
              onPageChanged: (int i) => setState(() => _heroIndex = i),
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 22, 16, 8),
            child: Text(
              '바로가기',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w700,
                color: labelColor,
              ),
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: SizedBox(
            height: 92,
            child: ListView.separated(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              scrollDirection: Axis.horizontal,
              itemCount: kAppDomainLinks.length,
              separatorBuilder: (_, _) => const SizedBox(width: 12),
              itemBuilder: (BuildContext context, int i) {
                final AppDomainLink link = kAppDomainLinks[i];
                final _MenuStyle st = _menuStyles[i % _menuStyles.length];
                return _QuickActionChip(
                  label: _quickLabels[i],
                  icon: st.icon,
                  onTap: () => _push(context, link.path),
                );
              },
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 20, 16, 8),
            child: _PromoBanner(onPrimaryTap: () => _push(context, '/home/soccer')),
          ),
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 20, 16, 8),
            child: Row(
              children: [
                Text(
                  'Labzang 메뉴',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    color: labelColor,
                  ),
                ),
                const Spacer(),
                CupertinoButton(
                  padding: EdgeInsets.zero,
                  minimumSize: Size.zero,
                  onPressed: () => _showAllMenus(context),
                  child: Text(
                    '전체 보기 →',
                    style: TextStyle(
                      fontSize: 13,
                      color: secondary,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 28),
            child: LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
                const double spacing = 10;
                const double runSpacing = 12;
                final double maxW = constraints.maxWidth;
                const double minTile = 104;
                int cols = (maxW / (minTile + spacing)).floor();
                if (cols < 2) cols = 2;
                if (cols > 4) cols = 4;
                final double tileW =
                    (maxW - spacing * (cols - 1)) / cols;

                return Wrap(
                  spacing: spacing,
                  runSpacing: runSpacing,
                  children: <Widget>[
                    for (int i = 0; i < kAppDomainLinks.length; i++)
                      SizedBox(
                        width: tileW,
                        child: _ThemeMenuCard(
                          link: kAppDomainLinks[i],
                          style: _menuStyles[i % _menuStyles.length],
                          onTap: () => _push(context, kAppDomainLinks[i].path),
                        ),
                      ),
                  ],
                );
              },
            ),
          ),
        ),
      ],
    );
  }
}

class _HeroSlide {
  const _HeroSlide({
    required this.caption,
    required this.colors,
    required this.badgeIcon,
  });

  final String caption;
  final List<Color> colors;
  final IconData badgeIcon;
}

class _MenuStyle {
  const _MenuStyle({
    required this.icon,
    required this.pastel,
    required this.accent,
  });

  final IconData icon;
  final Color pastel;
  final Color accent;
}

class _HeroCarousel extends StatelessWidget {
  const _HeroCarousel({
    required this.controller,
    required this.slides,
    required this.index,
    required this.onPageChanged,
  });

  final PageController controller;
  final List<_HeroSlide> slides;
  final int index;
  final ValueChanged<int> onPageChanged;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: SizedBox(
            height: 176,
            child: Stack(
              fit: StackFit.expand,
              children: [
                PageView.builder(
                  controller: controller,
                  onPageChanged: onPageChanged,
                  itemCount: slides.length,
                  itemBuilder: (BuildContext context, int i) {
                    final _HeroSlide s = slides[i];
                    return DecoratedBox(
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                          colors: s.colors,
                        ),
                      ),
                      child: Stack(
                        fit: StackFit.expand,
                        children: [
                          Positioned(
                            left: 12,
                            top: 12,
                            child: Container(
                              width: 28,
                              height: 28,
                              alignment: Alignment.center,
                              decoration: BoxDecoration(
                                color: CupertinoColors.white.withValues(
                                  alpha: 0.28,
                                ),
                                shape: BoxShape.circle,
                              ),
                              child: Text(
                                '${i + 1}',
                                style: const TextStyle(
                                  color: CupertinoColors.white,
                                  fontWeight: FontWeight.w700,
                                  fontSize: 13,
                                ),
                              ),
                            ),
                          ),
                          Positioned(
                            right: 12,
                            top: 12,
                            child: Container(
                              padding: const EdgeInsets.all(6),
                              decoration: BoxDecoration(
                                color: CupertinoColors.white.withValues(
                                  alpha: 0.22,
                                ),
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: Icon(
                                s.badgeIcon,
                                size: 18,
                                color: CupertinoColors.white,
                              ),
                            ),
                          ),
                          Positioned(
                            left: 0,
                            right: 0,
                            bottom: 0,
                            child: DecoratedBox(
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  begin: Alignment.topCenter,
                                  end: Alignment.bottomCenter,
                                  colors: <Color>[
                                    CupertinoColors.black.withValues(
                                      alpha: 0,
                                    ),
                                    CupertinoColors.black.withValues(
                                      alpha: 0.55,
                                    ),
                                  ],
                                ),
                              ),
                              child: Padding(
                                padding: const EdgeInsets.fromLTRB(
                                  14,
                                  28,
                                  14,
                                  14,
                                ),
                                child: Text(
                                  s.caption,
                                  maxLines: 2,
                                  overflow: TextOverflow.ellipsis,
                                  style: const TextStyle(
                                    color: CupertinoColors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.w600,
                                    height: 1.25,
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 10),
        Row(
          children: [
            Expanded(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List<Widget>.generate(slides.length, (int i) {
                  if (i == index) {
                    return Container(
                      width: 22,
                      height: 5,
                      margin: const EdgeInsets.symmetric(horizontal: 3),
                      decoration: BoxDecoration(
                        color: AppBrand.purple,
                        borderRadius: BorderRadius.circular(3),
                      ),
                    );
                  }
                  return Container(
                    width: 6,
                    height: 6,
                    margin: const EdgeInsets.symmetric(horizontal: 3),
                    decoration: BoxDecoration(
                      color: CupertinoColors.systemGrey3,
                      shape: BoxShape.circle,
                    ),
                  );
                }),
              ),
            ),
            Text(
              '${index + 1} / ${slides.length}',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: CupertinoColors.secondaryLabel.resolveFrom(context),
              ),
            ),
          ],
        ),
      ],
    );
  }
}

class _QuickActionChip extends StatelessWidget {
  const _QuickActionChip({
    required this.label,
    required this.icon,
    required this.onTap,
  });

  final String label;
  final IconData icon;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return CupertinoButton(
      padding: EdgeInsets.zero,
      onPressed: onTap,
      child: SizedBox(
        width: 72,
        child: Column(
          children: [
            Container(
              width: 56,
              height: 56,
              decoration: BoxDecoration(
                color: CupertinoColors.white,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(
                  color: CupertinoColors.separator.resolveFrom(context),
                ),
                boxShadow: <BoxShadow>[
                  BoxShadow(
                    color: CupertinoColors.black.withValues(alpha: 0.04),
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              alignment: Alignment.center,
              child: Icon(
                icon,
                size: 26,
                color: AppBrand.purple,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              label,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w500,
                color: CupertinoColors.label.resolveFrom(context),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _PromoBanner extends StatelessWidget {
  const _PromoBanner({required this.onPrimaryTap});

  final VoidCallback onPrimaryTap;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppBrand.greenMuted,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppBrand.greenBorder, width: 1.2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: CupertinoColors.white.withValues(alpha: 0.85),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              'Labzang · Pilot',
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w600,
                color: AppBrand.green,
              ),
            ),
          ),
          const SizedBox(height: 10),
          const Text(
            '축구·데이터 기능을 바로 써 보세요',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              height: 1.2,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            '승패 예측 챗, 캐글·워드클라우드·크롤링까지 한 화면에서 이동할 수 있어요.',
            style: TextStyle(
              fontSize: 13,
              height: 1.35,
              color: CupertinoColors.secondaryLabel.resolveFrom(context),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Expanded(
                child: CupertinoButton(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  color: AppBrand.green,
                  borderRadius: BorderRadius.circular(10),
                  onPressed: onPrimaryTap,
                  child: const Text(
                    '축구 승패 예측 열기',
                    style: TextStyle(
                      color: CupertinoColors.white,
                      fontWeight: FontWeight.w600,
                      fontSize: 14,
                    ),
                  ),
                ),
              ),
              CupertinoButton(
                padding: const EdgeInsets.only(left: 8),
                onPressed: () => _showHowToUse(context),
                child: Text(
                  '이용 안내',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: AppBrand.green,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _showHowToUse(BuildContext context) {
    showCupertinoDialog<void>(
      context: context,
      builder: (BuildContext ctx) => CupertinoAlertDialog(
        title: const Text('이용 안내'),
        content: const Text(
          '상단 메뉴(☰)에서도 모든 기능으로 이동할 수 있습니다.\n'
          '아래 카드를 탭하면 해당 화면으로 바로 이동합니다.',
        ),
        actions: [
          CupertinoDialogAction(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }
}

class _ThemeMenuCard extends StatelessWidget {
  const _ThemeMenuCard({
    required this.link,
    required this.style,
    required this.onTap,
  });

  final AppDomainLink link;
  final _MenuStyle style;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return CupertinoButton(
      padding: EdgeInsets.zero,
      onPressed: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 10),
        decoration: BoxDecoration(
          color: style.pastel,
          borderRadius: BorderRadius.circular(14),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(style.icon, size: 32, color: style.accent),
            const SizedBox(height: 10),
            Text(
              link.label,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w700,
                color: style.accent,
                height: 1.2,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
