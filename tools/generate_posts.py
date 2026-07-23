#!/usr/bin/env python3
"""
Generate blog post templates from Algorithm solutions.

Usage:
    python3 generate_posts.py <YYYY-MM-DD|YYYY-MM> [problem_numbers...]
    python3 generate_posts.py 2026-03-25
    python3 generate_posts.py 2026-03
"""

import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

from config import (
    ALGO_DIR, BLOG_DIR, DRAFTS_DIR, POSTS_DIR,
    PLATFORMS, LANG_ORDER, CODE_FILE_PREFIXES, FILENAME_SANITIZE,
)
from code_utils import process_java, read_codes


# ──────────────────────────────────────────────
# HTTP helpers
# ──────────────────────────────────────────────

def api_get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def api_post(url, data):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def url_get_text(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode('utf-8')


# ──────────────────────────────────────────────
# Title fetchers
# ──────────────────────────────────────────────

def fetch_title_boj(number):
    data = api_get(f"https://solved.ac/api/v3/problem/show?problemId={number}")
    return data.get('titleKo') or data.get('title'), None


def fetch_title_prms(number):
    html = url_get_text(
        f"https://school.programmers.co.kr/learn/courses/30/lessons/{number}"
    )
    m = re.search(r'<title>코딩테스트 연습 - (.+?) \| 프로그래머스', html)
    if not m:
        m = re.search(r'<title>(.+?) \| 프로그래머스', html)
    return (m.group(1) if m else None), None


def fetch_title_leet(number):
    data = api_post("https://leetcode.com/graphql", {
        "query": (
            "query q($categorySlug:String,$limit:Int,$skip:Int,"
            "$filters:QuestionListFilterInput)"
            "{problemsetQuestionList:questionList("
            "categorySlug:$categorySlug limit:$limit skip:$skip "
            "filters:$filters){data{questionId title titleSlug}}}"
        ),
        "variables": {
            "categorySlug": "",
            "skip": 0,
            "limit": 1,
            "filters": {"searchKeywords": str(number)},
        },
    })
    questions = data['data']['problemsetQuestionList']['data']
    if questions and questions[0]['questionId'] == str(number):
        return questions[0]['title'], questions[0]['titleSlug']
    return None, None


def fetch_title_cf(number):
    m = re.match(r'(\d+)([A-Za-z]\d?)', str(number))
    if not m:
        return None, None
    contest_id, index = m.group(1), m.group(2).upper()
    data = api_get(
        f"https://codeforces.com/api/contest.standings?"
        f"contestId={contest_id}&from=1&count=1"
    )
    for p in data['result']['problems']:
        if p['index'] == index:
            return p['name'], None
    return None, None


def fetch_title_swea(number):
    return None, None  # Requires browser (MCP)


FETCHERS = {
    'boj': fetch_title_boj,
    'prms': fetch_title_prms,
    'leet': fetch_title_leet,
    'cofo': fetch_title_cf,
    'swea': fetch_title_swea,
}


def fetch_title(platform, number):
    try:
        return FETCHERS[platform](number)
    except Exception as e:
        print(f"  [ERROR] Title fetch failed: {e}")
        return None, None


# ──────────────────────────────────────────────
# Problem link
# ──────────────────────────────────────────────

def get_problem_link(platform, number, slug=None):
    if platform == 'boj':
        return f"https://www.acmicpc.net/problem/{number}"
    if platform == 'prms':
        return f"https://school.programmers.co.kr/learn/courses/30/lessons/{number}"
    if platform == 'leet':
        return f"https://leetcode.com/problems/{slug}/" if slug else "TODO"
    if platform == 'cofo':
        m = re.match(r'(\d+)([A-Za-z]\d?)', str(number))
        if m:
            return (
                f"https://codeforces.com/problemset/problem/"
                f"{m.group(1)}/{m.group(2).upper()}"
            )
    if platform == 'swea':
        return "TODO"
    return "TODO"



# ──────────────────────────────────────────────
# Post generation
# ──────────────────────────────────────────────

def sanitize(name):
    for c, r in FILENAME_SANITIZE.items():
        name = name.replace(c, r)
    return name


def generate_post(date_str, platform, number, title, codes, link):
    plat = PLATFORMS[platform]

    seen = []
    for c in codes:
        if c[0]["name"] not in seen:
            seen.append(c[0]["name"])
    lang_tags = ''.join(f'[{name}]' for name in seen)
    post_title = plat['title_format'].format(num=number, title=title)
    slug = f"{plat['slug_prefix']}-{number}".lower()

    lines = [
        '---',
        f'title: "{post_title} {lang_tags}"',
        f'slug: {slug}',
        f'date: {date_str}',
        f"categories: [PS, {plat['category']}]",
        'tags: [Unlinked]',
        'toc: true',
        'math: true',
        '---',
        '',
        f'[문제 링크]({link})',
        '',
        '---',
        '',
        '## 1. 아이디어',
        '',
        '',
        '',
        '---',
        '',
        '## 2. 코드',
        '',
    ]

    for i, (lang, code) in enumerate(codes, 1):
        lines.append(f'### {i}. 풀이 [{lang["name"]}]')
        lines.append('')
        lines.append(f'```{lang["block"]}')
        lines.append(code)
        lines.append('```')
        lines.append('')

    lines += ['---', '', '## 3. 리뷰', '', '없음.', '', '---', '']

    return '\n'.join(lines)


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def process_day(year, month, day, filter_numbers):
    day_dir = ALGO_DIR / f"{year}-{month:02d}" / "src" / f"day_{day:02d}"
    date_str = f"{year}-{month:02d}-{day:02d}"

    if not day_dir.exists():
        print(f"Error: Not found: {day_dir}")
        return 0

    # Scan problem directories
    problems = []
    for entry in sorted(day_dir.iterdir()):
        if not entry.is_dir():
            continue
        name_lower = entry.name.lower()
        for prefix in PLATFORMS:
            if name_lower.startswith(f'{prefix}_'):
                number = entry.name[len(prefix) + 1:]
                if filter_numbers and number not in filter_numbers:
                    continue
                problems.append((prefix, number, entry))
                break
        else:
            if not filter_numbers:
                print(f"  [SKIP] {entry.name}")

    if not problems:
        print(f"No problems found in {day_dir}")
        return 0

    print(f"Found {len(problems)} problem(s) in {day_dir}\n")

    generated = []
    for platform, number, problem_dir in problems:
        plat = PLATFORMS[platform]
        print(f"[{plat['name_ko']} {number}]")

        # Fetch title
        title, extra = fetch_title(platform, number)
        if not title:
            title = "TODO"
            print("  Title: TODO (manual input needed)")
        else:
            print(f"  Title: {title}")

        # Read code
        codes = read_codes(problem_dir)
        if not codes:
            print("  No code files found. Skipping.")
            continue
        print(f"  Languages: {', '.join(c[0]['name'] for c in codes)}")

        # Generate
        link = get_problem_link(platform, number, slug=extra)
        content = generate_post(date_str, platform, number, title, codes, link)

        draft_dir = DRAFTS_DIR / plat['post_dir']
        draft_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{date_str}-{plat['name_ko']} {number} {sanitize(title)}.md"
        draft_path = draft_dir / filename
        post_path = POSTS_DIR / plat['post_dir'] / filename

        if draft_path.exists() or post_path.exists():
            print(f"  SKIP (already exists)")
            continue

        draft_path.write_text(content, encoding='utf-8')
        print(f"  Created: _drafts/{plat['post_dir']}/{filename}")
        generated.append(draft_path)

    return len(generated)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <YYYY-MM-DD|YYYY-MM> [problem_numbers...]")
        sys.exit(1)

    date_str = sys.argv[1]
    filter_numbers = set(sys.argv[2:]) if len(sys.argv) >= 3 else None

    parts = date_str.split('-')
    try:
        if len(parts) == 3:
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            day_targets = [(year, month, day)]
        elif len(parts) == 2:
            year, month = int(parts[0]), int(parts[1])
            month_dir = ALGO_DIR / f"{year}-{month:02d}" / "src"
            if not month_dir.exists():
                print(f"Error: Not found: {month_dir}")
                sys.exit(1)
            day_targets = []
            for d in sorted(month_dir.iterdir()):
                if d.is_dir() and d.name.startswith("day_"):
                    try:
                        day_num = int(d.name[len("day_"):])
                    except ValueError:
                        continue
                    day_targets.append((year, month, day_num))
            if not day_targets:
                print(f"No day_* directories in {month_dir}")
                sys.exit(0)
        else:
            raise ValueError
    except ValueError:
        print(f"Error: Invalid date '{date_str}'. Use YYYY-MM-DD or YYYY-MM.")
        sys.exit(1)

    total = 0
    for year, month, day in day_targets:
        total += process_day(year, month, day, filter_numbers)

    print(f"\nDone. Generated {total} post(s).")


if __name__ == '__main__':
    main()
