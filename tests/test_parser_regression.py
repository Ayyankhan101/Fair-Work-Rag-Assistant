"""Parser regression tests for ingest_markdown and ingest."""
import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestMarkdownParser:
    """DEF-040: Parser oracle regression tests."""

    def test_parse_sections_with_preamble(self):
        """DEF-049: Preserve preamble content before first heading."""
        from ingest_markdown import parse_md_sections

        md = """This is the preamble text that should be preserved.
It contains important information about the award.

## Part 1 - Introduction

This is the first section.

### 1.1 Definition

This is clause 1.1."""

        sections = parse_md_sections(md, "Test Award 2020", "test.md")
        assert len(sections) >= 2
        # Preamble should be preserved
        preamble = sections[0]
        assert "preamble" in preamble['text'].lower() or "important" in preamble['text'].lower()

    def test_parse_subclause_identity(self):
        """DEF-050: Retain subclause identity (e.g., 15.1)."""
        from ingest_markdown import parse_md_sections, extract_clause_number

        md = """## Part 2

### 15.1 The maximum number of ordinary hours is 11 hours.

Some additional text here.

### 15.2 An employee must not work more than 11 hours.

More text."""

        sections = parse_md_sections(md, "Test Award 2020", "test.md")
        # Should find clause 15.1 and 15.2
        titles = [s['title'] for s in sections]
        assert any("15.1" in t for t in titles), f"Expected 15.1 in titles: {titles}"
        assert any("15.2" in t for t in titles), f"Expected 15.2 in titles: {titles}"

        # Extract clause numbers
        for section in sections:
            if "15.1" in section['title']:
                clause = extract_clause_number(section['title'])
                assert clause == "15.1", f"Expected 15.1, got {clause}"

    def test_chunk_respects_max_size(self):
        """DEF-051: Split oversized single paragraphs."""
        from ingest_markdown import chunk_text

        long_text = "This is a sentence. " * 200  # ~2200 chars
        chunks = chunk_text(long_text, max_chunk_size=1500)

        for chunk in chunks:
            assert len(chunk) <= 1500, f"Chunk too large: {len(chunk)} chars"

    def test_chunk_preserves_content(self):
        """DEF-051: Verify no content loss after chunking."""
        from ingest_markdown import chunk_text

        text = "First paragraph content.\n\nSecond paragraph content.\n\nThird paragraph content."
        chunks = chunk_text(text, max_chunk_size=1500)

        combined = " ".join(chunks)
        assert "First paragraph" in combined
        assert "Second paragraph" in combined
        assert "Third paragraph" in combined

    def test_md_to_documents_includes_metadata(self):
        """DEF-052: Verify metadata includes source_version."""
        from ingest_markdown import md_to_documents

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Award 2020\n\n## Part 1\n\n### 1.1 Clause\n\nThis is enough content to pass the minimum length check for chunk inclusion in the documents list.")
            f.flush()

        try:
            docs = md_to_documents(f.name)
            assert len(docs) > 0
            for doc in docs:
                assert 'source_version' in doc.metadata
                assert 'award_name' in doc.metadata
        finally:
            os.unlink(f.name)

    def test_extract_clause_number(self):
        """Test clause number extraction."""
        from ingest_markdown import extract_clause_number

        # Valid clause numbers (with period and space after)
        assert extract_clause_number("15.1. Some title") == "15.1"
        assert extract_clause_number("13.5. The maximum") == "13.5"
        assert extract_clause_number("Part 2—Introduction") == "Part 2"
        assert extract_clause_number("Schedule A—Rates") == "Schedule A"
        
        # No clause number
        assert extract_clause_number("General title without number") == ""

    def test_empty_chunk_skipped(self):
        """DEF-053: Skip empty/header-only chunks."""
        from ingest_markdown import md_to_documents

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Award 2020\n\n## Part 1\n\n### 1.1\n\nx\n\n### 1.2\n\nThis has enough content to be included in the documents.")
            f.flush()

        try:
            docs = md_to_documents(f.name)
            # Short chunks should be skipped
            for doc in docs:
                assert len(doc.page_content.strip()) >= 50
        finally:
            os.unlink(f.name)


class TestPDFParser:
    """DEF-040: PDF parser regression tests."""

    def test_extract_award_name_override(self):
        """DEF-003: MA000002 should be labelled correctly."""
        from ingest import AWARD_NAME_OVERRIDES

        assert "MA000002.pdf" in AWARD_NAME_OVERRIDES
        assert "Clerks" in AWARD_NAME_OVERRIDES["MA000002.pdf"]

    def test_award_url_map_has_new_entries(self):
        """DEF-001/002: MA000095 and MA000121 should be in the map."""
        from ingest import AWARD_URL_MAP

        assert "MA000095" in AWARD_URL_MAP
        assert "MA000121" in AWARD_URL_MAP
        assert "car-parking" in AWARD_URL_MAP["MA000095"]
        assert "state-government" in AWARD_URL_MAP["MA000121"]

    def test_chunk_text_enforces_max(self):
        """DEF-051: PDF chunking respects max size."""
        from ingest import chunk_text

        # Use proper sentences so sentence splitting works
        long_text = "This is a test sentence. " * 200  # ~5200 chars with sentence boundaries
        chunks = chunk_text(long_text, max_chunk_size=1500)
        for chunk in chunks:
            assert len(chunk) <= 1500, f"Chunk too large: {len(chunk)}"

    def test_corpus_version_exists(self):
        """DEF-006: Corpus version should be defined."""
        from ingest import CORPUS_VERSION
        assert CORPUS_VERSION is not None
        assert len(CORPUS_VERSION) > 10
