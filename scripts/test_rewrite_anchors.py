"""Tests for scripts/rewrite_anchors.py."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rewrite_anchors as ra  # noqa: E402


class TestSmoke(unittest.TestCase):
    def test_module_imports(self):
        self.assertTrue(hasattr(ra, "main"))


class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(ra.slugify("Naming of Photographs"), "naming-of-photographs")

    def test_lowercases(self):
        self.assertEqual(ra.slugify("UPPER Case"), "upper-case")

    def test_strips_apostrophe(self):
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
        self.assertEqual(ra.slugify("piñata"), "pinata")


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
        headings = [
            self._h(1, "Foo", "h-1"),
            self._h(2, "Bar", "h-2"),
            self._h(2, "Bar", "h-3"),
            self._h(2, "Bar", "h-4"),
        ]
        entries = ra.build_file_mapping(headings)
        slugs = [e.new_slug for e in entries]
        self.assertEqual(len(set(slugs)), len(slugs))


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
        self.assertEqual(lines[2], "Fake [link](#h-a).")
        self.assertEqual(lines[4], "Another [link](#alpha).")

    def test_does_not_match_non_h_anchors(self):
        text = "See [x](#section-1)."
        lookup = {}
        new, orphans = ra.rewrite_references(text, "foo.md", lookup)
        self.assertEqual(new, text)
        self.assertEqual(orphans, [])


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


if __name__ == "__main__":
    unittest.main()
