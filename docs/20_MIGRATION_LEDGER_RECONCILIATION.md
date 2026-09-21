# Migration ledger reconciliation

## 2026-09-21 live inventory

Issue #26 tracks a historical divergence between repository migration files and the Supabase platform migration ledger. This document records the observed state without rewriting production history.

The repository contains migrations `0001` through `0027`. A read-only `list_migrations` query against the live Historical Slavery Atlas project on 2026-09-21 showed:

- `0001`–`0011`: present once;
- `0012_publish_map_geometry_land_clip`: absent from the platform ledger;
- `0013_canonical_cartographic_land_fabric`: absent from the platform ledger;
- `0014_cartography_land_fabric_created_at_default`: absent from the platform ledger;
- `0015`: present once;
- `0016_restore_fast_map_geometry`: present **three times**, at platform versions `20260920115331`, `20260920115433`, and `20260920115608`;
- `0017`–`0027`: present once.

The absence of 0012–0014 is ledger drift, not evidence that their schema effects are absent. Issue #26 records that their objects were already live when a direct replay of 0012 failed because `publish.neutral_land_mask` already existed. Later migrations and the public API depend on this state. Therefore **do not replay 0012–0014 against production merely to fill the ledger**.

The three 0016 entries are preserved as historical retry evidence. They must not be deleted or rewritten casually.

## Reconciliation policy

Reconciliation is non-destructive:

1. inventory repository and remote names;
2. verify the expected schema effects separately;
3. record historical gaps/retries explicitly;
4. only repair platform migration metadata through a reviewed mechanism that changes metadata without replaying migration SQL;
5. never make production schema/data changes solely to make a ledger look tidy.

`tools/check_migration_ledger.py` provides the read-only comparison used for future drift detection. It intentionally returns non-zero for missing, duplicate, or unknown remote migration names so CI/deployment tooling can surface divergence before applying new migrations.

## Current disposition

The live inventory is complete and the irregularities are documented. Actual platform-ledger mutation is **not performed here**: production writes require an already-reviewed explicit gate, and the repository currently has no safe metadata-only reconciliation path. Until such a path is reviewed, 0012–0014 remain documented historical gaps and the repeated 0016 entries remain documented retries.
