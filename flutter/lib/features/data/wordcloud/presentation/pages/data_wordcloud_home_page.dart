import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:labzang_app/features/data/wordcloud/presentation/wordcloud_routes.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// `labzang.apps.data.wordcloud` 홈
class DataWordcloudHomePage extends StatelessWidget {
  const DataWordcloudHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return AppDrawerLayout(
      title: '워드클라우드',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
        children: [
          const Text(
            'Getting Started',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 6),
          Text(
            '샘플 미니 카드로 삼성 리포트 워드클라우드를 보여줍니다.',
            style: TextStyle(
              color: CupertinoColors.systemGrey.resolveFrom(context),
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 18),
          _WordcloudSampleCard(
            title: 'Samsung Report',
            subtitle: '삼성 보고서 텍스트 워드클라우드 샘플',
            tag: 'SAMPLE',
            onTap: () => context.push(WordcloudRoutePaths.samsungReport),
          ),
        ],
      ),
    );
  }
}

class _WordcloudSampleCard extends StatelessWidget {
  const _WordcloudSampleCard({
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
                      CupertinoIcons.cloud,
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
                          maxLines: 3,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            fontSize: 15,
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
