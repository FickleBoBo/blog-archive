#!/usr/bin/env python3
"""
Mechanical review checks for PS blog posts.

Usage:
    python3 review_check.py              # check all drafts
    python3 review_check.py 24265        # check specific problem
"""

import re
import sys
from pathlib import Path

from config import BLOG_DIR
from code_utils import find_posts

# 유니코드 첨자/수학 기호 → LaTeX 대체 제안
SUPERSCRIPT = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿ"
SUBSCRIPT = "₀₁₂₃₄₅₆₇₈₉"
MATH_SYMBOL = {
    "×": r"\times", "÷": r"\div", "≤": r"\le", "≥": r"\ge", "≠": r"\ne",
    "⌊": r"\lfloor", "⌋": r"\rfloor", "⌈": r"\lceil", "⌉": r"\rceil",
    "√": r"\sqrt", "∑": r"\sum", "∏": r"\prod", "∈": r"\in", "∉": r"\notin",
    "⊆": r"\subseteq", "∞": r"\infty", "≡": r"\equiv",
}


# 코드 관례 규칙: (항목, 위반 정규식, 권장, 적용 언어)
# 발행본 502개 실측에서 **반례 0건**인 것만 등재한다 (다수결 아님, 만장일치).
# 반례가 1건이라도 있으면 규칙이 아니므로 넣지 말 것 (예: grid 25 vs board 1 → 제외).
# 근거·수치·등급은 tools/conventions.md 참고.
CODE_RULES = [
    ("상수명",      r"\bMX\b",                        "MAX",       None),
    ("방문 배열",    r"\bvisited\b",                   "vis",       None),
    ("큐 삽입",      r"\b(?:q|dq|pq|queue)\.add\(",    "offer()",   "java"),
    ("카운트 변수",  r"\bint count\b|\bcount\+\+",      "cnt",       None),
    ("결과 변수",    r"\b(?:int|long) (?:result|answer)\b", "ans / res", None),
    ("방향 배열",    r"\bd[xy]\b",                     "dr / dc",   None),
    ("이전 변수",    r"\bprev\b",                      "prv",       None),
    ("거리 배열",    r"\bdistance\b",                  "dist",      None),
    ("C++ 개행",    r"\bendl\b",                      "'\\n'",     "c++"),
    # Scanner/scanf는 규칙에서 제외 — 문제 특성상 자연스러운 선택으로 사용자가 판단.
    # (16394 홍익대학교의 Scanner, 10953 A+B - 6의 scanf. 각각 1건씩.)
]

# 함수명 규범 (2026-07-17 사용자 확정):
#   Java  = camelCase (언어 차원의 보편 관례) → 검사함
#   C++   = snake_case 우세하나 **camelCase도 허용** → 검사 안 함.
#           C++엔 통일된 함수명 관례가 없음(stdlib·Boost는 snake, LLVM·Qt는 camel,
#           Google은 Pascal). 사용자가 둘 다 쓰기로 결정.
# 예외 1: 문제가 명령어 이름을 지정하는 경우(덱 문제의 push_front 등)는 위반 아님.
# 예외 2: 수학 표기를 그대로 옮긴 이름(nCr 등)은 표기 그대로 두는 게 나음.
PROBLEM_COMMAND_NAMES = {
    "push_front", "push_back", "pop_front", "pop_back", "size", "empty",
    "front", "back", "push", "pop", "top",
}
MATH_NOTATION_NAMES = {"nCr", "nPr", "nHr"}


def _blank(m):
    """매치를 같은 길이의 공백으로 치환 (오프셋 보존)."""
    return re.sub(r"\S", " ", m.group(0))


def _code_blocks(content):
    """(언어, 코드) 목록. 언어 태그 없는 블록은 제외.

    언어 태그는 실제로 ```java / ```c++ 두 가지다. `+`가 \\w에 안 걸리므로
    문자 클래스에 반드시 포함할 것 — 빠뜨리면 C++ 블록이 통째로 누락된다.
    """
    return [
        (lang.lower(), body)
        for lang, body in re.findall(r"```([\w+#]+)\n(.*?)```", content, re.DOTALL)
    ]


