-- Migration 0010: provenance for research-coverage assessments.
-- A source reviewed for project coverage is not automatically evidence for a historical practice claim.

BEGIN;

CREATE TABLE audit.research_coverage_source (
    coverage_assessment_id uuid NOT NULL
        REFERENCES audit.research_coverage_assessment(coverage_assessment_id) ON DELETE CASCADE,
    source_version_id uuid NOT NULL
        REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    source_role text NOT NULL DEFAULT 'reviewed_source',
    locator text,
    notes text,
    PRIMARY KEY (coverage_assessment_id, source_version_id, source_role)
);

CREATE INDEX research_coverage_source_version_idx
    ON audit.research_coverage_source(source_version_id);

COMMENT ON TABLE audit.research_coverage_source IS
'Records exact source versions considered in a research-coverage assessment. This relation does not by itself support a territorial-practice claim.';

COMMIT;
