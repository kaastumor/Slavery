# Gate 1 v0.6.1 live repair protocol

**Issue:** #304  
**Parent:** #300  
**Mode:** review/release — migration repair  
**Canonical release:** v0.6.1 unchanged  
**Public channel:** unchanged

## Trigger

Live execution of the unchanged canonical repository test
`db/tests/002_v061_reconciliation.sql` failed on 2026-09-26.

The Atlantic/core migration is present, but the workbook-wide raw-preservation and
global-evidence semantic phase is absent.

## Repair boundary

This repair is allowed to add only the missing v0.6.1 migration phase:

- 288 `v061_workbook_row` raw records;
- exact global source/version provenance;
- 36 evidence-sheet coverage-source links;
- 18 reviewed global spatial research targets;
- 22 explicit semantic claim targets;
- claim-specific source links;
- v0.6.1 evidence-to-claim mappings.

It must not:
- recreate Atlantic actors/voyages/owners;
- alter existing historical/public claims;
- assign P0–P4;
- create practice geometry;
- update the public release channel;
- make the DB canonical;
- ingest v3.

## Atomicity / idempotence

The repair tool:
- validates the exact workbook checksum and dry-run counts;
- validates preserved Atlantic/core counts and workbook ingest lineage;
- classifies live repair state as `READY_TO_REPAIR`, `COMPLETE`, or
  `PARTIAL_OR_CONFLICTING`;
- applies all missing rows in one transaction;
- uses deterministic UUIDv5 IDs for every newly created source, source version,
  raw workbook row, spatial target, claim and claim-source relation;
- reuses an already-existing exact source version only when the URL resolves to
  exactly one version;
- refuses ambiguous exact URLs;
- refuses partial/conflicting live repair state;
- is a verified no-op once complete.

The old full importer remains unchanged and must not be replayed against production.

## Historical semantics

The explicit mapping in `tools/v061_global_evidence.py` remains authoritative.

Controls:
- all RI rows stop at research-coverage provenance;
- territorial P-level remains NULL;
- Anshan/Elam is external participation only;
- Shang captive-taking and disputed slavery remain separate claims;
- network/external and territorial claims remain separate;
- exact URL/version provenance is retained;
- all repaired claims remain reviewed + unpublished.

## Done gate

After reviewed repair code passes:
1. run tool dry-run against production;
2. apply once under transaction;
3. run unchanged `db/tests/002_v061_reconciliation.sql`;
4. rerun schema/security/release-channel invariants;
5. only if all pass, resolve live blocker
   `V061_LIVE_RECONCILIATION_INCOMPLETE`;
6. record `V061_DB_RECONCILED` under #300.

No canonical/public cutover follows automatically.
