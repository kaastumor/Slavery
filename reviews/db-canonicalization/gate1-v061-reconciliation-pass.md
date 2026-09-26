# Gate 1 — v0.6.1 live reconciliation PASS

**Parent:** #300  
**Execution slice:** #304  
**Date:** 2026-09-26  
**Disposition:** `V061_DB_RECONCILED`  
**Canonical release effect:** none; v0.6.1 remains canonical  
**Public channel effect:** none

## Before

Gate-1 revalidation of the live `0.6.1-db-migration-candidate` failed the unchanged
repository test `db/tests/002_v061_reconciliation.sql`.

The valid Atlantic/core foundation was already present:
- 8 voyages;
- 11 actors;
- 12 voyage-owner rows;
- 17 source mappings;
- 12 owner-actor mappings;
- 8 voyage mappings;
- 12 voyage-owner mappings;
- 17 Atlantic evidence mappings;
- 99 coverage assessments.

Missing:
- 288 `v061_workbook_row` raw records;
- 36 evidence-sheet coverage/source relations;
- all v0.4.7–v0.5.0 global evidence semantic mappings;
- 3 expected external-participation claims;
- 1 expected legal-event claim.

A blocking live QC issue
`V061_LIVE_RECONCILIATION_INCOMPLETE` correctly prevented authority promotion.

## Reviewed repair

PR #306 merged the dedicated fail-closed repair path:
- `tools/repair_v061_live.py`;
- `tools/v061_global_evidence.py`;
- repair tests and protocol.

The repair:
- requires the exact workbook SHA-256
  `0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`;
- preserves the existing workbook source/version/asset and ingest run;
- refuses partial/conflicting repair state;
- refuses ambiguous exact source URLs;
- uses deterministic migration identities;
- inserts the missing phase atomically;
- keeps repaired claims reviewed + unpublished;
- assigns no P-level;
- creates no practice geometry;
- does not move any release channel.

Foundation CI for the reviewed repair head passed before production apply.

## Production dry-run/preconditions

Immediately before apply:
- live state classified as the intended fully-missing repair state;
- canonical workbook checksum and ingest lineage matched exactly;
- workbook parse reconstructed 288 non-empty rows;
- global evidence reconstructed 36 rows, 29 exact source URLs,
  18 positive/disputed rows and 22 semantic targets;
- exact URL lookup had no ambiguous URL;
- existing core/crosswalk/coverage counts matched repair preconditions.

## Atomic production apply

The guarded transaction committed once.

Receipt:
- raw workbook rows: **288**;
- coverage-source rows: **36**;
- global evidence mappings: **22**;
- territorial-practice mappings: **18**;
- external-participation mappings: **3**;
- legal-event mappings: **1**;
- distinct global source versions: **29**;
- non-null global P-levels: **0**.

Semantic controls preserved:
- RI rows stop at coverage/source provenance;
- Anshan/Elam is external participation only;
- Shang captive-taking and disputed slavery remain separate claims;
- territorial practice and external/network participation remain separate;
- no geometry inference.

## Live regression after apply

PASS:
- unchanged `db/tests/002_v061_reconciliation.sql`;
- `db/tests/001_schema_smoke.sql`;
- `db/tests/009_claim_kind_integrity.sql`.

Unchanged release/public state:
- release-claim membership total: 42;
- release-spatial membership total: 35;
- release-geometry membership total: 73;
- release-source-version membership total: 62;
- `public_mvp_preview` still points to `mvp-preview-ancient-v2`.

Security:
- Supabase security advisor: **0 lints**;
- `anon` / `authenticated` retain no internal-schema table grants.

The blocking QC issue was then resolved with those test results recorded in its
resolution notes.

## Release-contract boundary

The existing D-054 `historical-slavery-atlas-full-state-bundle-v1` contract is
deliberately scoped to a **territorial-practice public preview**. It cannot represent
the now-reconciled full v0.6.1 database state without silently omitting voyages,
actors, research coverage, external participation and legal events.

Therefore Gate 1 does **not** misuse that preview bundle as a canonical v0.6.1 bundle.

A broader preservation-grade canonical release contract is a later Gate 3/4
requirement before DB authority/public canonical release.

## Gate 1 disposition

`V061_DB_RECONCILED`.

This means the live DB now reproduces the canonical v0.6.1 semantics required by the
repository reconciliation contract.

It does **not** mean:
- PostgreSQL is canonical research state yet;
- v3 is ingested;
- a new canonical release exists;
- public preview/channel has changed;
- UI/API cutover is authorized.
