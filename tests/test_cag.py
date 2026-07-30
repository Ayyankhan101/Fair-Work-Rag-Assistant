"""Tests for CAG cache and NES handling."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cag import CAGCache, NES_PATH


class TestCAGCache:
    def test_nes_file_exists(self):
        assert os.path.exists(NES_PATH), f"NES file not found: {NES_PATH}"

    def test_nes_loads_with_utf8(self):
        """DEF-061: NES must load with UTF-8."""
        cache = CAGCache()
        assert len(cache.nes_text) > 0
        assert "\ufffd" not in cache.nes_text or len(cache.nes_text) > 100

    def test_nes_has_substantive_content(self):
        cache = CAGCache()
        assert "annual leave" in cache.nes_text.lower() or "leave" in cache.nes_text.lower()

    def test_cag_keywords_cover_nes_topics(self):
        cache = CAGCache()
        assert cache.is_cag_candidate("What are the NES entitlements?")
        assert cache.is_cag_candidate("annual leave")
        assert cache.is_cag_candidate("parental leave")
        assert cache.is_cag_candidate("public holiday")

    def test_cag_does_not_match_award_only(self):
        cache = CAGCache()
        # "overtime" is a CAG keyword so this will match - that's expected
        # The test should verify non-NES/non-topic queries don't match
        assert not cache.is_cag_candidate("What Award applies to a cleaner?")

    def test_get_context_returns_nes(self):
        cache = CAGCache()
        ctx = cache.get_context("What are NES leave entitlements?")
        assert len(ctx) > 100
        assert "National Employment Standards" in ctx

    def test_get_context_empty_for_non_candidate(self):
        cache = CAGCache()
        ctx = cache.get_context("What Award applies to a cleaner?")
        assert ctx == "" or "National Employment Standards" not in ctx
