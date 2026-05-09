# Readable Anchor Slugs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the random `{#h-xxx}` anchors on every heading in `docs/*.md` with readable slugs auto-generated from heading text, and rewrite all internal references to match.

**Architecture:** A single Python 3 script in `scripts/rewrite_anchors.py` that runs in two phases. Phase 1 walks every markdown file, parses headings, computes auto-slugs that match MkDocs' `toc` extension, detects intra-file collisions (resolved by prepending parent-section slug), and emits `scripts/anchor_mapping.json`. Phase 2 reads that mapping, deletes `{#h-xxx}` anchors from headings (writing explicit `{#slug}` only where collision disambiguation requires it), and rewrites every `(#h-xxx)` and `(file.md#h-xxx)` reference. Orphan references (no matching heading) are warned about but left untouched.

**Tech Stack:** Python 3 standard library only (re, unicodedata, json, pathlib, argparse). No third-party deps — the slugify algorithm is reimplemented to match `markdown.extensions.toc.slugify`. Tests use unittest from stdlib.

**Spec:** `docs/superpowers/specs/2026-05-09-readable-anchor-slugs-design.md`

---

## File Structure

- **Create:** `scripts/rewrite_anchors.py` — the rewriter (single file, ~250 LOC)
- **Create:** `scripts/test_rewrite_anchors.py` — unit tests
- **Create (transient):** `scripts/anchor_mapping.json` — emitted by Phase 1, deleted after Phase 2 succeeds
- **Modify:** all 95 files in `docs/*.md`

The rewriter is internally split into pure functions:
- `slugify(text: str) -> str` — matches MkDocs' toc slugify
- `strip_inline_markdown(text: str) -> str` — removes `*`, `_`, backticks, link wrappers
- `parse_heading(line: str) -> Optional[Heading]` — extracts level, text, optional `{#h-xxx}` id
- `build_file_mapping(headings: list[Heading]) -> list[MappingEntry]` — slug + collision resolution
- `rewrite_headings(text: str, entries: list[MappingEntry]) -> str` — strip/replace `{#h-xxx}` on heading lines
- `rewrite_references(text: str, current_file: str, lookup: dict) -> tuple[str, list[Orphan]]` — link rewrite

Each is independently testable. The CLI (`--plan` / `--apply`) is a thin shell over them.

---

## Task 1: Bootstrap script skeleton + test runner

**Files:**
- Create: `scripts/rewrite_anchors.py`
- Create: `scripts/test_rewrite_anchors.py`

- [ ] **Step 1: Create the script skeleton**

Write `scripts/rewrite_anchors.py`:

