#!/usr/bin/env python3
"""SEO 콘텐츠 감사 스크립트 (청춘 도약 일자리교육원 정적 사이트).

루트에 있는 모든 .html 페이지를 읽어서 title, meta description, canonical,
Open Graph 태그, H1/H2 구조, JSON-LD 구조화 데이터, 대략적인 본문 단어 수를
추출하고 기본적인 SEO 기준(길이, 중복, 누락) 위반 여부를 함께 표시합니다.

외부 라이브러리 없이 표준 라이브러리(html.parser)만 사용합니다.

사용법:
    python3 scripts/seo_audit.py                # 터미널에 표로 출력
    python3 scripts/seo_audit.py --md report.md # 마크다운 리포트도 함께 저장
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser

# SEO 권장 기준값 (Google 검색결과 노출 관행 기준의 대략적인 가이드라인)
TITLE_MAX = 60
DESC_MIN = 70
DESC_MAX = 160
THIN_CONTENT_WORDS = 300


@dataclass
class PageSEO:
    path: str
    title: str = ""
    description: str = ""
    canonical: str = ""
    og: dict = field(default_factory=dict)
    h1: list = field(default_factory=list)
    h2: list = field(default_factory=list)
    json_ld: list = field(default_factory=list)
    word_count: int = 0


class SEOParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.page = PageSEO(path="")
        self._tag_stack: list[str] = []
        self._capture_for: str | None = None
        self._buffer: list[str] = []
        self._in_jsonld = False
        self._jsonld_buffer: list[str] = []
        self._visible_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "title":
            self._capture_for = "title"
            self._buffer = []
        elif tag == "meta":
            name = (attrs_d.get("name") or "").lower()
            prop = (attrs_d.get("property") or "").lower()
            if name == "description":
                self.page.description = attrs_d.get("content", "")
            elif prop.startswith("og:"):
                self.page.og[prop] = attrs_d.get("content", "")
        elif tag == "link" and attrs_d.get("rel") == "canonical":
            self.page.canonical = attrs_d.get("href", "")
        elif tag in ("h1", "h2"):
            self._capture_for = tag
            self._buffer = []
        elif tag == "script" and attrs_d.get("type") == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_buffer = []
        self._tag_stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "title" and self._capture_for == "title":
            self.page.title = re.sub(r"\s+", " ", "".join(self._buffer)).strip()
            self._capture_for = None
        elif tag in ("h1", "h2") and self._capture_for == tag:
            text = re.sub(r"\s+", " ", "".join(self._buffer)).strip()
            getattr(self.page, tag).append(text)
            self._capture_for = None
        elif tag == "script" and self._in_jsonld:
            raw = "".join(self._jsonld_buffer)
            try:
                self.page.json_ld.append(json.loads(raw))
            except json.JSONDecodeError:
                self.page.json_ld.append({"@type": "(파싱 오류)"})
            self._in_jsonld = False
        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()

    def handle_data(self, data):
        if self._in_jsonld:
            self._jsonld_buffer.append(data)
            return
        if self._capture_for:
            self._buffer.append(data)
        if self._tag_stack and self._tag_stack[-1] in ("script", "style"):
            return
        stripped = data.strip()
        if stripped:
            self._visible_text.append(stripped)


def analyze(path: str) -> PageSEO:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    parser = SEOParser()
    parser.page.path = os.path.basename(path)
    parser.feed(content)
    text = " ".join(parser._visible_text)
    parser.page.word_count = len(re.findall(r"[\w가-힣]+", text))
    return parser.page


def summarize_json_ld(entries: list[dict]) -> list[str]:
    out = []
    for entry in entries:
        t = entry.get("@type", "?")
        if t == "FAQPage":
            out.append(f"FAQPage({len(entry.get('mainEntity', []))}문항)")
        elif t == "Article":
            out.append(f"Article:{entry.get('headline', '')[:30]}")
        else:
            out.append(str(t))
    return out


def check_issues(p: PageSEO) -> list[str]:
    issues = []
    if not p.title:
        issues.append("title 없음")
    elif len(p.title) > TITLE_MAX:
        issues.append(f"title {len(p.title)}자 (권장 ≤{TITLE_MAX})")

    if not p.description:
        issues.append("meta description 없음")
    elif not (DESC_MIN <= len(p.description) <= DESC_MAX):
        issues.append(f"description {len(p.description)}자 (권장 {DESC_MIN}~{DESC_MAX})")

    if len(p.h1) == 0:
        issues.append("H1 없음")
    elif len(p.h1) > 1:
        issues.append(f"H1 {len(p.h1)}개 (1개 권장)")

    if not p.canonical:
        issues.append("canonical 없음")
    elif "example.com" in p.canonical:
        issues.append("canonical이 example.com placeholder 상태")

    if p.word_count < THIN_CONTENT_WORDS:
        issues.append(f"본문 {p.word_count}단어 (얇은 콘텐츠 우려, 권장 ≥{THIN_CONTENT_WORDS})")

    return issues


def main() -> None:
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("--md", help="마크다운 리포트를 저장할 경로")
    args = arg_parser.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(f for f in glob.glob(os.path.join(root, "*.html")) if os.path.isfile(f))

    pages = [analyze(f) for f in files]

    # 제목/설명 중복 체크 (서로 다른 페이지가 같은 값을 쓰면 SEO에 불리)
    title_counts: dict[str, list[str]] = {}
    desc_counts: dict[str, list[str]] = {}
    for p in pages:
        title_counts.setdefault(p.title, []).append(p.path)
        desc_counts.setdefault(p.description, []).append(p.path)

    print(f"검사 대상: {len(pages)}개 페이지\n")
    header = f"{'파일':28s} {'Title':>6s} {'Desc':>6s} {'H1':>3s} {'H2':>3s} {'단어수':>6s}  구조화데이터"
    print(header)
    print("-" * len(header))
    for p in pages:
        jsonld_summary = ", ".join(summarize_json_ld(p.json_ld)) or "-"
        print(
            f"{p.path:28s} {len(p.title):6d} {len(p.description):6d} "
            f"{len(p.h1):3d} {len(p.h2):3d} {p.word_count:6d}  {jsonld_summary}"
        )

    print("\n=== 페이지별 이슈 ===")
    any_issue = False
    for p in pages:
        issues = check_issues(p)
        if len(title_counts.get(p.title, [])) > 1:
            issues.append("title이 다른 페이지와 중복")
        if len(desc_counts.get(p.description, [])) > 1:
            issues.append("description이 다른 페이지와 중복")
        if issues:
            any_issue = True
            print(f"\n[{p.path}]")
            for i in issues:
                print(f"  - {i}")
    if not any_issue:
        print("발견된 이슈 없음")

    if args.md:
        write_markdown(args.md, pages, title_counts, desc_counts)
        print(f"\n마크다운 리포트 저장: {args.md}")


def write_markdown(md_path, pages, title_counts, desc_counts) -> None:
    lines = ["# SEO 콘텐츠 감사 리포트", "", f"검사 대상: {len(pages)}개 페이지", ""]
    for p in pages:
        jsonld_summary = ", ".join(summarize_json_ld(p.json_ld)) or "없음"
        issues = check_issues(p)
        if len(title_counts.get(p.title, [])) > 1:
            issues.append("title이 다른 페이지와 중복")
        if len(desc_counts.get(p.description, [])) > 1:
            issues.append("description이 다른 페이지와 중복")

        lines.append(f"## {p.path}")
        lines.append("")
        lines.append(f"- **Title** ({len(p.title)}자): {p.title}")
        lines.append(f"- **Meta description** ({len(p.description)}자): {p.description}")
        lines.append(f"- **Canonical**: {p.canonical or '(없음)'}")
        for k, v in p.og.items():
            lines.append(f"- **{k}**: {v}")
        lines.append(f"- **H1**: {' / '.join(p.h1) or '(없음)'}")
        lines.append(f"- **H2** ({len(p.h2)}개): {' | '.join(p.h2) or '(없음)'}")
        lines.append(f"- **구조화 데이터(JSON-LD)**: {jsonld_summary}")
        lines.append(f"- **본문 단어 수(대략)**: {p.word_count}")
        if issues:
            lines.append("- **이슈**:")
            for i in issues:
                lines.append(f"  - {i}")
        else:
            lines.append("- **이슈**: 없음")
        lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
