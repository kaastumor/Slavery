-- Migration 0022: make research-case ingestion retry-safe and auditable.
-- Future claim-centric research packages receive a stable case_key and content hash.
-- Reapplying equivalent logical content is a no-op; changing already-applied
-- content under the same case_key is rejected by the loader.

BEGIN;

CREATE TABLE audit.research_case_ingest (
    case_key text PRIMARY KEY,
    content_sha256 text NOT NULL
        CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    claim_id uuid NOT NULL UNIQUE
        REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    source_path text,
    git_revision text,
    applied_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE audit.research_case_ingest IS
'Idempotency/provenance ledger for claim-centric research case ingestion. One immutable case_key maps to one claim and canonicalized JSON content hash.';

COMMENT ON COLUMN audit.research_case_ingest.case_key IS
'Stable repository/research identity for one immutable ingested research package.';

COMMENT ON COLUMN audit.research_case_ingest.content_sha256 IS
'SHA-256 of canonical JSON serialization used to reject silent mutation on retry.';

COMMIT;
