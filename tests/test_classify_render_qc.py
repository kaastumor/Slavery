from pathlib import Path
import importlib.util
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "classify_render_qc.py"
SPEC = importlib.util.spec_from_file_location("classify_render_qc", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class RenderQcClassificationTests(unittest.TestCase):
    def setUp(self):
        self.policy = {
            "policy_id": "test-policy",
            "hard_gates": {
                "geometry_valid": True,
                "max_abs_area_delta_pct": 2.0,
                "max_symmetric_difference_pct": 5.0,
            },
            "candidate_selection": {
                "preferred_snap_tolerance_m": 10000,
                "evaluated_snap_tolerances_m": [10000, 15000, 20000, 25000],
                "alternate_tolerance_rule": "diagnostic_or_explicit_visual_override_only",
                "preferred_failure_rule": "quarantine_and_keep_previous_approved_render_or_fallback",
            },
            "visual_review_required_before_promotion": True,
        }

    def _write(self, path, payload):
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_pass_and_quarantine(self):
        qc = {
            "features": [
                {
                    "geometry_id": "good",
                    "name": "Good",
                    "ok": True,
                    "area_delta_pct": 0.4,
                    "symmetric_difference_pct": 1.2,
                    "hausdorff_m": 50000,
                },
                {
                    "geometry_id": "bad",
                    "name": "Bad",
                    "ok": True,
                    "area_delta_pct": -8.4,
                    "symmetric_difference_pct": 10.3,
                    "hausdorff_m": 49000,
                },
            ]
        }
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            qc_path = td / "qc.json"
            policy_path = td / "policy.json"
            output_path = td / "decision.json"
            self._write(qc_path, qc)
            self._write(policy_path, self.policy)

            old_argv = __import__("sys").argv
            try:
                __import__("sys").argv = [
                    "classify_render_qc.py",
                    str(qc_path),
                    str(policy_path),
                    str(output_path),
                    "--snap-tolerance-m",
                    "10000",
                ]
                self.assertEqual(MODULE.main(), 0)
            finally:
                __import__("sys").argv = old_argv

            result = json.loads(output_path.read_text(encoding="utf-8"))
            by_id = {row["geometry_id"]: row for row in result["features"]}
            self.assertEqual(by_id["good"]["status"], "qc_passed")
            self.assertEqual(by_id["good"]["review_state"], "awaiting_visual_review")
            self.assertEqual(by_id["bad"]["status"], "quarantined")
            self.assertEqual(by_id["bad"]["review_state"], "not_eligible")
            self.assertIn("area_delta", by_id["bad"]["reasons"])
            self.assertIn("symmetric_difference", by_id["bad"]["reasons"])
            self.assertEqual(result["summary"], {"qc_passed": 1, "quarantined": 1})
            self.assertEqual(
                result["candidate_selection"]["selection_role"],
                "preferred_baseline",
            )
            self.assertEqual(
                result["candidate_selection"]["preferred_snap_tolerance_m"],
                10000,
            )

    def test_alternate_tolerance_is_not_preferred(self):
        selection = MODULE.candidate_selection(self.policy, 20000)
        self.assertEqual(selection["selection_role"], "alternate_candidate")
        self.assertEqual(selection["preferred_snap_tolerance_m"], 10000)


if __name__ == "__main__":
    unittest.main()
