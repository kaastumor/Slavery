# M1 temporal and spatial inference prototype

**Gate:** #100  
**Atomic task:** #103  
**Status:** experimental; not canonical methodology or schema  
**Baseline:** v0.6.1 and the current public preview remain unchanged

## Question

How can the atlas distinguish uncertain dating from asserted historical duration, and the place where evidence was observed from the geographic extent that a reviewed claim may legitimately cover?

## Smallest proposal

Keep the existing normalized integer ranges for coarse filtering, but add two independent semantic layers in a future-compatible representation.

### 1. Temporal assertion

A claim/evidence item carries:

- `query_window`: the normalized outer interval in which the assertion may be relevant;
- `time_mode`: `continuous_interval`, `bounded_occurrence`, `alternative_dates`, `terminus_after`, `terminus_before`, `approximate_period`, or `unknown`;
- `asserted_intervals`: zero or more intervals actually asserted as applicable;
- `display_date`: source-faithful human-readable dating/precision.

The key invariant is that **query-window membership is not sufficient for selected-year historical validity**. A year is positively active only when the temporal mode and asserted interval semantics support that year. `alternative_dates` may be discoverable throughout its outer query window, but must not render as continuous positive presence between alternatives.

Open termini likewise constrain possibility without asserting an indefinitely continuous historical state. A later reviewed synthesis may separately assert continuity, but that is a different statement.

### 2. Spatial inference

A claim/evidence item carries:

- `evidence_locus`: the spatial entity/entities where the underlying observation or source is anchored;
- `inference_extent`: the spatial entity/entities over which the reviewed historical assertion is justified;
- `generalization_basis`: `same_as_locus`, `specialist_polity_synthesis`, `explicit_source_jurisdiction`, `multi_locus_synthesis`, `other_reviewed`, or `none`;
- `generalization_rationale`: required when inference extent is broader than the evidence locus.

The key invariant is that **geometry availability does not authorize generalization**. A polity polygon may receive a territorial fill only when the reviewed claim's inference extent includes that polity under an explicit rationale. Otherwise the locus remains local or geometry unresolved.

These semantics sit beside, rather than replace, source geometry, claim provenance, the #102 semantic prototype, or P0–P4.

## Selected-year behavior

A minimal predicate is:

1. use `query_window` only to find candidates;
2. evaluate `time_mode` + `asserted_intervals` for positive selected-year applicability;
3. use `inference_extent`, not `evidence_locus` or convenient containing geometry, to choose what may be filled;
4. if temporal applicability or spatial extent is unresolved, preserve the record/evidence but do not manufacture a positive continuous/polity-wide map state.

This keeps uncertain evidence inspectable without converting uncertainty into presence.

## Adversary and alternatives

| Attack / simpler alternative | Disposition | Evidence / consequence |
| --- | --- | --- |
| Keep one broad start/end range and explain uncertainty in prose | **reject** | Silla's competing 695/815/819 dating can become 125 years of apparent selected-year validity; prose cannot repair the query truth condition. |
| Treat every year inside an uncertainty envelope as positive but style it as uncertain | **reject** | This still asserts occurrence/applicability at intermediate years; uncertainty styling changes confidence, not the predicate. |
| Expand local evidence to the containing polity when a polygon exists | **reject** | Geometry is a display resource, not evidence of historical representativeness. M1-A04 and the Silla village case directly falsify this shortcut. |
| Require exact dates before anything can be queried | **reject** | It discards legitimate approximate, terminus and alternative-date evidence rather than representing its limits. |
| Preserve normalized outer ranges as candidate-search indexes | **survives** | They remain useful for retrieval if positive applicability is evaluated separately. |
| Preserve unresolved geometry instead of inventing an extent | **survives** | Existing Maya/Silla restraint already satisfies the north-star requirement; no new geometry system is needed. |
| Separate evidence locus from reviewed inference extent | **revise** | This makes the spatial generalization decision explicit and machine-testable without changing source geometry. |
| Add a temporal mode plus asserted intervals beside the outer query window | **revise** | This is the smallest representation that distinguishes uncertainty envelopes from continuous validity. |
| Build probabilistic temporal/spatial surfaces now | **park** | M1 demonstrates semantic ambiguity, not a need for probabilistic infrastructure or invented probability distributions. |

## Real-case discriminating examples

### Silla Village Register — BCE/CE-safe integer semantics, uncertain document date

The existing case records a broad 695–819 CE window because scholarship offers competing dates for the register and explicitly warns that it is not a 125-year continuous observation. Under this prototype the outer query window remains 695–819 for discovery, while `time_mode=alternative_dates` and asserted candidate dates/intervals prevent an arbitrary intermediate year such as 750 from becoming positive continuous presence.

The four village communities are the evidence locus. A whole-Silla polygon is not an inference extent merely because one is available; absent a reviewed polity-wide generalization rationale, the map remains local/unresolved.

### BCE case — Hittite central Anatolia

BCE normalized years remain ordinary signed historical-year values; no separate calendar system is introduced. A broad scholarly period can be represented as `approximate_period` and may be continuously applicable only when the reviewed synthesis actually asserts the practice across that period. This distinguishes a genuinely period-level synthesis from a single uncertainly dated attestation encoded with the same outer bounds.

### Local evidence / large polity

A city, village, estate, inscription findspot or port can be an evidence locus while a polity is the inference extent only when specialist synthesis or explicit source jurisdiction supports that enlargement. The rationale is therefore data, not an implicit spatial join.

## Machine-testable invariants

1. `alternative_dates` must not produce positive selected-year applicability merely because a year lies between minimum and maximum candidate dates.
2. `continuous_interval` may produce positive applicability for years inside an asserted interval.
3. open termini do not by themselves imply indefinite continuous applicability.
4. an inference extent broader than its evidence locus requires a non-`none` generalization basis and rationale.
5. drawable containing geometry cannot enlarge inference extent.
6. unresolved extent remains representable and must not be coerced to a polity.
7. existing signed historical-year/BCE convention is retained.

## Decision

**Revise experimentally.** Keep outer normalized ranges and existing geometry/provenance machinery, but prototype temporal applicability separately from discovery windows and spatial inference extent separately from evidence locus. The simpler notes-only/range-only alternatives fail the selected-year and polity-fill attacks. Probabilistic modeling and schema migration are parked pending the integrated M1 gate.

No historical case is reinterpreted or republished. Canonical release v0.6.1 and the public preview remain unchanged.