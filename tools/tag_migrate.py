"""Tag migration — bulk-update post frontmatter when tag taxonomy changes.

Commands:
    attach --post NUM --tag TAG          # add TAG to a single post (ancestry auto-expand)
    detach --post NUM --tag TAG          # remove TAG from a single post (stale ancestor cleanup)
    rename OLD NEW                       # OLD → NEW (1:1)
    merge SRC1 SRC2 ... --into DST       # multiple → DST, dedup
    delete TAG [--fallback PARENT]       # remove TAG (optionally replace with PARENT)
    move TAG --to-parent NEW_PARENT      # change parent in tags.md, then recompute
    recompute-ancestry                   # rebuild ancestry chains for all posts based on current tags.md

All commands are dry-run by default. Use --apply to actually modify files.
Use --post NUMBER to limit to a single post (required for attach/detach).

Examples:
    python tag_migrate.py attach --post 9658 --tag dfs
    python tag_migrate.py attach --post 9658 --tag dfs --apply
    python tag_migrate.py detach --post 9658 --tag dfs --apply
    python tag_migrate.py rename "mo algorithm" "mo's algorithm" --apply
    python tag_migrate.py merge "articulation point" "bridge" --into articulation
    python tag_migrate.py move dijkstra --to-parent graph --apply
    python tag_migrate.py recompute-ancestry --apply
"""

import sys
import datetime
from pathlib import Path
from tag_utils import (
    parse_tags_md,
    parse_frontmatter,
    write_frontmatter_tags,
    expand_with_ancestry,
    minimal_specific,
    compute_ancestry,
    remove_stale_ancestors,
    find_all_posts,
    UNLINKED,
    TAGS_FILE,
)


def recompute(post_tags, tags_dict):
    """Convert post_tags (flat ancestry-expanded list) to canonical form.

    Vocab tags are normalized via minimal_specific + expand_with_ancestry.
    Non-vocab tags are preserved as-is so audit can flag them separately.
    """
    invalid = [t for t in post_tags if t not in tags_dict]
    specific = minimal_specific(post_tags, tags_dict)
    expanded = expand_with_ancestry(specific, tags_dict)
    return list(expanded) + sorted(set(invalid))
from code_utils import find_posts


def log_change(command, summary, applied):
    """Append a change log entry to tools/tags.md."""
    if not applied:
        return
    log_line = f"- {datetime.date.today().isoformat()}: `{command}` — {summary}\n"
    text = TAGS_FILE.read_text(encoding='utf-8')
    if "# Change Log" not in text:
        text += "\n\n# Change Log\n\n"
    # Append at the end of the file
    if not text.endswith('\n'):
        text += '\n'
    text += log_line
    TAGS_FILE.write_text(text, encoding='utf-8')


def collect_target_posts(post_filter):
    """Get list of posts to process. post_filter is None or a problem number string."""
    if post_filter:
        return find_posts(post_filter)
    return find_all_posts()


def show_diff(path, old_tags, new_tags):
    """Print a single-line diff for a post's tag change."""
    rel = path.name
    print(f"  {rel}")
    print(f"    - {old_tags}")
    print(f"    + {new_tags}")


def cmd_attach(args, tags_dict):
    """Attach a tag to a specific post (with ancestry auto-expand)."""
    post_filter = get_post_filter(args)
    if not post_filter:
        die("attach requires --post NUMBER")
    if '--tag' not in args:
        die("attach requires --tag TAG")
    tag_idx = args.index('--tag')
    if tag_idx + 1 >= len(args):
        die("--tag requires a value")
    tag = args[tag_idx + 1]
    apply = '--apply' in args

    if tag not in tags_dict:
        die(f"tag '{tag}' not in vocabulary")
    if not tags_dict[tag].get('auto_companion', True):
        die(f"tag '{tag}' has auto_companion=false (cannot attach directly)")

    posts = collect_target_posts(post_filter)
    if not posts:
        die(f"no posts found for {post_filter}")

    print(f"\nattach: '{tag}' to post {post_filter} ({'APPLY' if apply else 'DRY-RUN'})\n")
    affected = 0
    for path in posts:
        fm, _ = parse_frontmatter(path)
        if not fm or 'tags' not in fm:
            continue
        post_tags = fm['tags']
        if post_tags == [UNLINKED]:
            post_tags = []
        if tag in post_tags:
            print(f"  {path.name}: '{tag}' already attached")
            continue
        new_tags = recompute(post_tags + [tag], tags_dict)
        show_diff(path, fm['tags'], new_tags)
        affected += 1
        if apply:
            write_frontmatter_tags(path, new_tags)

    print(f"\n{affected} post(s) affected.")
    if apply and affected:
        log_change(f"attach {tag} --post {post_filter}", f"{affected} post", True)


