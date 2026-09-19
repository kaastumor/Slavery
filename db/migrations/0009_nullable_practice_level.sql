-- Migration 0009: distinguish an unassigned P-level from explicit P0.
-- NULL = no P0-P4 assessment has yet been recorded for this claim.
-- P0 = an explicit assessment that no usable practice classification is currently available; never absence.
BEGIN;
ALTER TABLE atlas.territorial_practice_claim ALTER COLUMN practice_level DROP NOT NULL;
COMMENT ON COLUMN atlas.territorial_practice_claim.practice_level IS 'Nullable until an explicit P0-P4 assessment is made. NULL means no P-level assessment recorded; P0 is an explicit unknown/no-usable-classification assessment and does not mean absence.';
COMMIT;
