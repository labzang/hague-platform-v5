import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:labzang_app/features/data/geospatial/presentation/geospatial_routes.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// `labzang.apps.dash.geospatial` 홈
/// Backend 콘텐츠:
/// - `labzang.apps.dash.geospatial.seoul_crime`
/// - `labzang.apps.dash.geospatial.us_unemployment`
class DataGeospatialHomePage extends StatelessWidget {
  const DataGeospatialHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return AppDrawerLayout(
      title: 'Data · 지리',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
        children: [
          const Text(
            'Geospatial Contents',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 6),
          Text(
            '백엔드 콘텐츠를 기반으로 지리 데이터셋을 표시합니다.',
            style: TextStyle(
              color: CupertinoColors.systemGrey.resolveFrom(context),
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 18),
          _GeoContentCard(
            title: 'Seoul Crime',
            subtitle: '서울 범죄 데이터 지리 분석',
            tag: 'seoul_crime',
            onTap: () => context.push(GeospatialRoutePaths.seoulCrime),
          ),
          const SizedBox(height: 12),
          _GeoContentCard(
            title: 'US Unemployment',
            subtitle: '미국 실업률 데이터 지리 시각화',
            tag: 'us_unemployment',
            onTap: () => _showSampleToast(context, 'US Unemployment'),
          ),
        ],
      ),
    );
  }

  void _showSampleToast(BuildContext context, String name) {
    showCupertinoDialog<void>(
      context: context,
      builder: (context) => CupertinoAlertDialog(
        title: const Text('Geospatial'),
        content: Text('$name 콘텐츠 화면은 준비 중입니다.'),
        actions: [
          CupertinoDialogAction(
            isDefaultAction: true,
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }
}

class _GeoContentCard extends StatelessWidget {
  const _GeoContentCard({
    required this.title,
    required this.subtitle,
    required this.tag,
    required this.onTap,
  });

  final String title;
  final String subtitle;
  final String tag;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return CupertinoButton(
      padding: EdgeInsets.zero,
      onPressed: onTap,
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: CupertinoColors.white,
          borderRadius: BorderRadius.circular(14),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 48,
                    height: 48,
                    decoration: const BoxDecoration(
                      color: Color(0xFFE7F2FF),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      CupertinoIcons.location_solid,
                      color: CupertinoColors.activeBlue,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          title,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            fontSize: 17,
                            fontWeight: FontWeight.w600,
                            color: CupertinoColors.black,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          subtitle,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            fontSize: 13,
                            color: CupertinoColors.systemGrey,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              Align(
                alignment: Alignment.centerRight,
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    color: CupertinoColors.systemGrey5,
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Padding(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    child: Text(
                      tag,
                      style: const TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w700,
                        color: CupertinoColors.systemGrey,
                      ),
                    ),
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