```python
#!/usr/bin/env python3
"""
Replace random {#h-xxx} anchors with readable heading-derived slugs.

Phase 1 (--plan): Build scripts/anchor_mapping.json from current headings.
Phase 2 (--apply): Apply mapping to docs/*.md and rewrite references.

See docs/superpowers/specs/2026-05-09-readable-anchor-slugs-design.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
MAPPING_PATH = REPO_ROOT / "scripts" / "anchor_mapping.json"


@dataclass
class Heading:
    level: int            # 1..6
    text: str             # raw heading text (with markdown formatting still in place)
    old_id: Optional[str] # e.g. "h-fk74mpuqoguv" or None if heading had no explicit id
    line_index: int       # 0-based index into the file's lines


@dataclass
class MappingEntry:
    old_id: Optional[str] # may be None (heading had no explicit anchor)
    new_slug: str
    explicit: bool        # True => write {#new_slug} into source (collision override)
    heading: str          # cleaned heading text, for human review
    line_index: int


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="phase", required=True)
    sub.add_parser("plan", help="Phase 1: build anchor_mapping.json")
    sub.add_parser("apply", help="Phase 2: apply anchor_mapping.json")
    args = parser.parse_args(argv)

    if args.phase == "plan":
        return run_plan()
    if args.phase == "apply":
        return run_apply()
    return 1


def run_plan() -> int:
    raise NotImplementedError


def run_apply() -> int:
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 2: Create the test file with one trivial passing test**

Write `scripts/test_rewrite_anchors.py`:

```python
"""Tests for scripts/rewrite_anchors.py."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rewrite_anchors as ra  # noqa: E402


class TestSmoke(unittest.TestCase):
    def test_module_imports(self):
        self.assertTrue(hasattr(ra, "main"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run tests to verify wiring**

Run: `python3 scripts/test_rewrite_anchors.py -v`
Expected: `test_module_imports ... ok` and `OK`.

- [ ] **Step 4: Commit**

```bash
git add scripts/rewrite_anchors.py scripts/test_rewrite_anchors.py
git commit -m "NEW: Skeleton for anchor rewrite script"
```

---

## Task 2: Slugify (matches MkDocs toc slugify)

**Files:**
- Modify: `scripts/rewrite_anchors.py`
- Modify: `scripts/test_rewrite_anchors.py`

The MkDocs `toc` extension uses `markdown.extensions.toc.slugify`, which is:
1. NFKD-normalize the input
2. Encode to ASCII, dropping non-ASCII codepoints
3. Substitute everything that is not `\w`, whitespace, or `-` with empty string
4. Strip whitespace, lowercase
5. Replace runs of whitespace + `-` with the separator

Before slugifying, we strip inline markdown so `**Foo**` → `Foo` (otherwise `**` survives the punctuation strip but introduces nothing — actually it gets removed because `*` is not `\w` — but link wrappers `[text](url)` would leave the URL behind, which is wrong).

- [ ] **Step 1: Write failing tests for `slugify`**

Append to `scripts/test_rewrite_anchors.py` before the `if __name__` line:

```python
class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(ra.slugify("Naming of Photographs"), "naming-of-photographs")

    def test_lowercases(self):
        self.assertEqual(ra.slugify("UPPER Case"), "upper-case")

    def test_strips_apostrophe(self):
        # Matches markdown.extensions.toc.slugify default behaviour.
        self.assertEqual(ra.slugify("ADAM's Settings"), "adams-settings")

    def test_collapses_multiple_spaces(self):
        self.assertEqual(ra.slugify("Foo   Bar"), "foo-bar")

    def test_strips_punctuation(self):
        self.assertEqual(ra.slugify("Hello, World!"), "hello-world")

    def test_keeps_hyphens(self):
        self.assertEqual(ra.slugify("Pre-Existing"), "pre-existing")

    def test_empty_after_strip(self):
        self.assertEqual(ra.slugify("!!!"), "")

    def test_unicode_ascii_fold(self):
        # NFKD then drop non-ASCII; "ñ" decomposes to "n" + combining tilde,
        # combining mark is non-ASCII so dropped → "n".
        self.assertEqual(ra.slugify("piñata"), "pinata")
```

- [ ] **Step 2: Write failing tests for `strip_inline_markdown`**

Append to the same test file:

```python
class TestStripInlineMarkdown(unittest.TestCase):
    def test_bold(self):
        self.assertEqual(ra.strip_inline_markdown("**Foo Bar**"), "Foo Bar")

    def test_italic_asterisk(self):
        self.assertEqual(ra.strip_inline_markdown("*Foo*"), "Foo")

    def test_italic_underscore(self):
        self.assertEqual(ra.strip_inline_markdown("_Foo_"), "Foo")

    def test_inline_code(self):
        self.assertEqual(ra.strip_inline_markdown("Use `git push`"), "Use git push")

    def test_link(self):
        self.assertEqual(ra.strip_inline_markdown("See [docs](http://x)"), "See docs")

    def test_mixed(self):
        self.assertEqual(
            ra.strip_inline_markdown("**Bold** and *italic* and `code`"),
            "Bold and italic and code",
        )
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 scripts/test_rewrite_anchors.py -v`
Expected: errors on `slugify` and `strip_inline_markdown` (not yet defined).

- [ ] **Step 4: Implement `strip_inline_markdown` and `slugify`**

Add to `scripts/rewrite_anchors.py` (above `main`):

```python
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_CODE_RE = re.compile(r"`([^`]+)`")
_EMPH_RE = re.compile(r"(\*{1,3}|_{1,3})(.+?)\1")


def strip_inline_markdown(text: str) -> str:
    """Remove markdown formatting that shouldn't appear in an anchor slug."""
    text = _LINK_RE.sub(r"\1", text)
    text = _CODE_RE.sub(r"\1", text)
    # Repeat emphasis pass to handle nested *_x_*-style cases.
    prev = None
    while prev != text:
        prev = text
        text = _EMPH_RE.sub(r"\2", text)
    return text


def slugify(text: str, separator: str = "-") -> str:
    """Match markdown.extensions.toc.slugify (default Python-Markdown slugifier)."""
    text = strip_inline_markdown(text)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", separator, text)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 scripts/test_rewrite_anchors.py -v`
Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/rewrite_anchors.py scripts/test_rewrite_anchors.py
git commit -m "NEW: slugify matching markdown.extensions.toc"
```

---

## Task 3: Heading parser

Heading lines look like `# Title {#h-xxx}` or `## Title` (no anchor). Indented headings are not real headings in MkDocs (kramdown-style); we only match a `#` at column 0. Headings inside fenced code blocks must be ignored.