def check_code_conventions(content, warnings):
    """코드 블록의 명명 관례 검사.

    표기(수식·백틱)와 달리 관례는 문맥/취향을 타지 않으므로 정적 검사에 적합.
    위반 시 고칠 곳은 포스트가 아니라 Algorithm 레포 원본 — 포스트만 고치면
    다음 /sync 에서 되돌아온다.
    """
    for lang, body in _code_blocks(content):
        for name, bad, good, only in CODE_RULES:
            if only and lang != only:
                continue
            for m in re.finditer(bad, body):
                warnings.append(
                    f"[CONVENTION] {name}: '{m.group(0)}' → '{good}' 권장"
                    f" ({lang}) — Algorithm 레포 원본 수정 필요"
                )
                break  # 규칙당 블록별 1건만 보고

        check_func_naming(lang, body, warnings)


def check_func_naming(lang, body, warnings):
    """함수명 스타일. Java만 검사 (C++는 camel/snake 둘 다 허용 — 위 주석 참고)."""
    if lang != "java":
        return
    good = "camelCase"
    hits = [
        n for n in re.findall(r"static \w+(?:\[\])* ([a-z]\w*) *\(", body) if "_" in n
    ]
    for n in hits:
        if n in PROBLEM_COMMAND_NAMES or n in MATH_NOTATION_NAMES:
            continue  # 문제가 지정한 명령어 / 수학 표기 — 위반 아님
        warnings.append(
            f"[CONVENTION] 함수명: '{n}' → {good} 권장 ({lang})"
            " — Algorithm 레포 원본 수정 필요"
        )


