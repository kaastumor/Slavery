-- Migration 0032: preserve the remaining frozen-v3 target-source relation fields losslessly.
-- These are research/review provenance fields; they do not create historical claims.

BEGIN;

ALTER TABLE audit.research_target_source
    ADD COLUMN source_id_raw text,
    ADD COLUMN decisive boolean,
    ADD COLUMN access_limitation text,
    ADD COLUMN accessed_at_text text,
    ADD COLUMN asset_sha256 text,
    ADD COLUMN dependency_note text,
    ADD CONSTRAINT research_target_source_asset_sha256_format
        CHECK (asset_sha256 IS NULL OR asset_sha256 ~ '^[0-9a-f]{64}$');

COMMENT ON COLUMN audit.research_target_source.source_id_raw IS
'Exact research-packet source_id preserved from the imported source-relation row. It is not a normalized source identity.';
COMMENT ON COLUMN audit.research_target_source.decisive IS
'Packet-level decisive flag preserved as reviewed research provenance; it does not mechanically determine confidence or prevalence.';
COMMENT ON COLUMN audit.research_target_source.access_limitation IS
'Claim/packet-specific access limitation exactly preserved from the research relation.';
COMMENT ON COLUMN audit.research_target_source.accessed_at_text IS
'Source-native/raw access-date text retained without forcing date normalization.';
COMMENT ON COLUMN audit.research_target_source.asset_sha256 IS
'Optional SHA-256 from the research relation. Blank source values remain NULL.';
COMMENT ON COLUMN audit.research_target_source.dependency_note IS
'Exact dependency/reuse note used to prevent false source independence.';

COMMIT;
