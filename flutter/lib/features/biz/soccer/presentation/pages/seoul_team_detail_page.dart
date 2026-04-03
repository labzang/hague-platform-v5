import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import 'package:labzang_app/core/theme/app_theme.dart';

/// 서울(K09) 샘플 상세 — 스타디움 히어로 + 등록 선수 가로 캐러셀 (여행 플래너 레이아웃 참고).
class SeoulTeamDetailPage extends StatelessWidget {
  const SeoulTeamDetailPage({super.key});

  /// 경기일정 카드 가로세로비. 값이 클수록 세로 높이가 줄어 등록 선수 영역이 한 화면에 더 들어온다.
  /// (기존 72/100 ≈0.72 대비 1.12는 세로 약 35% 감소.)
  static const double _matchCardAspectRatio = 1.12;

  /// 스타디움 더미(네트워크). 빌드 환경에 따라 로드 실패 시 플레이스홀더.
  static const String _stadiumImageUrl =
      'https://images.unsplash.com/photo-1522778119023-d35faa932fa9?w=1200&q=80';

  /// 경기일정 더미 (여행 카드 레이아웃: 배경 이미지 + 좌상단 배지 + 하단 텍스트).
  static const List<_MatchDummy> _dummyMatches = <_MatchDummy>[
    _MatchDummy(
      imageUrl:
          'https://images.unsplash.com/photo-1574623452334-1fcf0b3e3b0a?w=800&q=80',
      title: 'vs 수원 FC',
      subtitle: '2026.04.05(토) 19:00 · 상암월드컵경기장',
      orderBadge: 1,
    ),
    _MatchDummy(
      imageUrl:
          'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&q=80',
      title: 'vs 전북 현대',
      subtitle: '2026.04.12(일) 15:00 · 전주월드컵경기장',
      orderBadge: 2,
    ),
  ];

  static const List<({String name, String position, String number})> _dummyPlayers =
      <({String name, String position, String number})>[
    (name: '김민재', position: 'DF', number: '4'),
    (name: '이강인', position: 'MF', number: '18'),
    (name: '황희찬', position: 'FW', number: '11'),
    (name: '조현우', position: 'GK', number: '21'),
    (name: '황의조', position: 'FW', number: '9'),
    (name: '정우영', position: 'MF', number: '6'),
    (name: '박용우', position: 'MF', number: '8'),
    (name: '김신욱', position: 'FW', number: '19'),
  ];

  @override
  Widget build(BuildContext context) {
    final Color label = CupertinoColors.label.resolveFrom(context);
    final Color secondary = CupertinoColors.secondaryLabel.resolveFrom(context);
    final double bottomInset = MediaQuery.paddingOf(context).bottom;

    return CupertinoPageScaffold(
      backgroundColor: const Color(0xFFF5F7FF),
      navigationBar: CupertinoNavigationBar(
        border: null,
        backgroundColor: CupertinoColors.systemBackground.resolveFrom(context),
        leading: CupertinoNavigationBarBackButton(
          onPressed: () => context.pop(),
        ),
        middle: const Text('서울'),
      ),
      child: SafeArea(
        child: CustomScrollView(
          physics: const ClampingScrollPhysics(),
          slivers: [
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 4),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'FC서울',
                      style: TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.w800,
                        color: label,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '권역별 대표 · 샘플 상세',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: secondary,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(16),
                  child: AspectRatio(
                    aspectRatio: 16 / 9,
                    child: Image.network(
                      _stadiumImageUrl,
                      fit: BoxFit.cover,
                      loadingBuilder: (
                        BuildContext context,
                        Widget child,
                        ImageChunkEvent? loadingProgress,
                      ) {
                        if (loadingProgress == null) return child;
                        return Container(
                          color: CupertinoColors.systemGrey5.resolveFrom(
                            context,
                          ),
                          alignment: Alignment.center,
                          child: const CupertinoActivityIndicator(),
                        );
                      },
                      errorBuilder: (_, _, _) => Container(
                        color: CupertinoColors.systemGrey4,
                        alignment: Alignment.center,
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(
                              CupertinoIcons.sportscourt,
                              size: 48,
                              color: secondary,
                            ),
                            const SizedBox(height: 8),
                            Text(
                              '스타디움 이미지(더미)',
                              style: TextStyle(color: secondary),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 20, 16, 0),
                child: Text(
                  '경기일정',
                  style: TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.w800,
                    color: label,
                  ),
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 10, 16, 6),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      child: AspectRatio(
                        aspectRatio: _matchCardAspectRatio,
                        child: _MatchScheduleCard(match: _dummyMatches[0]),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: AspectRatio(
                        aspectRatio: _matchCardAspectRatio,
                        child: _MatchScheduleCard(match: _dummyMatches[1]),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 24, 16, 12),
                child: Text(
                  '등록 선수 (샘플)',
                  style: TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.w800,
                    color: label,
                  ),
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: SizedBox(
                height: 188,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                  physics: const BouncingScrollPhysics(),
                  itemCount: _dummyPlayers.length,
                  separatorBuilder: (_, _) => const SizedBox(width: 12),
                  itemBuilder: (BuildContext context, int index) {
                    final p = _dummyPlayers[index];
                    return _PlayerCarouselCard(
                      name: p.name,
                      position: p.position,
                      number: p.number,
                      rank: index + 1,
                    );
                  },
                ),
              ),
            ),
            SliverToBoxAdapter(
              child: SizedBox(height: 16 + bottomInset),
            ),
          ],
        ),
      ),
    );
  }
}

