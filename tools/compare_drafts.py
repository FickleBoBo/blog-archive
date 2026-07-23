#!/usr/bin/env python3
"""Compare _drafts/<platform> (template from /ps) vs _drafts/last (manual).

baekjoon 파일은 /ps 스킬이 생성한 정본 템플릿이고,
last 파일은 사용자가 직접 작성한 포스팅이라 실수가 있을 수 있다.

검증 항목 (일치해야 함):
  - frontmatter (title, slug, date, categories, toc, math)
  - 문제 링크
  - 코드 블록 내용
  - 섹션 구조 (헤더 순서)

기대되는 차이 (사람이 작성하는 부분):
  - 아이디어 섹션 본문
  - 코드 블록 사이/뒤 설명 텍스트
  - 리뷰 섹션 본문
  - tags (last가 Unlinked가 아닐 수 있음)

Usage:
    python3 tools/compare_drafts.py              # _drafts/ 전체
    python3 tools/compare_drafts.py 1000 2161     # 특정 번호만
"""

import re
import sys
from pathlib import Path
from config import DRAFTS_DIR


def parse_post(path):
    """Parse a post into structured components."""
    text = path.read_text(encoding="utf-8")
    result = {
        "frontmatter": {},
        "problem_link": None,
        "code_blocks": [],
        "section_headers": [],
    }

    # Parse frontmatter
    if not text.startswith("---"):
        return result
    end = text.find("\n---", 3)
    if end == -1:
        return result
    fm_text = text[3:end].strip()
    for line in fm_text.splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            result["frontmatter"][m.group(1)] = m.group(2).strip()

    body = text[end + 4 :]

    # Extract problem link
    m = re.search(r"\[문제 링크\]\((https?://[^\)]+)\)", body)
    if m:
        result["problem_link"] = m.group(1)

    # Extract section headers
    for m in re.finditer(r"^(#{2,3}\s+.+)$", body, re.MULTILINE):
        result["section_headers"].append(m.group(1).strip())

    # Extract code blocks (language + content)
    for m in re.finditer(r"```(\w+)\n(.*?)```", body, re.DOTALL):
        result["code_blocks"].append((m.group(1), m.group(2).strip()))

    return result


def compare_pair(template_path, manual_path):
    """Compare template (baekjoon) vs manual (last) file.

    Returns list of issue strings. Empty = all OK.
    """
    issues = []
    t = parse_post(template_path)
    m = parse_post(manual_path)

    # Frontmatter (skip tags — expected to differ)
    check_keys = ["title", "slug", "date", "categories", "toc", "math"]
    for key in check_keys:
        tv = t["frontmatter"].get(key, "")
        mv = m["frontmatter"].get(key, "")
        if tv != mv:
            issues.append(f"frontmatter.{key}: template={tv!r} last={mv!r}")

    # Problem link
    if t["problem_link"] != m["problem_link"]:
        issues.append(
            f"문제 링크: template={t['problem_link']} last={m['problem_link']}"
        )

    # Section headers
    if t["section_headers"] != m["section_headers"]:
        t_only = set(t["section_headers"]) - set(m["section_headers"])
        m_only = set(m["section_headers"]) - set(t["section_headers"])
        detail = []
        if t_only:
            detail.append(f"template에만: {t_only}")
        if m_only:
            detail.append(f"last에만: {m_only}")
        if not detail:
            detail.append("순서 다름")
        issues.append(f"섹션 구조: {'; '.join(detail)}")

    # Code blocks
    if len(t["code_blocks"]) != len(m["code_blocks"]):
        issues.append(
            f"코드 블록 수: template={len(t['code_blocks'])} last={len(m['code_blocks'])}"
        )
    else:
        for i, (tb, mb) in enumerate(zip(t["code_blocks"], m["code_blocks"])):
            t_lang, t_code = tb
            m_lang, m_code = mb
            if t_lang != m_lang:
                issues.append(f"코드 블록 #{i+1} 언어: template={t_lang} last={m_lang}")
            if t_code != m_code:
                # Show first difference line
                t_lines = t_code.splitlines()
                m_lines = m_code.splitlines()
                diff_line = None
                for j, (tl, ml) in enumerate(zip(t_lines, m_lines)):
                    if tl != ml:
                        diff_line = j + 1
                        break
                if diff_line is None and len(t_lines) != len(m_lines):
                    diff_line = min(len(t_lines), len(m_lines)) + 1
                issues.append(
                    f"코드 블록 #{i+1} [{t_lang}] 내용 불일치 (line {diff_line})"
                )

    return issues


def main():
    numbers = set()
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            numbers.add(arg.strip())

    # Collect platform subdirs in _drafts (excluding last, tmp, made)
    skip_dirs = {"last", "tmp", "made"}
    platform_dirs = [
        d
        for d in DRAFTS_DIR.iterdir()
        if d.is_dir() and d.name not in skip_dirs
    ]

    last_dir = DRAFTS_DIR / "last"
    if not last_dir.exists():
        print("_drafts/last/ 없음")
        return

    total = 0
    matched = 0
    ok = 0
    issues_found = 0

    for pdir in sorted(platform_dirs):
        for template_path in sorted(pdir.glob("*.md")):
            base = template_path.name
            manual_path = last_dir / base

            # Filter by number if specified
            if numbers:
                m = re.search(r"(\d+)", base)
                if not m or m.group(1) not in numbers:
                    continue

            if not manual_path.exists():
                continue

            total += 1
            matched += 1
            issues = compare_pair(template_path, manual_path)

            if issues:
                issues_found += 1
                print(f"  ❌ {base}")
                for issue in issues:
                    print(f"     {issue}")
            else:
                ok += 1
                print(f"  ✅ {base}")

    print(f"\n완료. {matched}개 비교, {ok}개 OK, {issues_found}개 불일치")


if __name__ == "__main__":
    main()