def cmd_detach(args, tags_dict):
    """Detach a tag from a specific post (and clean up stale ancestors)."""
    post_filter = get_post_filter(args)
    if not post_filter:
        die("detach requires --post NUMBER")
    if '--tag' not in args:
        die("detach requires --tag TAG")
    tag_idx = args.index('--tag')
    if tag_idx + 1 >= len(args):
        die("--tag requires a value")
    tag = args[tag_idx + 1]
    apply = '--apply' in args

    if tag not in tags_dict:
        die(f"tag '{tag}' not in vocabulary")

    posts = collect_target_posts(post_filter)
    if not posts:
        die(f"no posts found for {post_filter}")

    # Ancestors of the detached tag are potentially stale
    stale_candidates = set(compute_ancestry(tag, tags_dict))

    print(f"\ndetach: '{tag}' from post {post_filter} ({'APPLY' if apply else 'DRY-RUN'})\n")
    affected = 0
    for path in posts:
        fm, _ = parse_frontmatter(path)
        if not fm or 'tags' not in fm:
            continue
        post_tags = fm['tags']
        if post_tags == [UNLINKED] or tag not in post_tags:
            continue
        without_tag = [t for t in post_tags if t != tag]
        cleaned = remove_stale_ancestors(without_tag, stale_candidates, tags_dict)
        new_tags = recompute(cleaned, tags_dict)
        # If everything cleared, fall back to [Unlinked] sentinel
        if not new_tags:
            new_tags = [UNLINKED]
        show_diff(path, post_tags, new_tags)
        affected += 1
        if apply:
            write_frontmatter_tags(path, new_tags)

    print(f"\n{affected} post(s) affected.")
    if apply and affected:
        log_change(f"detach {tag} --post {post_filter}", f"{affected} post", True)


def cmd_rename(args, tags_dict):
    if len(args) < 2:
        die("rename requires OLD and NEW")
    old_name, new_name = args[0], args[1]
    apply = '--apply' in args
    post_filter = get_post_filter(args)

    if new_name not in tags_dict:
        die(f"target tag '{new_name}' not in vocabulary (add to tags.md first)")

    posts = collect_target_posts(post_filter)
    affected = 0
    print(f"\nrename: '{old_name}' → '{new_name}' ({'APPLY' if apply else 'DRY-RUN'})\n")

    for path in posts:
        fm, _ = parse_frontmatter(path)
        if not fm or 'tags' not in fm:
            continue
        post_tags = fm['tags']
        if post_tags == [UNLINKED] or old_name not in post_tags:
            continue
        new_tags = [new_name if t == old_name else t for t in post_tags]
        # dedupe while preserving order
        seen = set()
        new_tags = [t for t in new_tags if not (t in seen or seen.add(t))]
        # recompute ancestry to keep frontmatter consistent
        new_tags = recompute(new_tags, tags_dict)
        show_diff(path, post_tags, new_tags)
        affected += 1
        if apply:
            write_frontmatter_tags(path, new_tags)

    print(f"\n{affected} post(s) affected.")
    if apply:
        log_change(f"rename {old_name} -> {new_name}", f"{affected} posts", True)


