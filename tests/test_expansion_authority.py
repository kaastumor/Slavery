from pathlib import Path
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "build_expansion_authority.py"
SPEC = importlib.util.spec_from_file_location("build_expansion_authority", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

SELECTION = ROOT / "release" / "selections" / "v0.8.0-expansion-02.json"
PREDECESSOR = ROOT / "data" / "releases" / "v0.7.0" / "authority-state.json"


class ExpansionAuthorityTests(unittest.TestCase):
    def test_selection_is_explicit_and_excludes_disputed_claims(self) -> None:
        selection = MODULE.load_selection(SELECTION)
        additions = selection["additions"]
        selected = set(additions["direct_recovery_claim_ids"]) | set(
            additions["post_m1_claim_ids"]
        )
        excluded = set(selection["exclusions"]["disputed_claim_ids"])
        self.assertEqual(len(selected), 35)
        self.assertEqual(len(additions["approved_geometry_ids"]), 49)
        self.assertTrue(selected.isdisjoint(excluded))
        self.assertTrue(selection["rules"]["explicit_membership_only"])
        self.assertTrue(selection["rules"]["reviewed_row_discovery_forbidden"])

    def test_final_selection_adds_todaiji_without_mutating_first_freeze(self) -> None:
        selection = MODULE.load_selection(SELECTION)
        additions = selection["additions"]
        self.assertIn(
            "687bed4f-281e-4821-bc23-1e75cb65dd99",
            additions["post_m1_claim_ids"],
        )
        self.assertIn(
            "4ea5165a-9bd2-4883-9cdd-4910aa491dc7",
            additions["approved_geometry_ids"],
        )
        self.assertEqual(
            selection["supersedes_selection"],
            "release/selections/v0.8.0-expansion-01.json",
        )
        self.assertEqual(selection["expected_counts"]["candidate_claims"], 75)
        self.assertEqual(selection["expected_counts"]["candidate_spatial_entities"], 50)
        self.assertEqual(selection["expected_counts"]["candidate_geometries"], 49)

    def test_v2_selection_keeps_claim_and_geometry_completeness_separate(self) -> None:
        selection = MODULE.load_selection(SELECTION)
        additions = selection["additions"]
        self.assertEqual(
            selection["selection_schema"],
            "historical-slavery-atlas-expansion-selection-v2",
        )
        self.assertEqual(len(additions["direct_recovery_claim_ids"]), 19)
        self.assertEqual(len(additions["post_m1_claim_ids"]), 11)
        self.assertEqual(len(additions["reviewed_state_claim_ids"]), 5)
        self.assertIn(
            "dac1fdbe-8a72-411e-a43c-6180e3d24298",
            additions["reviewed_state_claim_ids"],
        )
        self.assertIn(
            "cfd709dd-55ad-4f92-a6ec-f6c7910b3fe1",
            additions["reviewed_state_claim_ids"],
        )
        self.assertTrue(selection["rules"]["claim_completeness_independent_of_geometry"])
        self.assertTrue(selection["rules"]["reviewed_disputes_may_be_complete"])

    def test_predecessor_identity_is_exact_v070_authority(self) -> None:
        selection = MODULE.load_selection(SELECTION)
        predecessor = MODULE.load_predecessor(selection, PREDECESSOR)
        self.assertEqual(len(predecessor["membership"]["claim_ids"]), 40)
        self.assertEqual(len(predecessor["membership"]["spatial_entity_ids"]), 18)
        self.assertEqual(predecessor["membership"]["geometry_ids"], [])
        self.assertEqual(
            predecessor["membership_sha256"],
            "ebc9d32f09857744841a0cf92699c41739b624ac4bd94c43798eb1f61e3b0dd3",
        )

    def test_management_sql_binding_is_literal_and_complete(self) -> None:
        rendered = MODULE._bind_sql(
            "select * from x where id=any(%s::uuid[]) and label=%s",
            (["00000000-0000-0000-0000-000000000001"], "O'Reilly"),
        )
        self.assertNotIn("%s", rendered)
        self.assertIn(
            "ARRAY['00000000-0000-0000-0000-000000000001']::uuid[]",
            rendered,
        )
        self.assertIn("'O''Reilly'", rendered)

    def test_empty_uuid_array_binding_remains_typed(self) -> None:
        rendered = MODULE._bind_sql(
            "select * from x where id=any(%s::uuid[])",
            ([],),
        )
        self.assertIn("ARRAY[]::uuid[]::uuid[]", rendered)

    def test_union_builder_preserves_nonexpanded_predecessor_dimensions(self) -> None:
        predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
        membership = MODULE.build_membership(
            predecessor,
            ["00000000-0000-0000-0000-000000000001"],
            ["00000000-0000-0000-0000-000000000002"],
            ["00000000-0000-0000-0000-000000000003"],
            ["00000000-0000-0000-0000-000000000004"],
        )
        for key in (
            "actor_ids",
            "voyage_ids",
            "coverage_assessment_ids",
            "research_target_result_ids",
        ):
            self.assertEqual(membership[key], predecessor["membership"][key])
        self.assertEqual(len(membership["claim_ids"]), 41)
        self.assertEqual(len(membership["spatial_entity_ids"]), 19)
        self.assertEqual(len(membership["geometry_ids"]), 1)


if __name__ == "__main__":
    unittest.main()
