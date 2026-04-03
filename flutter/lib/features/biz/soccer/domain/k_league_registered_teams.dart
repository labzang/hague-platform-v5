import 'package:flutter/cupertino.dart';

/// 백엔드 [teams.jsonl](labzang/apps/biz/soccer/team/domain/teams.jsonl)과 동일한 등록 구단.
class KLeagueRegisteredTeam {
  const KLeagueRegisteredTeam({
    required this.id,
    required this.teamCode,
    required this.teamName,
    required this.regionName,
    required this.eTeamName,
    required this.origYyyy,
    required this.homepage,
    required this.primary,
    required this.emoji,
    this.secondary,
  });

  final int id;
  final String teamCode;
  final String teamName;
  final String regionName;
  final String eTeamName;
  final String origYyyy;
  final String homepage;
  final Color primary;
  /// 카드 사각 아이콘 영역에 표시할 이모지(1글자 그래픽).
  final String emoji;
  final Color? secondary;

  /// 원형 버튼 중앙에 넣는 짧은 라벨 (연고지 2글자).
  String get monogram {
    if (regionName.length >= 2) {
      return regionName.substring(0, 2);
    }
    return teamName.length >= 2 ? teamName.substring(0, 2) : teamCode;
  }
}

/// 등록 순서는 jsonl 라인 순서와 동일.
const List<KLeagueRegisteredTeam> kKLeagueRegisteredTeams = <KLeagueRegisteredTeam>[
  KLeagueRegisteredTeam(
    id: 1000,
    teamCode: 'K05',
    regionName: '전북',
    teamName: '현대모터스',
    eTeamName: 'CHUNBUK  HYUNDAI MOTORS  FC',
    origYyyy: '1995',
    homepage: 'http://www.hyundai-motorsfc.com',
    primary: Color(0xFF007A33),
    emoji: '🌲',
    secondary: Color(0xFF005C28),
  ),
  KLeagueRegisteredTeam(
    id: 1001,
    teamCode: 'K08',
    regionName: '성남',
    teamName: '일화천마',
    eTeamName: 'SEONGNAM  ILHWA CHUNMA FC',
    origYyyy: '1988',
    homepage: 'http://www.esifc.com',
    primary: Color(0xFFE31B23),
    emoji: '✨',
    secondary: Color(0xFFB8141C),
  ),
  KLeagueRegisteredTeam(
    id: 1002,
    teamCode: 'K03',
    regionName: '포항',
    teamName: '스틸러스',
    eTeamName: 'FC POHANG  STEELERS',
    origYyyy: '1973',
    homepage: 'http://www.steelers.co.kr',
    primary: Color(0xFFE4002B),
    emoji: '⚙️',
    secondary: Color(0xFF1A1A1A),
  ),
  KLeagueRegisteredTeam(
    id: 1003,
    teamCode: 'K07',
    regionName: '전남',
    teamName: '드래곤즈',
    eTeamName: 'CHUNNAM  DRAGONS FC',
    origYyyy: '1994',
    homepage: 'http://www.dragons.co.kr',
    primary: Color(0xFF5B2D8C),
    emoji: '🐉',
    secondary: Color(0xFF3D1F5E),
  ),
  KLeagueRegisteredTeam(
    id: 1004,
    teamCode: 'K09',
    regionName: '서울',
    teamName: 'FC서울',
    eTeamName: 'FOOTBALL CLUB  SEOUL',
    origYyyy: '1983',
    homepage: 'http://www.fcseoul.com',
    primary: Color(0xFFE60012),
    emoji: '🏙️',
    secondary: Color(0xFF2B2B2B),
  ),
  KLeagueRegisteredTeam(
    id: 1005,
    teamCode: 'K04',
    regionName: '인천',
    teamName: '유나이티드',
    eTeamName: 'INCHEON  UNITED FC',
    origYyyy: '2004',
    homepage: 'http://www.incheonutd.com',
    primary: Color(0xFF003B7A),
    emoji: '⚓',
    secondary: Color(0xFFFFD200),
  ),
  KLeagueRegisteredTeam(
    id: 1006,
    teamCode: 'K11',
    regionName: '경남',
    teamName: '경남FC',
    eTeamName: 'GYEONGNAM  FC',
    origYyyy: '2006',
    homepage: 'http://www.gsndfc.co.kr',
    primary: Color(0xFFC8102E),
    emoji: '🌺',
    secondary: Color(0xFF1D1D1B),
  ),
  KLeagueRegisteredTeam(
    id: 1007,
    teamCode: 'K01',
    regionName: '울산',
    teamName: '울산현대',
    eTeamName: 'ULSAN HYUNDAI  FC',
    origYyyy: '1986',
    homepage: 'http://www.uhfc.tv',
    primary: Color(0xFFFF6B00),
    emoji: '🐯',
    secondary: Color(0xFF004B9B),
  ),
  KLeagueRegisteredTeam(
    id: 1008,
    teamCode: 'K10',
    regionName: '대전',
    teamName: '시티즌',
    eTeamName: 'DAEJEON CITIZEN  FC',
    origYyyy: '1996',
    homepage: 'http://www.dcfc.co.kr',
    primary: Color(0xFF0072CE),
    emoji: '🏛️',
    secondary: Color(0xFFE4002B),
  ),
  KLeagueRegisteredTeam(
    id: 1009,
    teamCode: 'K02',
    regionName: '수원',
    teamName: '삼성블루윙즈',
    eTeamName: 'SUWON  SAMSUNG BLUEWINGS  FC',
    origYyyy: '1995',
    homepage: 'http://www.bluewings.kr',
    primary: Color(0xFF0047AB),
    emoji: '🏯',
    secondary: Color(0xFFE31937),
  ),
  KLeagueRegisteredTeam(
    id: 1010,
    teamCode: 'K12',
    regionName: '광주',
    teamName: '광주상무',
    eTeamName: 'GWANGJU  SANGMU FC',
    origYyyy: '1984',
    homepage: 'http://www.gwangjusmfc.co.kr',
    primary: Color(0xFFFFD100),
    emoji: '☀️',
    secondary: Color(0xFF1E1E1E),
  ),
  KLeagueRegisteredTeam(
    id: 1011,
    teamCode: 'K06',
    regionName: '부산',
    teamName: '아이파크',
    eTeamName: 'BUSAN IPARK  FC',
    origYyyy: '1983',
    homepage: 'http://www.busanipark.co.kr',
    primary: Color(0xFFE60012),
    emoji: '🌊',
    secondary: Color(0xFF231F20),
  ),
  KLeagueRegisteredTeam(
    id: 1012,
    teamCode: 'K13',
    regionName: '강원',
    teamName: '강원FC',
    eTeamName: 'GANGWON  FC',
    origYyyy: '2008',
    homepage: 'http://www.gangwon-fc.com',
    primary: Color(0xFFFF6B35),
    emoji: '🏔️',
    secondary: Color(0xFF1F4C2D),
  ),
  KLeagueRegisteredTeam(
    id: 1013,
    teamCode: 'K14',
    regionName: '제주',
    teamName: '제주유나이티드FC',
    eTeamName: 'JEJU  UNITED FC',
    origYyyy: '1982',
    homepage: 'http://www.jeju-utd.com',
    primary: Color(0xFFFF8C00),
    emoji: '🍊',
    secondary: Color(0xFF00573F),
  ),
  KLeagueRegisteredTeam(
    id: 1014,
    teamCode: 'K15',
    regionName: '대구',
    teamName: '대구FC',
    eTeamName: 'DAEGU  FC',
    origYyyy: '2002',
    homepage: 'http://www.daegufc.co.kr',
    primary: Color(0xFF00A9E0),
    emoji: '🌹',
    secondary: Color(0xFF003087),
  ),
];
