from pathlib import Path
import importlib.util
import hashlib
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "promote_geometry_artifact.py"
SPEC = importlib.util.spec_from_file_location("promote_geometry_artifact", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def write_json(path: Path, payload) -> str:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GeometryPromotionTests(unittest.TestCase):
    def fixture(self, root: Path):
        candidate = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"geometry_id": "good", "name": "Good"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"geometry_id": "bad", "name": "Bad"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[2, 0], [3, 0], [3, 1], [2, 0]]],
                    },
                },
            ],
        }
        decision = {
            "features": [
                {
                    "geometry_id": "good",
                    "status": "qc_passed",
                    "metrics": {
                        "source_npoints": 4,
                        "render_npoints": 4,
                        "hausdorff_m": 100.0,
                        "area_delta_pct": 0.2,
                        "symmetric_difference_pct": 0.3,
                    },
                },
                {
                    "geometry_id": "bad",
                    "status": "quarantined",
                    "reasons": ["area_delta"],
                    "metrics": {
                        "source_npoints": 4,
                        "render_npoints": 4,
                        "hausdorff_m": 200.0,
                        "area_delta_pct": -8.0,
                        "symmetric_difference_pct": 9.0,
                    },
                },
            ]
        }

        candidate_path = root / "candidate.geojson"
        decision_path = root / "decision.json"
        candidate_sha = write_json(candidate_path, candidate)
        decision_sha = write_json(decision_path, decision)

        manifest = {
            "schema_version": "atlas-artifact-manifest-v1",
            "artifact_kind": "geometry-render-candidate",
            "created_at": "2026-09-20T00:00:00+00:00",
            "git_sha": "a" * 40,
            "metadata": {
                "land_fabric": "land-v1",
                "land_sha256": "b" * 64,
                "promotion_state": "candidate",
            },
            "parameters": {
                "snap_tolerance_m": "10000",
                "smooth_iterations": "1",
            },
            "artifacts": [
                {
                    "path": "/tmp/candidate.geojson",
                    "sha256": candidate_sha,
                    "size_bytes": candidate_path.stat().st_size,
                }
            ],
            "qc": [
                {
                    "path": "/tmp/decision.json",
                    "sha256": decision_sha,
                    "size_bytes": decision_path.stat().st_size,
                }
            ],
        }
        manifest_path = root / "artifact_manifest.json"
        manifest_sha = write_json(manifest_path, manifest)

        plan = {
            "schema_version": "geometry-promotion-plan-v1",
            "promotion_id": "test",
            "policy_id": "external-test",
            "artifact": {
                "git_sha": "a" * 40,
                "manifest_file": "artifact_manifest.json",
                "manifest_sha256": manifest_sha,
                "land_fabric_id": "land-v1",
                "land_sha256": "b" * 64,
                "parameters": {
                    "snap_tolerance_m": "10000",
                    "smooth_iterations": "1",
                },
                "files": {
                    "candidate.geojson": candidate_sha,
                    "decision.json": decision_sha,
                },
            },
            "features": [
                {
                    "geometry_id": "good",
                    "name": "Good",
                    "artifact_file": "candidate.geojson",
                    "decision_file": "decision.json",
                    "qc_status": "qc_passed",
                    "visual_status": "visually_accepted_candidate",
                    "semantic_scope_status": "accepted_polity_context",
                    "semantic_scope_note": "test",
                    "action": "promote",
                },
                {
                    "geometry_id": "bad",
                    "name": "Bad",
                    "artifact_file": "candidate.geojson",
                    "decision_file": "decision.json",
                    "qc_status": "quarantined",
                    "visual_status": "quarantined/fallback",
                    "semantic_scope_status": "blocked_bounded_event",
                    "semantic_scope_note": "test",
                    "action": "quarantine",
                },
            ],
        }
        plan_path = root / "plan.json"
        write_json(plan_path, plan)
        return plan_path, candidate_path

    def test_exact_artifact_passes_and_quarantine_is_not_promotable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plan_path, _candidate_path = self.fixture(root)
            plan, manifest, rows = MODULE.validate_artifact(plan_path, root)

            self.assertEqual(plan["promotion_id"], "test")
            self.assertEqual(manifest["git_sha"], "a" * 40)
            by_id = {row["geometry_id"]: row for row in rows}
            self.assertEqual(by_id["good"]["action"], "promote")
            self.assertEqual(by_id["bad"]["action"], "quarantine")

    def test_mutated_candidate_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plan_path, candidate_path = self.fixture(root)
            candidate_path.write_text(
                candidate_path.read_text(encoding="utf-8") + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(MODULE.PromotionError):
                MODULE.validate_artifact(plan_path, root)

    def test_promote_requires_visual_and_semantic_acceptance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plan_path, _candidate_path = self.fixture(root)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["features"][0]["semantic_scope_status"] = "blocked_bounded_event"
            write_json(plan_path, plan)

            with self.assertRaises(MODULE.PromotionError):
                MODULE.validate_artifact(plan_path, root)


if __name__ == "__main__":
    unittest.main()
