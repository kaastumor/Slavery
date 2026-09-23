# COV-003 — Tiered Completeness Architecture Protocol

**Issue:** #155  
**Authorized:** 2026-09-23  
**Base main:** `ca96b9880a1e8fe20bc874c00d71f1d5719e171d`  
**Canonical historical release:** v0.6.1 unchanged  
**State:** setup only until adversarial review passes

## Research question

Can a tiered, versioned, source-centric coverage architecture preserve the demonstrated cross-history value while reducing the need to deeply research and continuously maintain every historical target?

This is deliberately not:
- another COV-002 row-by-row scale test;
- a claim of literal historical completeness;
- an Atlas product experiment.

## Architecture under test

### C0 — target / research-state register

Every selected target gets only:
- source-native identity and interval;
- anchor year / sector;
- identity-validation state;
- research state;
- reviewed-through/version;
- explicit statement that unresearched != absence.

C0 contains **no slavery conclusion** unless inherited from a higher tier.

### C1 — compact coverage

Only the preregistered research subset gets:
- coverage outcome;
- strongest bounded proposition;
- required abstention;
- law/practice note when material;
- network/territorial warning when material;
- Cambridge coverage;
- Palgrave coverage;
- unresolved reason;
- source references;
- access/language warning;
- reviewed-through/version.

### C2 — deep packet

Only one target per batch may escalate after C1 under a frozen rule.

C2 adds:
- source role/direction;
- terminology/category qualification;
- temporal scope precision;
- evidence locus / inference extent;
- limiting/contrary evidence;
- richer source metadata.

## Sampling frame

Reuse the exact pinned Cliopatria source used by COV-001/002:
- commit: `ad28a691b7c07c1fca89d0e0636d324667d2a258`
- SHA-256: `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`

Reuse:
- anchors: -500, 500, 1300, 1800;
- sectors A–F;
- COV-001 eligibility rules;
- COV-001 deterministic candidate ranking.

### Batch selection

1. Identify strata with at least 10 eligible candidates.
2. Rank strata by SHA-256:
   `COV-003-BATCH|cell_id`
3. Take the first **3** strata.
4. Within each selected stratum:
   - ranks 1–2 are reserved/previously used by COV-001/002 where applicable;
   - select ranks **3–10** as the new COV-003 target set.

Total new targets: **24**.

This is frozen before slavery/coercion research.

## Tier assignment

Within each 8-target batch:
- all ranks 3–10 -> C0;
- ranks 3–6 -> C1 research;
- ranks 7–10 remain C0-only for this experiment.

Total:
- 24 C0 targets;
- 12 C1 targets;
- at most 3 C2 targets.

No C0-only target may be promoted to C1 after evidence is inspected.

## Identity validation

C0 is allowed to remain `identity_unreviewed`.

To measure target-frame burden without validating all 24:
- deterministically select **2 C0 targets per batch** using SHA-256
  `COV-003-IDENTITY|target-source-row-ordinal`;
- manually validate identity/time against the supplied Wikidata identity or a specialist/reference source;
- record:
  - valid;
  - mismatch;
  - ambiguous;
  - access-limited.

No invalid target is silently replaced.

The validation sample is an estimate of target-frame defect pressure, not a correction sweep.

## Source-centric C1 workflow

Research each batch as a **batch**, not four isolated packets.

### Stage B0 — shared orientation
For the batch:
1. one global synthesis / handbook query relevant to period + broad region;
2. one regional specialist synthesis query where a credible synthesis exists;
3. freeze the shared-source packet.

A shared source may support/contextualize multiple targets.

### Stage B1 — target resolution
For each of the four C1 targets:
- apply the frozen shared packet first;
- run target-specific specialist follow-up only when the shared packet does not safely resolve the bounded proposition/abstention;
- maximum two target-specific specialist follow-ups per target;
- preserve researched-inconclusive.

### Source-reuse accounting
Record:
- unique shared sources;
- unique target-specific sources;
- total cell-source links;
- number of cells informed by each shared source;
- number of C1 targets requiring any target-specific follow-up.

## Row-centric baseline

Use the already-frozen COV-002 12-row expansion as the principal row-centric baseline.

Compute for that cohort:
- unique sources;
- total cell-source links;
- source reuse factor = cell-source-links / unique-sources;
- repeated URLs across cells;
- median sources per row.

This is an artifact baseline, not a claim about human time.

## Batch-economy gate

Batch/source-centric research shows a material structural advantage if:

