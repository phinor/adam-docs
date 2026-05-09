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
