#!/usr/bin/env python3
"""
Replace random {#h-xxx} anchors with readable heading-derived slugs.

Phase 1 (plan):  build scripts/anchor_mapping.json from current headings.
Phase 2 (apply): apply mapping to docs/*.md and rewrite references.

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
    level: int
    text: str
    old_id: Optional[str]
    line_index: int


@dataclass
class MappingEntry:
    old_id: Optional[str]
    new_slug: str
    explicit: bool
    heading: str
    line_index: int


_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_CODE_RE = re.compile(r"`([^`]+)`")
_EMPH_RE = re.compile(r"(\*{1,3}|_{1,3})(.+?)\1")


def strip_inline_markdown(text: str) -> str:
    """Remove markdown formatting that shouldn't appear in an anchor slug."""
    text = _LINK_RE.sub(r"\1", text)
    text = _CODE_RE.sub(r"\1", text)
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
