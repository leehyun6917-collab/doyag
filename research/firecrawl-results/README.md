# Firecrawl 조사 자료

REFERENCE.md에 등록된 경쟁사 URL을 Firecrawl(map/scrape)로 수집한 원시 조사 자료를 **경쟁사별 폴더**로 정리한 것이다. `.claude/reference/SITE_ANALYSIS.md`가 "구조 패턴 요약 + 자사 적용 제안"이라면, 이 폴더는 그 근거가 된 **원자료(제목/헤딩/CTA 문구/링크 등)를 사이트별로 상세 정리**한 것이다.

## 수집 범위

| 폴더 | 경쟁사 | 페이지 |
|---|---|---|
| `01-miliconnect/` | 대한민국청춘진흥원 | `main-page.md`(메인), `soldier-counseling.md`(군인상담실), `job-busking.md`(채용버스킹) |
| `02-yedi/` | 청년취업진흥교육원 (yedi.kr) | `main.md` (메인 + 상담후기 페이지 구조 포함) |
| `03-jobdesign/` | 청년취업컨설팅센터 (jobdesign.kr) | `home.md` |

`seongo.kr` 전체 map 결과에는 `01-miliconnect` 외에 에이전시 자체 소개/포트폴리오 페이지가 다수 존재하나 REFERENCE.md 대상이 아니므로 제외했다. `yedi.kr`은 `center-intro.html`, `military-tips.html`, `youth-employment-column.html` 등 정보성 서브페이지도 보유하고 있으나, 이번 조사는 메인 페이지와 상담후기 구조까지만 확인했다.

## 경쟁사 간 눈에 띄는 차이 (다음 SITE_ANALYSIS/SITE_PLAN 갱신 시 참고)

- **후기 유무**: yedi.kr만 실제 후기(카카오톡 캡처 + 통계 배지 + 필터)를 운영. miliconnect·jobdesign은 후기 섹션 자체가 없음.
- **가격 노출**: jobdesign.kr만 가격을 정면에 노출(1회 3만원/2회 5만원, 최저가보장제). 나머지 2곳은 "문의 시 안내"로 비공개.
- **자가진단 인터랙션**: miliconnect·yedi 2곳 모두 자가진단형 위젯 보유(진입 방식만 다름: 2단계 vs 4단계). jobdesign은 인터랙션 요소 없음.
- **서류 신뢰 보강**: yedi.kr이 유일하게 실제 서류 샘플 이미지 + "진위확인 QR코드" 언급으로 신뢰를 시각화.
- **프로그램 구조화**: yedi.kr만 1일/2일 프로그램을 tier 카드로 비교 제시(추천대상/제공문서 등 항목화).
- **환불 정책 공개**: jobdesign.kr만 환불 규정을 FAQ에 명시.

## 주의사항 (CLAUDE.md 원칙)

- 헤딩(H1~H3)과 CTA 버튼 문구는 구조 분석 목적상 원문 그대로 기록했다. **실제 자사 홈페이지 구현 시 반드시 새 문구로 교체**해야 하며 그대로 옮기지 않는다.
- 본문은 문장 단위 전문 복사가 아닌 섹션별 요약으로 정리했다.
- 로고 이미지, 실제 후기 원문(작성자/내용/스크린샷), 개인정보(전화번호·주소·사업자번호)는 이 자료에도 옮기지 않았다. 후기는 "구조"만 기록했다.

## 수집 방법

- `firecrawl map`으로 각 도메인 전체 URL 구조 확인
- 대상 URL을 `firecrawl scrape --format markdown,links --only-main-content`로 스크랩 (JS 렌더링이 필요한 jobdesign.kr은 `--wait-for 4000` 추가 적용)
