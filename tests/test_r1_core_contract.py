import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "programmes" / "r1" / "validate_core_contract.py"
spec = importlib.util.spec_from_file_location("r1core", P)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class CoreContractTests(unittest.TestCase):
    def test_c0_cannot_claim_absence_or_presence(self):
        row = {
            "tier":"C0","research_stage":"not_researched","classification_outcome":"unassessed",
            "bounded_proposition":"No slavery"
        }
        self.assertTrue(m.validate_row(row))

    def test_safe_c0_passes(self):
        row = {"tier":"C0","research_stage":"not_researched","classification_outcome":"unassessed"}
        self.assertEqual(m.validate_row(row), [])

    def test_positive_c1_rejects_only_context_sources(self):
        row = {
            "tier":"C1","research_stage":"review_complete","classification_outcome":"classified",
            "bounded_proposition":"Bounded claim","required_abstention":"Do not generalize.",
            "temporal_applicability":"bounded_occurrence","temporal_precision":"approximate",
            "evidence_locus":"site","inference_extent":"site",
            "language_access_limitations":"English-only packet","coverage_confidence":"limited",
            "review_state":"internally_reviewed","release_id":"R1-candidate",
            "sources":[{"source_version_ref":"S1","decisive":True,"claim_fitness":"context_only"}]
        }
        self.assertTrue(m.validate_row(row))

    def test_positive_c1_with_production_source_passes(self):
        row = {
            "tier":"C1","research_stage":"review_complete","classification_outcome":"classified",
            "bounded_proposition":"Bounded claim","required_abstention":"Do not generalize.",
            "temporal_applicability":"bounded_occurrence","temporal_precision":"approximate",
            "evidence_locus":"site","inference_extent":"site",
            "language_access_limitations":"none known","coverage_confidence":"moderate",
            "review_state":"internally_reviewed","release_id":"R1-candidate",
            "sources":[{"source_version_ref":"S1","decisive":True,"claim_fitness":"production_grade"}]
        }
        self.assertEqual(m.validate_row(row), [])

if __name__ == "__main__":
    unittest.main()
