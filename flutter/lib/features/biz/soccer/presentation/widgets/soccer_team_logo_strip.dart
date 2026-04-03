import 'dart:math' as math;

import 'package:flutter/cupertino.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart'
    show MaterialScrollBehavior, ScrollConfiguration, Scrollbar;
import 'package:go_router/go_router.dart';

import 'package:labzang_app/features/biz/soccer/domain/k_league_registered_teams.dart';
import 'package:labzang_app/features/biz/soccer/presentation/soccer_routes.dart';

/// K리그 등록 구단 — 검색 + 2열 카드 그리드(이모지 아이콘) + **세로 스크롤·스크롤바**.
class SoccerTeamLogoStrip extends StatefulWidget {
  const SoccerTeamLogoStrip({super.key});

  @override
  State<SoccerTeamLogoStrip> createState() => _SoccerTeamLogoStripState();
}

class _SoccerTeamLogoStripState extends State<SoccerTeamLogoStrip> {
  final TextEditingController _searchController = TextEditingController();
  final ScrollController _gridScrollController = ScrollController();

  @override
  void dispose() {
    _searchController.dispose();
    _gridScrollController.dispose();
    super.dispose();
  }

  List<KLeagueRegisteredTeam> get _filtered {
    final String q = _searchController.text.trim().toLowerCase();
    if (q.isEmpty) {
      return List<KLeagueRegisteredTeam>.from(kKLeagueRegisteredTeams);
    }
    return kKLeagueRegisteredTeams.where((KLeagueRegisteredTeam t) {
      return t.teamName.toLowerCase().contains(q) ||
          t.regionName.toLowerCase().contains(q) ||
          t.eTeamName.toLowerCase().contains(q) ||
          t.teamCode.toLowerCase().contains(q);
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    final List<KLeagueRegisteredTeam> teams = _filtered;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
          child: Text(
            'K리그 등록 구단',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w800,
              letterSpacing: -0.3,
              color: CupertinoColors.label.resolveFrom(context),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
          child: _SearchPillField(
            controller: _searchController,
            placeholder: '구단·연고지 검색 (예: 전북, 서울, 스틸러스)',
            onChanged: (_) => setState(() {}),
          ),
        ),
        Expanded(
          child: teams.isEmpty
              ? Center(
                  child: Text(
                    '검색 결과가 없습니다',
                    style: TextStyle(
                      fontSize: 14,
                      color:
                          CupertinoColors.secondaryLabel.resolveFrom(context),
                    ),
                  ),
                )
              : LayoutBuilder(
                  builder: (BuildContext context, BoxConstraints constraints) {
                    const int crossAxisCount = 2;
                    const double spacing = 12;
                    const double runSpacing = 14;
                    const double horizontalPad = 16;
                    final double maxW = constraints.maxWidth;
                    final double innerW = maxW - horizontalPad * 2;
                    final double cellW =
                        (innerW - spacing * (crossAxisCount - 1)) /
                            crossAxisCount;

                    const double cardPadding = 14;
                    final double emojiFont = math.min(
                      58,
                      math.max(36, cellW * 0.42),
                    );
                    const double gapAfterEmoji = 10;
                    const double textBlock = 48;
                    final double cardH = cardPadding +
                        emojiFont +
                        gapAfterEmoji +
                        textBlock +
                        cardPadding;

                    return ScrollConfiguration(
                      behavior: const _KLeagueGridScrollBehavior(),
                      child: Scrollbar(
                        controller: _gridScrollController,
                        thumbVisibility: true,
                        trackVisibility: true,
                        interactive: true,
                        thickness: 8,
                        radius: const Radius.circular(8),
                        child: Padding(
                          padding: const EdgeInsets.only(
                            left: horizontalPad,
                            right: 2,
                          ),
                          child: GridView.builder(
                            controller: _gridScrollController,
                            padding: const EdgeInsets.only(
                              bottom: 12,
                              right: 4,
                            ),
                            physics: const ClampingScrollPhysics(),
                            gridDelegate:
                                SliverGridDelegateWithFixedCrossAxisCount(
                              crossAxisCount: crossAxisCount,
                              mainAxisSpacing: runSpacing,
                              crossAxisSpacing: spacing,
                              childAspectRatio: cellW / cardH,
                            ),
                            itemCount: teams.length,
                            itemBuilder: (BuildContext context, int index) {
                              return SoccerTeamCard(
                                team: teams[index],
                                emojiFontSize: emojiFont,
                              );
                            },
                          ),
                        ),
                      ),
                    );
                  },
                ),
        ),
      ],
    );
  }
}

class _SearchPillField extends StatelessWidget {
  const _SearchPillField({
    required this.controller,
    required this.placeholder,
    required this.onChanged,
  });

