from pathlib import Path
import importlib.util
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "promote_render_artifact.py"
SPEC = importlib.util.spec_from_file_location("promote_render_artifact", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


GOOD_ID = "11111111-1111-4111-8111-111111111111"
BAD_ID = "22222222-2222-4222-8222-222222222222"


class GeometryPromotionTests(unittest.TestCase):
    def _write_package(
        self,
        root: Path,
        *,
        tolerance: int = 10000,
        selection_role: str = "preferred_baseline",
        allow_alternate: bool = False,
    ):
        candidate = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"geometry_id": GOOD_ID, "name": "Good"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"geometry_id": BAD_ID, "name": "Bad"},
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [[[[2, 0], [3, 0], [3, 1], [2, 1], [2, 0]]]],
                    },
                },
            ],
        }
        decision = {
            "policy_id": "qc-policy-v1",
            "candidate_selection": {
                "snap_tolerance_m": tolerance,
                "selection_role": selection_role,
                "preferred_snap_tolerance_m": 10000,
            },
            "features": [
                {
                    "geometry_id": GOOD_ID,
                    "status": "qc_passed",
                    "review_state": "awaiting_visual_review",
                    "metrics": {
                        "source_npoints": 5,
                        "render_npoints": 5,
                        "area_delta_pct": 0.2,
                        "symmetric_difference_pct": 1.0,
                        "hausdorff_m": 1200,
                    },
                },
                {
                    "geometry_id": BAD_ID,
                    "status": "quarantined",
                    "review_state": "not_eligible",
                    "metrics": {
                        "source_npoints": 5,
                        "render_npoints": 5,
                        "area_delta_pct": -8.4,
                        "symmetric_difference_pct": 10.3,
                        "hausdorff_m": 49000,
                    },
                },
            ],
        }

        candidate_path = root / "representative.geojson"
        decision_path = root / "representative_decision.json"
        artifact_path = root / "artifact_manifest.json"
        approval_path = root / "approval.json"
        candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
        decision_path.write_text(json.dumps(decision), encoding="utf-8")

        artifact = {
            "schema_version": "atlas-artifact-manifest-v1",
            "git_sha": "abc123",
            "parameters": {
                "snap_tolerance_m": str(tolerance),
                "smooth_iterations": "1",
            },
            "metadata": {
                "land_fabric": "natural-earth-test",
                "render_policy_id": "render-policy-v1",
            },
            "artifacts": [
                {
                    "path": f"/tmp/{candidate_path.name}",
                    "sha256": MODULE.sha256(candidate_path),
                }
            ],
            "qc": [
                {
                    "path": f"/tmp/{decision_path.name}",
                    "sha256": MODULE.sha256(decision_path),
                }
            ],
        }
        artifact_path.write_text(json.dumps(artifact), encoding="utf-8")

        approval = {
            "schema_version": MODULE.APPROVAL_SCHEMA,
            "visual_review_status": "accepted",
            "reviewed_by": "test-reviewer",
            "reviewed_at": "2026-09-20T17:00:00Z",
            "build_git_sha": "abc123",
            "candidate_sha256": MODULE.sha256(candidate_path),
            "decision_sha256": MODULE.sha256(decision_path),
            "qc_policy_id": "qc-policy-v1",
            "render_policy_id": "render-policy-v1",
            "fabric_id": "natural-earth-test",
            "snap_tolerance_m": tolerance,
            "allow_alternate_tolerance": allow_alternate,
            "approved_geometry_ids": [GOOD_ID],
            "quarantined_geometry_ids": [BAD_ID],
        }
        approval_path.write_text(json.dumps(approval), encoding="utf-8")
        return candidate_path, decision_path, artifact_path, approval_path

    def test_valid_preferred_package_preserves_quarantine(self):
        with tempfile.TemporaryDirectory() as td:
            paths = self._write_package(Path(td))
            package = MODULE.validate_package(*paths)
            self.assertEqual(package["approved_ids"], [GOOD_ID])
            self.assertEqual(package["quarantined_ids"], [BAD_ID])
            self.assertEqual(package["qc_policy_id"], "qc-policy-v1")
            self.assertEqual(package["render_policy_id"], "render-policy-v1")
            self.assertEqual(package["snap_tolerance_m"], 10000)

    def test_checksum_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = self._write_package(root)
            approval_path = paths[-1]
            approval = json.loads(approval_path.read_text(encoding="utf-8"))
            approval["candidate_sha256"] = "0" * 64
            approval_path.write_text(json.dumps(approval), encoding="utf-8")
            with self.assertRaisesRegex(MODULE.PromotionError, "candidate checksum mismatch"):
                MODULE.validate_package(*paths)

    def test_quarantined_geometry_cannot_be_approved(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = self._write_package(root)
            approval_path = paths[-1]
            approval = json.loads(approval_path.read_text(encoding="utf-8"))
            approval["approved_geometry_ids"] = [GOOD_ID, BAD_ID]
            approval["quarantined_geometry_ids"] = []
            approval_path.write_text(json.dumps(approval), encoding="utf-8")
            with self.assertRaisesRegex(MODULE.PromotionError, "QC status 'quarantined'"):
                MODULE.validate_package(*paths)

    def test_alternate_tolerance_requires_explicit_override(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = self._write_package(
                root,
                tolerance=20000,
                selection_role="alternate_candidate",
                allow_alternate=False,
            )
            with self.assertRaisesRegex(MODULE.PromotionError, "explicit alternate approval"):
                MODULE.validate_package(*paths)

    def test_explicit_alternate_override_is_auditable(self):
        with tempfile.TemporaryDirectory() as td:
            paths = self._write_package(
                Path(td),
                tolerance=20000,
                selection_role="alternate_candidate",
                allow_alternate=True,
            )
            package = MODULE.validate_package(*paths)
            self.assertEqual(package["snap_tolerance_m"], 20000)


if __name__ == "__main__":
    unittest.main()
