-- Migration 0014: give canonical cartography fabric rows a created_at default.

BEGIN;

ALTER TABLE cartography.land_fabric
    ALTER COLUMN created_at SET DEFAULT now();

COMMIT;