class _MatchDummy {
  const _MatchDummy({
    required this.imageUrl,
    required this.title,
    required this.subtitle,
    required this.orderBadge,
  });

  final String imageUrl;
  final String title;
  final String subtitle;
  final int orderBadge;
}

/// 참고 UI: 좌상단 주황 원 배지 + 전면 배경 이미지 + 하단 제목/부제.
class _MatchScheduleCard extends StatelessWidget {
  const _MatchScheduleCard({required this.match});

  final _MatchDummy match;

  static const Color _badgeOrange = Color(0xFFFF6B35);

  @override
  Widget build(BuildContext context) {
    final Color secondary = CupertinoColors.secondaryLabel.resolveFrom(context);

    return ClipRRect(
      borderRadius: BorderRadius.circular(14),
      child: Stack(
        fit: StackFit.expand,
        children: [
          Image.network(
            match.imageUrl,
            fit: BoxFit.cover,
            loadingBuilder: (
              BuildContext context,
              Widget child,
              ImageChunkEvent? loadingProgress,
            ) {
              if (loadingProgress == null) return child;
              return ColoredBox(
                color: CupertinoColors.systemGrey5.resolveFrom(context),
                child: const Center(child: CupertinoActivityIndicator()),
              );
            },
            errorBuilder: (_, _, _) => ColoredBox(
              color: CupertinoColors.systemGrey4,
              child: Center(
                child: Icon(
                  CupertinoIcons.calendar,
                  size: 40,
                  color: secondary,
                ),
              ),
            ),
          ),
          Positioned.fill(
            child: DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    CupertinoColors.black.withValues(alpha: 0.0),
                    CupertinoColors.black.withValues(alpha: 0.55),
                  ],
                  stops: const <double>[0.35, 1.0],
                ),
              ),
            ),
          ),
          Positioned(
            left: 8,
            top: 8,
            child: Container(
              width: 28,
              height: 28,
              alignment: Alignment.center,
              decoration: const BoxDecoration(
                color: _badgeOrange,
                shape: BoxShape.circle,
              ),
              child: Text(
                '${match.orderBadge}',
                style: const TextStyle(
                  color: CupertinoColors.white,
                  fontWeight: FontWeight.w800,
                  fontSize: 13,
                ),
              ),
            ),
          ),
          Positioned(
            left: 10,
            right: 10,
            bottom: 10,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  match.title,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    color: CupertinoColors.white,
                    fontWeight: FontWeight.w800,
                    fontSize: 14,
                    height: 1.2,
                    shadows: [
                      Shadow(color: Color(0x99000000), blurRadius: 6),
                    ],
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  match.subtitle,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    color: CupertinoColors.white,
                    fontWeight: FontWeight.w500,
                    fontSize: 11,
                    height: 1.25,
                    shadows: [
                      Shadow(color: Color(0x99000000), blurRadius: 4),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _PlayerCarouselCard extends StatelessWidget {
  const _PlayerCarouselCard({
    required this.name,
    required this.position,
    required this.number,
    required this.rank,
  });

  final String name;
  final String position;
  final String number;
  final int rank;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 148,
      decoration: BoxDecoration(
        color: CupertinoColors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: CupertinoColors.black.withValues(alpha: 0.07),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      clipBehavior: Clip.antiAlias,
      child: Stack(
        fit: StackFit.expand,
        children: [
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  AppBrand.purpleMuted,
                  CupertinoColors.white,
                ],
              ),
            ),
            child: Center(
              child: Text(
                position,
                style: TextStyle(
                  fontSize: 36,
                  fontWeight: FontWeight.w900,
                  color: AppBrand.purple.withValues(alpha: 0.35),
                ),
              ),
            ),
          ),
          Positioned(
            left: 8,
            top: 8,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: CupertinoColors.black.withValues(alpha: 0.45),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                '$rank',
                style: const TextStyle(
                  color: CupertinoColors.white,
                  fontWeight: FontWeight.w700,
                  fontSize: 12,
                ),
              ),
            ),
          ),
          Positioned(
            left: 10,
            right: 10,
            bottom: 12,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  name,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    color: CupertinoColors.white,
                    fontWeight: FontWeight.w800,
                    fontSize: 15,
                    shadows: [
                      Shadow(
                        color: Color(0x88000000),
                        blurRadius: 4,
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  'No.$number · $position',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    color: CupertinoColors.white,
                    fontSize: 11,
                    fontWeight: FontWeight.w600,
                    shadows: [
                      Shadow(
                        color: Color(0x88000000),
                        blurRadius: 4,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
