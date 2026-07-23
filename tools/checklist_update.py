#!/usr/bin/env python3
"""체크리스트 자동 체크"""

import re

from config import POSTS_DIR, CHECKLISTS_DIR


def main():
    # 1. _posts/에서 백준 문제 번호 추출
    solved = set()
    for path in POSTS_DIR.rglob("*.md"):
        m = re.search(r"-백준 (\d+) ", path.name)
        if m:
            solved.add(m.group(1))

    print(f"스캔된 포스트: {len(solved)}개")

    # 2-3. 체크리스트 갱신
    updated_files = 0
    newly_checked = 0

    for path in sorted(CHECKLISTS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        original = content
        count = [0]

        def replace_check(m, _solved=solved, _count=count):
            num = m.group(1)
            rest = m.group(2)
            if num in _solved:
                _count[0] += 1
                return f"- [x] [{num}{rest}"
            return m.group(0)

        content = re.sub(r"- \[ \] \[(\d+)([^\]]*\]\([^)]*\))", replace_check, content)
        if content != original:
            path.write_text(content, encoding="utf-8")
            updated_files += 1
            newly_checked += count[0]
            print(f"  {path.name}: {count[0]}개 체크")

    print(f"\n업데이트된 파일: {updated_files}개")
    print(f"새로 체크된 문제: {newly_checked}개")


if __name__ == "__main__":
    main()
