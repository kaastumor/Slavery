# Gate 2 live reconciliation — frozen v3

**Parent:** #300  
**Execution issue:** #308  
**Disposition:** **V3_DB_RECONCILED**  
**Canonical release:** `v0.6.1` unchanged

## Live result

The frozen internal candidate
`post-r1-cumulative-review-v3-cross-frame` is now represented in the live
PostgreSQL research layer without semantic loss.

Exact live membership:

- 26 research targets/results;
- 21 internally admitted bounded evidence states;
- 5 explicit HOLD states;
- 166 research-target/source relations;
- 164 unique exact source versions;
- 0 historical claim bridges created by Gate 2;
- 0 target spatial links invented;
- 0 independent historical reviews;
- 0 target/result/review field mismatches against the frozen payload;
- 0 source-relation field mismatches;
- 0 extra target or source-relation rows.

A representative rerun of the same deterministic target/result/review/source identities
left the candidate at exactly 26 / 26 / 26 / 166 rows: **idempotence PASS**.

## Semantic controls that survived

- HOLD and researched-inconclusive remain valid non-absence states;
- target-level reviewed sources do not automatically become positive claim evidence;
- no P-level is assigned;
- no historical geometry is promoted;
- target identity/frame/anchor, proposition, abstention, temporal state, evidence locus,
  inference extent, category mapping, language/access limits and unresolved geometry
  round-trip exactly;
- source-version identity, source-native relation IDs, independence/dependency groups,
  claim fitness, decisive flags, access limitations/dates, asset SHA and dependency
  notes round-trip exactly;
- internal review remains distinct from independent review.

## Live regressions

Passed:

- `db/tests/001_schema_smoke.sql`;
- `db/tests/002_v061_reconciliation.sql`;
- `db/tests/004_private_data_api_boundary.sql`;
- release-channel guard using a rollback-only production-safe fixture;
- `db/tests/006_release_membership.sql`;
- `db/tests/009_claim_kind_integrity.sql`;
- `db/tests/010_v3_research_evidence_model.sql`;
- `db/tests/011_v3_source_relation_provenance.sql`;
- Supabase security advisor: **0 lints**.

The repository's stock `005_release_channel.sql` assumes a fresh database and tries
to insert the already-live `public_mvp_preview` key. That production collision is a
test-fixture limitation, not a release-channel defect; the same validation behavior was
verified under a unique rollback-only test channel.

## What Gate 2 does not do

Gate 2 does **not**:

- make PostgreSQL canonical research authority;
- change canonical release `v0.6.1`;
- move the public channel;
- publish v3;
- create historical claim rows merely because a reviewed target exists;
- assign P0–P4;
- resolve practice geometry;
- claim independent historical review.

## Next gate

Advance #300 to **Gate 3 — DB authority proof**.

That gate must prove stable/idempotent research state, preservation-grade release
reconstruction, backup/rollback, draft/published separation, security and repository↔live
agreement before PostgreSQL becomes canonical research authority.
