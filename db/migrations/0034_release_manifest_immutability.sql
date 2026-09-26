-- Migration 0034: freeze release-manifest metadata after publication.
--
-- D-112 closes a Gate-5 integrity gap: typed membership and release artifacts were
-- already immutable after publication, but the parent audit.release_manifest row
-- remained owner-mutable even though public serving uses manifest metadata.
--
-- Published release metadata is immutable. A published release may transition to
-- archived only when every other column remains byte/semantically identical. Archived
-- releases are fully immutable. Draft/validated rows retain their pre-publication
-- lifecycle.

CREATE OR REPLACE FUNCTION audit.guard_published_release_manifest()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog
AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        IF OLD.status IN ('published', 'archived') THEN
            RAISE EXCEPTION
                'release manifest % is immutable while status is %',
                OLD.release_version, OLD.status;
        END IF;
        RETURN OLD;
    END IF;

    IF TG_OP = 'UPDATE' AND OLD.status = 'published' THEN
        IF NEW.status = 'archived'
           AND (to_jsonb(NEW) - 'status') IS NOT DISTINCT FROM
               (to_jsonb(OLD) - 'status') THEN
            RETURN NEW;
        END IF;

        RAISE EXCEPTION
            'published release manifest % is immutable except for metadata-identical archival',
            OLD.release_version;
    END IF;

    IF TG_OP = 'UPDATE' AND OLD.status = 'archived' THEN
        RAISE EXCEPTION
            'archived release manifest % is immutable',
            OLD.release_version;
    END IF;

    RETURN NEW;
END;
$$;

REVOKE EXECUTE ON FUNCTION audit.guard_published_release_manifest() FROM PUBLIC;

CREATE TRIGGER release_manifest_immutable
BEFORE UPDATE OR DELETE ON audit.release_manifest
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_manifest();
