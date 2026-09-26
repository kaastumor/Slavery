# Gate 1 live v0.6.1 reconciliation failure

**Date:** 2026-09-26  
**Parent:** #300  
**Repair:** #304  
**Canonical release:** v0.6.1 unchanged  
**Public channel:** mvp-preview-ancient-v2 unchanged

## Test result

Live:
- `db/tests/001_schema_smoke.sql` — PASS
- `db/tests/002_v061_reconciliation.sql` — **FAIL**

First failure:

> Expected 11 Atlantic evidence IDs + 18 positive/disputed global evidence rows to map
> to claims, found 11.

The reconciliation SQL is byte-identical on current `main` and at repository commit
`057333bccc35636ab007b486266c34e0ab8b8b5b`, the reconciliation commit named in the
existing DB-candidate manifest.

This is therefore a live-state defect, not later test drift.

## Live state at diagnosis

Present:
- 8 voyages;
- 11 actors;
- 12 voyage-owner relations;
- 17 Atlantic source mappings;
- 17 Atlantic evidence mappings over 11 evidence IDs;
- 99 coverage assessments with 57 classified / 18 reviewed / 4 disputed /
  20 researched-inconclusive;
- canonical workbook source/version/asset and original ingest run;
- exact workbook SHA-256
  `0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`.

Missing:
- `raw.raw_record(record_type='v061_workbook_row')`: 0 / 288;
- v0.4.7–v0.5.0 evidence mappings: 0 / 22;
- `research_coverage_source(source_role='evidence_sheet_source')`: 0 / 36;
- global workbook external-participation mappings: 0 / 3;
- global workbook legal-event mappings: 0 / 1.

The live database contains 111 sources/source versions overall, but only two of the
29 exact global-evidence URLs already resolve to an existing source version.

## Protection

Live blocking QC:

`V061_LIVE_RECONCILIATION_INCOMPLETE`

is unresolved against `0.6.1-db-migration-candidate`.

The old candidate manifest's prior “migration validation passed” statement cannot be
used as current proof.

## Repair disposition

Use the bounded #304 repair. Do not replay the full importer.

The repair:
- reuses the preserved workbook lineage and existing Atlantic/core state;
- restores only the missing raw/global phase;
- uses deterministic UUIDs;
- applies in one transaction;
- refuses partial/conflicting state;
- becomes a verified no-op after completion;
- leaves all repaired claims unpublished and all P-levels NULL;
- does not touch public release/channel membership.

The blocking QC issue remains unresolved until the unchanged repository reconciliation
test passes after live repair.
