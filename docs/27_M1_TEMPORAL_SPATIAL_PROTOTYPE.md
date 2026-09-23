# M1 temporal and spatial inference prototype

**Gate:** #100  
**Original task:** #103  
**Corrective task:** #112  
**Status:** experimental; not canonical methodology or schema  
**Prototype:** v2 after integrated adversarial correction  
**Baseline:** v0.6.1 and current public preview remain unchanged

## Question

How can the atlas distinguish uncertain dating from asserted historical duration, and evidence location from the spatial extent a reviewed claim may legitimately cover?

## Correction from v1

The first prototype correctly separated `query_window` from positive selected-year applicability, but put `approximate_period` in the same `time_mode` field as continuity and bounded occurrence.

That still mixed two concepts:

- **applicability** — what years the claim positively applies to;
- **precision/certainty** — how exact the dates are.

Approximation cannot itself assert continuity.

## Temporal representation

A claim/evidence item carries:

- **query_window** — outer normalized interval used to retrieve candidate records;
- **applicability_mode** — `continuous_interval`, `bounded_occurrence`, `alternative_dates`, `terminus_after`, `terminus_before`, or `unknown`;
- **asserted_intervals** — intervals/dates positively asserted under the applicability mode;
- **temporal_precision** — independently describes exactness such as `exact`, `approximate`, `broad_range`, `disputed_alternatives`, or `unknown`;
- source-faithful date text/other existing certainty metadata may remain alongside these fields.

### Invariant

**Changing temporal precision alone must not change selected-year truth.**

An approximate continuous period can be active throughout an asserted interval because continuity was separately reviewed and asserted. An approximately dated bounded occurrence does not become active across its entire uncertainty envelope.

## Real cases

### Silla Village Register

The source case records 695–819 CE as an outer range because proposed dates include 695, 755, 815, and 818–819.

Prototype v2:

- query window: 695–819
- applicability: alternative dates
- precision: disputed alternatives
- asserted intervals: 695, 755, 815, 818–819

Years such as 700, 750, and 800 remain discoverable through the outer window but are not positive selected-year validity.

### Hittite central Anatolia

The reviewed claim is a broad period-level synthesis (1400–1200 BCE), not one uncertainly dated event.

Prototype v2 therefore uses:

- applicability: continuous interval
- precision: broad range
- asserted interval: the reviewed historical period

Continuity comes from the synthesis, not from the fact that the boundaries are broad.

## Spatial inference

The #103 spatial split survives unchanged:

- **evidence_locus** — where the observation/source is anchored;
- **inference_extent** — where the reviewed historical assertion is justified;
- **generalization_basis** — explicit reviewed basis for any enlargement;
- **generalization_rationale** — required when extent exceeds locus.

Geometry availability never authorizes generalization. A polity polygon can be drawn only when the claim's reviewed inference extent includes that polity.

## Selected-year behavior

1. use query window for candidate retrieval;
2. evaluate applicability mode + asserted intervals for positive selected-year truth;
3. treat temporal precision/certainty as metadata about the dates, not as the truth predicate;
4. use inference extent, not a containing geometry, for map fill;
5. unresolved applicability/extent remains representable without manufacturing a positive state.

## Compatibility boundary

The current preview still filters active claims using legacy `from_year/to_year`. M1 does not silently alter that released preview.

Before post-M1 semantics become publishable, the serving/API path must carry enough temporal semantics for the client to evaluate selected-year applicability without treating uncertainty envelopes as continuous presence.

That later integration must be deliberate and release-aware.

## Adversarial alternatives

| Alternative | Disposition | Result |
| --- | --- | --- |
| Keep `approximate_period` as an applicability mode | **reject** | Approximation says nothing about continuity. |
| Infer continuity from a broad range | **reject** | Recreates the Silla failure mode. |
| Let precision change truth behavior | **reject** | Precision and applicability are orthogonal. |
| Keep outer range for retrieval | **survives** | Useful and simple when not treated as positive validity. |
| Evidence locus vs inference extent split | **survives** | Prevents geometry-driven generalization. |
| Probabilistic time/space surfaces | **park** | No evidence M1 needs probability distributions. |

## Machine-testable invariants

1. query-window membership is not sufficient for positive selected-year validity;
2. applicability mode is independent from temporal precision;
3. approximation alone cannot assert continuity;
4. alternative dates do not fill intermediate years;
5. a reviewed continuous interval can remain continuous even with broad/approximate date precision;
6. geometry cannot enlarge inference extent;
7. broader inference requires a reviewed basis and rationale;
8. unresolved extent is valid;
9. the existing signed atlas historical-year convention remains intact; Cliopatria source-native year normalization remains a separate integration decision.

## Decision

**Revise → survives at prototype level.**

The v2 representation removes the precision/applicability collision without changing source data, canonical releases, public serving, or database schema. #105 must still rerun the integrated gate before M1 can close.
