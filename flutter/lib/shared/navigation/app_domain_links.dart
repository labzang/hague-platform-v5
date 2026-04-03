/// 앱 전역 사이드 메뉴에 쓰는 도메인 진입점 (게스트 메뉴와 동일 소스).
typedef AppDomainLink = ({String label, String path});

/// [guest_page] 및 [AppSideMenuPanel]에서 공유합니다.
const List<AppDomainLink> kAppDomainLinks = <AppDomainLink>[
  (label: '채팅', path: '/home/chat'),
  (label: '상품 리뷰 감성 분석', path: '/home/sentiment'),
  (label: '축구 승패 예측', path: '/home/soccer'),
  (label: '지오코딩', path: '/home/geospatial'),
  (label: '캐글', path: '/home/kaggle'),
  (label: '워드클라우드', path: '/home/wordcloud'),
  (label: '크롤링', path: '/home/crawler'),
];

/// 현재 라우트가 해당 링크(또는 그 하위 경로)인지 — 예: `/home/kaggle/titanic` → Kaggle 링크 선택.
bool appDomainLinkMatches(String location, String linkPath) {
  if (location == linkPath) return true;
  return location.startsWith('$linkPath/');
}