def cmd_merge(args, tags_dict):
    if '--into' not in args:
        die("merge requires --into DST")
    into_idx = args.index('--into')
    sources = args[:into_idx]
    if into_idx + 1 >= len(args):
        die("--into requires a target tag name")
    dst = args[into_idx + 1]
    apply = '--apply' in args
    post_filter = get_post_filter(args)

    if not sources:
        die("merge requires at least one source tag")
    if dst not in tags_dict:
        die(f"destination '{dst}' not in vocabulary")

    posts = collect_target_posts(post_filter)
    affected = 0
    print(f"\nmerge: {sources} → '{dst}' ({'APPLY' if apply else 'DRY-RUN'})\n")

    src_set = set(sources)
    for path in posts:
        fm, _ = parse_frontmatter(path)
        if not fm or 'tags' not in fm:
            continue
        post_tags = fm['tags']
        if post_tags == [UNLINKED]:
            continue
        if not (src_set & set(post_tags)):
            continue
        new_tags = []
        added_dst = False
        for t in post_tags:
            if t in src_set:
                if not added_dst:
                    new_tags.append(dst)
                    added_dst = True
            elif t != dst:
                new_tags.append(t)
            else:
                new_tags.append(t)
        # ensure dst present
        if dst not in new_tags:
            new_tags.append(dst)
        # dedupe
        seen = set()
        new_tags = [t for t in new_tags if not (t in seen or seen.add(t))]
        new_tags = recompute(new_tags, tags_dict)
        show_diff(path, post_tags, new_tags)
        affected += 1
        if apply:
            write_frontmatter_tags(path, new_tags)

    print(f"\n{affected} post(s) affected.")
    if apply:
        log_change(f"merge {sources} -> {dst}", f"{affected} posts", True)


def cmd_delete(args, tags_dict):
    if not args:
        die("delete requires TAG")
    tag = args[0]
    fallback = None
    if '--fallback' in args:
        idx = args.index('--fallback')
        if idx + 1 < len(args):
            fallback = args[idx + 1]
    apply = '--apply' in args
    post_filter = get_post_filter(args)

    if fallback and fallback not in tags_dict:
        die(f"fallback '{fallback}' not in vocabulary")

    posts = collect_target_posts(post_filter)
    affected = 0
    print(f"\ndelete: '{tag}'" + (f" (fallback: {fallback})" if fallback else "") + f" ({'APPLY' if apply else 'DRY-RUN'})\n")

    for path in posts:
        fm, _ = parse_frontmatter(path)
        if not fm or 'tags' not in fm:
            continue
        post_tags = fm['tags']
        if post_tags == [UNLINKED] or tag not in post_tags:
            continue
        new_tags = [t for t in post_tags if t != tag]
        if fallback and fallback not in new_tags:
            new_tags.append(fallback)
        new_tags = recompute(new_tags, tags_dict)
        show_diff(path, post_tags, new_tags)
        affected += 1
        if apply:
            write_frontmatter_tags(path, new_tags)

    print(f"\n{affected} post(s) affected.")
    if apply:
        log_change(f"delete {tag}" + (f" --fallback {fallback}" if fallback else ""), f"{affected} posts", True)