**Files:**
- Modify: `scripts/rewrite_anchors.py`
- Modify: `scripts/test_rewrite_anchors.py`

- [ ] **Step 1: Write failing tests for `parse_heading` and `iter_headings`**

Append:

```python
class TestParseHeading(unittest.TestCase):
    def test_h1_with_anchor(self):
        h = ra.parse_heading("# Staff Photographs {#h-evbfhabz0cr1}", line_index=0)
        self.assertIsNotNone(h)
        self.assertEqual(h.level, 1)
        self.assertEqual(h.text, "Staff Photographs")
        self.assertEqual(h.old_id, "h-evbfhabz0cr1")

    def test_h2_no_anchor(self):
        h = ra.parse_heading("## Some Section", line_index=5)
        self.assertIsNotNone(h)
        self.assertEqual(h.level, 2)
        self.assertEqual(h.text, "Some Section")
        self.assertIsNone(h.old_id)

    def test_h4_with_formatting(self):
        h = ra.parse_heading("#### **Bold** Heading {#h-abc}", line_index=2)
        self.assertEqual(h.level, 4)
        self.assertEqual(h.text, "**Bold** Heading")
        self.assertEqual(h.old_id, "h-abc")

    def test_not_a_heading(self):
        self.assertIsNone(ra.parse_heading("Just text", line_index=0))
        self.assertIsNone(ra.parse_heading("    # Indented", line_index=0))
        self.assertIsNone(ra.parse_heading("#NoSpace", line_index=0))

    def test_strips_trailing_anchor_only_when_id_starts_with_h_dash(self):
        # Other {#x} would also match in real markdown, but we only care about
        # the h-xxx form for migration.
        h = ra.parse_heading("# Foo {#custom}", line_index=0)
        self.assertIsNotNone(h)
        self.assertEqual(h.text, "Foo {#custom}")
        self.assertIsNone(h.old_id)


class TestIterHeadings(unittest.TestCase):
    def test_skips_code_fences(self):
        text = "\n".join([
            "# Real Heading {#h-1}",
            "",
            "```",
            "# Not a heading {#h-2}",
            "```",
            "",
            "## Another {#h-3}",
        ])
        headings = list(ra.iter_headings(text))
        self.assertEqual([h.old_id for h in headings], ["h-1", "h-3"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 scripts/test_rewrite_anchors.py -v`
Expected: errors on `parse_heading` / `iter_headings`.

- [ ] **Step 3: Implement `parse_heading` and `iter_headings`**

Add to `scripts/rewrite_anchors.py` (above `main`):

```python
_HEADING_RE = re.compile(r"^(#{1,6}) +(.+?)\s*$")
_TRAILING_HID_RE = re.compile(r"\s*\{#(h-[a-z0-9]+)\}\s*$")


def parse_heading(line: str, line_index: int) -> Optional[Heading]:
    m = _HEADING_RE.match(line)
    if not m:
        return None
    level = len(m.group(1))
    rest = m.group(2)
    old_id = None
    hid_match = _TRAILING_HID_RE.search(rest)
    if hid_match:
        old_id = hid_match.group(1)
        rest = rest[: hid_match.start()].rstrip()
    return Heading(level=level, text=rest, old_id=old_id, line_index=line_index)


def iter_headings(text: str):
    """Yield Heading objects, skipping content inside ``` fenced blocks."""
    in_fence = False
    for i, line in enumerate(text.splitlines()):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        h = parse_heading(line, line_index=i)
        if h is not None:
            yield h
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 scripts/test_rewrite_anchors.py -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/rewrite_anchors.py scripts/test_rewrite_anchors.py
git commit -m "NEW: heading parser with code-fence awareness"
```

---

## Task 4: Per-file mapping with collision resolution

When two headings on the same page produce the same slug, walk up the heading hierarchy (latest higher-level heading) and prepend its slug. Repeat until unique. The result is an **explicit** entry that must be written into the source as `{#new_slug}`.

**Files:**
- Modify: `scripts/rewrite_anchors.py`
- Modify: `scripts/test_rewrite_anchors.py`

- [ ] **Step 1: Write failing tests for `build_file_mapping`**

Append:

```python
class TestBuildFileMapping(unittest.TestCase):
    def _h(self, level, text, old_id="h-x"):
        return ra.Heading(level=level, text=text, old_id=old_id, line_index=0)

    def test_no_collisions(self):
        headings = [
            self._h(1, "Staff Photographs", "h-1"),
            self._h(2, "Naming of Photographs", "h-2"),
            self._h(2, "Uploading Staff Photographs", "h-3"),
        ]
        entries = ra.build_file_mapping(headings)
        self.assertEqual([(e.old_id, e.new_slug, e.explicit) for e in entries], [
            ("h-1", "staff-photographs", False),
            ("h-2", "naming-of-photographs", False),
            ("h-3", "uploading-staff-photographs", False),
        ])

    def test_collision_disambiguated_by_parent(self):
        headings = [
            self._h(1, "Assessment Management", "h-1"),
            self._h(2, "Overview", "h-2"),
            self._h(1, "Mark Book Administration", "h-3"),
            self._h(2, "Overview", "h-4"),
        ]
        entries = ra.build_file_mapping(headings)
        # First Overview keeps the bare slug; second one gets disambiguated.
        bare = [e for e in entries if e.old_id == "h-2"][0]
        dup = [e for e in entries if e.old_id == "h-4"][0]
        self.assertEqual(bare.new_slug, "overview")
        self.assertFalse(bare.explicit)
        self.assertEqual(dup.new_slug, "mark-book-administration-overview")
        self.assertTrue(dup.explicit)

    def test_empty_slug_falls_back_to_section_n(self):
        headings = [
            self._h(1, "!!!", "h-1"),
            self._h(2, "Real", "h-2"),
        ]
        entries = ra.build_file_mapping(headings)
        self.assertEqual(entries[0].new_slug, "section-1")
        self.assertTrue(entries[0].explicit)

    def test_three_way_collision(self):
        # Two ancestors share the same H1 → second-pass climb still collides.
        headings = [
            self._h(1, "Foo", "h-1"),
            self._h(2, "Bar", "h-2"),
            self._h(2, "Bar", "h-3"),
            self._h(2, "Bar", "h-4"),
        ]
        entries = ra.build_file_mapping(headings)
        slugs = [e.new_slug for e in entries]
        # All slugs unique.
        self.assertEqual(len(set(slugs)), len(slugs))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 scripts/test_rewrite_anchors.py -v`

- [ ] **Step 3: Implement `build_file_mapping`**

Add to `scripts/rewrite_anchors.py` (above `main`):

```python
def build_file_mapping(headings: list[Heading]) -> list[MappingEntry]:
    """
    Compute new slugs for a single file's headings, disambiguating collisions
    by prepending the slug of the nearest higher-level ancestor heading until
    the result is unique. As a last resort, append a numeric suffix.
    """
    natural_slugs: list[str] = []
    for h in headings:
        s = slugify(h.text)
        natural_slugs.append(s)

    # Build ancestor index: for each heading i, list of indices j<i where
    # headings[j].level < headings[i].level, in reverse order (nearest first).
    ancestors: list[list[int]] = []
    stack: list[int] = []
    for i, h in enumerate(headings):
        while stack and headings[stack[-1]].level >= h.level:
            stack.pop()
        ancestors.append(list(reversed(stack)))
        stack.append(i)

    used: set[str] = set()
    entries: list[MappingEntry] = []
    for i, h in enumerate(headings):
        natural = natural_slugs[i]
        if not natural:
            # Empty after stripping — fall back to section-N (1-based).
            slug = f"section-{i + 1}"
            explicit = True
        elif natural not in used:
            slug = natural
            explicit = False
        else:
            # Climb ancestors prepending their natural slugs.
            slug = natural
            for j in ancestors[i]:
                anc_slug = natural_slugs[j] or f"section-{j + 1}"
                slug = f"{anc_slug}-{natural}"
                if slug not in used:
                    break
            # If still colliding, append numeric suffix.
            if slug in used:
                n = 2
                while f"{slug}-{n}" in used:
                    n += 1
                slug = f"{slug}-{n}"
            explicit = True

        used.add(slug)
        entries.append(MappingEntry(
            old_id=h.old_id,
            new_slug=slug,
            explicit=explicit,
            heading=strip_inline_markdown(h.text),
            line_index=h.line_index,
        ))
    return entries
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 scripts/test_rewrite_anchors.py -v`

- [ ] **Step 5: Commit**

```bash
git add scripts/rewrite_anchors.py scripts/test_rewrite_anchors.py
git commit -m "NEW: per-file mapping with parent-context collision resolution"
```

---

## Task 5: Reference rewriter

Rewrites two link forms in the body of a file:

- Intra-page: `](#h-xxx)` → `](#new_slug)` using the *current file's* mapping.
- Cross-page: `](other.md#h-xxx)` → `](other.md#new_slug)` using the global lookup keyed by `(target_file, h-xxx)`.

References whose target isn't in the lookup are orphans: leave the link untouched, return them in a list for warning.

Skip references inside fenced code blocks.

**Files:**
- Modify: `scripts/rewrite_anchors.py`
- Modify: `scripts/test_rewrite_anchors.py`

- [ ] **Step 1: Write failing tests**

Append:

```python
class TestRewriteReferences(unittest.TestCase):
    def test_intra_page(self):
        text = "See [the section](#h-abc) for details."
        lookup = {("foo.md", "h-abc"): "the-section"}
        new, orphans = ra.rewrite_references(text, "foo.md", lookup)
        self.assertEqual(new, "See [the section](#the-section) for details.")
        self.assertEqual(orphans, [])

    def test_cross_page(self):
        text = "See [overview](other.md#h-xyz)."
        lookup = {("other.md", "h-xyz"): "overview"}
        new, orphans = ra.rewrite_references(text, "foo.md", lookup)
        self.assertEqual(new, "See [overview](other.md#overview).")
        self.assertEqual(orphans, [])

    def test_orphan_left_alone(self):
        text = "See [missing](#h-gone)."
        lookup = {}
        new, orphans = ra.rewrite_references(text, "foo.md", lookup)
        self.assertEqual(new, text)
        self.assertEqual(len(orphans), 1)
        self.assertEqual(orphans[0], ("foo.md", "foo.md", "h-gone"))

    def test_skips_code_fence(self):
        text = "\n".join([
            "Real [link](#h-a).",
            "```",
            "Fake [link](#h-a).",
            "```",
            "Another [link](#h-a).",
        ])
        lookup = {("foo.md", "h-a"): "alpha"}
        new, _ = ra.rewrite_references(text, "foo.md", lookup)
        lines = new.splitlines()
        self.assertEqual(lines[0], "Real [link](#alpha).")
        self.assertEqual(lines[2], "Fake [link](#h-a).")  # untouched inside fence
        self.assertEqual(lines[4], "Another [link](#alpha).")

    def test_does_not_match_non_h_anchors(self):
        text = "See [x](#section-1)."
        lookup = {}
        new, orphans = ra.rewrite_references(text, "foo.md", lookup)
        self.assertEqual(new, text)
        self.assertEqual(orphans, [])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 scripts/test_rewrite_anchors.py -v`

- [ ] **Step 3: Implement `rewrite_references`**

Add to `scripts/rewrite_anchors.py`:

```python
_REF_RE = re.compile(r"\]\(([a-z0-9][a-z0-9_-]*\.md)?#(h-[a-z0-9]+)\)")


def rewrite_references(text: str, current_file: str, lookup: dict[tuple[str, str], str]):
    """
    Rewrite ](#h-xxx) and ](file.md#h-xxx) references using lookup.
    Returns (new_text, orphans). Each orphan is (source_file, target_file, old_id).
    """
    orphans: list[tuple[str, str, str]] = []
    out_lines: list[str] = []
    in_fence = False

    def replace(match: re.Match) -> str:
        target_file = match.group(1) or current_file
        old_id = match.group(2)
        new_slug = lookup.get((target_file, old_id))
        if new_slug is None:
            orphans.append((current_file, target_file, old_id))
            return match.group(0)
        prefix = match.group(1) or ""
        return f"]({prefix}#{new_slug})"

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        out_lines.append(_REF_RE.sub(replace, line))
    return "".join(out_lines), orphans
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 scripts/test_rewrite_anchors.py -v`

- [ ] **Step 5: Commit**

```bash
git add scripts/rewrite_anchors.py scripts/test_rewrite_anchors.py
git commit -m "NEW: reference rewriter with code-fence awareness"
```

---

## Task 6: Heading rewriter (strip / replace `{#h-xxx}`)

Given the file text and the per-file mapping entries, modify each heading line so that:
- `{#h-xxx}` is removed if `explicit=False`.
- `{#h-xxx}` is replaced with `{#new_slug}` if `explicit=True`.
- Heading lines without an `old_id` and `explicit=True` get `{#new_slug}` appended (e.g., the empty-slug fallback case where the source had no anchor at all).

**Files:**
- Modify: `scripts/rewrite_anchors.py`
- Modify: `scripts/test_rewrite_anchors.py`

- [ ] **Step 1: Write failing tests**

Append:

```python
class TestRewriteHeadings(unittest.TestCase):
    def test_strip_when_not_explicit(self):
        text = "# Foo {#h-a}\n\nbody\n"
        entries = [ra.MappingEntry(old_id="h-a", new_slug="foo", explicit=False, heading="Foo", line_index=0)]
        out = ra.rewrite_headings(text, entries)
        self.assertEqual(out, "# Foo\n\nbody\n")

    def test_replace_when_explicit(self):
        text = "## Overview {#h-b}\n"
        entries = [ra.MappingEntry(old_id="h-b", new_slug="mark-book-overview", explicit=True, heading="Overview", line_index=0)]
        out = ra.rewrite_headings(text, entries)
        self.assertEqual(out, "## Overview {#mark-book-overview}\n")

    def test_append_when_no_old_id_but_explicit(self):
        text = "# !!!\n"
        entries = [ra.MappingEntry(old_id=None, new_slug="section-1", explicit=True, heading="!!!", line_index=0)]
        out = ra.rewrite_headings(text, entries)
        self.assertEqual(out, "# !!! {#section-1}\n")

    def test_leaves_other_lines_alone(self):
        text = "# Foo {#h-a}\nSome [link](#h-a) stays as-is here.\n"
        entries = [ra.MappingEntry(old_id="h-a", new_slug="foo", explicit=False, heading="Foo", line_index=0)]
        out = ra.rewrite_headings(text, entries)
        self.assertEqual(out, "# Foo\nSome [link](#h-a) stays as-is here.\n")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 scripts/test_rewrite_anchors.py -v`

- [ ] **Step 3: Implement `rewrite_headings`**

Add to `scripts/rewrite_anchors.py`:

```python
def rewrite_headings(text: str, entries: list[MappingEntry]) -> str:
    """Rewrite each entry's heading line: strip or replace its {#h-xxx}."""
    by_line = {e.line_index: e for e in entries}
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        e = by_line.get(i)
        if e is None:
            continue
        # Preserve the trailing newline (if any) while editing the body.
        body = line.rstrip("\n")
        eol = line[len(body):]
        # Strip an existing trailing {#h-xxx}, if present.
        body = re.sub(r"\s*\{#h-[a-z0-9]+\}\s*$", "", body)
        if e.explicit:
            body = f"{body} {{#{e.new_slug}}}"
        lines[i] = body + eol
    return "".join(lines)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 scripts/test_rewrite_anchors.py -v`

- [ ] **Step 5: Commit**

```bash
git add scripts/rewrite_anchors.py scripts/test_rewrite_anchors.py
git commit -m "NEW: heading-line rewriter (strip or replace anchor)"
```

---

## Task 7: Wire up `--plan` and `--apply`

**Files:**
- Modify: `scripts/rewrite_anchors.py`

- [ ] **Step 1: Implement `run_plan`**

Replace the `run_plan` stub:

```python
def run_plan() -> int:
    md_files = sorted(p for p in DOCS_DIR.glob("*.md"))
    by_file: dict[str, list[dict]] = {}
    lookup: dict[str, str] = {}

    total_entries = 0
    total_collisions = 0

    for path in md_files:
        rel = path.relative_to(DOCS_DIR).as_posix()
        text = path.read_text(encoding="utf-8")
        headings = list(iter_headings(text))
        entries = build_file_mapping(headings)
        by_file[rel] = [asdict(e) for e in entries]
        for e in entries:
            if e.old_id is not None:
                lookup[f"{rel}#{e.old_id}"] = e.new_slug
        total_entries += len(entries)
        total_collisions += sum(1 for e in entries if e.explicit)

    MAPPING_PATH.write_text(
        json.dumps({"by_file": by_file, "lookup": lookup}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {MAPPING_PATH.relative_to(REPO_ROOT)}")
    print(f"  files: {len(md_files)}")
    print(f"  headings: {total_entries}")
    print(f"  explicit (collision/empty): {total_collisions}")
    if total_collisions:
        print("  explicit slugs (review these):")
        for rel, items in by_file.items():
            for item in items:
                if item["explicit"]:
                    print(f"    {rel}: {item['new_slug']}  <- {item['heading']!r}")
    return 0
```

- [ ] **Step 2: Implement `run_apply`**

Replace the `run_apply` stub:

```python
def run_apply() -> int:
    if not MAPPING_PATH.exists():
        print(f"ERROR: {MAPPING_PATH} not found. Run --plan first.", file=sys.stderr)
        return 2
    data = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    by_file: dict[str, list[dict]] = data["by_file"]

    # Build the (target_file, old_id) -> new_slug lookup expected by rewrite_references.
    ref_lookup: dict[tuple[str, str], str] = {}
    for rel, items in by_file.items():
        for item in items:
            if item["old_id"] is not None:
                ref_lookup[(rel, item["old_id"])] = item["new_slug"]

    files_modified = 0
    refs_rewritten = 0
    all_orphans: list[tuple[str, str, str]] = []

    for rel, items in by_file.items():
        path = DOCS_DIR / rel
        original = path.read_text(encoding="utf-8")
        entries = [MappingEntry(**item) for item in items]
        # Heading rewrite first, then reference rewrite (reference rewrite
        # ignores heading lines anyway because they don't match _REF_RE).
        new_text = rewrite_headings(original, entries)
        new_text, orphans = rewrite_references(new_text, rel, ref_lookup)
        all_orphans.extend(orphans)
        # Count rewrites by diffing reference occurrences.
        before_refs = len(re.findall(r"\]\([a-z0-9_.-]*#h-[a-z0-9]+\)", original))
        after_refs = len(re.findall(r"\]\([a-z0-9_.-]*#h-[a-z0-9]+\)", new_text))
        refs_rewritten += before_refs - after_refs
        if new_text != original:
            path.write_text(new_text, encoding="utf-8")
            files_modified += 1

    print(f"Files modified: {files_modified}")
    print(f"References rewritten: {refs_rewritten}")
    print(f"Orphan references (left as-is): {len(all_orphans)}")
    for src, tgt, old_id in all_orphans:
        print(f"  ORPHAN: {src} -> {tgt}#{old_id}")
    return 0
```

- [ ] **Step 3: Smoke test the CLI on a temporary scratch dir**

Run:

```bash
python3 -c "
import sys, tempfile, pathlib, shutil, os
sys.path.insert(0, 'scripts')
import rewrite_anchors as ra
tmp = pathlib.Path(tempfile.mkdtemp())
docs = tmp / 'docs'
docs.mkdir()
(docs / 'a.md').write_text('# Foo {#h-1}\n\nSee [b](b.md#h-2).\n')
(docs / 'b.md').write_text('# Bar {#h-2}\n\nSee [a](a.md#h-1).\n')
ra.DOCS_DIR = docs
ra.MAPPING_PATH = tmp / 'mapping.json'
assert ra.run_plan() == 0
assert ra.run_apply() == 0
print('---a.md---')
print((docs/'a.md').read_text())
print('---b.md---')
print((docs/'b.md').read_text())
shutil.rmtree(tmp)
"
```

Expected output (between the `---` markers):
```
# Foo

See [b](b.md#bar).
```
and
```
# Bar

See [a](a.md#foo).
```

- [ ] **Step 4: Commit**

```bash
git add scripts/rewrite_anchors.py
git commit -m "NEW: --plan and --apply CLI for anchor rewrite"
```

---

## Task 8: Run Phase 1 against `docs/`, review mapping

**Files:**
- Create (transient): `scripts/anchor_mapping.json`

- [ ] **Step 1: Run `--plan`**

Run: `python3 scripts/rewrite_anchors.py plan`

Expected: prints file/heading counts, lists every `explicit` slug for review. The mapping file is written to `scripts/anchor_mapping.json`.

- [ ] **Step 2: Sanity-check the mapping**

Run:

```bash
# Confirm every old h-xxx anchor is mapped.
python3 -c "
import json, re, pathlib
data = json.loads(pathlib.Path('scripts/anchor_mapping.json').read_text())
mapped = {(f, item['old_id']) for f, items in data['by_file'].items() for item in items if item['old_id']}
defined = set()
for p in sorted(pathlib.Path('docs').glob('*.md')):
    for m in re.finditer(r'\{#(h-[a-z0-9]+)\}', p.read_text()):
        defined.add((p.name, m.group(1)))
missing = defined - mapped
print('defined:', len(defined), 'mapped:', len(mapped), 'missing:', len(missing))
assert not missing, missing
"
```

Expected: `missing: 0`.

- [ ] **Step 3: Eyeball every explicit slug printed in Step 1**

Look for any disambiguated slug that reads poorly (e.g. unhelpful parent prefix). If any look bad, edit `scripts/anchor_mapping.json` directly to override the `new_slug` field for that entry. (Setting `explicit: true` keeps the slug in the source.)

- [ ] **Step 4 (no commit yet)**

The mapping is transient and will be deleted at the end of Task 9.

---

## Task 9: Run Phase 2, verify, commit

**Files:**
- Modify: all 95 `docs/*.md` files
- Delete: `scripts/anchor_mapping.json`

- [ ] **Step 1: Run `--apply`**

Run: `python3 scripts/rewrite_anchors.py apply`

Expected: prints "Files modified: ~95", "References rewritten: ~372", and an orphan count. Note any orphans for manual follow-up.

- [ ] **Step 2: Verify no `#h-` survives outside fenced code blocks**

Run:

```bash
# Should print nothing (or only orphans you've already noted).
grep -rn "{#h-" docs/ || echo OK
grep -rnE "\]\([a-z0-9_.-]*#h-[a-z0-9]+\)" docs/ || echo OK
```

Expected: `OK` for the first grep. Second grep should print only the orphans previously reported by `--apply` (if any).

- [ ] **Step 3: Spot-check 5 random pages**

Run: `ls docs/*.md | shuf -n 5`

For each one printed, open it and confirm:
- No `{#h-xxx}` remains on heading lines.
- Any `{#slug}` present is a real disambiguation (not a left-over).
- Internal links use readable slugs.

- [ ] **Step 4: Build the site and confirm it still builds**

Run via Docker (matches deployment):

```bash
docker run --rm --user "$(id -u):$(id -g)" \
    -v "$(pwd):/docs" -w /docs \
    squidfunk/mkdocs-material:latest build --strict --site-dir /tmp/site-check
```

Expected: build succeeds. `--strict` makes any internal-link warning fatal — if a slug doesn't match the algorithm MkDocs uses, this will surface it.

If Docker isn't available, install MkDocs in a venv with `pip` and run `mkdocs build --strict`.

- [ ] **Step 5: Confirm rendered IDs match expectations**

```bash
grep -oE 'id="[^"]+"' /tmp/site-check/staff-photographs.html | head -10
```

Expected: IDs like `id="naming-of-photographs"` rather than `id="h-fk74mpuqoguv"`.

- [ ] **Step 6: Run the full test suite once more**

Run: `python3 scripts/test_rewrite_anchors.py -v`
Expected: all tests pass.

- [ ] **Step 7: Delete the transient mapping**

Run: `rm scripts/anchor_mapping.json`

- [ ] **Step 8: Commit the rewritten docs**

```bash
git add docs/
git commit -m "$(cat <<'EOF'
CHANGED: Replace random h-xxx anchors with readable slugs

Removed every {#h-xxx} from headings in docs/*.md and rewrote all
intra-page and cross-page references to use slugs derived from heading
text (matching markdown.extensions.toc.slugify). Explicit {#slug} is
kept only where collision disambiguation requires it.

See docs/superpowers/specs/2026-05-09-readable-anchor-slugs-design.md
EOF
)"
```

- [ ] **Step 9: Verify clean working tree**

Run: `git status`
Expected: clean (no untracked `anchor_mapping.json`, no leftover edits).

---

## Self-Review

**Spec coverage:**
- Goals 1 (replace random anchors), 2 (update references), 3 (clean source unless collision), 4 (mkdocs build still works) — all covered by Tasks 6–9.
- Slug algorithm — Task 2 (matches the spec's six-step description).
- Phase 1 / Phase 2 architecture — Tasks 7–9.
- Edge cases:
  - Empty slug fallback to `section-N` — Task 4.
  - Intra-file collisions via parent-prefix — Task 4.
  - Orphan references — Task 5 + reported in Task 9.
  - Code fences — Tasks 3 (heading parser) and 5 (reference rewriter).
  - HTML blocks — implicitly handled (the reference rewriter only matches markdown link syntax `](...)`, so a raw `<a href="#h-xxx">` would be left alone — flag if any exist via grep in Task 9 Step 2).

**Placeholder scan:** none.

**Type/name consistency:** `Heading`, `MappingEntry`, `slugify`, `strip_inline_markdown`, `parse_heading`, `iter_headings`, `build_file_mapping`, `rewrite_references`, `rewrite_headings`, `run_plan`, `run_apply` — names used identically across all tasks. CLI subcommands are `plan` and `apply` (not `--plan`/`--apply` flags) — referenced consistently in Tasks 7–9.
