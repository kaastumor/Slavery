# Gate 0 / Gate 1 live reconciliation findings

**Parent:** #300  
**Canonical release:** v0.6.1 unchanged  
**DB canonicality:** not granted  
**Public preview:** unchanged

## Red-team result

The DB-first sequence remains justified, but live validation found two independent
blockers that must both be repaired before PostgreSQL can become canonical.

## Blocker A — migration history

Supabase platform history:
- 0012–0014 absent even though their persistent schema effects are verified live;
- 0016 recorded three times;
- 0029 recorded twice.

Repository checksum history:
- `atlas_meta.schema_migration` is absent in production.

Therefore:
- do not replay 0012–0014;
- do not run `tools/migrate.py up` against production yet;
- preserve retry history;
- bootstrap any repository checksum ledger only from the reviewed exact file hashes in
  `gate0-migration-matrix.json` after the live-state baseline is accepted.

## Blocker B — v0.6.1 live semantic migration is incomplete

The current repository test `db/tests/002_v061_reconciliation.sql` was executed
against production and failed.

The file is byte-identical to the copy at the reconciliation commit recorded by the
existing DB-candidate manifest, so this is not a later-test drift explanation.

Current production:
- Atlantic voyage/owner/source core present;
- 99 coverage assessments present with expected 57 classified / 18 reviewed /
  4 disputed / 20 researched-inconclusive distribution;
- 17 Atlantic evidence mappings over 11 legacy evidence IDs;
- 159 normalized Atlantic raw rows present;
- **0** `v061_workbook_row` rows;
- **0** global v0.4.7–v0.5.0 evidence mappings;
- **0** evidence-sheet `research_coverage_source` links;
- **0** workbook external-participation claims;
- **0** workbook legal-event claims.

Canonical importer expectations:
- 288 non-empty workbook rows raw-preserved;
- 36 global evidence rows;
- 29 exact source URLs;
- 18 S/P/D rows mapping to 22 explicit semantic claim targets;
- 18 RI rows contributing coverage-source provenance only;
- no automatic P-level.

The canonical workbook source/version/asset and original ingest-run identity remain
present with exact SHA-256
`0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`.

This permits a bounded incremental repair. A full importer replay is forbidden because
Atlantic crosswalks already contain data.

## Protection

A blocking live QC issue now exists:

`V061_LIVE_RECONCILIATION_INCOMPLETE`

on `0.6.1-db-migration-candidate`.

The old candidate manifest must not be used as proof of current reconciliation.

## Repair contract

The repair must:
1. reuse the existing workbook source/version/asset and ingest run;
2. preserve all 288 non-empty workbook rows as `v061_workbook_row`;
3. reuse the 99 existing coverage assessments;
4. restore exact source/version provenance for all 36 global evidence rows;
5. restore 36 coverage-source links;
6. restore the explicit 22 global semantic claim targets exactly as
   `tools/v061_global_evidence.py` specifies;
7. retain RI as non-positive coverage provenance;
8. retain NULL P-level for migrated territorial claims;
9. preserve Anshan/Elam as external participation only;
10. preserve Shang captive-taking and disputed slavery as separate claims;
11. be idempotent and refuse ambiguous partial state;
12. rerun the unchanged repository reconciliation test after repair.

Only after the canonical test passes may the blocking QC issue be resolved.

## Security

Supabase's generic advisor reports RLS-disabled internal tables.

Read-only live checks show `anon` and `authenticated` currently have no schema USAGE
and no direct table grants on atlas/audit/raw/staging/publish/cartography.

No blind RLS change was made. Recheck at the later DB/public cutover gate.
