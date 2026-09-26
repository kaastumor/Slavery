# Gate 3 adversarial authority review

**Date:** 2026-09-26  
**Parent:** #300  
**Gate:** #313  
**Disposition:** `PROMOTE_DB_CANONICAL_RESEARCH_STATE`

## Decision scope

PostgreSQL/PostGIS may now become the project's authoritative **current research
state**, but authority attaches to the explicitly selected and reviewed Gate-3
membership closure—not to every row present in mutable database schemas and not merely
to a row carrying `review_status='reviewed'`.

The exact Gate-3 authority baseline is `gate3-db-authority-proof-v1`:

- schema head: `0033`;
- canonical predecessor workbook SHA-256:
  `0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`;
- reviewed input: `post-r1-cumulative-review-v3-cross-frame`;
- 40 claims;
- 11 actors;
- 18 spatial entities;
- 0 reviewed historical geometries;
- 8 voyages;
- 99 coverage assessments;
- 211 exact source versions;
- 26 research-target results;
- membership SHA-256:
  `ebc9d32f09857744841a0cf92699c41739b624ac4bd94c43798eb1f61e3b0dd3`;
- frozen production database-state SHA-256:
  `31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff`.

The canonical **historical release** remains `v0.6.1`. The public release channel
remains `mvp-preview-ancient-v2`. Independent historical review remains exactly 0.

## Adversarial findings

### 1. Deterministic identity and idempotence — PASS

Gate 2 retained stable IDs, exact source-version identity and representative idempotent
re-ingestion. Gate 3 freezes stable top-level membership plus deterministic composite
object digests. Drift tests deliberately fail on changed claim and research-result
objects.

### 2. Repository ↔ live schema agreement — PASS

Live schema head is migration 0033. The live checksum ledger records
`0033_release_research_target_result_membership.sql` as:

`3522058c53893f9e82c344d85ce5dd56c33987497b7ff7ac138432cff55a9e78`

which matches the merged repository file. Gate 0's historical reconciliation remains
closed; old missing/duplicate migration-history observations are not an active blocker.

### 3. Full-state preservation breadth — PASS, with explicit authority boundary

The D-106 preservation contract covers claims and typed children, claim-source
relations, actors, spatial entities, voyages and network children, research coverage,
exact source versions, and versioned research-target results with review/source/claim
bridges.

A live audit found 82 claims marked reviewed, while only 40 belong to the Gate-3
authority closure. This is not hidden canonical content:

- the 40-member closure consists of the reconciled canonical-research baseline selected
  for Gate 3;
- 31 reviewed/published claims outside that closure belong to the legacy noncanonical
  preview lineage;
- 11 reviewed/unpublished claims outside that closure are older preview/prototype
  material;
- those 42 rows predate the canonicalization work.

Therefore `review_status` alone must never be interpreted as canonical-research
membership. Explicit governed membership is the authority boundary.

### 4. Exact membership and object digests — PASS

The frozen bundle records exact member IDs, per-object SHA-256 values, sorted membership
digests and the production database-state digest. Repository CI independently validates
the frozen live artifact and drift behavior.

### 5. Reconstruction without mutable draft tables — PASS

PR #318 merged after a fresh-database recovery test:

1. created an empty PostgreSQL/PostGIS database;
2. applied repository migrations from zero;
3. rebuilt the pinned Natural Earth land fabric;
4. refused merge-style restore into occupied canonical tables;
5. restored the frozen Gate-3 composite objects with stable IDs;
6. recomputed all research-object digests;
7. verified the portable cartography fingerprint.

The successful recovery receipt reports:

- `restored: true`;
- verification:
  `EXACT_OBJECT_DIGESTS_AND_PORTABLE_CARTOGRAPHY_MATCH`;
- logical-recovery SHA-256:
  `802f5b00c9e5d3237cfdf3492a33f690c4884c1067e662b699a8a30afb06356f`;
- production database-state SHA-256:
  `31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff`.

### 6. Cartography portability — PASS after correction

The first recovery attempt usefully falsified D-107's assumption that raw EWKB bytes are
portable across PostGIS/GEOS runtimes.

