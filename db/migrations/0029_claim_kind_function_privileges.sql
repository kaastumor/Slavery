-- Migration 0029: preserve D-051 private-schema function boundary for D-060 helpers.
-- 0028 is already applied and immutable; explicitly revoke PostgreSQL's default PUBLIC execution.

BEGIN;

REVOKE EXECUTE ON FUNCTION atlas.enforce_claim_kind() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION atlas.prevent_claim_kind_change() FROM PUBLIC;

COMMIT;
