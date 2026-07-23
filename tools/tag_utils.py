"""Shared utilities for tag tools (parsing tags.md, post frontmatter)."""

import re
from pathlib import Path
from config import POSTS_DIR, DRAFTS_DIR

TAGS_FILE = Path(__file__).parent / "tags.md"

# Sentinel ancestry value used by Jekyll for unlinked posts
UNLINKED = "Unlinked"


def parse_tags_md(path=TAGS_FILE):
    """Parse tools/tags.md into a dict of tag definitions.

    Returns:
        dict: {tag_name: {parent, attach_when, attach_policy, solved_ac, auto_companion, note}}
    """
    if not path.exists():
        raise FileNotFoundError(f"tags.md not found at {path}")

    text = path.read_text(encoding='utf-8')
    tags = {}
    current_tag = None
    current_fields = {}

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        # Skip change log section and below
        if line.startswith("# Change Log"):
            break

        # Tag header: [tag-name]
        m = re.match(r'^\[([^\]]+)\]\s*$', line)
        if m:
            # Save previous tag
            if current_tag is not None:
                tags[current_tag] = current_fields
            current_tag = m.group(1).strip()
            current_fields = {
                'parent': None,
                'attach_when': None,
                'attach_policy': None,
                'solved_ac': None,
                'auto_companion': True,
                'note': None,
            }
            continue

        # Empty line ends current tag definition
        if line == '' and current_tag is not None:
            tags[current_tag] = current_fields
            current_tag = None
            current_fields = {}
            continue

        # Field line: key: value
        if current_tag is not None:
            m = re.match(r'^(\w+):\s*(.*)$', line)
            if m:
                key = m.group(1).strip()
                value = m.group(2).strip()
                if key == 'auto_companion':
                    current_fields['auto_companion'] = value.lower() != 'false'
                elif key in current_fields:
                    current_fields[key] = value if value else None

    # Catch the last tag if file doesn't end with blank line
    if current_tag is not None:
        tags[current_tag] = current_fields

    return tags


def compute_ancestry(tag_name, tags_dict):
    """Compute full ancestry chain for a tag (excluding the tag itself).

    Returns list of ancestor tag names from immediate parent to root.
    """
    chain = []
    current = tags_dict.get(tag_name, {}).get('parent')
    seen = set()
    while current:
        if current in seen:
            break  # cycle protection
        seen.add(current)
        chain.append(current)
        current = tags_dict.get(current, {}).get('parent')
    return chain


def expand_with_ancestry(specific_tags, tags_dict):
    """Expand a list of specific tags to include full ancestry.

    Respects auto_companion: false (technique category).
    Returns sorted unique list.
    """
    result = set()
    for tag in specific_tags:
        if tag not in tags_dict:
            result.add(tag)  # unknown tag, leave as-is for audit to catch
            continue
        result.add(tag)
        for ancestor in compute_ancestry(tag, tags_dict):
            if tags_dict.get(ancestor, {}).get('auto_companion', True):
                result.add(ancestor)
    def _depth(tag):
        """Root = 0, each parent hop adds 1."""
        d = 0
        cur = tags_dict.get(tag, {}).get('parent')
        seen = set()
        while cur:
            if cur in seen:
                break
            seen.add(cur)
            d += 1
            cur = tags_dict.get(cur, {}).get('parent')
        return d

    return sorted(result, key=lambda t: (_depth(t), t))


def remove_stale_ancestors(post_tags, stale_set, tags_dict):
    """Remove tags in stale_set from post_tags unless they are still ancestors of another tag.

    Used by move/reparent commands when old ancestry chain differs from new.
    """
    if not stale_set:
        return list(post_tags)
    result = []
    for t in post_tags:
        if t not in stale_set:
            result.append(t)
            continue
        # Check if any other vocab tag in this post still has t as an ancestor
        needed = False
        for other in post_tags:
            if other == t or other not in tags_dict:
                continue
            if t in compute_ancestry(other, tags_dict):
                needed = True
                break
        if needed:
            result.append(t)
    return result


def minimal_specific(flat_tags, tags_dict):
    """Extract the minimal vocab specific set from a flat (ancestry-expanded) tag list.

    A vocab tag is "specific" if no other vocab tag in the list is its descendant.
    Non-vocab tags are excluded from the result (caller preserves them separately if needed).
    Tags with auto_companion=false (e.g., technique) are kept as specific
    (since they wouldn't be auto-added by ancestry expansion).
    """
    valid = [t for t in flat_tags if t in tags_dict]

    # Collect every ancestor that appears in the chains of valid tags
    covered_ancestors = set()
    for t in valid:
        for ancestor in compute_ancestry(t, tags_dict):
            covered_ancestors.add(ancestor)

    # A tag is specific if it's not an ancestor of any other valid tag
    return [t for t in valid if t not in covered_ancestors]


def parse_frontmatter(path):
    """Read a post and return (frontmatter_dict, body_offset).

    Only the `tags` field is parsed (extracted as a list).
    Other fields are returned as raw strings.
    """
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        return None, None

    end = text.find('\n---', 3)
    if end == -1:
        return None, None

    fm_text = text[3:end].strip()
    body_offset = end + 4  # after \n---

    fm = {}
    for line in fm_text.splitlines():
        m = re.match(r'^(\w+):\s*(.*)$', line)
        if not m:
            continue
        key = m.group(1)
        value = m.group(2).strip()
        if key == 'tags':
            # Parse [tag1, tag2] or [Unlinked]
            inner = value.strip('[]').strip()
            if inner:
                fm['tags'] = [t.strip() for t in inner.split(',')]
            else:
                fm['tags'] = []
        else:
            fm[key] = value

    return fm, body_offset


def write_frontmatter_tags(path, new_tags):
    """Update only the `tags` field in a post's frontmatter, preserving everything else.

    Args:
        path: post file path
        new_tags: list of tag names (will be written as `tags: [a, b, c]`)
    """
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        raise ValueError(f"No frontmatter in {path}")

    end = text.find('\n---', 3)
    if end == -1:
        raise ValueError(f"Unterminated frontmatter in {path}")

    fm_text = text[3:end]
    rest = text[end:]

    # Replace tags line
    tags_str = '[' + ', '.join(new_tags) + ']'
    new_fm_lines = []
    found = False
    for line in fm_text.splitlines():
        if re.match(r'^tags:\s*', line):
            new_fm_lines.append(f'tags: {tags_str}')
            found = True
        else:
            new_fm_lines.append(line)

    if not found:
        # Insert tags line before the closing
        new_fm_lines.append(f'tags: {tags_str}')

    new_text = '---' + '\n'.join(new_fm_lines) + rest
    # Preserve leading/trailing newlines around frontmatter
    if not new_text.startswith('---\n'):
        new_text = '---\n' + new_text[3:]
    path.write_text(new_text, encoding='utf-8')


def find_all_posts():
    """Return list of all PS post paths in _posts/ and _drafts/."""
    from code_utils import PS_DIRS
    posts = []
    for base in [POSTS_DIR, DRAFTS_DIR]:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            try:
                if path.relative_to(base).parts[0] in PS_DIRS:
                    posts.append(path)
            except ValueError:
                pass
    return sorted(posts)
