#!/usr/bin/env python3
"""체크리스트 진행률 요약"""

import re

from config import CHECKLISTS_DIR

for path in sorted(CHECKLISTS_DIR.glob("*.md")):
    content = path.read_text(encoding="utf-8")

    done = len(re.findall(r"^- \[x\]", content, re.MULTILINE))
    todo = len(re.findall(r"^- \[ \]", content, re.MULTILINE))
    total = done + todo

    if total == 0:
        continue

    pct = done / total * 100
    bar_len = 30
    filled = round(bar_len * done / total)
    bar = "█" * filled + "░" * (bar_len - filled)

    print(f"{path.name:<20s} {bar} {done:>4d}/{total:<4d} ({pct:5.1f}%)")
