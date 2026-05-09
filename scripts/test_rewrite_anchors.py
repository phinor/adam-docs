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


if __name__ == "__main__":
    unittest.main()
