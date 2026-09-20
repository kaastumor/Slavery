-- Migration 0023: enforce D-051 private-schema Data API boundary.
-- Internal research/publication schemas are server-side database boundaries, not
-- direct anon/authenticated PostgREST surfaces.

BEGIN;

-- PUBLIC is inherited by every role. Remove any present or future accidental
-- PUBLIC access from the internal schemas and their objects.
REVOKE ALL PRIVILEGES ON SCHEMA atlas, audit, cartography, publish FROM PUBLIC;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA atlas, audit, cartography, publish FROM PUBLIC;
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA atlas, audit, cartography, publish FROM PUBLIC;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA atlas, audit, cartography, publish FROM PUBLIC;

ALTER DEFAULT PRIVILEGES IN SCHEMA atlas, audit, cartography, publish
    REVOKE ALL PRIVILEGES ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA atlas, audit, cartography, publish
    REVOKE ALL PRIVILEGES ON SEQUENCES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA atlas, audit, cartography, publish
    REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;

-- Supabase client roles do not exist in the generic local PostGIS container,
-- so apply explicit revokes only where those platform roles are present.
DO $$
DECLARE
    role_name text;
    schema_name text;
BEGIN
    FOREACH role_name IN ARRAY ARRAY['anon', 'authenticated'] LOOP
        IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = role_name) THEN
            FOREACH schema_name IN ARRAY ARRAY['atlas', 'audit', 'cartography', 'publish'] LOOP
                EXECUTE format(
                    'REVOKE ALL PRIVILEGES ON SCHEMA %I FROM %I',
                    schema_name,
                    role_name
                );
                EXECUTE format(
                    'REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA %I FROM %I',
                    schema_name,
                    role_name
                );
                EXECUTE format(
                    'REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA %I FROM %I',
                    schema_name,
                    role_name
                );
                EXECUTE format(
                    'REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA %I FROM %I',
                    schema_name,
                    role_name
                );
                EXECUTE format(
                    'ALTER DEFAULT PRIVILEGES IN SCHEMA %I REVOKE ALL PRIVILEGES ON TABLES FROM %I',
                    schema_name,
                    role_name
                );
                EXECUTE format(
                    'ALTER DEFAULT PRIVILEGES IN SCHEMA %I REVOKE ALL PRIVILEGES ON SEQUENCES FROM %I',
                    schema_name,
                    role_name
                );
                EXECUTE format(
                    'ALTER DEFAULT PRIVILEGES IN SCHEMA %I REVOKE EXECUTE ON FUNCTIONS FROM %I',
                    schema_name,
                    role_name
                );
            END LOOP;
        END IF;
    END LOOP;
END $$;

COMMIT;