def strip_noise(content, keep_math=True):
    """산문만 남긴다. 오프셋은 보존(같은 길이 공백으로 치환).

    제거: front matter, 코드 블록, 인라인 백틱, 링크 타겟, 언어명.
    keep_math=False면 $...$ 내부까지 제거.
    """
    text = re.sub(r"\A---\n.*?\n---", _blank, content, count=1, flags=re.DOTALL)
    text = re.sub(r"```.*?```", _blank, text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", _blank, text)
    text = re.sub(r"\]\([^)\n]*\)", _blank, text)  # [텍스트](링크) 의 링크 부분
    text = re.sub(r"\bC\+\+|\bJava\b|\bPython\b", _blank, text)
    if not keep_math:
        text = re.sub(r"\$\$.*?\$\$", _blank, text, flags=re.DOTALL)
        text = re.sub(r"\$[^$\n]+\$", _blank, text)
    return text


def _context(text, pos, width=30):
    s = text[max(0, pos - width):pos + width]
    return re.sub(r"\s+", " ", s).strip()


def check_frontmatter(content, errors):
    """front matter 필수 필드 검사"""
    fm_match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not fm_match:
        errors.append("[FRONTMATTER] front matter 없음")
        return
    fm = fm_match.group(1)
    for field in ["title", "slug", "date", "categories", "tags", "toc", "math"]:
        if not re.search(rf"^{field}:", fm, re.MULTILINE):
            errors.append(f"[FRONTMATTER] '{field}' 필드 누락")


def check_structure(content, errors):
    """포스트 구조 검사"""
    if "[문제 링크]" not in content:
        errors.append("[STRUCTURE] 문제 링크 없음")
    if "## 1. 아이디어" not in content and "## 1. 문제 풀이" not in content:
        errors.append("[STRUCTURE] '## 1. 아이디어' 또는 '## 1. 문제 풀이' 섹션 없음")
    if "## 2. 코드" not in content:
        errors.append("[STRUCTURE] '## 2. 코드' 섹션 없음")
    if "## 3. 리뷰" not in content:
        errors.append("[STRUCTURE] '## 3. 리뷰' 섹션 없음")


def check_code_blocks(content, errors):
    """코드 블록 언어 태그 검사 (여는 태그만 검사)"""
    # 여는 코드 블록만 찾기: 줄 시작이 ```이고 뒤에 내용이 있거나 없는 경우
    # 닫는 ```는 줄이 ```만으로 끝남
    opening_blocks = []
    in_code = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```") and not in_code:
            lang = stripped[3:].strip()
            opening_blocks.append(lang)
            in_code = True
        elif stripped == "```" and in_code:
            in_code = False
    for i, lang in enumerate(opening_blocks):
        if not lang:
            errors.append(f"[CODE] {i+1}번째 코드 블록에 언어 태그 없음")


def check_math_spacing(content, errors):
    """인라인 수식 앞뒤 공백 검사"""
    # front matter와 코드 블록 제외
    text = re.sub(r"^---\n.+?\n---", "", content, count=1, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # $...$ 패턴 찾기 ($$...$$는 제외)
    for m in re.finditer(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", text):
        start = m.start()
        end = m.end()
        line_start = text.rfind("\n", 0, start) + 1
        line_end = text.find("\n", end)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end].strip()

        # 앞 글자 검사 (공백, 줄시작, 괄호가 아니면 경고)
        if start > 0 and start > line_start:
            prev_char = text[start - 1]
            if prev_char not in (" ", "\n", "(", "[", ",", "、"):
                errors.append(
                    f"[MATH] 수식 앞 공백 없음: ...{text[max(0,start-5):end+5]}..."
                )

        # 뒤 글자 검사 (공백, 줄끝, 괄호, 구두점, 한글 조사가 아니면 경고)
        if end < len(text) and end < line_end:
            next_char = text[end]
            # 허용: 공백, 줄끝, 닫는 괄호, 구두점
            allowed = {" ", "\n", ")", "]", ",", ".", "。", "!"}
            # 허용: 한글 조사 (단일 문자)
            korean_particles = {"의", "이", "를", "은", "는", "에", "와", "과", "로", "가", "도", "만", "씩", "번"}
            if next_char not in allowed and next_char not in korean_particles:
                errors.append(
                    f"[MATH] 수식 뒤 공백 없음: ...{text[max(0,start-5):end+5]}..."
                )


def check_complexity_case(content, errors):
    """복잡도 표기 대소문자 검사"""
    # front matter와 코드 블록 제외
    text = re.sub(r"^---\n.+?\n---", "", content, count=1, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # $O(...)$ 패턴에서 소문자 변수 검출
    for m in re.finditer(r"\$O\(([^)]+)\)\$", text):
        inner = m.group(1)
        # 소문자 단독 변수 검출 (log, min, max 등 함수명은 제외)
        if re.search(r"(?<!\w)[a-z](?!\w*[a-z]{2})", inner):
            # log, min, max, mod 등은 허용
            cleaned = re.sub(r"\b(log|min|max|mod|sin|cos|tan)\b", "", inner)
            if re.search(r"(?<!\w)[a-z](?!\w)", cleaned):
                errors.append(
                    f"[COMPLEXITY] 소문자 변수 사용: $O({inner})$ → 대문자로 변경 필요"
                )


def _plain_vars(content):
    """산문(수식·코드·백틱 제외)에 평문으로 단독 출현하는 알파벳 변수를 수집.

    반환: {변수: [(위치, 문맥), ...]}
    """
    plain = strip_noise(content, keep_math=False)
    found = {}
    # 앞뒤가 영숫자/밑줄/백슬래시/달러가 아닌 홑글자.
    # 뒤에 +,# 이 오는 경우(C++, C#)는 strip_noise가 이미 지웠지만 방어적으로 제외.
    # 뒤에 '(' 가 오면 함수 표기(O(1), f(x))이므로 제외 — COMPLEXITY 검사와 중복 보고 방지.
    for m in re.finditer(r"(?<![A-Za-z0-9_$\\])([A-Za-z])(?![A-Za-z0-9_+#]|\s*\()", plain):
        found.setdefault(m.group(1), []).append((m.start(), _context(plain, m.start())))
    return found


def check_math_var_consistency(content, warnings):
    """수식 변수가 일관되게 수식으로 표현되는지 검사.

    (1) 혼재: 어딘가 `$X$`로 쓴 변수가 평문으로도 출현 → 확신 높음
    (2) 전량 평문: 수식으로 쓴 적 없는 단독 변수 → 검토 후보 (오탐 가능)
    """
    text = strip_noise(content)  # 수식은 남김

    # 수식으로 표기된 적 있는 단일 변수 수집
    math_vars = set()
    for m in re.finditer(r"\$([^$\n]+)\$", text):
        inner = m.group(1).strip()
        if re.match(r"^[a-zA-Z]$", inner):
            math_vars.add(inner)

    plain_vars = _plain_vars(content)

    for var, hits in sorted(plain_vars.items()):
        if var in math_vars:
            # (1) 혼재 — 변수당 전체 건수를 보고 (기존엔 첫 건만 보고하고 break)
            label = f"[MATH_VAR] 변수 '{var}' 수식/평문 혼재 ({len(hits)}건)"
        else:
            # (2) 전량 평문 — 기존 검사가 놓치던 사각지대
            label = f"[MATH_VAR?] 평문 단독 변수 '{var}' ({len(hits)}건, 검토 필요)"
        for _, ctx in hits[:2]:
            warnings.append(f"{label}: ...{ctx}...")
        if len(hits) > 2:
            warnings.append(f"{label}: (외 {len(hits) - 2}건)")


def check_unicode_math(content, errors):
    """유니코드 첨자·수학 기호 검사 → LaTeX로 바꿔야 함"""
    text = strip_noise(content)  # 수식 안에 있어도 잘못된 표기이므로 남겨둠

    for m in re.finditer(f"[{SUPERSCRIPT}{SUBSCRIPT}]+", text):
        errors.append(
            f"[UNICODE] 유니코드 첨자 '{m.group(0)}' → LaTeX 필요"
            f" (예: 2³¹ → $2^{{31}}$): ...{_context(text, m.start())}..."
        )

    for m in re.finditer(f"[{''.join(MATH_SYMBOL)}]", text):
        sym = m.group(0)
        errors.append(
            f"[UNICODE] 유니코드 기호 '{sym}' → '{MATH_SYMBOL[sym]}' 필요"
            f": ...{_context(text, m.start())}..."
        )


def check_by_pattern(content, warnings):
    """'3 by 3' 표기 검사 → '$3 \\times 3$'"""
    text = strip_noise(content, keep_math=False)
    for m in re.finditer(r"(\w+)\s+by\s+(\w+)", text, re.IGNORECASE):
        a, b = m.group(1), m.group(2)
        warnings.append(
            f"[BY] '{m.group(0)}' → '${a} \\times {b}$' 검토"
            f": ...{_context(text, m.start())}..."
        )


def check_plain_complexity(content, errors):
    """평문 O(...) 검사 → $O(...)$"""
    text = strip_noise(content, keep_math=False)
    for m in re.finditer(r"(?<![$\w])O\s*\(", text):
        errors.append(
            f"[COMPLEXITY] 평문 복잡도 표기 → $O(...)$ 필요"
            f": ...{_context(text, m.start())}..."
        )


def check_idea_empty(content, warnings):
    """아이디어 섹션 비어있는지 검사"""
    idea_match = re.search(
        r"## 1\. (?:아이디어|문제 풀이)\n\n(.*?)(?=\n---|\n## 2\.)", content, re.DOTALL
    )
    if idea_match:
        idea_text = idea_match.group(1).strip()
        if not idea_text:
            warnings.append("[IDEA] 아이디어 섹션이 비어있음")


def check_review_empty(content, info):
    """리뷰 섹션 상태 확인"""
    review_match = re.search(
        r"## 3\. 리뷰\n\n(.*?)(?=\n---|\Z)", content, re.DOTALL
    )
    if review_match:
        review_text = review_match.group(1).strip()
        if review_text == "없음.":
            info.append("[REVIEW] 리뷰 섹션: 없음.")
        elif not review_text:
            info.append("[REVIEW] 리뷰 섹션이 비어있음")


def check_post(filepath):
    content = filepath.read_text(encoding="utf-8")
    errors = []
    warnings = []
    info = []

    check_frontmatter(content, errors)
    check_structure(content, errors)
    check_code_blocks(content, errors)
    check_math_spacing(content, errors)
    check_complexity_case(content, errors)
    check_plain_complexity(content, errors)
    check_unicode_math(content, errors)
    check_math_var_consistency(content, warnings)
    check_by_pattern(content, warnings)
    check_code_conventions(content, warnings)
    check_idea_empty(content, warnings)
    check_review_empty(content, info)

    return errors, warnings, info


def main():
    number = sys.argv[1] if len(sys.argv) >= 2 else None

    if number:
        print(f"문제 {number}번 기계적 검사\n")
    else:
        print("_drafts/ 전체 기계적 검사\n")

    posts = find_posts(number)
    if not posts:
        print("대상 포스트 없음.")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0

    for post in posts:
        rel = post.relative_to(BLOG_DIR)
        errors, warnings, info = check_post(post)

        if errors or warnings:
            print(f"{'❌' if errors else '⚠️'} {rel}")
            for e in errors:
                print(f"    {e}")
                total_errors += 1
            for w in warnings:
                print(f"    {w}")
                total_warnings += 1
        else:
            print(f"  ✅ {rel}")

        for i in info:
            print(f"    {i}")

    print(f"\n완료. {len(posts)}개 검사, 오류 {total_errors}개, 경고 {total_warnings}개")


if __name__ == "__main__":
    main()
