#!/usr/bin/env python3
"""
Commit a problem to both Algorithm and Blog repos.

Usage:
    python3 commit.py <problem_number>
    python3 commit.py 24265
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

from config import BLOG_DIR, ALGO_DIR, DRAFTS_DIR, POSTS_DIR, PLATFORMS
from code_utils import parse_filename, PS_DIRS


def find_draft(number):
    matches = []
    for path in DRAFTS_DIR.rglob("*.md"):
        if path.relative_to(DRAFTS_DIR).parts[0] not in PS_DIRS:
            continue
        if f" {number} " in path.name:
            matches.append(path)
    if not matches:
        print(f"Error: _drafts/에서 {number}번 포스트를 찾을 수 없습니다.")
        sys.exit(1)
    if len(matches) > 1:
        print(f"Error: 여러 개 매칭됨:")
        for m in matches:
            print(f"  {m}")
        sys.exit(1)
    return matches[0]


def extract_frontmatter(filepath, key):
    with open(filepath, "r") as f:
        for line in f:
            m = re.match(rf'^{key}:\s*"?(.+?)"?\s*$', line)
            if m:
                return m.group(1)
    return None


def extract_title(filepath):
    return extract_frontmatter(filepath, "title")


def extract_slug(filepath):
    return extract_frontmatter(filepath, "slug")


def move_to_posts(draft_path, platform_dir_name):
    post_dir = POSTS_DIR / platform_dir_name
    post_dir.mkdir(parents=True, exist_ok=True)
    dest = post_dir / draft_path.name
    shutil.move(str(draft_path), str(dest))
    return dest


def assets_paths(slug):
    """리부트 대기 자리와 발행 자리. 포스트의 _drafts/ ↔ _posts/와 같은 구조."""
    return BLOG_DIR / "assets" / slug, BLOG_DIR / "assets" / "posts" / slug


def move_assets(slug):
    """assets/{slug}/ → assets/posts/{slug}/ 이동 (포스트 이동과 짝).

    포스트만 _posts로 옮기고 이미지를 그대로 두면 리부트가 반쪽만 되어
    발행본이 아직 옮겨오지 않은 경로를 참조하게 된다.
    반환값: (이동했는지, 커밋 대상 경로 목록)
    """
    if not slug:
        return False, []
    flat, pub = assets_paths(slug)
    moved = False
    if flat.is_dir():
        pub.parent.mkdir(parents=True, exist_ok=True)
        if pub.is_dir():
            for f in flat.iterdir():
                shutil.move(str(f), str(pub / f.name))
            flat.rmdir()
        else:
            shutil.move(str(flat), str(pub))
        moved = True
        print(f"  이미지 이동: assets/{slug}/ → assets/posts/{slug}/")
    if not pub.is_dir():
        return moved, []
    # flat 경로도 add — 추적 중이었다면 삭제를 스테이징해야 한다
    return moved, [str(pub.relative_to(BLOG_DIR)), str(flat.relative_to(BLOG_DIR))]


def unmove_assets(slug):
    """move_assets 롤백."""
    flat, pub = assets_paths(slug)
    if pub.is_dir():
        shutil.move(str(pub), str(flat))
        print(f"  (롤백: assets/posts/{slug}/ → assets/{slug}/)")


def git_commit(repo_dir, files_to_add, message):
    # 기존 스테이징 초기화 — 의도하지 않은 파일 커밋 방지
    subprocess.run(["git", "reset"], cwd=repo_dir,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for f in files_to_add:
        subprocess.run(["git", "add", str(f)], cwd=repo_dir,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # 스테이징된 파일이 있는지 확인
    check = subprocess.run(["git", "diff", "--cached", "--stat"],
                           cwd=repo_dir, capture_output=True, text=True)
    if not check.stdout.strip():
        print("  (커밋할 변경사항 없음, 건너뜀)")
        return
    print(check.stdout.strip())
    result = subprocess.run(["git", "commit", "-m", message],
                            cwd=repo_dir, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        sys.exit(1)


def checklist_update():
    """checklist_update.py를 subprocess로 실행하고 변경된 파일 목록을 반환"""
    script = Path(__file__).parent / "checklist_update.py"
    subprocess.run([sys.executable, str(script)], cwd=script.parent)
    # 변경된 체크리스트 파일을 git diff로 확인
    result = subprocess.run(
        ["git", "diff", "--name-only", "checklists/"],
        cwd=BLOG_DIR, capture_output=True, text=True,
    )
    changed = []
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            changed.append(str(BLOG_DIR / line.strip()))
    return changed


def commit_one(number):
    """단일 문제 커밋"""
    # 1. Find draft
    draft_path = find_draft(number)
    print(f"[1] 드래프트: {draft_path.relative_to(BLOG_DIR)}")

    # 2. Parse filename
    parsed = parse_filename(draft_path)
    if not parsed:
        print(f"Error: 파일명 파싱 실패: {draft_path.name}")
        sys.exit(1)
    date_str, platform_ko, prefix, num, year_month, day = parsed

    # 목적지 폴더는 파일명에서 파싱한 prefix로 결정 (드래프트 부모 폴더와 다를 수 있음)
    platform_dir = PLATFORMS[prefix]['post_dir']
    if draft_path.parent.name != platform_dir:
        print(f"  ⚠ 드래프트 부모 폴더({draft_path.parent.name})와 플랫폼({platform_dir}) 불일치 → {platform_dir}로 이동")

    # 3. Extract title
    title = extract_title(draft_path)
    if not title:
        print("Error: title 추출 실패")
        sys.exit(1)
    commit_msg = f"feat: {title}"
    print(f"[2] 커밋 메시지: {commit_msg}")

    # 4. Commit to Algorithm repo (before move — no rollback needed on failure)
    algo_problem_dir = f"{year_month}/src/day_{day:02d}/{prefix}_{num}"
    algo_full_path = ALGO_DIR / algo_problem_dir
    if not algo_full_path.exists():
        print(f"Warning: Algorithm 경로 없음: {algo_problem_dir}")
    else:
        print(f"\n[3] Algorithm 레포 커밋")
        git_commit(ALGO_DIR, [algo_problem_dir], commit_msg)

    # 5. Move draft to posts
    post_path = move_to_posts(draft_path, platform_dir)
    print(f"\n[4] 이동: _drafts/ → {post_path.relative_to(BLOG_DIR)}")

    # 6. Commit to Blog repo (rollback move on failure)
    print(f"\n[5] Blog 레포 커밋")
    blog_files = [
        str(post_path.relative_to(BLOG_DIR)),
        str(draft_path.relative_to(BLOG_DIR)),
    ]
    # 이미지도 포스트와 함께 발행 자리로 이동
    slug = extract_slug(post_path)
    assets_moved, assets_files = move_assets(slug)
    blog_files.extend(assets_files)
    if assets_files:
        print(f"  이미지 포함: assets/posts/{slug}/")
    try:
        git_commit(BLOG_DIR, blog_files, commit_msg)
    except SystemExit:
        # 커밋 실패 시 파일을 _drafts/로 복원
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(post_path), str(draft_path))
        print(f"  (롤백: {draft_path.relative_to(BLOG_DIR)}로 복원)")
        if assets_moved:
            unmove_assets(slug)
        raise

    print(f"\n완료.")


def find_all_drafts():
    """_drafts/에서 문제 번호 목록 추출 (PS 플랫폼 폴더만 — legacy/tmp 제외)"""
    numbers = []
    for path in sorted(DRAFTS_DIR.rglob("*.md")):
        if path.relative_to(DRAFTS_DIR).parts[0] not in PS_DIRS:
            continue
        parsed = parse_filename(path)
        if parsed:
            numbers.append(parsed[3])
    return numbers


def main():
    if len(sys.argv) >= 2:
        numbers = sys.argv[1:]
    else:
        numbers = find_all_drafts()
        if not numbers:
            print("_drafts/에 커밋할 포스트가 없습니다.")
            sys.exit(0)
        print(f"_drafts/ 전체 커밋: {len(numbers)}개 문제\n")

    for i, number in enumerate(numbers):
        if len(numbers) > 1:
            print(f"\n{'='*50}")
            print(f"[{i+1}/{len(numbers)}] 문제 {number}")
            print(f"{'='*50}\n")
        commit_one(number)

    # 체크리스트 갱신 (전체 커밋 후 1회)
    print(f"\n{'='*50}")
    print("체크리스트 갱신")
    print(f"{'='*50}\n")
    changed_checklists = checklist_update()
    if changed_checklists:
        git_commit(BLOG_DIR, changed_checklists, "chore: 체크리스트 갱신")


if __name__ == "__main__":
    main()
