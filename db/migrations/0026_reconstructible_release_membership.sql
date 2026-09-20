-- Migration 0026: typed release membership and immutable artifact metadata.
-- D-054 hybrid model: queryable typed membership + preservation-grade bundle.

BEGIN;

CREATE TABLE audit.release_claim (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    object_sha256 text,
    capture_status text NOT NULL,
    PRIMARY KEY (release_version, claim_id),
    CONSTRAINT release_claim_sha256_format CHECK (
        object_sha256 IS NULL OR object_sha256 ~ '^[0-9A-Fa-f]{64}$'
    ),
    CONSTRAINT release_claim_capture_state CHECK (
        (capture_status = 'legacy_membership_backfill' AND object_sha256 IS NULL)
        OR
        (capture_status = 'captured_at_release' AND object_sha256 IS NOT NULL)
    )
);

CREATE TABLE audit.release_actor (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    actor_id uuid NOT NULL REFERENCES atlas.actor(actor_id) ON DELETE RESTRICT,
    object_sha256 text,
    capture_status text NOT NULL,
    PRIMARY KEY (release_version, actor_id),
    CONSTRAINT release_actor_sha256_format CHECK (
        object_sha256 IS NULL OR object_sha256 ~ '^[0-9A-Fa-f]{64}$'
    ),
    CONSTRAINT release_actor_capture_state CHECK (
        (capture_status = 'legacy_membership_backfill' AND object_sha256 IS NULL)
        OR
        (capture_status = 'captured_at_release' AND object_sha256 IS NOT NULL)
    )
);

CREATE TABLE audit.release_spatial_entity (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    object_sha256 text,
    capture_status text NOT NULL,
    PRIMARY KEY (release_version, spatial_entity_id),
    CONSTRAINT release_spatial_entity_sha256_format CHECK (
        object_sha256 IS NULL OR object_sha256 ~ '^[0-9A-Fa-f]{64}$'
    ),
    CONSTRAINT release_spatial_entity_capture_state CHECK (
        (capture_status = 'legacy_membership_backfill' AND object_sha256 IS NULL)
        OR
        (capture_status = 'captured_at_release' AND object_sha256 IS NOT NULL)
    )
);

CREATE TABLE audit.release_geometry (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    geometry_id uuid NOT NULL REFERENCES atlas.geometry(geometry_id) ON DELETE RESTRICT,
    object_sha256 text,
    capture_status text NOT NULL,
    PRIMARY KEY (release_version, geometry_id),
    CONSTRAINT release_geometry_sha256_format CHECK (
        object_sha256 IS NULL OR object_sha256 ~ '^[0-9A-Fa-f]{64}$'
    ),
    CONSTRAINT release_geometry_capture_state CHECK (
        (capture_status = 'legacy_membership_backfill' AND object_sha256 IS NULL)
        OR
        (capture_status = 'captured_at_release' AND object_sha256 IS NOT NULL)
    )
);

CREATE TABLE audit.release_voyage (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    voyage_id uuid NOT NULL REFERENCES atlas.voyage(voyage_id) ON DELETE RESTRICT,
    object_sha256 text,
    capture_status text NOT NULL,
    PRIMARY KEY (release_version, voyage_id),
    CONSTRAINT release_voyage_sha256_format CHECK (
        object_sha256 IS NULL OR object_sha256 ~ '^[0-9A-Fa-f]{64}$'
    ),
    CONSTRAINT release_voyage_capture_state CHECK (
        (capture_status = 'legacy_membership_backfill' AND object_sha256 IS NULL)
        OR
        (capture_status = 'captured_at_release' AND object_sha256 IS NOT NULL)
    )
);

CREATE TABLE audit.release_coverage_assessment (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    coverage_assessment_id uuid NOT NULL REFERENCES audit.research_coverage_assessment(coverage_assessment_id) ON DELETE RESTRICT,
    object_sha256 text,
    capture_status text NOT NULL,
    PRIMARY KEY (release_version, coverage_assessment_id),
    CONSTRAINT release_coverage_sha256_format CHECK (
        object_sha256 IS NULL OR object_sha256 ~ '^[0-9A-Fa-f]{64}$'
    ),
    CONSTRAINT release_coverage_capture_state CHECK (
        (capture_status = 'legacy_membership_backfill' AND object_sha256 IS NULL)
        OR
        (capture_status = 'captured_at_release' AND object_sha256 IS NOT NULL)
    )
);

ALTER TABLE audit.release_source_version
    ADD COLUMN object_sha256 text,
    ADD COLUMN capture_status text;

UPDATE audit.release_source_version
SET capture_status='legacy_membership_backfill'
WHERE capture_status IS NULL;

