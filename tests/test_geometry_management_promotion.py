from pathlib import Path
import importlib.util
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "promote_geometry_management.py"
SPEC = importlib.util.spec_from_file_location("promote_geometry_management", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class GeometryManagementPromotionTests(unittest.TestCase):
    def fixture(self):
        plan = {
            "promotion_id": "test",
            "policy_id": "external-test",
            "artifact": {
                "land_fabric_id": "land-v1",
                "land_sha256": "b" * 64,
            },
        }
        manifest = {
            "created_at": "2026-09-20T00:00:00+00:00",
            "parameters": {"smooth_iterations": "1"},
        }
        rows = [
            {
                "geometry_id": "11111111-1111-1111-1111-111111111111",
                "action": "promote",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
                },
                "metrics": {
                    "source_npoints": 4,
                    "render_npoints": 4,
                    "hausdorff_m": 100.0,
                    "area_delta_pct": 0.2,
                },
            },
            {
                "geometry_id": "22222222-2222-2222-2222-222222222222",
                "action": "quarantine",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[2, 0], [3, 0], [3, 1], [2, 0]]],
                },
                "metrics": {
                    "source_npoints": 4,
                    "render_npoints": 4,
                    "hausdorff_m": 200.0,
                    "area_delta_pct": -8.0,
                },
            },
            {
                "geometry_id": "33333333-3333-3333-3333-333333333333",
                "action": "preserve_existing_live",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[4, 0], [5, 0], [5, 1], [4, 0]]],
                },
                "metrics": {
                    "source_npoints": 4,
                    "render_npoints": 4,
                    "hausdorff_m": 50.0,
                    "area_delta_pct": 0.1,
                },
            },
        ]
        return plan, manifest, rows

    def test_apply_sql_inserts_only_promotable_geometry(self):
        plan, manifest, rows = self.fixture()
        sql = MODULE.build_apply_sql(plan, manifest, rows)
        self.assertIn("insert into cartography.render_geometry_cache", sql)
        self.assertIn("11111111-1111-1111-1111-111111111111", sql)
        self.assertIn("22222222-2222-2222-2222-222222222222", sql)
        self.assertIn("33333333-3333-3333-3333-333333333333", sql)
        self.assertEqual(sql.count("insert into cartography.render_geometry_cache"), 1)
        self.assertIn("post-insert exact geometry verification failed", sql)
        self.assertIn("begin;", sql)
        self.assertIn("commit;", sql)

    def test_preflight_accepts_expected_database_state(self):
        plan, _manifest, rows = self.fixture()
        database_rows = [
            {"kind": "fabric", "id": "land-v1", "detail1": "b" * 64, "detail2": "true"},
            {"kind": "policy", "id": "external-test", "detail1": "external", "detail2": "true"},
            {"kind": "source", "id": rows[0]["geometry_id"], "detail1": "reviewed", "detail2": "4"},
            {"kind": "source", "id": rows[1]["geometry_id"], "detail1": "reviewed", "detail2": "4"},
            {"kind": "source", "id": rows[2]["geometry_id"], "detail1": "reviewed", "detail2": "4"},
            {"kind": "cache", "id": rows[2]["geometry_id"], "detail1": "external-test", "detail2": "4"},
        ]
        MODULE.validate_preflight_rows(plan, rows, database_rows)

    def test_preflight_rejects_quarantined_cache_row(self):
        plan, _manifest, rows = self.fixture()
        database_rows = [
            {"kind": "fabric", "id": "land-v1", "detail1": "b" * 64, "detail2": "true"},
            {"kind": "policy", "id": "external-test", "detail1": "external", "detail2": "true"},
        ]
        database_rows.extend(
            {"kind": "source", "id": row["geometry_id"], "detail1": "reviewed", "detail2": "4"}
            for row in rows
        )
        database_rows.append(
            {"kind": "cache", "id": rows[2]["geometry_id"], "detail1": "external-test", "detail2": "4"}
        )
        database_rows.append(
            {"kind": "cache", "id": rows[1]["geometry_id"], "detail1": "external-test", "detail2": "4"}
        )
        with self.assertRaises(MODULE.PromotionError):
            MODULE.validate_preflight_rows(plan, rows, database_rows)


if __name__ == "__main__":
    unittest.main()
