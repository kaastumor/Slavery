# EXP-02 — Minimum Sufficient Evidence Packet — Result

**Issue:** #205  
**Date:** 2026-09-24  
**Frozen R1 input:** `a6987d3f14369c6ea2d7b2b3db74ac65faa8ec57` / candidate blob `057a61f4758a5ce1dce247c1eb97c7e421c5f979`  
**External participants:** none  
**Canonical historical release:** `v0.6.1` unchanged

## Disposition

**PORTABLE CORE SURVIVES + SIMPLIFY CANDIDATE**

The frozen R1 safety/reconstructibility contract does not require the current application-shaped JSON structure.

A smaller package consisting of:
1. a package manifest;
2. one flat target table;
3. one flat source-relation table;

preserves the fixed EXP-02 invariants for the frozen R1 set.

A compact Markdown packet also preserves the reviewed-claim invariants.

This is an internal structural result only. It does **not** establish user demand, adoption, preference, product-market fit, or independent historical correctness.

## Size evidence

- current committed candidate JSON: **332,010 bytes**
- compact experiment JSON: **116,459 bytes** (**35%** of reference)
- manifest + target CSV + source CSV: **63,391 bytes** (**19%** of reference)
- reviewed Markdown packets: **43,333 bytes**

These are uncompressed byte counts and are not a performance benchmark.

## What proved structurally necessary

### Preserve core

- bounded proposition + required abstention;
- evidence locus + inference extent;
- per-target temporal state + display rule;
- source version + locator + independence group;
- language/access limitations;
- coverage confidence;
- explicit research-state / non-absence semantics.

### Preserve when present

- law/practice note;
- network/territorial note.

These fields carry domain distinctions that cannot be safely reconstructed from generic classification without reinterpretation.

## What can be simplified in the frozen set

### Per-row review state

All 19 reviewed rows are `internally_adversarially_reviewed`.

That state can be hoisted to package-level review scope for this frozen release.

### Per-target geometry state

All 77 targets are `unresolved_no_geometry`.

A package default plus zero overrides preserves the current frozen contract.

This does **not** justify removing per-target geometry state from a future release that contains resolved or mixed geometry.

### Application-specific machinery

`atlas_internal_year` is not required by the portable evidence packet when source anchor and explicit temporal state/display rule are retained.

Detailed unresolved-geometry provenance is not required in the minimum evidence packet because no historical geometry is materialized and geometry has no claim effect.

Source role / claim-fitness / free-text relation notes remain useful enrichment in the full candidate, but the fixed EXP-02 invariants survive without them.

## Why temporal state cannot be derived from anchor

The same frozen anchor can contain different evidence-time states.

At **1800**, reviewed rows include:
- selected-year unknown;
- aggregate / no single territorial state;
- exact cross-section.

At **1300**, reviewed rows include:
- selected-year unknown;
- period-level support.

Therefore the selected anchor itself cannot carry historical precision semantics.

## Why source-family dependency survives

The 45 reviewed source relations collapse to 37 independence groups.

Seven groups contain multiple source relations.

Removing the independence group would reintroduce a known false-independence failure mode.

## Why research state survives

All five research states are actually occupied:
- reviewed bounded-supported;
- reviewed inconclusive;
- planned/unresearched;
- held;
- C0-only.

A single nullable “evidence” field cannot safely replace them without recreating the project’s missing-evidence/absence problem.

## Minimum packet proposal

### Package manifest

Keep:
- candidate/release identity;
- canonical historical release pointer;
- publication state;
- review scope;
- non-absence rule;
- immutable source-input identity;
- research-state definitions;
- temporal-state definitions;
- geometry default/policy.

### Target table

Keep:
- target identity + anchor;
- research state + classification outcome;
- unreviewed interpretation / QA / frame / identity limitation;
- bounded proposition + abstention for reviewed rows;
- evidence locus + inference extent;
- temporal state + display rule;
- optional law/practice and network/territorial notes;
- language/access limitation;
- coverage confidence.

### Source relation table

Keep at minimum:
- target id;
- source version ref;
- human-readable title/URL;
- locator;
- independence group;
- direction;
- decisive flag.

## Adversarial interpretation

This result does **not** prove that the Atlas UI is unnecessary.

It proves something narrower:

> the current internally demonstrated evidence contract is portable and does not inherently require bespoke application structure.

That strengthens the “interoperate / smaller artifact” hypothesis and weakens any claim that application complexity is necessary to preserve the R1 core.

## Explicit non-decisions

EXP-02 does not:
- modify the canonical schema;
- change Core Contract v1;
- alter any historical classification;
- publish R1;
- authorize a CSV-first rewrite;
- remove the Atlas;
- reopen feature development;
- establish external value.

## Next

Stop.

Re-evaluate project form from the new evidence before creating another experiment or delivery queue.
