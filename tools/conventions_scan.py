#!/usr/bin/env python3
"""포스트 코드 블록을 스캔하여 코드 관례를 추출한다."""

import re
from collections import Counter
from pathlib import Path

from config import POSTS_DIR

CONVENTIONS_PATH = Path(__file__).parent / "conventions.md"
MIN_CONFIRMED = 3
MIN_CANDIDATE = 2

# ── 패턴 정의 ──
# (이름, 정규식) — 포스트당 1회 카운트

VAR_PATTERNS = {
    "방문 배열": [("vis", r"\bvis\b"), ("visited", r"\bvisited\b")],
    "상수": [("INF", r"\bINF\b"), ("MAX", r"\bMAX\b"), ("MX", r"\bMX\b")],
    "인접 리스트": [("adj", r"\badj\b"), ("graph", r"\bgraph\b")],
    "방향 배열": [("dx/dy", r"\bdx\b"), ("dr/dc", r"\bdr\b")],
    "DP 배열": [("dp", r"\bdp\b"), ("memo", r"\bmemo\b")],
    "결과 변수": [("ans", r"\bans\b"), ("res", r"\bres\b"), ("result", r"\bresult\b")],
    "카운트 변수": [("cnt", r"\bcnt\b")],
    "투 포인터": [
        ("left/right", r"(?s)(?=.*\bleft\b)(?=.*\bright\b)"),
        ("lo/hi", r"(?s)(?=.*\blo\b)(?=.*\bhi\b)"),
    ],
}

FUNC_PATTERNS = {
    "DFS": [("dfs", r"\bdfs\b")],
    "BFS": [("bfs", r"\bbfs\b")],
    "유클리드 호제법": [("gcd", r"\bgcd\b")],
    "거듭제곱": [("modPow", r"\bmod[Pp]ow\b"), ("power", r"\bpower\b")],
    "에라토스테네스": [("sieve", r"\bsieve\b")],
}

JAVA_STYLE = {
    "I/O": [("BufferedReader", r"BufferedReader"), ("Scanner", r"new Scanner")],
    "출력": [("StringBuilder", r"StringBuilder"), ("System.out", r"System\.out\.print")],
}

CPP_STYLE = {
    "헤더": [("bits/stdc++.h", r"bits/stdc\+\+\.h"), ("개별 헤더", r"#include\s*<(?!bits/stdc)")],
    "I/O 최적화": [("sync_with_stdio", r"ios(?:_base)?::sync_with_stdio")],
    "네임스페이스": [("using namespace std", r"using namespace std")],
}


def extract_code_blocks(content):
    return [
        (m.group(1), m.group(2))
        for m in re.finditer(r"```(java|c\+\+|python)\n(.*?)\n```", content, re.DOTALL)
    ]


def count_patterns(posts, patterns, lang_filter=None):
    results = {}
    for category, items in patterns.items():
        counter = Counter()
        for post in posts:
            content = post.read_text(encoding="utf-8")
            blocks = extract_code_blocks(content)
            if lang_filter:
                blocks = [(l, c) for l, c in blocks if l == lang_filter]
            if not blocks:
                continue
            combined = "\n".join(c for _, c in blocks)
            for name, regex in items:
                if re.search(regex, combined):
                    counter[name] += 1
        results[category] = counter
    return results


def format_section(title, results, patterns):
    lines = [f"## {title}", ""]
    has_content = False
    for category in patterns:
        counter = results[category]
        if not counter:
            continue
        items = counter.most_common()
        confirmed = [(n, c) for n, c in items if c >= MIN_CONFIRMED]
        candidates = [(n, c) for n, c in items if MIN_CANDIDATE <= c < MIN_CONFIRMED]
        if not confirmed and not candidates:
            continue
        has_content = True
        if confirmed:
            parts = [f"`{n}` ({c})" for n, c in confirmed]
            lines.append(f"- **{category}**: {' / '.join(parts)}")
        if candidates:
            cand = ", ".join(f"`{n}` ({c})" for n, c in candidates)
            lines.append(f"- **{category}** [후보]: {cand}")
    if not has_content:
        lines.append("(패턴 없음)")
    return "\n".join(lines)


def main():
    posts = sorted(
        [p for p in POSTS_DIR.rglob("*.md") if p.parent != POSTS_DIR],
        reverse=True,
    )
    if not posts:
        print("대상 포스트 없음.")
        return

    print(f"스캔 대상: {len(posts)}개 포스트\n")

    var_results = count_patterns(posts, VAR_PATTERNS)
    func_results = count_patterns(posts, FUNC_PATTERNS)
    java_results = count_patterns(posts, JAVA_STYLE, lang_filter="java")
    cpp_results = count_patterns(posts, CPP_STYLE, lang_filter="c++")

    confirmed = sum(
        1 for results in [var_results, func_results, java_results, cpp_results]
        for counter in results.values()
        for _, c in counter.items() if c >= MIN_CONFIRMED
    )
    candidates = sum(
        1 for results in [var_results, func_results, java_results, cpp_results]
        for counter in results.values()
        for _, c in counter.items() if MIN_CANDIDATE <= c < MIN_CONFIRMED
    )

    content = "\n".join([
        "# PS 코드 관례 레퍼런스",
        "",
        "이 파일은 블로그 포스팅의 코드 일관성 검수에 사용된다.",
        f"스캔 대상: {len(posts)}개 포스트 / 관례 확정: {MIN_CONFIRMED}회 이상, 후보: {MIN_CANDIDATE}회",
        "",
        "---",
        "",
        format_section("변수명/상수명", var_results, VAR_PATTERNS),
        "",
        "---",
        "",
        format_section("함수명", func_results, FUNC_PATTERNS),
        "",
        "---",
        "",
        format_section("Java 코드 스타일", java_results, JAVA_STYLE),
        "",
        "---",
        "",
        format_section("C++ 코드 스타일", cpp_results, CPP_STYLE),
        "",
        "---",
        "",
        "## 알고리즘 구현 패턴",
        "",
        "(수동 확인 필요 — 자동 스캔 범위 외)",
        "",
    ])

    CONVENTIONS_PATH.write_text(content, encoding="utf-8")

    print(f"확정된 관례: {confirmed}개")
    print(f"후보 (2회 등장): {candidates}개")
    print(f"\n갱신 완료: tools/{CONVENTIONS_PATH.name}")
    print(f"\n{'='*50}\n")
    print(content)


if __name__ == "__main__":
    main()
