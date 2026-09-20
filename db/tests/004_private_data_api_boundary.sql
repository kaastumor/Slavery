-- D-051 private Data API boundary regression test.
-- A fresh unprivileged role must not inherit access through PUBLIC, and
-- Supabase anon/authenticated roles (when present) must also have no direct
-- privileges on internal schemas.

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'atlas_data_api_probe') THEN
        CREATE ROLE atlas_data_api_probe NOLOGIN;
    END IF;
END $$;

DO $$
DECLARE
    role_name text;
    schema_name text;
    relation_row record;
    routine_row record;
    sequence_row record;
BEGIN
    FOREACH role_name IN ARRAY ARRAY['atlas_data_api_probe', 'anon', 'authenticated'] LOOP
        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = role_name) THEN
            CONTINUE;
        END IF;

        FOREACH schema_name IN ARRAY ARRAY['atlas', 'audit', 'cartography', 'publish'] LOOP
            IF has_schema_privilege(role_name, schema_name, 'USAGE')
               OR has_schema_privilege(role_name, schema_name, 'CREATE') THEN
                RAISE EXCEPTION '% unexpectedly has schema privilege on %', role_name, schema_name;
            END IF;
        END LOOP;

        FOR relation_row IN
            SELECT c.oid, n.nspname, c.relname
            FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname IN ('atlas', 'audit', 'cartography', 'publish')
              AND c.relkind IN ('r', 'p', 'v', 'm', 'f')
        LOOP
            IF has_table_privilege(role_name, relation_row.oid, 'SELECT')
               OR has_table_privilege(role_name, relation_row.oid, 'INSERT')
               OR has_table_privilege(role_name, relation_row.oid, 'UPDATE')
               OR has_table_privilege(role_name, relation_row.oid, 'DELETE') THEN
                RAISE EXCEPTION '% unexpectedly has table privilege on %.%',
                    role_name, relation_row.nspname, relation_row.relname;
            END IF;
        END LOOP;

        FOR sequence_row IN
            SELECT c.oid, n.nspname, c.relname
            FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname IN ('atlas', 'audit', 'cartography', 'publish')
              AND c.relkind = 'S'
        LOOP
            IF has_sequence_privilege(role_name, sequence_row.oid, 'USAGE')
               OR has_sequence_privilege(role_name, sequence_row.oid, 'SELECT')
               OR has_sequence_privilege(role_name, sequence_row.oid, 'UPDATE') THEN
                RAISE EXCEPTION '% unexpectedly has sequence privilege on %.%',
                    role_name, sequence_row.nspname, sequence_row.relname;
            END IF;
        END LOOP;

        FOR routine_row IN
            SELECT p.oid, n.nspname, p.proname
            FROM pg_proc p
            JOIN pg_namespace n ON n.oid = p.pronamespace
            WHERE n.nspname IN ('atlas', 'audit', 'cartography', 'publish')
        LOOP
            IF has_function_privilege(role_name, routine_row.oid, 'EXECUTE') THEN
                RAISE EXCEPTION '% unexpectedly has EXECUTE on %.%',
                    role_name, routine_row.nspname, routine_row.proname;
            END IF;
        END LOOP;
    END LOOP;
END $$;

DROP ROLE atlas_data_api_probe;
