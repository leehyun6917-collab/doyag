# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status

This repository is currently empty aside from a README. There is no source code, build tooling, package manifest, or test suite yet. Once code is added, update this file with actual build/lint/test commands and an architecture overview.


# 프로젝트 목표

이 프로젝트는 참고 사이트의 디자인 원리와 정보 구조를 분석하여 자사 홈페이지를 새롭게 구현하는 프로젝트다.

# 기본 원칙

- 참고 사이트의 로고, 상호명, 본문, 후기, 이미지, 영상, 아이콘을 그대로 복사하지 않는다.
- 레이아웃, 배치, 여백, 색상 사용 방식, 타이포그래피 체계만 참고한다.
- 실제 콘텐츠는 자사 브랜드와 서비스 내용으로 작성한다.
- 기존에 정상 작동하는 기능은 임의로 제거하지 않는다.
- 작업 전에 현재 프로젝트 구조와 기존 코드를 먼저 분석한다.
- 대규모 변경 전에는 반드시 구현 계획을 먼저 제시한다.
- 승인받지 않은 페이지나 기능으로 작업 범위를 확대하지 않는다.

# 작업 순서

1. reference 폴더의 자료를 확인한다.
2. 참고 사이트의 페이지와 섹션 구조를 분석한다.
3. IMPLEMENTATION_PLAN.md를 기준으로 작업한다.
4. 공통 디자인 시스템을 먼저 구현한다.
5. 헤더와 히어로 영역부터 구현한다.
6. 한 번에 최대 1~2개 섹션만 수정한다.
7. 각 단계가 끝날 때 실제 브라우저에서 확인한다.
8. 모바일 화면을 별도로 검수한다.
9. 변경 내용을 보고한 후 다음 단계로 진행한다.

# 반응형 기준

- 모바일: 390px
- 태블릿: 768px
- 노트북: 1024px
- 데스크톱: 1440px

# 디자인 규칙

- 색상과 폰트는 reference/brand.json과 docs/DESIGN_SYSTEM.md를 기준으로 한다.
- px 값을 무작정 고정하지 말고 반응형 구조를 사용한다.
- 모바일에서 가로 스크롤이 발생하지 않아야 한다.
- 이미지는 원래 비율을 유지한다.
- 제목의 과도한 줄바꿈을 방지한다.
- 애니메이션은 최소화하고 접근성을 우선한다.

# 검수 규칙

- 구현 후 실제 브라우저에서 페이지를 실행한다.
- 390px, 768px, 1024px, 1440px 화면을 확인한다.
- 콘솔 오류를 확인한다.
- 깨진 링크와 이미지가 없는지 확인한다.
- 모바일 메뉴, 버튼, FAQ 등 상호작용을 확인한다.
- 기존 기능이 유지되는지 확인한다.
- 검수하지 않은 상태에서 완료됐다고 보고하지 않는다.

# Git 규칙

- 작업 전 git status를 확인한다.
- 사용자의 요청 없이 force push를 하지 않는다.
- 사용자의 요청 없이 기존 브랜치를 삭제하지 않는다.
- 대규모 수정 전에는 현재 상태를 커밋하도록 안내한다.