# R1.6 — Release-Level QC Result

**Issue:** #172  
**Base research commit:** `4dd230dc6d4a5cd0a2edd0ab148b7a04ea1cb7ca`  
**QC date:** 2026-09-24  
**Disposition:** **PASS WITH EXPLICIT UNRESOLVED LIMITATIONS → R1.7 candidate-release/MVP materialization**

## Scope

R1.6 audits the completed R1 evidence package as a release candidate.

It does **not**:
- reopen subject research;
- alter Core Contract v1;
- publish or canonicalize a release;
- resolve historical geometry by assumption;
- claim independent peer review.

## Frozen package audited

Historical subject research is frozen at:

- 19 reviewed C1 rows;
- 5 classified / bounded-supported;
- 14 researched-inconclusive;
- 4 completed C2 packets;
- 19/19 internally adversarially replayed;
- 0 target substitutions.

The candidate target/research-state registry contains 77 frozen targets:

- 19 reviewed C1;
- 15 planned-C1 targets ready but intentionally unresearched;
- 2 held identity/time targets;
- 41 C0-only registered targets.

Every non-reviewed target remains explicitly **unassessed** and carries a non-absence guard.

## QC gates

### 1. Membership / substitution

**PASS**

- exactly 19 unique reviewed C1 target IDs;
- no duplicate reviewed target IDs;
- all 19 are present in the frozen identity/queue frame;
- no post-evidence target substitution.

### 2. Core Contract v1

**PASS**

All 19 final rows satisfy the deterministic Core Contract validator:
- required bounded proposition;
- required abstention;
- temporal applicability/precision;
- evidence locus;
- inference extent;
- language/access limitation;
- coverage confidence;
- review state;
- recoverable source relation(s).

### 3. Review provenance

**PASS**

- 19/19 rows: `internally_adversarially_reviewed`;
- 4/4 earned C2 packets: completed;
- no row remains with `c2_required = true`.

This is still **internal adversarial review**, not independent review.

### 4. Positive candidate rows

**PASS WITH TEMPORAL DISPLAY GUARDS**

The five positive rows are:

- Middle Kingdom of Egypt — period-level support around 2000 BCE;
- Gao — near-anchor/approximate support around 1500 CE;
- Carthage — period-level support around 500 BCE;
- United States — exact 1800 census cross-section;
- Chimú — period-level state labor-service/corvée support containing 1300.

No positive row relies only on `context_only` or `review_required` decisive evidence.

Chimú contains one decisive `usable_with_limitation` source relation, and the row received full adversarial replay as required.

R1.6 adds a separate temporal rendering artifact so the MVP cannot silently turn period-level or near-anchor support into an exact-year event.

### 5. §19 release-wide error-class scan

**PASS**

The final 19-row package preserves the corrected failure classes that triggered full replay:

- selected-year leakage — blocked by explicit temporal applicability/render states;
- target/context leakage — bounded by target-specific locus/extent and abstentions;
- network/territorial leakage — explicitly separated where material;
- event/status inflation — corrected in cases such as Teotihuacan/Cahokia and preserved in final rows;
- false source independence — dependency groups normalized for derivative/common-source evidence.

No repeated uncorrected instance was found in the final package.

### 6. Source/version reconstruction

**PASS**

Materialized release-level dependency table:

- 45 source relations;
- 45 unique source-version references;
- 37 independence groups.

Every source relation contains:
- source/version reference;
- recoverable URL;
- locator;
- claim-fitness state;
- direction/role where material;
- dependency target(s);
- independence group.

Publication count is not treated as evidence independence.

### 7. Coverage / language / access

**PASS WITH EXPLICIT LIMITATIONS**

Coverage confidence across the 19 rows is heterogeneous.

The release must preserve row-level limitations, especially where:
- non-English source traditions are mediated through specialist translation;
- target-specific local-language literature was not exhaustive;
- archaeological evidence cannot directly identify legal status;
- aggregate or network frames prevent one territorial state.

This is compatible with a candidate research release because:
- inconclusive remains visible;
- unresearched remains visible;
- no absence claim is inferred from access limitations.

### 8. Frozen balance

**PASS**

Researched polity-sector counts:

- A: 2
- B: 1
- C: 3
- D: 2
- E: 1
- F: 3

12 researched polity rows; maximum sector share = **25%**.

All six release sectors are represented.

### 9. C0 / unresearched / held state

**PASS**

The candidate target registry preserves all 77 frozen targets, including:
- 15 planned-C1 targets not researched;
- 2 held targets;
- 41 C0-only targets.

These rows are explicitly unassessed and must render as research/coverage state, never historical absence.

### 10. Geometry

**PASS AS A RELEASE BOUNDARY; NOT YET MATERIALIZED**

R1.6 does not silently assign map geometry.

Every target has:
- an expected geometry form;
- an explicit `not_materialized_in_r1_6_qc` release state;
- a rule that geometry availability/proxy status cannot create or strengthen historical truth.

R1.7/MVP must resolve each visible target to one of:
- accepted historical geometry;
- point/route/fuzzy representation appropriate to frame;
- approximate/proxy with explicit label;
- unresolved/no geometry with neutral world land retained.

This is the principal remaining release-engineering task.

### 11. Reconstructibility

**PASS**

`r1_release_qc_manifest.json` pins the immutable input files by Git blob SHA.

The deterministic R1.6 validator verifies:
- manifest input identity;
- reviewed row membership;
- target registry state;
- dependency reconstruction;
- C2 closure;
- temporal rendering membership;
- balance invariants.

## Unresolved limitations carried into R1.7

1. **Concrete geometry materialization is not complete.**
2. **No independent historical review has occurred.**
3. **Language/access coverage varies materially by row.**
4. **Three positive rows are period-level/near-anchor rather than exact-year observations.**
5. **The public/simple Atlas surface has not yet been materialized from the immutable candidate package.**
6. **v0.6.1 remains the canonical historical release; R1 is still candidate-only.**

None of these justifies reopening historical subject research.

## R1.6 decision

**PASS WITH EXPLICIT UNRESOLVED LIMITATIONS.**

Proceed to **R1.7 as the project MVP**:

> immutable R1 candidate package + neutral world map + explicit geometry/research states + compact evidence register.

The MVP should be deliberately boring:
- static/read-only by default;
- no new backend or production database migration;
- no custom graph/search infrastructure;
- no bespoke interaction unless later discovery evidence earns it.

R1.7 must end with a technical candidate, changelog, QC summary, unresolved-issues list and a simple Atlas surface suitable for the explicit R1.8 publish/hold/rework decision.
