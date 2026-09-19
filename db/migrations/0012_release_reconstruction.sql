-- Migration 0012: explicit immutable release membership and release artifacts.
-- Implements D-030 on the architecture/release-reconstruction branch.

BEGIN;

CREATE TABLE audit.release_claim (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    claim_id uuid NOT NULL REFERENCES atlas.claim(claim_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, claim_id)
);

CREATE TABLE audit.release_actor (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    actor_id uuid NOT NULL REFERENCES atlas.actor(actor_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, actor_id)
);

CREATE TABLE audit.release_spatial_entity (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, spatial_entity_id)
);

CREATE TABLE audit.release_geometry (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    geometry_id uuid NOT NULL REFERENCES atlas.geometry(geometry_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, geometry_id)
);

CREATE TABLE audit.release_spatial_relation (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    spatial_relation_id uuid NOT NULL REFERENCES atlas.spatial_relation(spatial_relation_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, spatial_relation_id)
);

CREATE TABLE audit.release_voyage (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    voyage_id uuid NOT NULL REFERENCES atlas.voyage(voyage_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, voyage_id)
);

CREATE TABLE audit.release_voyage_owner (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    voyage_owner_id uuid NOT NULL REFERENCES atlas.voyage_owner(voyage_owner_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, voyage_owner_id)
);

CREATE TABLE audit.release_voyage_finance (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    voyage_finance_id uuid NOT NULL REFERENCES atlas.voyage_finance(voyage_finance_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, voyage_finance_id)
);

CREATE TABLE audit.release_voyage_stop (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    voyage_stop_id uuid NOT NULL REFERENCES atlas.voyage_stop(voyage_stop_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, voyage_stop_id)
);

CREATE TABLE audit.release_coverage_assessment (
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    coverage_assessment_id uuid NOT NULL REFERENCES audit.research_coverage_assessment(coverage_assessment_id) ON DELETE RESTRICT,
    PRIMARY KEY (release_version, coverage_assessment_id)
);

CREATE TABLE audit.release_artifact (
    release_artifact_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE CASCADE,
    artifact_role text NOT NULL,
    filename text NOT NULL,
    checksum_sha256 text NOT NULL,
    size_bytes bigint NOT NULL,
    media_type text,
    storage_locator text,
    preservation_identifier text,
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (release_version, artifact_role, filename),
    CONSTRAINT release_artifact_sha256_format CHECK (checksum_sha256 ~ '^[0-9A-Fa-f]{64}$'),
    CONSTRAINT release_artifact_size_nonnegative CHECK (size_bytes >= 0)
);

CREATE INDEX release_claim_claim_idx ON audit.release_claim(claim_id);
CREATE INDEX release_actor_actor_idx ON audit.release_actor(actor_id);
CREATE INDEX release_spatial_entity_entity_idx ON audit.release_spatial_entity(spatial_entity_id);
CREATE INDEX release_geometry_geometry_idx ON audit.release_geometry(geometry_id);
CREATE INDEX release_spatial_relation_relation_idx ON audit.release_spatial_relation(spatial_relation_id);
CREATE INDEX release_voyage_voyage_idx ON audit.release_voyage(voyage_id);
CREATE INDEX release_voyage_owner_owner_idx ON audit.release_voyage_owner(voyage_owner_id);
CREATE INDEX release_voyage_finance_finance_idx ON audit.release_voyage_finance(voyage_finance_id);
CREATE INDEX release_voyage_stop_stop_idx ON audit.release_voyage_stop(voyage_stop_id);
CREATE INDEX release_coverage_assessment_idx ON audit.release_coverage_assessment(coverage_assessment_id);
CREATE INDEX release_artifact_release_idx ON audit.release_artifact(release_version);

