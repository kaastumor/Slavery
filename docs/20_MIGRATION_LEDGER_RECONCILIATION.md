# Migration ledger reconciliation

## 2026-09-21 live inventory

Issue #26 tracks divergence between repository migration files and the Supabase platform ledger. Repository migrations run `0001` through `0027`. A read-only live `list_migrations` inventory found `0001`–`0011`, then `0015`–`0027`; `0012_publish_map_geometry_land_clip`, `0013_canonical_cartographic_land_fabric`, and `0014_cartography_land_fabric_created_at_default` are absent from the platform ledger.

`0016_restore_fast_map_geometry` is recorded three times, at platform versions `20260920115331`, `20260920115433`, and `20260920115608`. These retries are historical evidence and must not be deleted casually.

The missing 0012–0014 entries are ledger drift, not evidence that their schema effects are absent. Issue #26 records that those objects were already live when replaying 0012 failed because `publish.neutral_land_mask` existed; later migrations and the public API depend on that state. **Do not replay 0012–0014 against production merely to fill the ledger.**

## Policy

Reconciliation is non-destructive: inventory names; verify schema effects separately; preserve retry history; repair platform metadata only through a reviewed metadata-only mechanism; never change production schema/data merely to make history tidy.

`tools/check_migration_ledger.py` is the read-only future divergence check. It reports missing, duplicate and unknown remote migration names and exits non-zero when any exist.

Actual platform-ledger mutation is not performed by this change. Production writes require an already-reviewed explicit gate, and no safe metadata-only reconciliation gate currently exists. Until one does, the gaps/retries remain explicitly documented rather than concealed or replayed.

## 2026-09-23 production reconciliation through 0028

During the controlled v0.6.1 database-migration validation, production migration `0028_claim_kind_integrity` was applied after a read-only compatibility check found zero claim-kind mismatches in the 42 existing territorial-practice rows. The migration adds structural guards that keep universal `atlas.claim.claim_kind_code` compatible with typed claim/subtype relations and makes claim kind immutable.

Repository issue #128 reconciles that already-live migration back into version control as `db/migrations/0028_claim_kind_integrity.sql`, with a rollback-only regression test and D-060. This is a normal forward reconciliation of a known production migration, not a replay of the unresolved historical 0012–0014 ledger gaps.

After #128 merges, the expected repository/live migration head is `0028`. The earlier 0012–0014 ledger gaps and repeated 0016 entries remain explicitly unresolved under the policy above; adding 0028 does not authorize rewriting them.

