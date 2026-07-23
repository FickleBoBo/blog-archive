#!/usr/bin/env python3
"""
Sync code blocks in posts with latest code from Algorithm directory.

Usage:
    python3 sync.py           # sync all drafts
    python3 sync.py 24265     # sync specific problem
"""

import difflib
import re
import sys
from pathlib import Path

from config import BLOG_DIR, ALGO_DIR
from code_utils import parse_filename, find_posts, read_codes


BLOCK_RE = re.compile(r"```(java|c\+\+|python)\n(.*?)\n```", re.DOTALL)


def sync_post(filepath, apply=False):
    parsed = parse_filename(filepath)
    if not parsed:
        print(f"  [SKIP] 파싱 실패: {filepath.name}")
        return False

    date_str, platform_ko, prefix, number, year_month, day = parsed
    algo_dir = ALGO_DIR / year_month / "src" / f"day_{day:02d}" / f"{prefix}_{number}"

    if not algo_dir.exists():
        print(f"  [SKIP] Algorithm 경로 없음: {algo_dir}")
        return False

    codes = read_codes(algo_dir)
    if not codes:
        print(f"  [SKIP] 코드 파일 없음: {algo_dir}")
        return False

    content = filepath.read_text(encoding="utf-8")
    original = content
    diffs = []

    # Positional matching: pair post code blocks with read_codes() results in order
    blocks = list(BLOCK_RE.finditer(content))
    if len(blocks) != len(codes):
        print(f"  [SKIP] 코드 블록 수 불일치: {filepath.name} — 포스트 {len(blocks)}개, Algorithm {len(codes)}개")
        return False

    # Build replacements in reverse order to preserve offsets
    replacements = []
    for block, (lang, new_code) in zip(blocks, codes):
        old_code = block.group(2)
        block_lang = block.group(1)
        if old_code != new_code:
            diff = difflib.unified_diff(
                old_code.splitlines(keepends=True),
                new_code.splitlines(keepends=True),
                fromfile="포스트",
                tofile="Algorithm",
            )
            diffs.append((block_lang, "".join(diff)))
            replacements.append((block.start(), block.end(),
                                 f"```{block_lang}\n{new_code}\n```"))

    for start, end, new_text in reversed(replacements):
        content = content[:start] + new_text + content[end:]

    if content == original:
        return False

    if diffs:
        langs = ", ".join(d[0] for d in diffs)
        print(f"\n  [DIFF] {filepath.name} ({langs})")
        for _, diff_text in diffs:
            print(diff_text)

    if apply:
        filepath.write_text(content, encoding="utf-8")
        print(f"  [SYNCED] {filepath.name}")
        return True
    else:
        print(f"  [PENDING] 적용하려면 --apply 플래그를 추가하세요.")
        return False


def main():
    apply = "--apply" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--apply"]
    number = args[0] if args else None

    if number:
        print(f"문제 {number}번 코드 동기화\n")
    else:
        print("_drafts/ 전체 코드 동기화\n")

    posts = find_posts(number)
    if not posts:
        print("대상 포스트 없음.")
        sys.exit(0)

    synced = 0
    for post in posts:
        if sync_post(post, apply=apply):
            synced += 1

    print(f"\n완료. {synced}/{len(posts)}개 갱신.")


if __name__ == "__main__":
    main()
