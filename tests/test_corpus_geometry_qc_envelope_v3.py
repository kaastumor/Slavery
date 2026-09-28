from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "cartography" / "corpus_geometry_qc_envelope_v3.json"
INVENTORY = (
    ROOT
    / "data"
    / "research"
    / "recovery"
    / "overnight_2026_09_28"
    / "morning_reconciliation_inventory.json"
)


class CorpusGeometryQcEnvelopeV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = json.loads(POLICY.read_text(encoding="utf-8"))
        cls.inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))

    def test_d120_geometry_metrics_are_inherited(self) -> None:
        inherited = self.policy["inherited_measurement_contract"]
        self.assertEqual(
            inherited["frontier_displacement_metric"],
            "source_to_smoothed_boundary_hausdorff_m",
        )
        self.assertEqual(inherited["max_candidate_frontier_displacement_m"], 35000)
        self.assertEqual(inherited["raw_to_final_render_hausdorff_role"], "diagnostic_only")

    def test_exact_source_feature_binding_is_a_hard_gate(self) -> None:
        gates = self.policy["provenance_hard_gates"]
        self.assertTrue(gates["exact_source_feature_binding_required_for_structured_geometry_sources"])
        self.assertTrue(gates["source_native_temporal_provenance_required"])
        self.assertTrue(gates["no_inferred_feature_binding"])
        self.assertTrue(gates["no_inferred_native_dates"])
        self.assertIn("source_feature_sha256_or_equivalent_content_fingerprint", gates["acceptable_feature_binding_fields"])

    def test_overnight_qc_findings_are_frozen(self) -> None:
        findings = self.policy["corpus_findings_2026_09_28"]
        self.assertEqual(findings["published_multi_slice_transitions_checked"], 30)
        self.assertEqual(findings["transition_gap_count"], 0)
        self.assertEqual(findings["transition_overlap_count"], 0)
        self.assertEqual(findings["mechanically_recoverable_native_interval_checks"], 10)
        self.assertEqual(findings["demonstrated_date_shift_errors"], 0)
        self.assertEqual(findings["released_cliopatria_polygons_audited"], 38)
        self.assertEqual(findings["demonstrated_wrong_feature_bindings"], 0)

    def test_pending_worker_inventory_preserves_all_three_lanes(self) -> None:
        inv = self.inventory
        self.assertEqual(len(inv["pending_expansion_packets"]), 16)
        self.assertEqual(len(inv["pending_geometry_resolution_packets"]), 14)
        self.assertIn("corpus_wide_qc_followup", inv)
        self.assertEqual(inv["release_effect"].split(".")[0], "None yet")


if __name__ == "__main__":
    unittest.main()
