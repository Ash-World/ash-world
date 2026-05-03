<div align="center">

# Ash-World

**개발과 기술에 관한 이야기**

[![Astro](https://img.shields.io/badge/Astro-5.0-FF5D01?style=flat-square&logo=astro&logoColor=white)](https://astro.build)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![MDX](https://img.shields.io/badge/MDX-Content-1B1F24?style=flat-square&logo=mdx&logoColor=white)](https://mdxjs.com)
[![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Deployed-222222?style=flat-square&logo=github&logoColor=white)](https://ash-hun.github.io/ash-world)

[🔗 블로그 방문하기](https://ash-hun.github.io/ash-world)

</div>

---

## ✨ 소개

AI Researcher로서 배우고 탐구한 것들을 기록하는 개인 기술 블로그입니다.  
RAG, Agent, LLM 등 AI/ML 분야의 Research 아티클과 컨퍼런스 후기를 주로 다룹니다.

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| **프레임워크** | [Astro 5](https://astro.build) — 정적 사이트 생성 |
| **스타일링** | [Tailwind CSS 3](https://tailwindcss.com) + [@tailwindcss/typography](https://tailwindcss.com/docs/typography-plugin) |
| **콘텐츠** | [MDX](https://mdxjs.com) — 마크다운 + JSX |
| **검색** | [Fuse.js](https://www.fusejs.io) — 퍼지 검색 |
| **UI 컴포넌트** | [React 18](https://react.dev) (Islands Architecture) |
| **배포** | [GitHub Pages](https://pages.github.com) + GitHub Actions |

---

## 📁 프로젝트 구조

```
ash-world/
├── public/
│   └── assets/              # 포스트 이미지
├── src/
│   ├── components/
│   │   ├── common/          # TagPill, SearchBox
│   │   ├── home/            # HeroSection, CategoryTags
│   │   ├── layout/          # BaseLayout, Header, Footer
│   │   └── post/            # PostCard
│   ├── config/
│   │   └── site.config.ts   # 사이트 전체 설정 (문구·링크 중앙 관리)
│   ├── content/
│   │   └── posts/           # MDX 블로그 포스트
│   ├── pages/
│   │   ├── index.astro      # 홈
│   │   ├── posts/           # 포스트 목록 · 상세
│   │   ├── tags/            # 태그별 목록
│   │   ├── search/          # 검색 페이지
│   │   └── about.astro      # 소개
│   └── styles/
│       └── global.css
├── astro.config.mjs
└── tailwind.config.mjs
```

---

## 🚀 로컬 실행

```bash
# 의존성 설치
npm install

# 개발 서버 실행 (http://localhost:4321)
npm run dev

# 프로덕션 빌드
npm run build

# 빌드 결과물 미리보기
npm run preview
```

---

## ✍️ 포스트 작성

`src/content/posts/` 에 `.mdx` 파일을 추가합니다.

```mdx
---
title: "포스트 제목"
description: "한 줄 요약"
publishDate: 2025-01-01
tags: ["Research", "LLM"]
draft: false
---

본문 내용...
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `title` | `string` | 포스트 제목 |
| `description` | `string` | 목록·메타에 표시되는 요약 |
| `publishDate` | `YYYY-MM-DD` | 발행일 |
| `tags` | `string[]` | 태그 목록 |
| `draft` | `boolean` | `true`면 빌드에서 제외 |
| `cover` | `string?` | 커버 이미지 경로 (선택) |

---

## 🔄 배포

`main` 브랜치에 Push하면 GitHub Actions가 자동으로 빌드 후 GitHub Pages에 배포합니다.

```
Push to main → GitHub Actions (astro build) → GitHub Pages
```

---

## 📝 주요 페이지

| 경로 | 설명 |
|------|------|
| `/ash-world/` | 홈 — 히어로 + 최신 포스트 |
| `/ash-world/posts` | 전체 포스트 목록 (연도·태그 필터) |
| `/ash-world/posts/:slug` | 포스트 상세 (이전/다음 네비게이션) |
| `/ash-world/tags/:tag` | 태그별 포스트 목록 |
| `/ash-world/search` | 전문 검색 (Fuse.js) |
| `/ash-world/about` | 소개 페이지 |

---

<div align="center">

© 2026 [ash-hun](https://github.com/ash-hun) · Built with [Astro](https://astro.build)

</div>
