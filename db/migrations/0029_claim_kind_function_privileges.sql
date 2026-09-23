-- Migration 0029: preserve D-051 private Data API boundary for claim-kind guard functions.
-- PostgreSQL grants EXECUTE on new functions to PUBLIC by default unless explicitly revoked.

revoke execute on function atlas.enforce_claim_kind() from public;
revoke execute on function atlas.prevent_claim_kind_change() from public;
