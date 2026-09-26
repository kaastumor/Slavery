# Migration ledger reconciliation

## 2026-09-21 live inventory

Issue #26 tracks divergence between repository migration files and the Supabase platform ledger. Repository migrations run `0001` through `0027`. A read-only live `list_migrations` inventory found `0001`–`0011`, then `0015`–`0027`; `0012_publish_map_geometry_land_clip`, `0013_canonical_cartographic_land_fabric`, and `0014_cartography_land_fabric_created_at_default` are absent from the platform ledger.

`0016_restore_fast_map_geometry` is recorded three times, at platform versions `20260920115331`, `20260920115433`, and `20260920115608`. These retries are historical evidence and must not be deleted casually.

The missing 0012–0014 entries are ledger drift, not evidence that their schema effects are absent. Issue #26 records that those objects were already live when replaying 0012 failed because `publish.neutral_land_mask` existed; later migrations and the public API depend on that state. **Do not replay 0012–0014 against production merely to fill the ledger.**

## Policy

Reconciliation is non-destructive: inventory names; verify schema effects separately; preserve retry history; repair platform metadata only through a reviewed metadata-only mechanism; never change production schema/data merely to make history tidy.

`tools/check_migration_ledger.py` is the read-only future divergence check. It reports missing, duplicate and unknown remote migration names and exits non-zero when any exist.

Actual platform-ledger mutation is not performed by this change. Production writes require an already-reviewed explicit gate, and no safe metadata-only reconciliation gate currently exists. Until one does, the gaps/retries remain explicitly documented rather than concealed or replayed.

## 2026-09-23 production reconciliation through 0029

During the controlled v0.6.1 database-migration validation, production migration `0028_claim_kind_integrity` was applied after a read-only compatibility check found zero claim-kind mismatches in the 42 existing territorial-practice rows. The migration adds structural guards that keep universal `atlas.claim.claim_kind_code` compatible with typed claim/subtype relations and makes claim kind immutable.

Repository issue #128 reconciles that already-live migration back into version control as `db/migrations/0028_claim_kind_integrity.sql`, with a rollback-only regression test and D-060. Fresh-schema CI then caught that PostgreSQL's default function privileges would make the two new guard functions executable by PUBLIC if schema USAGE were ever granted. Production therefore received append-only migration `0029_claim_kind_function_privileges`, which revokes PUBLIC EXECUTE on those functions and restores the D-051 defense-in-depth invariant. The Supabase platform ledger recorded that idempotent 0029 twice, at versions `20260923134302` and `20260923134428`; preserve both retry records as history rather than deleting them casually, just as with the older repeated 0016 entries. This is a normal forward reconciliation of known production migrations, not a replay of the unresolved historical 0012–0014 ledger gaps.

After #128 merges, the expected repository/live migration head is `0029`. The earlier 0012–0014 ledger gaps and repeated 0016 entries remain explicitly unresolved under the policy above; adding 0028–0029 does not authorize rewriting them.

## 2026-09-26 DB-canonicalization Gate 0 policy

Issue #300 now makes migration reconciliation a prerequisite to the database becoming
canonical research state.

A second migration-history problem was found during the live audit:

- Supabase platform history contains the known 0012–0014 gaps and 0016/0029 retries;
- the live database has **no** `atlas_meta.schema_migration` checksum ledger, even
  though repository `tools/migrate.py` expects it.

This means `tools/migrate.py up` must **not** be run against production until the live
schema has been verified and a checksum baseline has been recorded. Otherwise an empty
ledger would make already-live migrations appear pending.

### Authority after reconciliation

Keep the two histories for different purposes:

1. **Supabase platform history** remains legacy operational/audit evidence. Known gaps
   and retries are preserved, not cosmetically deleted.
2. **Repository checksum ledger** becomes the deterministic authority for future Atlas
   migrations after one guarded verified-baseline bootstrap.

The platform ledger is therefore checked against an explicit exception policy:
- 0012–0014 may remain absent only while their live schema effects are separately
  verified;
- 0016 must remain exactly the documented three retry entries unless explicitly
  reconciled;
- 0029 must remain exactly the documented two retry entries unless explicitly
  reconciled;
- any new missing, duplicate or unknown migration fails the check.

### Bootstrap semantics

`tools/bootstrap_migration_ledger.py` is the only approved path for the initial
checksum-ledger baseline.

It is dry-run by default and requires, before apply:
- exact repository migration set 0001–0029;
- exact accepted platform-history exception shape;
- live 0012–0014 sentinel objects;
- live `0.6.1-db-migration-candidate` at schema head 0029;
- recorded prior migration validation;
- exact v0.6.1 workbook checksum lineage;
- no conflicting existing checksum ledger.

An apply requires explicit `--confirm-head 0029`.

Rows recorded by this bootstrap use
`recording_method='verified_production_baseline'`. Their `applied_at` timestamp is
the **baseline recording time**, not a claim about when the historical migration
originally executed.

After bootstrap, normal migrations use the checksum runner and must reject changed
already-applied migration files.

The frozen before-state is recorded in
`reviews/db-canonicalization/gate0-migration-matrix.json`.

No production schema/data or release membership is changed by documenting this policy.
