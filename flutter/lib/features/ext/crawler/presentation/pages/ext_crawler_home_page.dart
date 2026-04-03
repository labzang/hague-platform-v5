import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:labzang_app/features/ext/crawler/presentation/crawler_routes.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// `labzang.apps.ext.crawler` 홈 — 벅스뮤직, 네이버 뉴스 미니 카드 허브.
class ExtCrawlerHomePage extends StatelessWidget {
  const ExtCrawlerHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return AppDrawerLayout(
      title: '크롤러',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
        children: [
          const Text(
            'Getting Started',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 6),
          Text(
            '벅스뮤직 차트·네이버 뉴스 샘플 크롤러를 미니 카드로 보여줍니다.',
            style: TextStyle(
              color: CupertinoColors.systemGrey.resolveFrom(context),
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 18),
          _CrawlerSampleCard(
            title: 'Bugs Music',
            subtitle: '음원 차트 크롤러 샘플',
            tag: 'SAMPLE',
            icon: CupertinoIcons.music_note_2,
            onTap: () => context.push(CrawlerRoutePaths.bugsmusic),
          ),
          const SizedBox(height: 12),
          _CrawlerSampleCard(
            title: 'Naver News',
            subtitle: '최신 뉴스 크롤러 샘플',
            tag: 'SAMPLE',
            icon: CupertinoIcons.doc_text,
            onTap: () => context.push(CrawlerRoutePaths.naverNews),
          ),
        ],
      ),
    );
  }
}

class _CrawlerSampleCard extends StatelessWidget {
  const _CrawlerSampleCard({
    required this.title,
    required this.subtitle,
    required this.tag,
    required this.icon,
    required this.onTap,
  });

  final String title;
  final String subtitle;
  final String tag;
  final IconData icon;
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
                    child: Icon(
                      icon,
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
