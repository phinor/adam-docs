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
