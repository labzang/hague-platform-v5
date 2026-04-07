import 'package:flutter/cupertino.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// 서울 범죄 지리 시각화 랜딩 — `labzang.apps.dash.geospatial.seoul_crime`
class SeoulCrimeLandingPage extends StatelessWidget {
  const SeoulCrimeLandingPage({super.key});

  static const _bannerAsset = 'assets/images/geospatial/seoul_crime_banner.png';

  @override
  Widget build(BuildContext context) {
    final bg = CupertinoColors.systemGroupedBackground.resolveFrom(context);

    return AppDrawerLayout(
      title: 'Seoul Crime',
      backgroundColor: bg,
      child: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: _HeroBanner(assetPath: _bannerAsset),
          ),
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(20, 20, 20, 32),
            sliver: SliverList(
              delegate: SliverChildListDelegate(
                [
                  _SectionTitle(
                    '서울 범죄 데이터 지리 분석',
                    subtitle:
                        '행정구역(구) 단위 코로플레스와 지점별 버블로 범죄 지표를 '
                        '한눈에 비교합니다.',
                  ),
                  const SizedBox(height: 16),
                  _InfoCard(
                    icon: CupertinoIcons.map,
                    title: '구역 음영 (Choropleth)',
                    body:
                        '각 자치구 폴리곤에 0.07 ~ 0.33 범위의 스케일로 값을 '
                        '색 농도로 표현합니다. 진한 마젠타일수록 상대적으로 높은 지표입니다.',
                  ),
                  const SizedBox(height: 12),
                  _InfoCard(
                    icon: CupertinoIcons.circle_grid_3x3_fill,
                    title: '버블 (밀도 지점)',
                    body:
                        '반투명 파란 원의 크기는 해당 위치의 사건 강도·건수 등 '
                        '집계 지표를 나타냅니다. 강북·강서·강남 등 클러스터를 확인할 수 있습니다.',
                  ),
                  const SizedBox(height: 24),
                  Text(
                    '백엔드 연동 후 실시간 데이터·필터·상세 지도가 이어집니다.',
                    style: TextStyle(
                      fontSize: 14,
                      height: 1.35,
                      color: CupertinoColors.secondaryLabel.resolveFrom(context),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _HeroBanner extends StatelessWidget {
  const _HeroBanner({required this.assetPath});

  final String assetPath;

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: const BorderRadius.only(
        bottomLeft: Radius.circular(18),
        bottomRight: Radius.circular(18),
      ),
      child: SizedBox(
        height: 240,
        width: double.infinity,
        child: Stack(
          fit: StackFit.expand,
          children: [
            Image.asset(
              assetPath,
              fit: BoxFit.cover,
              errorBuilder: (_, _, _) => Container(
                color: CupertinoColors.systemGrey4,
                alignment: Alignment.center,
                child: const Text('이미지를 불러올 수 없습니다'),
              ),
            ),
            DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    CupertinoColors.black.withValues(alpha: 0.35),
                    CupertinoColors.black.withValues(alpha: 0.65),
                  ],
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 28, 20, 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: CupertinoColors.white.withValues(alpha: 0.22),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      'GEOSPATIAL · SEOUL',
                      style: TextStyle(
                        color: CupertinoColors.white,
                        fontSize: 11,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 1.2,
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    'Seoul Crime Map',
                    style: TextStyle(
                      color: CupertinoColors.white,
                      fontSize: 28,
                      fontWeight: FontWeight.w800,
                      height: 1.1,
                      letterSpacing: -0.5,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    '서울 범죄 통계 · 시각화 랜딩',
                    style: TextStyle(
                      color: CupertinoColors.white.withValues(alpha: 0.92),
                      fontSize: 15,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.title, {required this.subtitle});

  final String title;
  final String subtitle;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.w700,
            color: CupertinoColors.label.resolveFrom(context),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          subtitle,
          style: TextStyle(
            fontSize: 15,
            height: 1.4,
            color: CupertinoColors.secondaryLabel.resolveFrom(context),
          ),
        ),
      ],
    );
  }
}

class _InfoCard extends StatelessWidget {
  const _InfoCard({
    required this.icon,
    required this.title,
    required this.body,
  });

  final IconData icon;
  final String title;
  final String body;

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        color: CupertinoColors.systemBackground.resolveFrom(context),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: CupertinoColors.separator.resolveFrom(context),
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, size: 26, color: CupertinoColors.activeBlue),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    body,
                    style: TextStyle(
                      fontSize: 14,
                      height: 1.35,
                      color: CupertinoColors.secondaryLabel.resolveFrom(context),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
