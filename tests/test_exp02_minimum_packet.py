import csv
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "exp02_minimum_packet"
CANDIDATE = ROOT / "web" / "public" / "data" / "r1-mvp-candidate.json"

FROZEN_BLOB_SHA = "057a61f4758a5ce1dce247c1eb97c7e421c5f979"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


class Exp02MinimumPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate_bytes = CANDIDATE.read_bytes()
        cls.candidate = json.loads(cls.candidate_bytes)
        cls.manifest = json.loads((EXP / "manifest.json").read_text(encoding="utf-8"))
        cls.analysis = json.loads((EXP / "analysis.json").read_text(encoding="utf-8"))
        with (EXP / "targets.csv").open(encoding="utf-8", newline="") as fh:
            cls.targets = list(csv.DictReader(fh))
        with (EXP / "sources.csv").open(encoding="utf-8", newline="") as fh:
            cls.sources = list(csv.DictReader(fh))

    def test_exact_frozen_candidate_is_used(self):
        self.assertEqual(git_blob_sha(self.candidate_bytes), FROZEN_BLOB_SHA)
        self.assertEqual(self.manifest["frozen_candidate_blob_sha"], FROZEN_BLOB_SHA)
        self.assertEqual(
            self.manifest["frozen_repo_commit"],
            "a6987d3f14369c6ea2d7b2b3db74ac65faa8ec57",
        )

    def test_portable_tables_cover_frozen_membership(self):
        self.assertEqual(len(self.targets), 77)
        self.assertEqual(len(self.sources), 45)
        self.assertEqual(len({row["target_id"] for row in self.targets}), 77)
        reviewed_ids = {row["target_id"] for row in self.targets if row["bounded_proposition"]}
        self.assertEqual(len(reviewed_ids), 19)

    def test_review_state_is_safely_hoisted_for_this_release(self):
        review_states = {row["review_state"] for row in self.candidate["reviewed_c1"]}
        self.assertEqual(review_states, {"internally_adversarially_reviewed"})
        self.assertEqual(
            self.manifest["reviewed_row_state_hoisted"],
            "internally_adversarially_reviewed",
        )
        self.assertNotIn("review_state", self.targets[0])

    def test_geometry_is_safely_hoisted_only_for_frozen_set(self):
        states = {row["representation_state"] for row in self.candidate["geometry_manifest"]["rows"]}
        self.assertEqual(states, {"unresolved_no_geometry"})
        self.assertEqual(self.manifest["geometry"]["default_state"], "unresolved_no_geometry")
        self.assertEqual(self.manifest["geometry"]["overrides"], [])
        self.assertNotIn("geometry_state", self.targets[0])

    def test_reviewed_claim_safety_fields_are_preserved(self):
        portable = {row["target_id"]: row for row in self.targets}
        for original in self.candidate["reviewed_c1"]:
            row = portable[original["target_id"]]
            self.assertEqual(row["bounded_proposition"], original["bounded_proposition"])
            self.assertEqual(row["required_abstention"], original["required_abstention"])
            self.assertEqual(row["evidence_locus"], original["evidence_locus"])
            self.assertEqual(row["inference_extent"], original["inference_extent"])
            self.assertEqual(
                row["language_access_limitations"],
                original["language_access_limitations"],
            )
            self.assertEqual(row["coverage_confidence"], original["coverage_confidence"])

    def test_temporal_state_is_not_replaced_by_anchor(self):
        portable = {row["target_id"]: row for row in self.targets}
        at_1800 = {
            row["temporal_state"]
            for row in self.targets
            if row["source_anchor"] == "1800" and row["bounded_proposition"]
        }
        self.assertEqual(
            at_1800,
            {"unknown", "not_applicable_aggregate", "supported_exact_cross_section"},
        )
        for original in self.candidate["temporal_navigation"]["targets"]:
            self.assertEqual(portable[original["target_id"]]["temporal_state"], original["state"])
            self.assertEqual(
                portable[original["target_id"]]["temporal_display_rule"],
                original["display_rule"],
            )

    def test_nonabsence_research_states_remain_distinct(self):
        states = {row["research_state"] for row in self.targets}
        self.assertEqual(
            states,
            {
                "reviewed_classified",
                "reviewed_inconclusive",
                "planned_unresearched",
                "held",
                "c0_only",
            },
        )
        rule = self.manifest["non_absence_rule"].lower()
        self.assertIn("absence", rule)
        self.assertTrue(
            "none imply" in rule
            or "does not imply" in rule
            or "do not imply" in rule
        )

    def test_held_and_unreviewed_frame_limits_are_not_optimized_away(self):
        candidate_by_id = {row["target_id"]: row for row in self.candidate["targets"]}
        portable = {row["target_id"]: row for row in self.targets}
        for target_id, original in candidate_by_id.items():
            if original["release_research_state"] != "c1_review_complete":
                row = portable[target_id]
                self.assertEqual(row["qa_state"], str(original.get("qa_state") or ""))
                self.assertEqual(
                    row["effective_frame_class"],
                    str(original.get("effective_frame_class") or ""),
                )
                self.assertEqual(
                    row["identity_limitation"],
                    str(original.get("identity_limitation") or ""),
                )

    def test_exact_source_locator_and_dependency_are_preserved(self):
        expected = {
            (
                row["target_id"],
                source["source_version_ref"],
                str(source.get("locator") or ""),
                str(source.get("independence_group") or ""),
            )
            for row in self.candidate["reviewed_c1"]
            for source in row["sources"]
        }
        actual = {
            (
                row["target_id"],
                row["source_version_ref"],
                row["locator"],
                row["independence_group"],
            )
            for row in self.sources
        }
        self.assertEqual(actual, expected)
        group_counts = {}
        for row in self.sources:
            group_counts[row["independence_group"]] = group_counts.get(row["independence_group"], 0) + 1
        self.assertEqual(sum(1 for count in group_counts.values() if count > 1), 7)

    def test_experiment_does_not_smuggle_application_fields_into_minimum_tables(self):
        self.assertNotIn("atlas_internal_year", self.targets[0])
        self.assertNotIn("review_state", self.targets[0])
        self.assertNotIn("role", self.sources[0])
        self.assertNotIn("claim_fitness", self.sources[0])
        self.assertNotIn("notes", self.sources[0])

    def test_result_is_subtractive_not_canonical_schema_change(self):
        matrix = {row["family"]: row["disposition"] for row in self.analysis["ablation_matrix"]}
        self.assertEqual(matrix["per-row review_state"], "SIMPLIFY_CANDIDATE")
        self.assertEqual(matrix["per-target geometry state"], "REDUNDANT_IN_CURRENT_FROZEN_SET")
        self.assertEqual(matrix["bounded proposition / required abstention"], "PRESERVE_CORE")
        self.assertEqual(matrix["research-state / non-absence distinction"], "PRESERVE_CORE")
        self.assertEqual(
            self.analysis["portable_format_result"]["flat_target_plus_source_tables"],
            "PORTABLE_CORE_SURVIVES",
        )
        self.assertLess(self.analysis["size_evidence"]["flat_tables_plus_manifest_ratio"], 0.25)
        self.assertLess(self.analysis["size_evidence"]["compact_json_ratio"], 0.40)


if __name__ == "__main__":
    unittest.main()