Production runs PostgreSQL 17.6 / PostGIS 3.3.7 / GEOS 3.14.1, while foundation CI uses
the replaceable `postgis/postgis:17-3.5` runtime. Raw EWKB differs across those
runtimes, but the production-captured portable fingerprint matches exactly:

- immutable source commit/blob/content identity;
- SRID;
- geometry type;
- component and point counts;
- rounded geodesic area;
- normalized WKB SHA-256
  `ed1322c8266ca5e73e8f7aa528b284ddc0e6d2671af06e92cd9e46adf3cde159`.

D-108 correctly demotes raw EWKB to a live-runtime drift fingerprint rather than
pretending it is a cross-runtime canonical identity.

### 7. Recovery/rollback on Supabase Free — PASS for preservation-grade logical recovery

The read-only managed-backup inventory probe returned HTTP 403 and the connected
organization is on the Supabase Free plan. The project therefore does **not** claim
verified managed backup/PITR capability.

Gate 3 instead proves provider-independent logical recovery of the reviewed canonical
research closure. This is sufficient for research-state authority because the citable
state is reconstructible without production mutation or provider-specific backup
features.

This does **not** prove physical cluster recovery, PITR, restoration of arbitrary mutable
draft/scratch rows, or an operational RTO/RPO. Those remain operational durability
improvements rather than historical-semantic guarantees.

Rollback semantics are:

1. stop admitting new canonical research membership if integrity is in doubt;
2. preserve the last immutable historical release unchanged;
3. reconstruct the latest frozen reviewed closure into a fresh migrated database;
4. verify object digests and cartography fingerprint before restoring authority;
5. do not move the public release channel as part of research-authority rollback.

### 8. Draft/reviewed/published separation and public boundary — PASS

Live checks on 2026-09-26 found:

- no `anon`/`authenticated` table grants in
  `atlas`, `audit`, `raw`, `staging`, `publish` or `cartography`;
- no `anon`/`authenticated` schema USAGE grants there;
- Supabase security advisor: 0 lints;
- public channel still `mvp-preview-ancient-v2`.

Database authority therefore does not publish unrestricted research state.

### 9. Unresolved QC — nonblocking and preserved

The only unresolved live QC item is the known warning
`V061_SOURCE_REGISTRY_GAP` for the Fredensborg SlaveVoyages voyage URL. The migration
created an explicit exact source/version rather than silently substituting a related
source. The historical Fredensborg 235 vs ~241 issue remains unresolved by design.

Neither condition is evidence corruption or an authority blocker; both remain explicit
unresolved state.

### 10. Release-builder reproducibility — PASS for Gate 3; publication remains Gate 4

The preservation bundle can be built and independently verified from explicit DB
membership, and the fresh-database proof reconstructs that frozen closure.

This proves the machinery needed to build a successor release. It does **not** turn the
Gate-3 proof bundle into a canonical historical release. Gate 4 must separately assemble,
lint, checksum and approve the first DB-backed successor release.

### 11. Hidden file-only truth — no blocking finding

The immutable v0.6.1 workbook remains predecessor release evidence and source-native
lineage rather than being silently replaced. Its migration/reconciliation tooling and
raw records remain auditable in the DB, while the frozen v3 target/result/review/source
state is represented relationally.

External source assets that cannot legally or practically be mirrored remain referenced
through exact source-version identities and locators under the existing source policy.
No reviewed Gate-3 authority member was found to depend on an untracked ad-hoc file as
its sole identity.

## Gate disposition

`PROMOTE_DB_CANONICAL_RESEARCH_STATE`

This promotion means:

- PostgreSQL/PostGIS is authoritative for the explicitly governed current research
  closure;
- explicit membership/review admission defines authority, not physical row presence or
  `review_status` alone;
- immutable release snapshots remain the citable historical release record;
- `v0.6.1` remains the canonical historical release until Gate 4 passes;
- the public preview remains unchanged until Gate 5;
- independent historical review remains 0;
- no new P-level, geometry or historical inference is introduced by this authority flip.

## Next gate

Proceed to Gate 4: build and adversarially validate the first DB-backed canonical
release, provisionally `v0.7.0` unless Gate-4 work discovers a compatibility-breaking
ontology change.
