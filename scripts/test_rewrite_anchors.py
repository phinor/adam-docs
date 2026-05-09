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


if __name__ == "__main__":
    unittest.main()