  final TextEditingController controller;
  final String placeholder;
  final ValueChanged<String> onChanged;

  @override
  Widget build(BuildContext context) {
    final Color bg = CupertinoColors.systemGrey6.resolveFrom(context);
    return DecoratedBox(
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(22),
      ),
      child: Row(
        children: [
          Padding(
            padding: const EdgeInsets.only(left: 12),
            child: Icon(
              CupertinoIcons.search,
              size: 20,
              color: CupertinoColors.systemGrey.resolveFrom(context),
            ),
          ),
          Expanded(
            child: CupertinoTextField(
              controller: controller,
              onChanged: onChanged,
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 11),
              placeholder: placeholder,
              placeholderStyle: TextStyle(
                color: CupertinoColors.placeholderText.resolveFrom(context),
                fontSize: 15,
              ),
              style: TextStyle(
                color: CupertinoColors.label.resolveFrom(context),
                fontSize: 15,
              ),
              decoration: const BoxDecoration(),
              clearButtonMode: OverlayVisibilityMode.editing,
            ),
          ),
        ],
      ),
    );
  }
}

/// 흰 둥근 카드 — 큰 이모지 + 연고·클럽명 (광역시 샘플과 동일한 정보 구조).
class SoccerTeamCard extends StatelessWidget {
  const SoccerTeamCard({
    super.key,
    required this.team,
    required this.emojiFontSize,
  });

  final KLeagueRegisteredTeam team;
  final double emojiFontSize;

  @override
  Widget build(BuildContext context) {
    // CupertinoButton은 세로 드래그와 제스처 경쟁으로 그리드 스크롤을 방해할 수 있음.
    return MouseRegion(
      cursor: SystemMouseCursors.click,
      child: GestureDetector(
        behavior: HitTestBehavior.translucent,
        onTap: () => _openTeam(context, team),
        child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 10),
        decoration: BoxDecoration(
          color: CupertinoColors.white,
          borderRadius: BorderRadius.circular(20),
          boxShadow: <BoxShadow>[
            BoxShadow(
              color: const Color(0xFF8FA8C8).withValues(alpha: 0.14),
              blurRadius: 14,
              offset: const Offset(0, 4),
            ),
            BoxShadow(
              color: CupertinoColors.black.withValues(alpha: 0.04),
              blurRadius: 4,
              offset: const Offset(0, 1),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              team.emoji,
              style: TextStyle(fontSize: emojiFontSize, height: 1.05),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            Text(
              team.regionName,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 17,
                fontWeight: FontWeight.w800,
                color: CupertinoColors.black,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              team.teamName,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w500,
                color: CupertinoColors.secondaryLabel.resolveFrom(context),
              ),
            ),
          ],
        ),
        ),
      ),
    );
  }
}

/// 웹·데스크톱에서 마우스·트랙패드로 스크롤·스크롤바 드래그가 동작하도록 한다.
class _KLeagueGridScrollBehavior extends MaterialScrollBehavior {
  const _KLeagueGridScrollBehavior();

  @override
  Set<PointerDeviceKind> get dragDevices => <PointerDeviceKind>{
        PointerDeviceKind.touch,
        PointerDeviceKind.mouse,
        PointerDeviceKind.trackpad,
        PointerDeviceKind.stylus,
      };
}

void _openTeam(BuildContext context, KLeagueRegisteredTeam team) {
  if (team.teamCode == 'K09') {
    context.push(SoccerRoutePaths.seoulDetail);
    return;
  }
  _showTeamDetail(context, team);
}

void _showTeamDetail(BuildContext context, KLeagueRegisteredTeam team) {
  showCupertinoDialog<void>(
    context: context,
    builder: (BuildContext context) => CupertinoAlertDialog(
      title: Text('${team.regionName} · ${team.teamName}'),
      content: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            const SizedBox(height: 8),
            _DetailRow(label: '코드', value: team.teamCode),
            _DetailRow(label: '창단', value: '${team.origYyyy}년'),
            _DetailRow(label: '영문', value: team.eTeamName.trim()),
            _DetailRow(label: '홈페이지', value: team.homepage),
          ],
        ),
      ),
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

class _DetailRow extends StatelessWidget {
  const _DetailRow({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: RichText(
        text: TextSpan(
          style: TextStyle(
            fontSize: 13,
            color: CupertinoColors.label.resolveFrom(context),
            height: 1.25,
          ),
          children: [
            TextSpan(
              text: '$label · ',
              style: TextStyle(
                color: CupertinoColors.secondaryLabel.resolveFrom(context),
              ),
            ),
            TextSpan(text: value),
          ],
        ),
      ),
    );
  }
}