CREATE OR REPLACE FUNCTION audit.assert_release_membership_mutable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_release_version text;
    v_status text;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_release_version := OLD.release_version;
    ELSE
        v_release_version := NEW.release_version;
    END IF;

    SELECT status INTO v_status
    FROM audit.release_manifest
    WHERE release_version = v_release_version;

    IF v_status IS NULL THEN
        RAISE EXCEPTION 'release % does not exist', v_release_version;
    END IF;

    IF v_status <> 'draft' THEN
        RAISE EXCEPTION 'release % membership is immutable once status is %', v_release_version, v_status;
    END IF;

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER release_source_version_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_source_version
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_claim_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_claim
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_actor_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_actor
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_spatial_entity_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_spatial_entity
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_geometry_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_geometry
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_spatial_relation_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_spatial_relation
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_voyage_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_voyage
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_voyage_owner_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_voyage_owner
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_voyage_finance_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_voyage_finance
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_voyage_stop_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_voyage_stop
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_coverage_assessment_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_coverage_assessment
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE TRIGGER release_artifact_mutability
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_artifact
FOR EACH ROW EXECUTE FUNCTION audit.assert_release_membership_mutable();

CREATE OR REPLACE FUNCTION audit.guard_release_manifest_lifecycle()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.status <> 'draft' THEN
            RAISE EXCEPTION 'new releases must start in draft status';
        END IF;
        RETURN NEW;
    END IF;

    IF TG_OP = 'DELETE' THEN
        IF OLD.status <> 'draft' THEN
            RAISE EXCEPTION 'validated/published/archived releases cannot be deleted';
        END IF;
        RETURN OLD;
    END IF;

    IF OLD.status = 'draft' THEN
        IF NEW.status NOT IN ('draft', 'validated') THEN
            RAISE EXCEPTION 'release lifecycle must progress draft -> validated -> published -> archived';
        END IF;
        RETURN NEW;
    END IF;

    IF (to_jsonb(NEW) - 'status') IS DISTINCT FROM (to_jsonb(OLD) - 'status') THEN
        RAISE EXCEPTION 'release content is immutable after validation';
    END IF;

    IF OLD.status = 'validated' AND NEW.status NOT IN ('validated', 'published') THEN
        RAISE EXCEPTION 'validated release may only remain validated or become published';
    ELSIF OLD.status = 'published' AND NEW.status NOT IN ('published', 'archived') THEN
        RAISE EXCEPTION 'published release may only remain published or become archived';
    ELSIF OLD.status = 'archived' AND NEW.status <> 'archived' THEN
        RAISE EXCEPTION 'archived release is immutable';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER release_manifest_lifecycle_guard
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_manifest
FOR EACH ROW EXECUTE FUNCTION audit.guard_release_manifest_lifecycle();

CREATE OR REPLACE VIEW audit.release_membership_summary AS
SELECT
    r.release_version,
    r.status,
    (SELECT count(*) FROM audit.release_claim x WHERE x.release_version = r.release_version) AS claim_count,
    (SELECT count(*) FROM audit.release_actor x WHERE x.release_version = r.release_version) AS actor_count,
    (SELECT count(*) FROM audit.release_spatial_entity x WHERE x.release_version = r.release_version) AS spatial_entity_count,
    (SELECT count(*) FROM audit.release_geometry x WHERE x.release_version = r.release_version) AS geometry_count,
    (SELECT count(*) FROM audit.release_spatial_relation x WHERE x.release_version = r.release_version) AS spatial_relation_count,
    (SELECT count(*) FROM audit.release_voyage x WHERE x.release_version = r.release_version) AS voyage_count,
    (SELECT count(*) FROM audit.release_voyage_owner x WHERE x.release_version = r.release_version) AS voyage_owner_count,
    (SELECT count(*) FROM audit.release_voyage_finance x WHERE x.release_version = r.release_version) AS voyage_finance_count,
    (SELECT count(*) FROM audit.release_voyage_stop x WHERE x.release_version = r.release_version) AS voyage_stop_count,
    (SELECT count(*) FROM audit.release_source_version x WHERE x.release_version = r.release_version) AS source_version_count,
    (SELECT count(*) FROM audit.release_coverage_assessment x WHERE x.release_version = r.release_version) AS coverage_assessment_count,
    (SELECT count(*) FROM audit.release_artifact x WHERE x.release_version = r.release_version) AS artifact_count
FROM audit.release_manifest r;

COMMIT;
