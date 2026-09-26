# PostgreSQL Canonicalization and First DB-Backed Release

**Parent gate:** #300  
**Current canonical release:** v0.6.1  
**Reviewed migration input:** post-r1-cumulative-review-v3-cross-frame  
**Public preview:** mvp-preview-ancient-v2 (unchanged until final cutover)  
**Status:** active cutover plan; no authority flip yet

## 1. Objective

Move the Historical Slavery Atlas from a workbook/file-first canonical research state
to a PostgreSQL/PostGIS canonical research state **without losing the immutable-release
boundary**.

The intended long-term chain is:

```text
source/native evidence
        ↓
raw + staging
        ↓
canonical PostgreSQL/PostGIS research state
        ↓
review/release gate
        ↓
immutable checksummed release package
        ↓
publish materialization / API / Atlas / GIS
```

The research DB is mutable and auditable. Releases are immutable historical snapshots.

## 2. Why not release v3 first?

v3 is a reviewed evidence candidate, not a complete successor to v0.6.1.

Publishing it as canonical first would introduce an avoidable sequence:

```text
v0.6.1 workbook → v0.7.0 file package → later DB migration → second reconciliation
```

The selected sequence is:

```text
v0.6.1 + frozen reviewed v3
        ↓
reconciled PostgreSQL/PostGIS
        ↓
first DB-backed immutable canonical release
        ↓
UI/API cutover
```

This creates one semantic migration boundary instead of two.

## 3. Frozen inputs

### v0.6.1

Exact workbook identity:

`0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`

It remains canonical throughout Gates 0–2.

### v3

`post-r1-cumulative-review-v3-cross-frame`

Frozen for this cutover:
- 26 members;
- 21 accepted bounded evidence states;
- 5 HOLD rows;
- 166 source relations;
- 2 exact cross-target source-version overlaps;
- 0 independent historical reviews.

EXP-15's three newly qualified node sites are outside this historical-content freeze.

## 4. Gate 0 — migration-history reconciliation

### Before-state

Repository migration files: 0001–0029.

**Critical additional finding:** the live database currently has no `atlas_meta.schema_migration` checksum ledger. The repository migration runner (`tools/migrate.py`) would create that ledger and otherwise consider every repository migration unrecorded. It must therefore **not** be run against production until a verified baseline has been established.

Live Supabase history:
- 0001–0011 present;
- 0012–0014 absent;
- 0015 onward present;
- 0016 name appears under three remote history versions;
- 0029 name appears under two remote history versions.

Verified live 0012–0014 effects:
- `publish.neutral_land_mask` exists;
- `cartography.land_fabric` exists;
- `cartography.land_fabric.created_at` has a default.

### Rule

Do **not** run 0012–0014 again.

The task is to prove live definitions match repository intent, then establish two non-destructive history layers where future tooling requires them:

1. reconcile the Supabase platform migration-history metadata; and
2. create/seed the repository checksum ledger only from migrations whose live effects have been verified against the exact repository SQL/checksum.

Do not let the checksum runner bootstrap an empty ledger and then replay production.

Duplicate history rows must be explained. They are not deleted merely to make a list
look tidy.

### Gate output

- repository↔live migration matrix;
- repository file checksum inventory;
- before/after Supabase migration history;
- before/after `atlas_meta.schema_migration` checksum ledger;
- verification queries;
- regression/QC result;
- explicit retained exceptions.

Pass marker: `MIGRATION_HISTORY_RECONCILED`.

## 5. Gate 1 — v0.6.1 reproduction

The database already contains a draft `0.6.1-db-migration-candidate`.

Gate 1 must re-prove it against the canonical artifact rather than trusting the old
label.

Required:
- exact workbook checksum;
- raw-record retention;
- source/owner/voyage/evidence crosswalk reconciliation;
- actor unknown semantics;
- claim/source lineage;
- QC issue preservation;
- exact release membership;
- deterministic immutable bundle reconstruction.

Pass marker: `V061_DB_RECONCILED`.

## 6. Gate 2 — v3 relational mapping

Use the existing schema first.

For every admitted v3 row, preserve:
- target identity/frame/anchor;
- proposition and required abstention;
- temporal applicability/precision;
- evidence locus and inference extent;
- law/practice and network/territorial distinctions;
- category mapping status;
- review state;
- source/version;
- claim fitness;
- dependency/independence group;
- language/access limitations;
- unresolved geometry.

HOLD and researched-inconclusive are explicit epistemic/review states, not P0 and not
absence.

Any field that cannot be represented without loss becomes a **schema decision gate**.
It is not silently packed into generic notes merely to complete ingestion.

Pass marker: `V3_DB_RECONCILED`.

## 7. Gate 3 — DB authority

Promote PostgreSQL/PostGIS to canonical research state only after:

- Gates 0–2 pass;
- stable IDs and idempotent retry are demonstrated;
- release membership is deterministic;
- release builder reconstructs byte/checksum-stable package identity;
- draft/reviewed/published separation is tested;
- backup/rollback is demonstrated;
- internal schema access boundary is verified;
- repository tests and live state agree;
- no open blocking QC issue remains.

DB authority does not automatically publish a release.

## 8. Gate 4 — first DB-backed canonical release

Default version hypothesis: **v0.7.0**.

Use a different semantic version only if Gate 2 discovers a compatibility-breaking
ontology change.

The release must include:
- predecessor identity;
- schema + methodology versions;
- exact release membership and digests;
- source/version membership;
- immutable exports/bundle;
- changelog;
- QC summary;
- unresolved issues;
- review/publication states;
- migration/reconciliation report;
- artifact checksums.

Older releases remain immutable.

## 9. Gate 5 — UI/API

The Atlas/UI is a consumer, not the owner of truth.

Cutover only after the exact release intended for production passes staging.

Verify:
- neutral world land remains present;
- HOLD/inconclusive/unresolved never read as absence;
- historical time labels remain correct;
- source/version/dependency inspection remains available;
- geometry states remain honest;
- public requests do not expose unrestricted draft schemas;
- rollback to the previous public channel works.

No UI redesign is part of the cutover.

## 10. Security note

Supabase currently reports RLS-disabled internal tables as an advisor finding.

The live audit also established:
- no `anon` or `authenticated` USAGE on internal schemas;
- no table grants to those roles in the internal schemas.

That means the current private-schema boundary is materially protective.

The RLS finding is still recorded and must be rechecked at Gate 3/Gate 5. Do not enable
RLS without policies/access-path analysis because that could break intended server-side
reads while adding no meaningful protection if the schemas remain unexposed.

## 11. Independent historical review

Independent review remains a future quality layer, not a DB-canonicalization blocker.

Canonical DB means “authoritative current state of this project's reviewed knowledge,”
not “externally verified historical truth.”

The review level remains queryable and visible in every release.