1. COV-003 C1 source-reuse factor is at least **1.35x** the COV-002 expansion baseline; and
2. at least **2/3 batches** have a shared specialist source that materially informs at least **3/4 C1 cells**; and
3. no more than **9/12 C1 targets** require target-specific follow-up; and
4. no C1 conclusion becomes broader or less cautious merely to increase source reuse.

Failing any one does not automatically fail the whole experiment, but prevents **STRONG SURVIVE**.

## C2 escalation rule

After all C1 rows are frozen, select one target per batch using:

1. first priority: materially_disputed or identity-unsafe;
2. second: researched_inconclusive with at least two credible sources pulling in different directions or periods;
3. third: bounded_supported with a material terminology/law/practice/network ambiguity;
4. tie-breaker: smallest SHA-256 of `COV-003-C2|cell_id`.

C2 research may add up to three new specialist/primary items.

The C2 question is:

> Does the extra detail materially change correctness, uncertainty, source recovery or inference boundaries compared with C1?

C2 earns its extra depth only if it creates a material gain on at least **2 of 3** escalated targets.

Otherwise C1 remains the preferred routine research tier.

## Versioned maintenance model

The experiment uses immutable/as-of snapshots.

Every C0/C1/C2 row records:
- `reviewed_through`;
- `release_id`;
- `review_state`: current / needs_review / superseded.

After the C1/C2 snapshot is frozen:
- deterministically select 3 researched targets using
  `COV-003-UPDATE|cell_id`;
- run one bounded new-source search per selected target;
- if a credible new source appears, do **not** rewrite the frozen snapshot;
- mark the row `needs_review` in an update ledger;
- calculate what a next-release update would touch.

The maintenance question is whether versioning localizes staleness without requiring immediate corpus-wide mutation.

Pass if:
- all material updates can be represented as local row/source review tasks;
- no frozen release becomes internally contradictory;
- no cross-cell query requires hidden silent recomputation.

This gate does **not** claim lower historian research time.

## Coverage / bias audit

Systematic C0 selection is compared with an **easy-evidence proxy**, not actual user demand.

Easy-evidence proxy:
- among the 24 C0 targets, identify those with direct Cambridge or Palgrave coverage after C1/shared-source inspection where known;
- do not research C0-only targets merely to populate this proxy;
- compare which strata/targets would disappear if selection favored direct handbook coverage.

The only permitted conclusion is whether systematic selection retains targets that an evidence-richness proxy would omit.

No claim about actual public demand is allowed.

## Emergent-query audit

After the 24-target C0 + 12-target C1 corpus is frozen, perform one non-independent exploratory query-generation pass.

Candidate query must:
- not duplicate COV-001/002 T1–T6;
- require at least 8 targets and at least 2 batches or existing COV cohorts;
- be answerable from C0/C1 metadata without new historical research;
- reveal a methodological, coverage, geography, or research-priority pattern;
- have a falsifiable answer.

Generate at most 5 candidates.

An emergent query counts only if:
- its answer is not already encoded as a single existing field count;
- it changes a research-priority or methodology conclusion;
- a strongest ordinary 12-row matrix could not answer it without additional reconstruction.

This audit is exploratory and **cannot alone produce STRONG SURVIVE**.

## Tier-value gates

### C0 survives if
- it can register all 24 selected targets without slavery inference;
- unreviewed/invalid targets remain visibly distinct from absence;
- identity-validation defects can be represented without forcing immediate C1 research.

### C1 survives if
- it preserves the four demonstrated cross-cell mechanisms from COV-001/002;
- source recovery remains direct/traceable;
- no safety-critical inference boundary requires routine C2 detail.

### C2 selective escalation survives if
- C2 materially improves at least 2/3 escalated targets.

If not, do not maintain C2 routinely.

## Outcomes

### FAIL / STOP
Use if:
- tiering does not preserve uncertainty/provenance;
- batch research does not improve source reuse;
- C0 creates misleading pseudo-coverage;
- or the architecture mainly creates more bookkeeping.

### TIERED SURVIVE
Use if:
- C0 and C1 survive;
- systematic selection demonstrates a defensible coverage/bias function;
- batch/versioned workflow avoids the specific COV-002 failure mode;
- even if C2 or the strong batch-economy gate fails.

### STRONG SURVIVE
Use only if:
- all TIERED SURVIVE conditions pass;
- the batch-economy gate passes;
- at least one nontrivial emergent query adds methodological/research value;
- no new false-completeness or maintenance failure appears.

No outcome authorizes comprehensive ingestion.
