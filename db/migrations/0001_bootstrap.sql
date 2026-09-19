-- Historical Slavery Atlas — database foundation
-- Migration 0001: extensions, logical schemas, stable domains, temporal helper
-- Target: PostgreSQL 16+ with PostGIS 3.x. The SQL intentionally avoids PG18-only features.

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS atlas;
CREATE SCHEMA IF NOT EXISTS publish;
CREATE SCHEMA IF NOT EXISTS audit;

CREATE DOMAIN atlas.review_status AS text
    CHECK (VALUE IN ('draft', 'reviewed', 'rejected'));

CREATE DOMAIN atlas.publication_status AS text
    CHECK (VALUE IN ('unpublished', 'published', 'superseded', 'withdrawn'));

CREATE DOMAIN atlas.practice_level AS text
    CHECK (VALUE IN ('P0', 'P1', 'P2', 'P3', 'P4'));

CREATE DOMAIN atlas.geometry_accuracy AS text
    CHECK (VALUE IN ('exact', 'specialist', 'approximate_historical', 'modern_proxy', 'unresolved'));

CREATE DOMAIN atlas.evidence_direction AS text
    CHECK (VALUE IN ('supports', 'challenges', 'qualifies', 'context'));

CREATE OR REPLACE FUNCTION atlas.make_year_range(p_from_year integer, p_to_year integer)
RETURNS int4range
LANGUAGE sql
IMMUTABLE
PARALLEL SAFE
AS $$
    SELECT CASE
        WHEN p_from_year IS NULL AND p_to_year IS NULL THEN NULL
        ELSE int4range(
            p_from_year,
            CASE WHEN p_to_year IS NULL THEN NULL ELSE p_to_year + 1 END,
            '[)'
        )
    END;
$$;

COMMENT ON FUNCTION atlas.make_year_range(integer, integer) IS
'Builds a half-open int4range from inclusive research bounds using astronomical integer years. NULL/NULL means unknown, not all time.';

COMMIT;
