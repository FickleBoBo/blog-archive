"""Shared code processing utilities."""

import re
from config import LANG_ORDER, CODE_FILE_PREFIXES, PLATFORM_MAP, PLATFORMS, DRAFTS_DIR, POSTS_DIR

PS_DIRS = {p['post_dir'] for p in PLATFORMS.values()}


def parse_filename(filepath):
    name = filepath.name
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+?) (\S+) (.+)\.md", name)
    if not m:
        return None
    date_str = m.group(1)
    platform_ko = m.group(2)
    number = m.group(3)
    prefix = PLATFORM_MAP.get(platform_ko)
    if not prefix:
        return None
    parts = date_str.split("-")
    year_month = f"{parts[0]}-{parts[1]}"
    day = int(parts[2])
    return date_str, platform_ko, prefix, number, year_month, day


def find_posts(number=None):
    posts = []
    if number:
        for search_dir in [DRAFTS_DIR, POSTS_DIR]:
            for path in search_dir.rglob("*.md"):
                if path.relative_to(search_dir).parts[0] not in PS_DIRS:
                    continue
                if f" {number} " in path.name:
                    posts.append(path)
            if posts:
                break
    else:
        for path in DRAFTS_DIR.rglob("*.md"):
            if path.relative_to(DRAFTS_DIR).parts[0] not in PS_DIRS:
                continue
            posts.append(path)
    return sorted(posts)


def process_java(code):
    code = re.sub(r'package\s+[\w.]+;\s*\n*', '', code)
    code = re.sub(r'(class\s+)(Main|Solution)\d+', r'\1\2', code)
    return code.strip()


def read_codes(problem_dir):
    codes = []
    # Find which prefix is used (Main or Solution)
    prefix = None
    for p in CODE_FILE_PREFIXES:
        if any((problem_dir / f"{p}{lang['ext']}").exists() for lang in LANG_ORDER):
            prefix = p
            break
    if not prefix:
        return codes
    # Collect in filename order: Main.java, Main.cpp, Main2.java, Main2.cpp, ...
    suffixes = ['']
    n = 2
    while True:
        if any((problem_dir / f"{prefix}{n}{lang['ext']}").exists() for lang in LANG_ORDER):
            suffixes.append(str(n))
            n += 1
        else:
            break
    for suffix in suffixes:
        for lang in LANG_ORDER:
            fp = problem_dir / f"{prefix}{suffix}{lang['ext']}"
            if fp.exists():
                code = fp.read_text(encoding='utf-8')
                if lang['ext'] == '.java':
                    code = process_java(code)
                else:
                    code = code.strip()
                codes.append((lang, code))
    return codes
