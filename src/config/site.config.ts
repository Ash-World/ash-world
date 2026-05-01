// ─── 사이트 전체 문구 및 이미지 설정 ───────────────────────────────────────
// 문구나 배경 이미지를 변경할 때 이 파일만 수정하면 전체에 반영됩니다.

export const SITE = {
  // 기본 정보
  title: 'Ash-World',
  description: '개발과 기술에 관한 이야기',
  author: 'ash-hun',
  url: 'https://ash-hun.github.io/ash-world',

  // 홈 히어로 섹션
  hero: {
    greeting: 'Hello,',
    name: 'Ash',
    subtitle: "What you want to today?",
    // public/images/backgrounds/ 경로 기준 (비우면 CSS 그라데이션 사용)
    backgroundImage: '/ash-world/images/backgrounds/hero-bg.jpg',
    // 이미지 교체 시 핵심 피사체 위치에 맞게 조정 (CSS background-position 값)
    // 예: 'center center', 'center top', '70% 60%'
    backgroundPosition: 'center 65%',
    backgroundFallbackColor: '#0a0a0f',
  },

  // 카테고리 태그 (홈 + 필터에 사용)
  categories: [
    'All',
    'AI',
    'LLM',
    'RAG',
    'Agent',
    'Harness',
  ],

  // 홈 페이지 섹션 문구
  home: {
    latestPostsTitle: 'Latest Posts',
    latestPostsCount: 6,
    practiceToolsTitle: 'Quick Links',
  },

  // 네비게이션
  nav: {
    links: [
      { label: 'Home', href: '/ash-world/' },
      { label: 'Posts', href: '/ash-world/posts' },
      { label: 'About', href: '/ash-world/about' },
    ],
  },

  // About 페이지
  about: {
    title: 'About Me',
    bio: '백엔드와 AI 시스템을 좋아하는 개발자입니다. 배운 것을 기록하고 공유합니다.',
    avatarImage: 'https://github.com/ash-hun.png',
    links: [
      { label: 'GitHub', href: 'https://github.com/ash-hun' },
      { label: 'LinkedIn', href: 'https://www.linkedin.com/in/choijaehun/' },
    ],
  },

  // 푸터
  footer: {
    copyright: `© ${new Date().getFullYear()} ash-hun. All rights reserved.`,
  },
} as const;
