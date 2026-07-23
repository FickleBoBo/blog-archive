"""Tag audit — verify all posts conform to tools/tags.md vocabulary.

Usage:
    python tag_audit.py              # audit all PS posts
    python tag_audit.py --post 1234  # audit single post by problem number
    python tag_audit.py --vocab      # self-check tags.md only
"""

import sys
from collections import defaultdict
from tag_utils import (
    parse_tags_md,
    parse_frontmatter,
    compute_ancestry,
    find_all_posts,
    UNLINKED,
)
from code_utils import find_posts


class AuditReport:
    def __init__(self):
        self.issues = defaultdict(list)  # category -> [(path, message)]
        self.checked = 0
        self.unlinked = 0

    def add(self, category, path, message):
        self.issues[category].append((path, message))

    def total(self):
        return sum(len(v) for v in self.issues.values())

    def render(self):
        lines = []
        lines.append(f"\n=== Tag Audit Report ===")
        lines.append(f"Posts checked: {self.checked} (unlinked: {self.unlinked})")
        lines.append(f"Total issues: {self.total()}\n")
        if self.total() == 0:
            lines.append("✓ No issues found.")
            return '\n'.join(lines)
        for category, items in sorted(self.issues.items()):
            lines.append(f"[{category}] ({len(items)})")
            for path, msg in items[:20]:
                rel = path.name if hasattr(path, 'name') else str(path)
                lines.append(f"  - {rel}: {msg}")
            if len(items) > 20:
                lines.append(f"  ... and {len(items) - 20} more")
            lines.append("")
        return '\n'.join(lines)


def audit_vocab(tags):
    """Self-check the vocabulary file for internal consistency."""
    issues = []

    # Check parent references
    for name, fields in tags.items():
        parent = fields.get('parent')
        if parent and parent not in tags:
            issues.append(f"[{name}] parent '{parent}' not defined in tags.md")

    # Detect cycles
    for name in tags:
        seen = set()
        current = name
        while current:
            if current in seen:
                issues.append(f"[{name}] cycle detected through {current}")
                break
            seen.add(current)
            current = tags.get(current, {}).get('parent')

    # attach_when must be present (except for category roots that are pure auto-companion)
    for name, fields in tags.items():
        if not fields.get('attach_when'):
            issues.append(f"[{name}] missing attach_when")

    # Naming consistency: lowercase, no double spaces
    for name in tags:
        if name != name.lower():
            issues.append(f"[{name}] not lowercase")
        if '  ' in name:
            issues.append(f"[{name}] contains double space")

    return issues


def audit_post(path, tags, report):
    """Audit a single post against the vocabulary."""
    fm, _ = parse_frontmatter(path)
    if fm is None:
        report.add('no_frontmatter', path, 'no frontmatter found')
        return

    post_tags = fm.get('tags', [])
    if not post_tags:
        report.add('empty_tags', path, 'tags field is empty')
        return

    # Skip Unlinked sentinel posts
    if post_tags == [UNLINKED]:
        report.unlinked += 1
        return

    # 1. Closed vocabulary check
    unknown = [t for t in post_tags if t not in tags]
    for t in unknown:
        report.add('unknown_tag', path, f"unknown tag '{t}'")

    # 2. Ancestry consistency check (option A: full ancestry must be present)
    known_tags = [t for t in post_tags if t in tags]
    expected_ancestry = set()
    for t in known_tags:
        expected_ancestry.add(t)
        for ancestor in compute_ancestry(t, tags):
            # Skip auto_companion: false (technique category)
            if tags.get(ancestor, {}).get('auto_companion', True):
                expected_ancestry.add(ancestor)

    actual = set(post_tags)
    missing = expected_ancestry - actual

    for m in sorted(missing):
        report.add('missing_ancestor', path, f"missing ancestor '{m}'")

    # Note: umbrella standalone is now ALLOWED by design (2026-04-09).
    # All umbrella categories (data structure, graph, dp, string, math, geometry, game theory, etc.)
    # can be attached standalone when no specific child algorithm fits but the classification is core.
    # The previous "orphan_ancestor" check has been removed as it conflicted with this design.

    # 3. auto_companion: false check
    for t in known_tags:
        if not tags.get(t, {}).get('auto_companion', True):
            report.add('forbidden_tag', path, f"tag '{t}' has auto_companion=false (should not be attached)")


def main():
    args = sys.argv[1:]
    tags = parse_tags_md()

    attachable = sum(1 for f in tags.values() if f.get('auto_companion', True))
    nonattachable = len(tags) - attachable
    print(f"Loaded {len(tags)} vocab entries from tools/tags.md ({attachable} attachable + {nonattachable} auto_companion=false)")

    if '--vocab' in args:
        issues = audit_vocab(tags)
        if issues:
            print(f"\n[vocab] {len(issues)} issues:")
            for i in issues:
                print(f"  - {i}")
            sys.exit(1)
        print("✓ Vocabulary self-check passed.")
        return

    # Always run vocab check first
    vocab_issues = audit_vocab(tags)
    if vocab_issues:
        print(f"\n[vocab] {len(vocab_issues)} issues found in tags.md:")
        for i in vocab_issues:
            print(f"  - {i}")
        print("\nFix tags.md before auditing posts.")
        sys.exit(1)

    # Determine posts to audit
    if '--post' in args:
        idx = args.index('--post')
        if idx + 1 >= len(args):
            print("--post requires a problem number")
            sys.exit(2)
        number = args[idx + 1]
        posts = find_posts(number)
    else:
        posts = find_all_posts()

    report = AuditReport()
    for path in posts:
        report.checked += 1
        audit_post(path, tags, report)

    print(report.render())
    sys.exit(0 if report.total() == 0 else 1)


if __name__ == '__main__':
    main()
