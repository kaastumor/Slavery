from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class M2TargetSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.method = (ROOT / "docs" / "02_METHOD_AND_ONTOLOGY.md").read_text(encoding="utf-8")
        cls.model = (ROOT / "docs" / "04_DATA_MODEL.md").read_text(encoding="utf-8")
        cls.schema = (ROOT / "docs" / "schema_draft.yaml").read_text(encoding="utf-8")
        cls.decisions = (ROOT / "docs" / "08_DECISIONS_LOG.md").read_text(encoding="utf-8")

    def test_p_levels_are_legacy_compatibility_not_target_ordinal(self):
        self.assertIn("Legacy P0–P4 compatibility", self.method)
        self.assertIn("legacy_practice_level_role: release_and_migration_compatibility_only", self.schema)
        self.assertIn("target universal comparative ontology", self.decisions)

    def test_historical_characterization_axes_are_orthogonal(self):
        for field in (
            "occurrence_pattern",
            "institutionalization",
            "prevalence_scope",
            "structural_significance",
        ):
            self.assertIn(field, self.schema)
            self.assertIn(field, self.model)
        self.assertIn("institutionalization_from_recurrence_alone", self.schema)
        self.assertIn("prevalence_from_institutionalization_alone", self.schema)

    def test_evidence_and_workflow_axes_are_split(self):
        for field in (
            "attestation_pattern",
            "interpretive_basis",
            "research_stage",
            "classification_outcome",
        ):
            self.assertIn(field, self.schema)
        self.assertIn("Research stage and classification outcome", self.method)

    def test_time_and_space_truth_are_not_inferred_from_query_or_geometry(self):
        self.assertIn("selected_year_truth_requires_applicability_semantics: true", self.schema)
        self.assertIn("selected_year_truth_from_outer_query_range_alone", self.schema)
        self.assertIn("inference_extent_from_containing_or_drawable_geometry", self.schema)
        self.assertIn("CLAIM_ASSERTED_INTERVAL", self.model)
        self.assertIn("CLAIM_EVIDENCE_LOCUS", self.model)
        self.assertIn("CLAIM_INFERENCE_EXTENT", self.model)

    def test_schema_is_target_prototype_not_live_production_claim(self):
        self.assertIn("schema_version: draft-0.11", self.schema)
        self.assertIn(
            "status: m2_target_semantics_canonicalized_and_disposable_prototype_validated_not_production_migrated",
            self.schema,
        )
        self.assertIn("canonical **target methodology/data model**", self.decisions)
        self.assertIn("This does not mutate canonical historical release v0.6.1", self.decisions)


if __name__ == "__main__":
    unittest.main()
