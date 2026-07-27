import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from config import detect_award, detect_topic
from router import RouteType, route_question


class AwardDetectionTests(unittest.TestCase):
    def test_specific_aliases(self):
        cases = {
            "Which award covers a cleaner?": "Cleaning Services Award 2020",
            "Which award covers a pharmacist?": "Pharmacy Industry Award 2020",
            "Which award covers an air pilot?": "Air Pilots Award 2020",
            "Which award covers an aged care worker?": "Aged Care Award 2010",
            "Which award covers a nurse?": "Nurses Award 2020",
            "Which award covers ambulance staff?": (
                "Ambulance and Patient Transport Industry Award 2020"
            ),
        }
        for question, expected in cases.items():
            with self.subTest(question=question):
                self.assertEqual(detect_award(question), expected)

    def test_longest_specific_match_wins(self):
        self.assertEqual(
            detect_award("black coal mining conditions"),
            "Black Coal Mining Industry Award 2020",
        )
        self.assertEqual(
            detect_award("marine towage conditions"),
            "Marine Towage Award 2020",
        )

    def test_generic_mining_does_not_map_to_black_coal(self):
        self.assertEqual(
            detect_award("mining industry overtime"),
            "Mining Industry Award 2020",
        )

    def test_substring_does_not_create_false_award(self):
        self.assertIsNone(detect_award("transport logistics"))

    def test_topic_aliases(self):
        self.assertEqual(detect_topic("What salary applies?"), "wages")
        self.assertEqual(detect_topic("How much annual leave applies?"), "leave")


class RouterTests(unittest.TestCase):
    def test_nes_only_route(self):
        self.assertEqual(
            route_question("What is annual leave under the NES?").route,
            RouteType.CAG,
        )

    def test_award_only_route(self):
        self.assertEqual(
            route_question("What is casual loading under the Retail Award?").route,
            RouteType.RAG,
        )

    def test_combined_route(self):
        decision = route_question(
            "How does NES annual leave interact with the Hospitality Award?"
        )
        self.assertEqual(decision.route, RouteType.COMBINED)
        self.assertEqual(
            decision.award_filter,
            "Hospitality Industry (General) Award 2020",
        )

    def test_unknown_question_defaults_to_rag(self):
        self.assertEqual(
            route_question("What rules apply to this job?").route,
            RouteType.RAG,
        )


if __name__ == "__main__":
    unittest.main()
