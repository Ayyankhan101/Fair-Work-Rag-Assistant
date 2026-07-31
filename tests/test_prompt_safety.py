"""Tests for prompt safety and RAG chain behavior."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rag import (
    SYSTEM_PROMPT, PROMPT_VERSION, PROMPT_HASH,
    needs_clarification, format_docs, format_cag_context,
)


class TestPromptSafety:
    def test_prompt_has_system_role(self):
        """DEF-032: Prompt must have system+user separation."""
        assert "You are a Fair Work" in SYSTEM_PROMPT

    def test_prompt_forbids_fabrication(self):
        """DEF-033: Must instruct against fabrication."""
        assert "never fabricate" in SYSTEM_PROMPT.lower()

    def test_prompt_handles_insufficient_evidence(self):
        """DEF-033: Must handle insufficient evidence."""
        assert "don't have enough information" in SYSTEM_PROMPT.lower()

    def test_prompt_has_version(self):
        """DEF-037: Prompt must have version and hash."""
        assert PROMPT_VERSION is not None
        assert PROMPT_HASH is not None
        assert len(PROMPT_HASH) == 16

    def test_prompt_no_arbitrary_comparison(self):
        """DEF-035: Must not instruct arbitrary cross-Award comparison."""
        assert "PRIORITIZE that Award" in SYSTEM_PROMPT


class TestClarification:
    def test_too_short_needs_clarification(self):
        assert needs_clarification("hi")

    def test_greeting_needs_clarification(self):
        assert needs_clarification("hello")

    def test_valid_question_no_clarification(self):
        assert not needs_clarification("What is the minimum break under the Hospitality Award?")

    def test_question_word_only_needs_clarification(self):
        assert needs_clarification("what")

    def test_punctuation_only_needs_clarification(self):
        assert needs_clarification("???")


class TestFormatDocs:
    def test_empty_docs_returns_empty(self):
        result = format_docs([])
        assert result == ""

    def test_truncation_respects_max_chars(self):
        from langchain_core.documents import Document
        doc = Document(
            page_content="x" * 5000,
            metadata={
                'award_name': 'Test Award',
                'clause_number': '1.1',
                'document_type': 'Award',
                'source_url': 'http://example.com',
                'section_title': 'Section 1',
            }
        )
        result = format_docs([doc], max_chars=4000)
        assert len(result) <= 4500

    def test_strips_contextual_prefix(self):
        from langchain_core.documents import Document
        doc = Document(
            page_content="[Award Name - Section] Actual content here",
            metadata={
                'award_name': 'Test Award',
                'clause_number': '1.1',
                'document_type': 'Award',
                'source_url': 'http://example.com',
                'section_title': 'Section 1',
            }
        )
        result = format_docs([doc])
        assert "[Award Name - Section]" not in result
        assert "Actual content here" in result


class TestFormatCAGContext:
    def test_empty_returns_empty(self):
        assert format_cag_context("") == ""

    def test_returns_formatted(self):
        result = format_cag_context("NES text here")
        assert "NES text here" in result
        assert "CAG Cache" in result
