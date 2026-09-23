# M1 integrated adversarial gate

**Gate:** #100  
**Atomic task:** #105  
**Date:** 2026-09-23  
**Status:** revise — one corrective task (#112) is required before the M1 Project Health Check

## Question

Does the integrated M1 result actually reduce false equivalence and false precision without adding unjustified complexity?

## Executive result

**Not yet.** The M1 work materially improved the design and several important pieces survive, but the integrated attack found that three semantic overloads were displaced rather than eliminated, and that the current public map still operationalizes the legacy P-level/time-range semantics that M1 is trying to harden.

This is a useful gate failure, not a project failure.

The smallest corrective action is #112. It must repair the experimental semantic axes and define a safe compatibility boundary around legacy P0–P4/current preview behavior. Canonical release v0.6.1 and the current public preview remain unchanged while that correction is tested.

## Attack 1 — Field and constraint semantics

### Finding 1.1 — `historical_characterization` is still overloaded
**Disposition: revise**

The #102 prototype replaces one overloaded P-level with a single-choice `historical_characterization` vocabulary containing:

- `bounded_occurrence`
- `recurrent`
- `institutional`
- `widespread_structurally_major`

These are not mutually exclusive values on one clean axis.

A historical practice can be recurrent **and** institutional. It can be institutional but geographically narrow. It can be widespread without the evidence justifying a claim about formal institutionalization. A single enum therefore recreates the ordering/comparability problem below P0–P4.

The Hittite real case makes this concrete: the source package contains repeated attestations, legal status/property rules and recurring functions. Forcing one headline characterization discards simultaneous truths.

**Correction required:** independent dimensions for at least occurrence pattern, institutionalization, and structural/spatial significance. They need not be elaborate taxonomies yet.

### Finding 1.2 — `evidence_basis` mixes two concepts
**Disposition: revise**

The #102 evidence vocabulary combines `isolated_attestation` / `recurrent_attestation` with `specialist_synthesis` / `mixed`.

The first pair describes the pattern of attestations. The latter describes the interpretive/source basis. A specialist synthesis can itself rest on one attestation, recurrent independent attestations, or a mixed evidentiary package.

**Correction required:** separate attestation configuration from interpretive basis. Do not multiply tables unless fixtures require them.

### Finding 1.3 — research stage vs classification outcome
**Disposition: survives**

The split between `research_stage` and `classification_outcome` survives the integrated attack.

`review_complete + disputed` and `review_complete + inconclusive` are simultaneous truths that the pre-M1 `coverage_state` could not express cleanly.

The legacy P0 compatibility example must not become an inference rule: an inconclusive outcome does not mechanically create P0.

## Attack 2 — Temporal and spatial inference

### Finding 2.1 — applicability vs uncertainty is improved, but `approximate_period` re-mixes them
**Disposition: revise**

The #103 design correctly separates an outer `query_window` from positive selected-year applicability and correctly prevents Silla's alternative dates from becoming continuous 695–819 CE presence.

However, `approximate_period` currently appears in the same `time_mode` field as truth predicates such as `continuous_interval`, `bounded_occurrence`, and `alternative_dates`.

“Approximate” describes temporal precision/certainty; it does not say whether a condition continuously held throughout the period.

This can recreate the original error if an approximate interval is treated as positive validity merely because it has bounds.

**Correction required:** applicability mode and temporal precision/certainty remain separate. Continuity must be positively asserted independently from approximation.

### Finding 2.2 — evidence locus vs inference extent
**Disposition: survives**

This is one of the strongest M1 improvements.

The rule that drawable containing geometry does not authorize generalization survives the attack. Silla and Late Classic Maya demonstrate why the inference extent must be an explicit reviewed assertion rather than an implicit spatial join.

The generalization basis/rationale model is sufficient at prototype stage. No probabilistic spatial surface or new GIS service is justified.

### Finding 2.3 — current selected-year serving still uses legacy ranges
**Disposition: revise**

The current web client still defines selected-year activity as simple inclusion in `from_year/to_year`.

That means M1's semantic correction is not yet integrated into the serving path. This is acceptable while M1 is experimental, but it proves that compatibility is an active boundary: new temporal semantics cannot merely exist in sidecar documentation while future claims continue through the old truth predicate.

No live change belongs in #105. #112 must define the migration/integration boundary explicitly.

## Attack 3 — Taxonomy and evidence classes

### Finding 3.1 — assertion form event/process vs practice/status
**Disposition: survives**

Baekje 369 demonstrates the value of distinguishing a bounded capture/enslavement/distribution event from an enduring territorial practice.

The additive `assertion_form` concept solves a real query problem without requiring a large subtype hierarchy.

### Finding 3.2 — multi-facet practice concepts
**Disposition: survives with constraint**

The move away from one exclusive `practice_type` toward simultaneous facets survives.

The Hittite case can carry status, function, property/legal and transmission concepts without treating them as mutually exclusive categories.

Constraint: M1 has not demonstrated an exhaustive controlled vocabulary. Only the need for orthogonal facets survives. A grand ontology remains parked.

### Finding 3.3 — claim-specific evidence direction
**Disposition: survives**

The Mauryan case still shows that `supports / challenges / qualifies / context` attached to specific claims is sufficient for ordinary conflicting evidence. No second competing-claim architecture is required by M1.

## Attack 4 — Compatibility with v0.6.1 and current preview

### Finding 4.1 — additive prototyping protected historical releases
**Disposition: survives**

M1 did not mutate v0.6.1, reinterpret existing case files, or silently republish new semantics. That is exactly the correct migration discipline.

### Finding 4.2 — P0–P4 cannot remain the target universal comparative scale
**Disposition: reject**

The assumption that P0–P4 can remain the long-term universal public summary merely by adding better semantics underneath does not survive in its current form.

The public application still:
- selects the highest active P-level for a place;
- displays P1–P4 as one sequence;
- increases polygon opacity from P1 through P4.

Even with a legend saying that only territorial practice drives the shading, the visual grammar is ordinal. Yet M1 demonstrates that the sequence combines evidence configuration and different forms of historical structure.

Therefore:
- P0–P4 may remain as **legacy compatibility data** for v0.6.1/current preview;
- it must not be treated as the target universal comparative ontology for new post-M1 semantics;
- no automatic conversion from old P-levels to new dimensions is valid;
- a later integration task must decide how the public map represents the new dimensions without rewriting historical releases.

M1 does **not** hot-fix the current preview. The preview remains explicitly non-canonical and historically reproducible.

## Attack 5 — Whole-Cliopatria geography behavior

### Finding 5.1 — complete-corpus pin/profile
**Disposition: survives**

The complete pinned corpus is small enough and reproducible enough to treat as a raw global fallback candidate:

- 13,765 features;
- 1,633 distinct names;
- 13,380 POLITY rows;
- 385 RELATION rows;
- source-native temporal extent -3400 to 2024.

The #104 implementation also found and fixed two real-corpus defects rather than passing only synthetic fixtures: archive metadata handling and property-presence counting.

This justifies whole-corpus preparation over polity-by-polity cherry-picking.

### Finding 5.2 — raw corpus is not yet selected-year atlas truth
**Disposition: experiment**

The profile does **not** yet prove that every selected-year feature should become an atlas map polygon.

Open questions remain about:
- explicit zero endpoints and atlas calendar normalization;
- RELATION/composite semantics;
- overlapping/concurrent features;
- mapping source entities to atlas spatial identities;
- case-specific specialist overrides;
- geometry QC and publication acceptance.

The correct conclusion is therefore stronger than “keep importing on demand” but weaker than “publish all vectors immediately”:

**preserve/profile the complete source corpus as infrastructure; resolve and publish selected-year geometry through reviewed source/identity/calendar rules.**

### Finding 5.3 — BCE calendar normalization
**Disposition: experiment**

Cliopatria explicitly contains zero endpoints. The atlas must not silently assume that source year 0 equals astronomical year 0 until the upstream convention is resolved and tested.

Raw source-native years remain preserved.

## Attack 6 — Map rhetoric and user interpretation

### Finding 6.1 — neutral land / unresolved geometry behavior
**Disposition: survives**

The neutral world outline, unresolved geometry state, source-geometry immutability and render-only cartographic transformations remain strong safeguards.

### Finding 6.2 — legacy ordinal shading
**Disposition: revise**

The current opacity progression P1→P4 conveys an ordinal “more” relationship more strongly than the methodology can defend across deep time.

This does not require an immediate UI rewrite during M1. It does require the post-M1 serving/UI integration to stop treating a legacy P-level as the sole visual summary once new semantics are published.

### Finding 6.3 — time slider rhetoric
**Disposition: revise**

A year slider is rhetorically precise. If the underlying query uses a broad uncertainty range as positive validity, the interface can imply knowledge of a specific year that the evidence does not support.

The #103 concept addresses this correctly, but the live query path has not adopted it yet.

## Attack 7 — Project-level claim of globally comparable evidence

### Finding 7.1 — “comparison without equivalence”
**Disposition: survives provisionally**

The project can still justify global comparison if comparison means exposing separable dimensions, evidence, uncertainty and disagreements—not ranking every society on one universal scale.

M1 strengthens this interpretation.

### Finding 7.2 — universal-intensity atlas claim
**Disposition: reject**

Any project claim equivalent to “the atlas measures slavery intensity worldwide through history on one P0–P4 scale” is not defensible after M1.

The project's stronger contribution is an evidence infrastructure that supports bounded comparison while retaining historical differences and uncertainty.

## Simpler-alternative attack

Could we keep the existing model and solve everything with better prose/legend wording?

**Reject.** Notes and labels cannot change query truth conditions, allow simultaneous classifications in one enum, or stop a selected-year filter from treating an uncertainty envelope as continuous presence.

Could we replace the whole schema/ontology now?

**Reject.** The existing universal claim/provenance/release architecture and several M1 pieces survive. A narrow correction is enough.

Could we introduce probabilistic spatiotemporal modeling?

**Park.** M1 shows semantic ambiguity, not evidence for defensible probability distributions.

## Gate decision

**REVISE.**

M1 has produced real value, but the integrated result does not yet satisfy the gate because three prototype axes remain semantically overloaded and legacy map semantics still need an explicit compatibility boundary.

Corrective issue: **#112 — M1 correct semantic axes and legacy map boundary**.

After #112:
1. rerun/update this integrated adversarial result;
2. close #105 only when the corrected prototype resolves these findings without new unjustified complexity;
3. then #106 may run the Project Health Check and choose continue / redirect / stop.

No new strategic horizon is authorized by this document.
