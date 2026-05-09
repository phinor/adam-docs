# Readable Anchor Slugs — Design

## Background

Every heading in `docs/*.md` carries an explicit anchor of the form `{#h-<random>}` (e.g. `## Naming of Photographs {#h-fk74mpuqoguv}`). There are 1,376 such anchors across 95 files. Internal links target them with `(#h-xxx)` and `(file.md#h-xxx)` — 372 reference occurrences spanning 111 unique anchor IDs.

These IDs are unreadable: a URL like `…/staff-photographs.html#h-fk74mpuqoguv` gives a reader no clue what section it points to. The goal is to replace them with slugs derived from the heading text (e.g. `#naming-of-photographs`).

## Goals

- Replace the random `h-xxx` anchor scheme with readable, heading-derived slugs across all `docs/*.md` files.
- Update every internal reference (intra-page and cross-page) to match.
- Source files stay clean: no explicit `{#slug}` on a heading unless it's needed to break a collision.
- `mkdocs build` continues to succeed; the rendered site behaves the same except for the new anchor URLs.

## Non-goals

- No backward-compatibility for old `#h-xxx` URLs (any external bookmark to one of those IDs will break — accepted).
- No changes to `theme/`, `mkdocs.yml`, file names, or nav.
- No content edits beyond the anchor rewrites.

## Design

A single Python script, `scripts/rewrite_anchors.py`, run in two phases.

### Slug algorithm

The MkDocs `toc` extension auto-generates slugs at build time. Our rewriter must produce slugs that match what `toc` will produce, otherwise references will point at IDs MkDocs never emits. The algorithm matches Python-Markdown's default `slugify`:

1. Strip surrounding markdown formatting from the heading text — emphasis (`*`, `_`), code (`` ` ``), link wrappers (`[text](url)` → `text`).
2. Apply NFKD Unicode normalization.
3. Encode to ASCII, dropping non-ASCII codepoints.
4. Drop all characters that are not word-characters, whitespace, or hyphens.
5. Lowercase, strip leading/trailing whitespace.
6. Collapse runs of whitespace and hyphens into a single `-`.

Example: `## ADAM's *Settings*` → `adams-settings`.

### Phase 1 — Plan (`--plan`)

1. Walk every `docs/*.md` file.
2. For each heading line (`#` through `####`):
   - Extract the visible heading text and any trailing `{#h-xxx}` anchor.
   - Compute the natural slug.
   - Record `(file, old_anchor_id, heading_text, natural_slug, heading_level, parent_path)`.
3. Detect intra-file slug collisions. For each collision, walk up the heading hierarchy and prepend the slug of the nearest ancestor heading until the slug is unique within the file. This is the **disambiguated slug** and is the slug that will be written explicitly to the source file (see Phase 2).
4. Emit `scripts/anchor_mapping.json`:
   ```json
   {
     "by_file": {
       "staff-photographs.md": [
         {"old": "h-fk74mpuqoguv", "new": "naming-of-photographs", "explicit": false, "heading": "Naming of Photographs"},
         ...
       ]
     },
     "lookup": {
       "staff-photographs.md#h-fk74mpuqoguv": "naming-of-photographs"
     }
   }
   ```
   `explicit: true` means the slug must be written into the source as `{#slug}` because it's a collision override; `explicit: false` means the explicit anchor is dropped and MkDocs will auto-generate the same slug.
5. Print a report: total anchors processed, number of collisions disambiguated, list of disambiguated slugs for review.

The user can edit `anchor_mapping.json` before running phase 2 to override any slug that looks ugly.

### Phase 2 — Apply (`--apply`)

1. Read `scripts/anchor_mapping.json`.
2. For each file in the mapping:
   - For each heading line, remove the trailing `{#h-xxx}`. If the entry has `explicit: true`, append `{#new-slug}` instead.
   - Rewrite every `](#h-xxx)` to `](#new-slug)` using the in-file mapping.
   - Rewrite every `](other.md#h-xxx)` to `](other.md#new-slug)` using the global lookup.
3. References whose `(file, old_anchor)` doesn't exist in the lookup (orphans — heading was deleted, or the link was always broken) are **left untouched** and printed to a warnings list at the end.
4. Print a report: files modified, references rewritten, orphan warnings.

### Verification

After applying:

1. `mkdocs build` runs cleanly — no anchor warnings beyond pre-existing ones.
2. `grep -r "#h-" docs/` returns nothing (or only deliberately-skipped orphans).
3. Spot-check 5 randomly chosen pages: anchor IDs in rendered HTML match the new slugs; internal links jump to the right section.

### Edge cases

- **Headings with no text after stripping** (e.g. a heading that's only an emoji or only punctuation): emits an empty slug. The script will fall back to `section-N` where N is the heading's 1-based position in the file, and warn.
- **Headings that produce numeric-only slugs**: kept as-is — MkDocs accepts them.
- **Collisions across files**: not a problem; anchors are page-local. Only intra-file collisions are disambiguated.
- **Existing `(#h-xxx)` references with no matching definition anywhere**: orphan, leave untouched, warn.
- **Anchors inside HTML blocks or code fences**: skipped. The script only rewrites markdown link syntax outside fenced code blocks.

## Outputs

- 95 markdown files modified in place.
- `scripts/rewrite_anchors.py` — kept in the repo for posterity.
- `scripts/anchor_mapping.json` — generated, then deleted after Phase 2 succeeds (one-shot artifact).
- One commit containing the script + the rewritten markdown files.

## Risks

- **Slug-algorithm drift**: if the rewriter's slug function ever diverges from what MkDocs actually emits at build time, references will silently break. Mitigation: the verification step runs `mkdocs build` and grep-checks `#h-` is gone; any divergence shows up immediately.
- **Heading renames after the rewrite**: with explicit IDs gone, future heading text changes will silently change the URL. Accepted — this is the trade-off of the "rely on auto-slug" choice.
- **External bookmarks break**: accepted per design decision.
