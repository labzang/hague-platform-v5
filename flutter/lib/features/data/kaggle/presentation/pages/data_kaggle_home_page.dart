import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:labzang_app/features/data/kaggle/presentation/kaggle_routes.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// `labzang.apps.dash.kaggle` 홈
class DataKaggleHomePage extends StatelessWidget {
  const DataKaggleHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return AppDrawerLayout(
      title: 'Kaggle 샘플',
      child: ListView(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
        children: [
          const Text(
            'Getting Started',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 6),
          Text(
            '샘플 미니 카드로 타이타닉 / 산탄데르를 보여줍니다.',
            style: TextStyle(
              color: CupertinoColors.systemGrey.resolveFrom(context),
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 18),
          _MiniCompetitionCard(
            title: 'Titanic - Machine Learning from Disaster',
            subtitle: 'Kaggle 입문 대표 대회',
            tag: 'SAMPLE',
            onTap: () => context.push(KaggleRoutePaths.titanic),
          ),
          const SizedBox(height: 12),
          _MiniCompetitionCard(
            title: 'Santander Customer Transaction',
            subtitle: '분류/피처 엔지니어링 샘플',
            tag: 'SAMPLE',
            onTap: () => _showSampleToast(context, '산탄데르'),
          ),
        ],
      ),
    );
  }

  void _showSampleToast(BuildContext context, String name) {
    showCupertinoDialog<void>(
      context: context,
      builder: (context) => CupertinoAlertDialog(
        title: const Text('샘플'),
        content: Text('$name 미니 화면 버튼입니다.'),
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

class _MiniCompetitionCard extends StatelessWidget {
  const _MiniCompetitionCard({
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
                      CupertinoIcons.sportscourt,
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