def cmd_move(args, tags_dict):
    """Move a tag to a new parent in tags.md, then recompute ancestry for affected posts."""
    if not args or '--to-parent' not in args:
        die("move requires TAG --to-parent NEW_PARENT")
    tag = args[0]
    idx = args.index('--to-parent')
    if idx + 1 >= len(args):
        die("--to-parent requires a parent tag name")
    new_parent = args[idx + 1]
    apply = '--apply' in args

    if tag not in tags_dict:
        die(f"tag '{tag}' not in vocabulary")
    if new_parent not in tags_dict:
        die(f"new parent '{new_parent}' not in vocabulary")

    old_parent = tags_dict[tag].get('parent')
    if old_parent == new_parent:
        print(f"'{tag}' already has parent '{new_parent}'. nothing to do.")
        return

    # Capture old ancestry chain before mutating tags_dict
    old_ancestors_set = set(compute_ancestry(tag, tags_dict))

    print(f"\nmove: '{tag}' parent: '{old_parent}' → '{new_parent}' ({'APPLY' if apply else 'DRY-RUN'})\n")
    print(f"Step 1: update tags.md `parent` field for [{tag}]")

    if apply:
        text = TAGS_FILE.read_text(encoding='utf-8')
        # Find the [tag] block and replace its parent line
        import re
        pattern = re.compile(
            rf'(\[{re.escape(tag)}\]\s*\n(?:[^\[\n].*\n)*?parent:\s*)([^\n]*)',
            re.MULTILINE
        )
        new_text, n = pattern.subn(rf'\g<1>{new_parent}', text)
        if n == 0:
            die(f"could not find parent line for [{tag}] in tags.md")
        TAGS_FILE.write_text(new_text, encoding='utf-8')
        print(f"  ✓ tags.md updated")
        # Reload tags_dict
        tags_dict = parse_tags_md()
    else:
        # Simulate the change locally
        tags_dict = dict(tags_dict)
        tags_dict[tag] = dict(tags_dict[tag])
        tags_dict[tag]['parent'] = new_parent

    # Compute new ancestry chain after the move and identify stale ancestors
    new_ancestors_set = set(compute_ancestry(tag, tags_dict))
    stale = old_ancestors_set - new_ancestors_set

    print(f"\nStep 2: recompute ancestry for posts containing '{tag}'" + (f" (stale: {sorted(stale)})" if stale else ""))
    posts = find_all_posts()
    affected = 0
    for path in posts:
        fm, _ = parse_frontmatter(path)
        if not fm or 'tags' not in fm:
            continue
        post_tags = fm['tags']
        if post_tags == [UNLINKED] or tag not in post_tags:
            continue
        # Strip stale ancestors first (only if not still needed by another tag), then recompute
        cleaned = remove_stale_ancestors(post_tags, stale, tags_dict)
        new_tags = recompute(cleaned, tags_dict)
        if new_tags != post_tags:
            show_diff(path, post_tags, new_tags)
            affected += 1
            if apply:
                write_frontmatter_tags(path, new_tags)

    print(f"\n{affected} post(s) affected.")
    if apply:
        log_change(f"move {tag} -> parent={new_parent}", f"{affected} posts", True)


def cmd_recompute_ancestry(args, tags_dict):
    """Rebuild ancestry chains for all posts using current tags.md."""
    apply = '--apply' in args
    post_filter = get_post_filter(args)

    posts = collect_target_posts(post_filter)
    affected = 0
    print(f"\nrecompute-ancestry ({'APPLY' if apply else 'DRY-RUN'})\n")

    for path in posts:
        fm, _ = parse_frontmatter(path)
        if not fm or 'tags' not in fm:
            continue
        post_tags = fm['tags']
        if post_tags == [UNLINKED]:
            continue
        new_tags = recompute(post_tags, tags_dict)
        if new_tags != post_tags:
            show_diff(path, post_tags, new_tags)
            affected += 1
            if apply:
                write_frontmatter_tags(path, new_tags)

    print(f"\n{affected} post(s) affected.")
    if apply:
        log_change("recompute-ancestry", f"{affected} posts", True)


def get_post_filter(args):
    if '--post' in args:
        idx = args.index('--post')
        if idx + 1 < len(args):
            return args[idx + 1]
    return None


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


COMMANDS = {
    'attach': cmd_attach,
    'detach': cmd_detach,
    'rename': cmd_rename,
    'merge': cmd_merge,
    'delete': cmd_delete,
    'move': cmd_move,
    'recompute-ancestry': cmd_recompute_ancestry,
}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]
    if command not in COMMANDS:
        die(f"unknown command: {command}. Use one of: {', '.join(COMMANDS.keys())}")

    tags_dict = parse_tags_md()
    COMMANDS[command](sys.argv[2:], tags_dict)


if __name__ == '__main__':
    main()
