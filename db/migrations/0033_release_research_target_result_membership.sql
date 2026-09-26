-- Migration 0033: add typed release membership for versioned research-target results.
-- A release member is the result version; its target/review/source/claim-bridge children
-- are frozen inside the preservation bundle object digest.

BEGIN;

CREATE TABLE audit.release_research_target_result (
    release_version text NOT NULL
        REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    research_target_result_id uuid NOT NULL
        REFERENCES audit.research_target_result(research_target_result_id) ON DELETE RESTRICT,
    object_sha256 text,
    capture_status text NOT NULL,
    PRIMARY KEY (release_version, research_target_result_id),
    CONSTRAINT release_research_target_result_sha256_format CHECK (
        object_sha256 IS NULL OR object_sha256 ~ '^[0-9A-Fa-f]{64}$'
    ),
    CONSTRAINT release_research_target_result_capture_state CHECK (
        (capture_status = 'legacy_membership_backfill' AND object_sha256 IS NULL)
        OR
        (capture_status = 'captured_at_release' AND object_sha256 IS NOT NULL)
    )
);

COMMENT ON TABLE audit.release_research_target_result IS
'Immutable release membership for versioned research-target results. The bundle digest for each result also freezes its target identity, review events, target-source provenance and target-claim bridges.';

CREATE INDEX release_research_target_result_result_idx
ON audit.release_research_target_result(research_target_result_id);

CREATE TRIGGER release_research_target_result_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_research_target_result
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

COMMIT;
