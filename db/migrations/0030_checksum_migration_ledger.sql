-- Migration 0030: establish the repository checksum migration ledger in production.
-- This does NOT replay migrations 0001-0029. Existing live schema is reconciled separately
-- under #26 / #300 before historical checksums are seeded.

BEGIN;

CREATE SCHEMA IF NOT EXISTS atlas_meta;

CREATE TABLE IF NOT EXISTS atlas_meta.schema_migration (
    migration_name text PRIMARY KEY,
    checksum_sha256 text NOT NULL,
    applied_at timestamptz NOT NULL DEFAULT now(),
    recording_method text NOT NULL DEFAULT 'runner_apply',
    notes text
);

ALTER TABLE atlas_meta.schema_migration
    ADD COLUMN IF NOT EXISTS recording_method text NOT NULL DEFAULT 'runner_apply',
    ADD COLUMN IF NOT EXISTS notes text;

COMMENT ON TABLE atlas_meta.schema_migration IS
'Atlas-controlled deterministic migration checksum ledger. Baseline rows may be recorded after verified live-schema reconciliation; applied_at on baseline rows is recording time, not original migration execution time.';

COMMENT ON COLUMN atlas_meta.schema_migration.recording_method IS
'runner_apply for normal migrations; verified_production_baseline for the one-time reconciled production baseline.';

COMMIT;