ALTER TABLE audit.release_source_version
    ALTER COLUMN capture_status SET NOT NULL,
    ADD CONSTRAINT release_source_version_sha256_format CHECK (
        object_sha256 IS NULL OR object_sha256 ~ '^[0-9A-Fa-f]{64}$'
    ),
    ADD CONSTRAINT release_source_version_capture_state CHECK (
        (capture_status = 'legacy_membership_backfill' AND object_sha256 IS NULL)
        OR
        (capture_status = 'captured_at_release' AND object_sha256 IS NOT NULL)
    );

CREATE TABLE audit.release_artifact (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    artifact_role text NOT NULL,
    filename text NOT NULL,
    sha256 text NOT NULL,
    size_bytes bigint NOT NULL CHECK (size_bytes >= 0),
    media_type text NOT NULL,
    storage_status text NOT NULL CHECK (
        storage_status IN ('workflow_artifact','object_store','repository','external')
    ),
    storage_locator text,
    capture_status text NOT NULL CHECK (
        capture_status IN ('captured_at_release','legacy_postpublish')
    ),
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (release_version, artifact_role, filename),
    CONSTRAINT release_artifact_sha256_format CHECK (
        sha256 ~ '^[0-9A-Fa-f]{64}$'
    )
);

-- Backfill only membership IDs recorded by older manifests. Do not invent
-- exact historical row digests for releases that predate D-054.
INSERT INTO audit.release_claim(release_version, claim_id, object_sha256, capture_status)
SELECT rm.release_version, x.value::uuid, NULL, 'legacy_membership_backfill'
FROM audit.release_manifest rm
CROSS JOIN LATERAL jsonb_array_elements_text(
    coalesce(rm.manifest->'claim_ids', '[]'::jsonb)
) AS x(value)
ON CONFLICT DO NOTHING;

INSERT INTO audit.release_spatial_entity(release_version, spatial_entity_id, object_sha256, capture_status)
SELECT rm.release_version, x.value::uuid, NULL, 'legacy_membership_backfill'
FROM audit.release_manifest rm
CROSS JOIN LATERAL jsonb_array_elements_text(
    coalesce(rm.manifest->'spatial_entity_ids', '[]'::jsonb)
) AS x(value)
ON CONFLICT DO NOTHING;

INSERT INTO audit.release_geometry(release_version, geometry_id, object_sha256, capture_status)
SELECT rm.release_version, x.value::uuid, NULL, 'legacy_membership_backfill'
FROM audit.release_manifest rm
CROSS JOIN LATERAL jsonb_array_elements_text(
    coalesce(rm.manifest->'geometry_ids', '[]'::jsonb)
) AS x(value)
ON CONFLICT DO NOTHING;

INSERT INTO audit.release_actor(release_version, actor_id, object_sha256, capture_status)
SELECT rm.release_version, x.value::uuid, NULL, 'legacy_membership_backfill'
FROM audit.release_manifest rm
CROSS JOIN LATERAL jsonb_array_elements_text(
    coalesce(rm.manifest->'actor_ids', '[]'::jsonb)
) AS x(value)
ON CONFLICT DO NOTHING;

INSERT INTO audit.release_voyage(release_version, voyage_id, object_sha256, capture_status)
SELECT rm.release_version, x.value::uuid, NULL, 'legacy_membership_backfill'
FROM audit.release_manifest rm
CROSS JOIN LATERAL jsonb_array_elements_text(
    coalesce(rm.manifest->'voyage_ids', '[]'::jsonb)
) AS x(value)
ON CONFLICT DO NOTHING;

INSERT INTO audit.release_coverage_assessment(
    release_version, coverage_assessment_id, object_sha256, capture_status
)
SELECT rm.release_version, x.value::uuid, NULL, 'legacy_membership_backfill'
FROM audit.release_manifest rm
CROSS JOIN LATERAL jsonb_array_elements_text(
    coalesce(rm.manifest->'coverage_assessment_ids', '[]'::jsonb)
) AS x(value)
ON CONFLICT DO NOTHING;

CREATE OR REPLACE FUNCTION audit.guard_published_release_membership()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog
AS $$
DECLARE
    target_release text;
    target_status text;
BEGIN
    target_release := CASE WHEN TG_OP = 'DELETE' THEN OLD.release_version ELSE NEW.release_version END;

    SELECT status
    INTO target_status
    FROM audit.release_manifest
    WHERE release_version = target_release;

    IF target_status IN ('published', 'archived') THEN
        RAISE EXCEPTION 'release membership for % is immutable while release status is %',
            target_release, target_status;
    END IF;

    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

REVOKE EXECUTE ON FUNCTION audit.guard_published_release_membership() FROM PUBLIC;

CREATE TRIGGER release_claim_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_claim
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

CREATE TRIGGER release_actor_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_actor
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

CREATE TRIGGER release_spatial_entity_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_spatial_entity
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

CREATE TRIGGER release_geometry_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_geometry
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

CREATE TRIGGER release_voyage_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_voyage
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

CREATE TRIGGER release_coverage_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_coverage_assessment
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

CREATE TRIGGER release_source_version_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_source_version
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

COMMIT;
