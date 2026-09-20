-- Migration 0025: explicit serving-channel pointer for reversible release promotion.

BEGIN;

CREATE TABLE audit.release_channel (
    channel_code text PRIMARY KEY,
    release_version text NOT NULL REFERENCES audit.release_manifest(release_version) ON DELETE RESTRICT,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by text,
    note text,
    CONSTRAINT release_channel_code_format
        CHECK (channel_code ~ '^[a-z][a-z0-9_]{2,63}$')
);

CREATE OR REPLACE FUNCTION audit.validate_release_channel_target()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = pg_catalog
AS $$
DECLARE
    target_status text;
    target_purpose text;
BEGIN
    SELECT rm.status, rm.manifest->>'purpose'
    INTO target_status, target_purpose
    FROM audit.release_manifest rm
    WHERE rm.release_version = NEW.release_version;

    IF target_status IS NULL THEN
        RAISE EXCEPTION 'release channel target % does not exist', NEW.release_version;
    END IF;

    IF target_status <> 'published' THEN
        RAISE EXCEPTION 'release channel target % has status %, expected published',
            NEW.release_version, target_status;
    END IF;

    IF target_purpose IS DISTINCT FROM NEW.channel_code THEN
        RAISE EXCEPTION 'release channel target % purpose % does not match channel %',
            NEW.release_version, coalesce(target_purpose, '<null>'), NEW.channel_code;
    END IF;

    NEW.updated_at := now();
    RETURN NEW;
END;
$$;

REVOKE EXECUTE ON FUNCTION audit.validate_release_channel_target() FROM PUBLIC;

CREATE TRIGGER release_channel_target_guard
BEFORE INSERT OR UPDATE OF channel_code, release_version
ON audit.release_channel
FOR EACH ROW
EXECUTE FUNCTION audit.validate_release_channel_target();

COMMIT;
