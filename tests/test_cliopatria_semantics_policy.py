import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "validation" / "cliopatria_v0.2.0_semantics.json"


def source_year_for_atlas_year(atlas_year: int) -> int:
    return atlas_year - 1 if atlas_year <= 0 else atlas_year


class CliopatriaSemanticPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_calendar_mapping_skips_source_zero_without_shifting_ce(self):
        examples = self.data["atlas_policy"]["selected_atlas_year_to_source_year"]["examples"]
        for example in examples:
            self.assertEqual(
                source_year_for_atlas_year(example["atlas_year"]),
                example["source_year"],
            )
        self.assertNotEqual(source_year_for_atlas_year(0), 0)
        self.assertEqual(source_year_for_atlas_year(1), 1)

    def test_zero_endpoint_rows_are_source_bridges_to_year_one(self):
        rows = self.data["exact_corpus_observations"]["zero_endpoint_rows"]
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(row["to_year"] == 0 for row in rows))
        self.assertTrue(all(row["next_from_year"] == 1 for row in rows))
        self.assertFalse(self.data["atlas_policy"]["source_zero_has_direct_atlas_historical_year"])

    def test_relation_rows_remain_distinct_from_polities(self):
        observed = self.data["exact_corpus_observations"]
        hierarchy = observed["hierarchy_counts"]
        self.assertEqual(observed["type_counts"]["RELATION"], 385)
        self.assertEqual(hierarchy["relation_rows_with_components"], 385)
        self.assertEqual(hierarchy["relation_rows_with_member_of"], 0)
        self.assertEqual(hierarchy["relation_name_parenthesized_count"], 385)
        self.assertEqual(
            self.data["atlas_policy"]["relation_rows"],
            "retain as relationship/composite records; do not coerce to POLITY or default territorial polity geometry",
        )

    def test_hierarchy_is_not_flat(self):
        observed = self.data["exact_corpus_observations"]
        self.assertEqual(observed["hierarchy_counts"]["rows_with_both"], 80)
        self.assertGreater(int(observed["member_of_arity_counts"]["2"]), 0)
        self.assertEqual(max(map(int, observed["component_arity_counts"].keys())), 20)

    def test_same_name_gaps_are_preserved_not_interpolated(self):
        adjacency = self.data["exact_corpus_observations"]["same_name_interval_adjacency"]
        self.assertEqual(adjacency["inclusive_overlap_or_parallel"], 0)
        self.assertGreater(adjacency["gap_more_than_one_integer"], 0)
        self.assertEqual(self.data["atlas_policy"]["interval_gaps"], "preserve; never interpolate automatically")

    def test_default_baseline_is_type_aware(self):
        baseline = self.data["atlas_policy"]["default_polity_baseline"]
        self.assertEqual(baseline["candidate_type"], "POLITY")
        self.assertIn("Type=POLITY", baseline["duplicate_suppression"])
        self.assertIn("Type=RELATION", baseline["duplicate_suppression"])
        self.assertIn("recursively", baseline["nested_polity_composites"])


if __name__ == "__main__":
    unittest.main()
