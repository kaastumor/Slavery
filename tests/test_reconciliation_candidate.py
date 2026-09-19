from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "reconciliation"))

from candidate import make_reconciliation_record, review_reconciliation  # noqa: E402


class ReconciliationCandidateTests(unittest.TestCase):
    def test_high_score_is_not_autoaccepted(self):
        record = make_reconciliation_record(
            raw_text="Alexandria",
            service={"name": "example historical gazetteer", "namespace": "example"},
            candidates=[{"id": "P1", "name": "Alexandria", "score": 100.0}],
            query_context={"year": -100},
        )
        self.assertEqual(record["judgment"], "unreviewed")
        self.assertIsNone(record["accepted_candidate_id"])
        self.assertFalse(record["automatic_acceptance_allowed"])

    def test_acceptance_requires_explicit_existing_candidate(self):
        record = make_reconciliation_record(
            raw_text="Anshan",
            service={"name": "WHG", "namespace": "whg"},
            candidates=[
                {"id": "whg:1", "name": "Anshan", "score": 88.0},
                {"id": "whg:2", "name": "Anshan (other)", "score": 71.0},
            ],
        )
        with self.assertRaises(ValueError):
            review_reconciliation(record, judgment="accepted", reviewer="researcher", candidate_id="missing")
        accepted = review_reconciliation(
            record,
            judgment="accepted",
            reviewer="researcher",
            candidate_id="whg:1",
            note="Accepted after temporal and geographic review.",
        )
        self.assertEqual(accepted["judgment"], "accepted")
        self.assertEqual(accepted["accepted_candidate_id"], "whg:1")
        self.assertFalse(accepted["jurisdiction_inference_allowed"])


if __name__ == "__main__":
    unittest.main()
