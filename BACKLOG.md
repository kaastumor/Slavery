# Historical Slavery Atlas — Backlog

**Updated:** 2026-09-29
**Role:** canonical execution queue only; methodology, risks and value evidence remain in the existing project documents.
**Canonical research authority:** governed PostgreSQL/PostGIS under D-109.
**Canonical historical release:** `v0.8.1`, unchanged.
**Observed live serving adapter:** `v0.8.1-public-mvp-v1`, unchanged at 2026-09-29 00:16 UTC.
**Observed live schema head:** `0034`.

# CURRENT MODE — EXECUTION / CONSOLIDATION — DEPLOYMENT-READY POPULATION (#360)

**WIP = 1: #360 — prepare the major evidence-backed production population batch.**

The sponsor explicitly accepts the current map candidate as good enough to proceed and defers remaining visual defects to a later Astra review. This supersedes the previous ordering that required further map refinement before batch preparation.

- #366 head `ecbc0e19aa4ac5d254e261d85f708879b8b9a983`: sponsor acceptance **ACCEPTED WITH KNOWN LIMITATIONS**; moved out of draft. Acceptance receipt: https://github.com/kaastumor/Slavery/pull/366#issuecomment-5881152185.
- #365: remaining cartographic defects are **deferred**, not declared fixed. Do not resume snapping, smoothing, context-layer expansion or source-substitution experiments under this batch.
- Technical merge/deployment checks remain distinct from visual acceptance. The generated-head workflows reported `action_required`; no passing check, merge, public cutover or exact screenshot/deployment identity is implied by sponsor acceptance.
- #332 / #363 / D-121: existing source, claim and successor-authority prerequisites remain dependencies of publication, not reasons to postpone read-only batch preparation. Do not clear or close them by this priority change.

## Current population preparation checkpoint

Read `data/research/recovery/production_batch_2026_09_29/preflight.json` and issue #360.

A connected, explicitly read-only Supabase census succeeded on 2026-09-29. The prior Management-API `database_read` failure must not be generalized to this interactive connector. This does not attest scheduled-worker or Actions access, full authority export or write permissions.

The census identified 11 tracked current-method territorial claims outside v0.8.1 membership. All are reviewed/unpublished with NULL practice level. Reuse their existing claim IDs rather than reinserting them. All 11 currently lack non-null, time-overlapping geometry directly attached to their target spatial entity. Separate evidence-locus relations were not tested by that count.

The 23 proposed new historical subjects have no canonical-name/display-name match under the explicitly checked aliases. This is not exhaustive identity resolution and does not establish that their complete packets are production-ready.

## Execution order and deliverables

1. Recover the complete first mixed five-subject packet set: Meroitic Kush/Hamadab, Goryeo, Dahomey, Mexica and Bagan/Pagan. Revalidate source editions, locators, dependencies, category and temporal/spatial scope. A fresh reconstruction must be labelled as new research, not the original lost packet.
2. Reconcile the existing tracked claim packages and the 27 geometry-resolution targets against actual live identities. Do not add overlapping inventories together as new map coverage. Complete defensible geometry or evidence loci where that makes accepted evidence usable; unknown geometry remains unknown.
3. Assemble explicit candidate IDs, exact source/packet fingerprints, geometry roles and expected database deltas. Report new claims, geometry-enriched existing claims, locus-only records, no-ops and held records separately.
4. Run disposable-database dry-run and idempotent replay with dependency closure and exact before/after checks. Build a candidate map with working sources and evidence panels, not merely political background fill.
5. Prepare immutable release/serving artifacts, changelog, QC summary, unresolved-issues register, staged rollout and rollback. Live admission/publication must satisfy the existing historical, provenance and technical gates; never select all reviewed rows.

Remaining new-subject batches retain #360's 5/5/5/4/4 grouping. Batch size is a planning target, not permission to lower per-claim review requirements or pad accepted counts.

## Boundaries

No new post-M1 P-levels, source-density prevalence, inferred nationality, false absence, unsupported modern proxies or evidence-locus-to-territory conversion. Preserve all canonical releases and source-native values. Public services consume reviewed/published materializations, not unrestricted drafts.

No new schema, scheduled worker, credential expansion, paid service, parallel research horizon or generic platform work is authorized by this priority change. Preserve existing saved schedules and recovery mode. No background execution is implied by this queue.

## Actions budget and standing protocols

Batch one coherent checkpoint per PR. Run the smallest relevant local checks and sanitation first. Do not rerun unchanged successful jobs or add heavy geometry sweeps. Public health remains weekly/manual. Use `AGENTS.md`, `docs/PROJECT_INSTRUCTIONS.md`, `docs/24_WAY_OF_WORKING.md`, the existing task/verification contracts and D-096. Discovery follows `docs/discovery/DISCOVERY_EXECUTION.md` and `RUN_PROMPT.md` only when a concrete evidence/representation question justifies it.

# PARKED / trigger-bound

#43 protected staging/production administration and paid backup infrastructure remain trigger-bound. #26 remains historical/closed. Independent expert outreach remains separately authorized; independent historical review is not increased by this checkpoint. Richer UI, PMTiles, search/graph infrastructure and new automation are not the active horizon.

## Preserved predecessor checkpoint

The complete prior queue, Gate-0→5 history, D-119/D-120 dispositions, D-121 HOLD and earlier scheduler reconciliations remain preserved at `git:d0d16ac2b1580bfb4907446a77ee7c11a0a81d25:BACKLOG.md`. This update changes active priority and records a scoped read-only observation; it does not rewrite those historical findings or clear the held v0.8.2 selection.
