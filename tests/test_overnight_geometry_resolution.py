from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKET = (
    ROOT
    / "data"
    / "research"
    / "geometry_reviews"
    / "overnight_2026_09_27_resolution_reconciliation.json"
)


class OvernightGeometryResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
        cls.by_subject = {row["subject"]: row for row in cls.packet["entries"]}

    def test_country_polygons_are_context_only(self) -> None:
        self.assertIn(
            "CONTEXT_ONLY",
            self.by_subject["DPRK"]["disposition"],
        )
        self.assertIn(
            "CONTEXT_ONLY",
            self.by_subject["Brazil"]["disposition"],
        )

    def test_shang_and_carolingian_fail_closed(self) -> None:
        self.assertTrue(self.by_subject["Shang China"]["disposition"].startswith("HOLD_"))
        self.assertTrue(
            self.by_subject["Carolingian Empire"]["disposition"].startswith("HOLD_")
        )

    def test_mycenaean_points_are_loci_not_territory(self) -> None:
        row = self.by_subject["Mycenaean Greece (Pylos/Knossos)"]
        self.assertEqual(row["disposition"], "ACCEPT_LOCUS_DESIGN_PENDING_DB_PROMOTION")
        self.assertEqual(len(row["candidates"]), 2)
        for candidate in row["candidates"]:
            self.assertEqual(candidate["role"], "evidence_locus")
            self.assertEqual(candidate["geometry"]["type"], "Point")
        self.assertIn("not Mycenaean territorial polygon", row["candidates"][1]["bounded_temporal_note"])

    def test_unretrieved_followups_are_not_silently_promoted(self) -> None:
        note = " ".join(self.packet["retrieval_notes"])
        for name in ("PRC/CShapes", "Peruvian Amazon/RAISG", "Hawaiʻi", "Funan"):
            self.assertIn(name, note)


if __name__ == "__main__":
    unittest.main()
