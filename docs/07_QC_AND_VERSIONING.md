# Quality Control and Versioning

## Mandatory QC rules

Reject or flag a record when any of the following occurs:

- actor nationality/political identity copied from ship flag
- actor nationality/political identity inferred from surname, port, residence, business base or corporate jurisdiction without independent evidence
- imputed carrier stored as documented flag
- voyage/route count used to set territorial P-level
- legal abolition treated as proof practice disappeared
- RI/P0 treated as absence
- modern state identity back-projected into an earlier polity without explicit historical resolution
- a modern boundary proxy is used without being marked as proxy
- multiple owners collapsed into one text field when relationships can be normalized
- ownership shares invented or equal-split without evidence
- finance/insurance relationship treated as ownership without separate evidence
- secondary works counted as independent when they rely on the same primary evidence
- forced labour automatically relabelled as slavery
- a source-native identifier is overwritten by an internal database identifier or vice versa
- an unknown/missing owner or place is materialized as a fictional historical entity
- relationship evidence is detached from the ownership/finance/spatial relation it actually supports
- research-coverage S/P/D/RI is used as territorial P0–P4 intensity
- disputed, researched-inconclusive, or merely reviewed evidence is coerced to P0 instead of leaving the P-level unassigned
- a source version is silently replaced by a different edition/snapshot
- a normalized value overwrites the only surviving raw/source-native value
- a port/place is assigned one timeless polity despite historically changing jurisdiction
- uncertain/broad historical dates are stored as falsely exact without precision metadata
- a draft/unreviewed claim is exposed through the public publish layer unintentionally

## Required provenance checks

Each substantive claim should answer:

- What exactly is being claimed?
- For what spatial entity/place?
- For what dates/range?
- What is the temporal precision?
- Which exact source version supports or challenges it?
- What locator identifies the supporting material?
- Is the source primary, secondary, dataset or methodology?
- Is it independent from other evidence used?
- Is the interpretation disputed?
- What remains unknown?

For imported records also ask:

- What was the original source-native value?
- Which source version/snapshot did it come from?
- Which ingest run/transformation produced the normalized record?

## Versioning

Use semantic-style project versions:

- Patch: corrections, source metadata, typographical fixes, no schema/interpretive change
- Minor: new researched batches, entities or implemented tables under the existing canonical ontology
- Major: ontology/classification/compatibility change that alters how existing canonical records are interpreted

During the pre-1.0 architecture phase, schema drafts may advance independently from the canonical data release. A draft schema does not become canonical simply because its file version increases.

Current data history:

- v0.5.0 — global first-pass coverage baseline complete
- v0.5.1 — Atlantic gate opened cautiously; controlled ingestion experiments
- v0.6.1 — canonical controlled Atlantic ingestion with strict owner semantics and claim-level provenance

Current architecture state:

- `schema_draft.yaml` draft-0.11 — current target contract; M2 semantics/geography have survived disposable relational prototypes but are not yet production-migrated
- canonical data remains v0.6.1 until migration reconciliation/QC succeeds

## Canonical-data rule

Only one data release should be labelled canonical at a time. Older releases remain archived and immutable.

A database may become canonical only after:

- explicit migration from the current canonical release
- value/meaning reconciliation against the source release
- mandatory QC
- documented unresolved differences
- changelog and migration report

Each release should contain or ship with:

- changelog
- schema/data dictionary version
- source-registry/version information
- QC summary
- unresolved-issues list
- release manifest/checksums where practical

Excel is optional as a human-readable export; it is not required for a valid data release.

## Exact canonical-release checksum

The canonical v0.6.1 workbook is identified by both version/filename and SHA-256:

`0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4`

The importer must reject a byte-different workbook presented as v0.6.1. Re-saving or modifying the workbook requires a new release/version rather than overwriting the historical release.
