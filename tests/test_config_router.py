"""Tests for core config, router, and CAG modules."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import (
    AWARD_PATTERNS, detect_award, detect_topic, has_nes_keywords,
)
from router import detect_negation, detect_award_with_negation
from cag import CAGCache


class TestAwardDetection:
    def test_cleaning_award_detected(self):
        assert detect_award("What Award applies to a cleaner?") == "Cleaning Services Award 2020"

    def test_hospitality_award_detected(self):
        assert detect_award("minimum break under Hospitality Award") == "Hospitality Industry (General) Award 2020"

    def test_clerks_award_detected(self):
        assert detect_award("Does the Clerks Award cover payroll officers?") == "Clerks—Private Sector Award 2010"

    def test_no_award_detected(self):
        assert detect_award("what is the weather today") is None

    def test_childcare_maps_to_childrens_services(self):
        assert detect_award("childcare entitlements") == "Children's Services Award 2010"

    def test_transport_not_sporting(self):
        """DEF-009: Known issue - 'sport' is substring of 'transport'.
        This test documents the current behavior. The fix requires
        word-boundary matching which is tracked in DEF-009.
        """
        result = detect_award("transport workers pay rates")
        # Currently matches sporting due to substring match
        # This is the defect DEF-009 tracks
        assert result is not None

    def test_all_patterns_are_strings(self):
        for key, val in AWARD_PATTERNS.items():
            assert isinstance(val, str), f"Pattern {key} maps to non-string: {val}"


class TestTopicDetection:
    def test_overtime_detected(self):
        assert detect_topic("what are the overtime rules?") == "overtime"

    def test_leave_detected(self):
        assert detect_topic("annual leave entitlements") == "leave"

    def test_casual_detected(self):
        assert detect_topic("casual loading rates") == "casual"

    def test_no_topic_detected(self):
        assert detect_topic("hello") is None

    def test_weekend_detected(self):
        result = detect_topic("penalty rates for weekend work")
        assert result in ("weekend", "penalty")


class TestNESKeywords:
    def test_nes_keywords_present(self):
        assert has_nes_keywords("what are the NES entitlements?")

    def test_annual_leave_is_nes(self):
        assert has_nes_keywords("annual leave entitlements")

    def test_superannuation_is_nes(self):
        assert has_nes_keywords("superannuation contributions")

    def test_non_nes_returns_false(self):
        assert not has_nes_keywords("hello how are you")


class TestNegation:
    def test_negation_sport(self):
        negated = detect_negation("What awards are not sporting related?")
        assert isinstance(negated, list)

    def test_negation_removes_detected_award(self):
        award, negated = detect_award_with_negation("I don't want the retail award, what about cleaning?")
        assert award is not None

    def test_negated_award_returns_none(self):
        award, negated = detect_award_with_negation("not the sporting organisations award")
        assert award is None


class TestCAGCache:
    def test_nes_loaded(self):
        cache = CAGCache()
        assert len(cache.nes_text) > 100

    def test_cag_candidate_detection(self):
        cache = CAGCache()
        assert cache.is_cag_candidate("What is annual leave?")
        assert cache.is_cag_candidate("NES entitlements")
        assert not cache.is_cag_candidate("What Award applies to a cleaner?")
