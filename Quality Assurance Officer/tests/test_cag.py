import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from cag import CAGCache


class CAGCacheTests(unittest.TestCase):
    def test_utf8_content_and_entitlement_headings_are_preserved(self):
        content = (
            "Skip to main content\n"
            "National Employment Standards\n"
            "Annual leave\n"
            "An award cannot exclude the NES.\n"
            "Personal/carer's leave\n"
            "Employees can’t receive less than the NES."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nes.txt"
            path.write_text(content, encoding="utf-8")
            cache = CAGCache(str(path))

        self.assertIn("Annual leave", cache.nes_text)
        self.assertIn("award cannot exclude", cache.nes_text)
        self.assertIn("Personal/carer's leave", cache.nes_text)
        self.assertIn("can’t receive less", cache.nes_text)

    def test_only_nes_topics_are_cache_candidates(self):
        cache = CAGCache.__new__(CAGCache)
        cache.nes_text = "NES content"

        self.assertTrue(cache.is_cag_candidate("What is annual leave?"))
        self.assertFalse(cache.is_cag_candidate("What is the meal break in an Award?"))
        self.assertFalse(cache.is_cag_candidate("What overtime rate applies?"))

    def test_missing_file_returns_empty_cache(self):
        cache = CAGCache("file-that-does-not-exist.txt")
        self.assertEqual(cache.get_nes_context(), "")


if __name__ == "__main__":
    unittest.main()
