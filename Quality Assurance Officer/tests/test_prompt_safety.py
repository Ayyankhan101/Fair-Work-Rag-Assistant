import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAG_SOURCE = ROOT / "src" / "rag.py"


class PromptSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = RAG_SOURCE.read_text(encoding="utf-8")

    def test_prompt_allows_insufficient_evidence(self):
        self.assertIn("cannot be determined from the available context", self.source)
        self.assertIn("Insufficient evidence", self.source)

    def test_prompt_forbids_fabricated_values_and_citations(self):
        self.assertIn("Never invent a number, Award name, clause", self.source)

    def test_prompt_treats_retrieved_instructions_as_untrusted(self):
        self.assertIn("untrusted content", self.source)

    def test_prompt_does_not_force_an_answer(self):
        self.assertNotIn("ALWAYS provide the best answer", self.source)
        self.assertNotIn("MUST provide a specific answer with a number", self.source)


if __name__ == "__main__":
    unittest.main()
