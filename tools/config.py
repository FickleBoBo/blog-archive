"""Shared configuration for all tools."""

from pathlib import Path

BLOG_DIR = Path.home() / "Desktop" / "GITHUB" / "FickleBoBo.github.io"
ALGO_DIR = Path.home() / "Desktop" / "GITHUB" / "Algorithm"
DRAFTS_DIR = BLOG_DIR / "_drafts"
POSTS_DIR = BLOG_DIR / "_posts"
CHECKLISTS_DIR = BLOG_DIR / "checklists"

PLATFORM_MAP = {
    "백준": "boj",
    "프로그래머스": "prms",
    "리트코드": "leet",
    "코드포스": "cofo",
    "SWEA": "swea",
}

PLATFORMS = {
    'boj': {
        'name_ko': '백준',
        'post_dir': 'baekjoon',
        'slug_prefix': 'baekjoon',
        'category': 'BaekJoon',
        'title_format': '[BaekJoon] {num}번 - {title}',
    },
    'prms': {
        'name_ko': '프로그래머스',
        'post_dir': 'programmers',
        'slug_prefix': 'programmers',
        'category': 'Programmers',
        'title_format': '[Programmers] {num}번 - {title}',
    },
    'leet': {
        'name_ko': '리트코드',
        'post_dir': 'leetcode',
        'slug_prefix': 'leetcode',
        'category': 'LeetCode',
        'title_format': '[LeetCode] {num}번 - {title}',
    },
    'cofo': {
        'name_ko': '코드포스',
        'post_dir': 'codeforces',
        'slug_prefix': 'codeforces',
        'category': 'Codeforces',
        'title_format': '[Codeforces] #{num} - {title}',
    },
    'swea': {
        'name_ko': 'SWEA',
        'post_dir': 'swea',
        'slug_prefix': 'swea',
        'category': 'SWEA',
        'title_format': '[SWEA] {num}번 - {title}',
    },
}

LANG_ORDER = [
    {'ext': '.java', 'name': 'Java', 'block': 'java'},
    {'ext': '.cpp', 'name': 'C++', 'block': 'c++'},
    {'ext': '.py', 'name': 'Python', 'block': 'python'},
]

CODE_FILE_PREFIXES = ['Main', 'Solution']

FILENAME_SANITIZE = {
    '/': '／', '?': '？', ':': '：', '*': '＊',
    '"': '＂', '<': '＜', '>': '＞', '|': '｜', '\\': '＼',
}
