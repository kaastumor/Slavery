# Gate 3 recovery proof — free-tier logical reconstruction

**Parent gate:** #313 / #300  
**Date:** 2026-09-26  
**Production restore performed:** no

## Managed-backup probe result

PR #317 added a read-only Supabase backup-inventory workflow.

Run \`36266187423\` proved:
- the configured management token exists;
- the backup inventory request returns HTTP **403**.

The connected Supabase organization is currently on the **Free** plan. The project
therefore does not claim managed backup/PITR recovery evidence that it cannot verify.

The backup-inventory workflow is retained as a **manual diagnostic only**. It is no
longer an automatic push dependency.

## Recovery contract used for Gate 3

Gate 3 proves recoverability of the project's **reviewed canonical-research closure**
without a destructive production restore or a paid temporary Supabase branch.

Recovery inputs:

1. repository migrations through the exact schema head;
2. the committed Gate-3 full-state preservation bundle;
3. the pinned Natural Earth 10m cartography source used by D-107.

Recovery procedure:

1. create an empty PostgreSQL/PostGIS database;
2. apply repository migrations from zero;
3. reconstruct the land fabric from immutable source commit/blob/content hashes;
4. refuse restore unless canonical/reviewed object tables are empty;
5. restore frozen composite objects with stable IDs and original metadata;
6. recompute every top-level composite object digest;
7. require exact frozen object digests for the reviewed relational state;
8. verify cartography using exact immutable source identity, SRID, validity and
   non-emptiness; record the rebuilt runtime EWKB fingerprint separately.

Raw EWKB remains recorded as the production implementation fingerprint from the frozen
live proof. It is deliberately not used as a cross-engine recovery invariant because
the first fresh-database run demonstrated that different PostGIS/GEOS runtimes can
serialize the same pinned-source land fabric to different EWKB bytes.

The restore tool does **not** claim to be a physical Supabase backup and does not
preserve arbitrary mutable scratch/draft rows outside the frozen reviewed closure.

This scope matches D-101's authority definition: PostgreSQL becomes authoritative for
the project's **reviewed knowledge state**. Draft research remains governed separately;
public services remain release/materialization consumers.

## Source-native/raw lineage

The v0.6.1 source-native ingestion layer remains governed by the immutable predecessor
release identity plus the Gate-1 reconciliation/ingestion tooling. The Gate-3 bundle is
not a replacement for the predecessor artifact.

Future managed-backup capability would improve operational disaster recovery, but it is
not represented as existing today.

## Success criterion

\`GATE3_LOGICAL_RECOVERY_PASS\` requires a fresh-database CI restore whose:
- reviewed research-object digests exactly match the frozen live bundle;
- cartography source commit/blob/content identity and SRID match exactly;
- rebuilt cartography is valid and non-empty, while its runtime EWKB fingerprint is
  reported separately from the frozen production EWKB fingerprint;
- the logical database-state SHA-256, using the frozen cartography identity after the
  source-equivalence check, equals
  \`31b7a7b675445e5758ffd68d64ff0f0cde83df1b0ea65f29835246deb2ae26ff\`.

No production state, canonical release, public channel or UI is changed by this proof.
