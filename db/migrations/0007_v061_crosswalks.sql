-- Migration 0007: explicit v0.6.1 reconciliation crosswalks.
BEGIN;
CREATE TABLE audit.v061_source_map (legacy_source_id text PRIMARY KEY, source_id uuid NOT NULL REFERENCES atlas.source(source_id) ON DELETE RESTRICT, source_version_id uuid NOT NULL REFERENCES atlas.source_version(source_version_id) ON DELETE RESTRICT, notes text);
CREATE TABLE audit.v061_owner_actor_map (legacy_owner_id text PRIMARY KEY, actor_id uuid REFERENCES atlas.actor(actor_id) ON DELETE RESTRICT, migration_action text NOT NULL CHECK (migration_action IN ('mapped_actor','missing_placeholder_no_actor','split','other')), notes text, CONSTRAINT missing_placeholder_has_no_actor CHECK ((migration_action='missing_placeholder_no_actor' AND actor_id IS NULL) OR migration_action<>'missing_placeholder_no_actor'));
CREATE TABLE audit.v061_voyage_map (legacy_voyage_id text PRIMARY KEY, voyage_id uuid NOT NULL REFERENCES atlas.voyage(voyage_id) ON DELETE RESTRICT, notes text);
CREATE TABLE audit.v061_voyage_owner_map (legacy_voyage_id text NOT NULL, legacy_owner_id text NOT NULL, owner_sequence integer, voyage_owner_id uuid NOT NULL REFERENCES atlas.voyage_owner(voyage_owner_id) ON DELETE RESTRICT, notes text, PRIMARY KEY(legacy_voyage_id,legacy_owner_id));
CREATE TABLE audit.v061_evidence_claim_map (legacy_evidence_id text NOT NULL, claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT, mapping_role text NOT NULL, notes text, PRIMARY KEY(legacy_evidence_id,claim_id));
COMMIT;
