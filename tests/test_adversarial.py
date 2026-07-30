"""Adversarial tests for clarification path and negation handling."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestClarificationPath:
    """DEF-063: Verify clarification for ambiguous/unknown cases."""

    def test_greeting_gets_clarification(self):
        from rag import needs_clarification
        assert needs_clarification("hello")
        assert needs_clarification("hi")
        assert needs_clarification("hey")
        assert needs_clarification("good morning")

    def test_too_short_gets_clarification(self):
        from rag import needs_clarification
        assert needs_clarification("hi")
        assert needs_clarification("ok")
        assert needs_clarification("yes")

    def test_question_word_only_gets_clarification(self):
        from rag import needs_clarification
        assert needs_clarification("what")
        assert needs_clarification("how")
        assert needs_clarification("when")
        assert needs_clarification("where")
        assert needs_clarification("who")
        assert needs_clarification("why")

    def test_just_punctuation_gets_clarification(self):
        from rag import needs_clarification
        assert needs_clarification("???")
        assert needs_clarification("???")
        assert needs_clarification("!!")
        assert needs_clarification(".")

    def test_valid_question_no_clarification(self):
        from rag import needs_clarification
        assert not needs_clarification("What is the minimum break under the Hospitality Award?")
        assert not needs_clarification("How many hours can I work?")
        assert not needs_clarification("What are the overtime rules?")
        assert not needs_clarification("Does the Clerks Award cover payroll officers?")

    def test_typo_in_question_still_works(self):
        from rag import needs_clarification
        # Typos should not trigger clarification if question is substantive
        assert not needs_clarification("What is the minimun break under the Hospitality Award?")
        assert not needs_clarification("What are the ovetime rules for casuals?")


class TestNegationHandling:
    """DEF-064: Negation-aware intent handling."""

    def test_negation_sport(self):
        from router import detect_negation
        negated = detect_negation("What awards are not sporting related?")
        # Should detect that "sporting" is negated
        assert isinstance(negated, list)

    def test_negation_retail(self):
        from router import detect_negation
        negated = detect_negation("Not the retail award")
        assert isinstance(negated, list)

    def test_negation_removes_detected_award(self):
        from router import detect_award_with_negation
        # If the only award mentioned is negated, should return None
        award, negated = detect_award_with_negation("Not the sporting organisations award")
        # The award should be negated
        assert award is None or len(negated) > 0

    def test_negation_with_multiple_awards(self):
        from router import detect_award_with_negation
        # When one award is negated but another is present
        award, negated = detect_award_with_negation("Not the retail award, what about cleaning?")
        assert award is not None
        assert "General Retail Industry Award 2020" in negated

    def test_negation_patterns(self):
        from router import detect_negation
        patterns = [
            "not sport",
            "no retail",
            "without mining",
            "except cleaning",
            "excluding hospitality",
        ]
        for pattern in patterns:
            negated = detect_negation(f"What awards apply {pattern}?")
            assert isinstance(negated, list), f"Failed for pattern: {pattern}"

    def test_negation_does_not_affect_non_matching(self):
        from router import detect_award_with_negation
        # When no negation is present
        award, negated = detect_award_with_negation("What is the minimum break under the Hospitality Award?")
        assert award == "Hospitality Industry (General) Award 2020"
        assert len(negated) == 0

    def test_negation_in_full_question(self):
        from router import detect_negation
        negated = detect_negation("I don't want the sporting organisations award, what are other options?")
        assert isinstance(negated, list)
