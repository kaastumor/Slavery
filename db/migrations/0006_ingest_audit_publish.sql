-- Migration 0006: ingest lineage, research coverage, release manifests and public views.

BEGIN;

CREATE TABLE audit.ingest_run (
    ingest_run_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_version_id uuid NOT NULL REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    source_asset_id uuid REFERENCES atlas.source_asset(source_asset_id) ON DELETE RESTRICT,
    started_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    code_version text,
    status text NOT NULL CHECK (status IN ('started', 'completed', 'failed', 'cancelled')),
    notes text,
    CONSTRAINT ingest_time_order CHECK (completed_at IS NULL OR completed_at >= started_at)
);

CREATE TABLE raw.raw_record (
    raw_record_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    ingest_run_id uuid NOT NULL REFERENCES audit.ingest_run(ingest_run_id) ON DELETE RESTRICT,
    record_type text NOT NULL,
    source_native_id text,
    raw_payload jsonb,
    raw_text text,
    checksum_sha256 text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT raw_record_has_payload CHECK (raw_payload IS NOT NULL OR raw_text IS NOT NULL),
    CONSTRAINT raw_record_sha256_format CHECK (
        checksum_sha256 IS NULL OR checksum_sha256 ~ '^[0-9A-Fa-f]{64}$'
    )
);

CREATE INDEX raw_record_ingest_idx ON raw.raw_record(ingest_run_id);
CREATE INDEX raw_record_native_id_idx ON raw.raw_record(source_native_id);

CREATE TABLE audit.research_coverage_assessment (
    coverage_assessment_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    spatial_entity_id uuid REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    region_label_raw text NOT NULL,
    period_label_raw text NOT NULL,
    from_year integer,
    to_year integer,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year, to_year)) STORED,
    legacy_coverage_code text,
    normalized_coverage_state_code text REFERENCES atlas.coverage_state(code),
    coverage_points integer,
    researchability text,
    release_version text,
    review_status atlas.review_status NOT NULL DEFAULT 'draft',
    publication_status atlas.publication_status NOT NULL DEFAULT 'unpublished',
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT research_coverage_year_order CHECK (from_year IS NULL OR to_year IS NULL OR from_year <= to_year),
    CONSTRAINT legacy_coverage_code_allowed CHECK (
        legacy_coverage_code IS NULL OR legacy_coverage_code IN ('S','P','D','RI','—')
    )
);

CREATE INDEX research_coverage_spatial_idx ON audit.research_coverage_assessment(spatial_entity_id);
CREATE INDEX research_coverage_years_gist ON audit.research_coverage_assessment USING gist(valid_years);

CREATE TABLE audit.release_manifest (
    release_version text PRIMARY KEY,
    schema_version text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    status text NOT NULL CHECK (status IN ('draft', 'validated', 'published', 'archived')),
    changelog text,
    qc_summary text,
    unresolved_issues text,
    manifest jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE audit.release_source_version (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    source_version_id uuid NOT NULL REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT,
    PRIMARY KEY(release_version, source_version_id)
);

CREATE TABLE audit.qc_issue (
    qc_issue_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    ingest_run_id uuid REFERENCES audit.ingest_run(ingest_run_id) ON DELETE SET NULL,
    release_version text REFERENCES audit.release_manifest(release_version) ON DELETE SET NULL,
    severity text NOT NULL CHECK (severity IN ('info','warning','error','blocking')),
    issue_code text NOT NULL,
    object_type text,
    object_identifier text,
    description text NOT NULL,
    resolved boolean NOT NULL DEFAULT false,
    resolution_notes text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE OR REPLACE VIEW publish.claim AS
SELECT * FROM atlas.claim WHERE review_status = 'reviewed' AND publication_status = 'published';

CREATE OR REPLACE VIEW publish.territorial_practice_claim AS
SELECT c.*, t.spatial_entity_id, t.practice_type_code, t.practice_level,
       t.coverage_state_code, t.classification_status, t.notes AS subtype_notes
FROM publish.claim c JOIN atlas.territorial_practice_claim t USING (claim_id);

CREATE OR REPLACE VIEW publish.legal_event AS
SELECT c.*, l.jurisdiction_spatial_entity_id, l.event_type, l.legal_status_after,
       l.instrument_name, l.scope, l.effective_date_text, l.notes AS subtype_notes
FROM publish.claim c JOIN atlas.legal_event l USING (claim_id);

CREATE OR REPLACE VIEW publish.actor AS SELECT * FROM atlas.actor WHERE review_status = 'reviewed';
CREATE OR REPLACE VIEW publish.spatial_entity AS SELECT * FROM atlas.spatial_entity WHERE review_status = 'reviewed';
CREATE OR REPLACE VIEW publish.geometry AS SELECT * FROM atlas.geometry WHERE review_status = 'reviewed';
CREATE OR REPLACE VIEW publish.research_coverage_assessment AS
SELECT * FROM audit.research_coverage_assessment WHERE review_status = 'reviewed' AND publication_status = 'published';

COMMIT;
