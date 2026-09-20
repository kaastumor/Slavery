-- Migration 0024: fix the remaining Supabase security-advisor warning.
-- The immutable temporal helper needs no caller-controlled namespace lookup.

BEGIN;

ALTER FUNCTION atlas.make_year_range(integer, integer)
    SET search_path = pg_catalog;

COMMIT;
