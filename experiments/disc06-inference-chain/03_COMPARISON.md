# DISC-06 comparison — baseline versus minimal inference ledger

## Method

The six frozen cases were replayed from their existing final R1 rows and adversarial
records. No historical sources were re-searched and no historical conclusion was
changed.

For each case, the current packet was first treated as the baseline. The experimental
ledger was then constructed using only the seven preregistered fields.

The question is **material information gain**, not readability or compactness.

## Result matrix

| Case | Known failure | Baseline reconstructs corrected premise? | Ledger makes impact lookup easier? | Material information unavailable in baseline? |
| --- | --- | --- | --- | --- |
| Teotihuacan | temporal leakage | yes — temporal precision/applicability + correction prose identify earlier Moon Pyramid evidence | yes | **no** |
| Shaolin | target/context join | yes — evidence locus, source notes and abstention separate Shaolin from generic monastery context | yes | **no** |
| Inuit | dimension + time/extent | yes — external/territorial summaries, locus/extent and abstention are explicit | yes | **no** |
| Cahokia | status + time | yes — source directions/notes, temporal precision and C2/adversarial correction expose the weakened status premises | yes | **no** |
| Lazica | time + dependency + dimension | yes — exact independence group, network/territorial note, temporal applicability and correction prose are explicit | yes | **no** |
| Nālandā | target/context + dependency | yes — target-specific tenancy versus generic monastery context and shared Yijing dependency are explicit | yes | **no** |

**Distinct failure mechanisms with material ledger-only information: 0.**

The preregistered SURVIVES threshold required at least 2.

## Task 1 — exact premise whose correction changed the conclusion

The baseline succeeds on all six cases.

This is not because the packet contains a formal argument graph. It is because the
post-R1 portable contract already carries the fields that the historical corrections
actually depended on:
- temporal applicability/precision;
- target-specific evidence locus;
- inference extent;
- dimension-specific notes;
- source direction/claim fitness;
- independence group;
- explicit adversarial correction.

The ledger turns those relationships into one-row lookups but does not add a premise
that was missing.

## Task 2 — revision impact

The ledger is somewhat easier to scan when asking “which conclusion key uses this
source/group?” That is **organizational convenience**, not yet material
reconstructibility gain.

For the six test cases, the same impact is recoverable from one target row plus its
source list and adversarial correction. None contains a large enough web of independent
derived conclusions for the lack of reverse edges to create a demonstrated correctness
failure.

The experiment therefore cannot claim a maintenance/scaling benefit that it did not
measure.

## Task 3 — source evidence versus project inference

The baseline already separates these effectively.

Example:
- Lazica's source says slave export; the Atlas inference refuses selected-year 500 and
  territorial-practice transfer.
- Inuit sources establish people being enslaved by external actors; the Atlas inference
  refuses internal/circumpolar practice.
- Shaolin/Nālandā sources include broad monastic context; the Atlas inference refuses
  target transfer.

The ledger labels the rule but does not create a new epistemic distinction.

## Task 4 — assertion granularity exposes the real first-refusal boundary

The most important negative result appears in Nālandā and Cahokia.

A source can contain multiple claim-relevant assertions:
- Bian/Yijing material contains target-specific Nālandā economic reconstruction **and**
  generic monastery servants/slaves context.
- Cahokia papers revise different premises: origin, sex, ritual configuration and
  social-status interpretation.

A ledger that references only a **source** is too coarse to model those distinctions.
To make it genuinely stronger, DISC-06 would need to create separate source-assertion /
factoid objects and then point inferences at them.

That is no longer the tiny seven-field addition under test. It would be a new durable
abstraction layer with new authoring, identity and review burden.

Under D-092 first refusal, that expansion is **not earned** merely because CRMinf/FPO
can represent it.

## Task 5 — review burden / duplication

The experimental ledger contains 15 manually maintained relations for six already
well-bounded rows.

Each relation repeats information already encoded in one or more of:
- temporal applicability;
- required abstention;
- evidence locus / inference extent;
- network/territorial note;
- source direction / claim fitness;
- independence group;
- adversarial correction.

Keeping both layers synchronized creates another review surface.

No tested case demonstrates that this cost prevents a real error better than the
current baseline.

## Mutation probes

Three hypothetical maintenance probes were also replayed conceptually:

### Procopius/Lazica source-family reinterpretation

Baseline:
- exact shared independence group already identifies Procopius + Braund as one family;
- network/territorial and temporal notes identify the conclusions that remain bounded.

Ledger:
- provides direct conclusion keys.

**Difference:** lookup convenience, not missing historical/review information.

### Moon Pyramid dating revision

Baseline:
- temporal precision/applicability already owns the selected-year boundary.

Ledger:
- repeats a `temporal_applicability` block.

**Difference:** none material.

### Yijing/Nālandā interpretation revision

Baseline:
- source notes and bounded proposition distinguish target-specific tenancy from generic
  monastery servants/slaves.

Ledger:
- source-level premise reference cannot express the two assertions any more precisely.

**Difference:** no gain without adding a new assertion/factoid layer.

## Discriminator

- material gains in >=2 distinct failure mechanisms: **0**
- organizational/readability gains: **6/6**
- cases requiring a richer assertion layer before the ledger could add new semantics:
  **at least 2** (Nālandā, Cahokia)
- infrastructure required by the tested ledger: none
- duplication introduced: 15 inference relations across 6 rows

The preregistered SURVIVES threshold is not met.
