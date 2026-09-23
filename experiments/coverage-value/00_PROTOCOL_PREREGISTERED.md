# COV-001 — Global Coverage-Value Experiment: Pre-registered Protocol

**Issue:** #148  
**Authorized:** 2026-09-23  
**State:** setup / no slavery research may begin until the setup adversary is resolved  
**Canonical historical release:** v0.6.1 unchanged  
**Base main:** `ac73a5604c3b5b904518df224fa163b797afd30b`

## Question

H2 tested whether the Atlas's bespoke representation/query machinery materially improved difficult case-level reasoning. It did not meet that threshold.

COV-001 tests a different thesis:

> Does a deliberately comprehensive, auditable global index of documented slavery/coercion provide material value because knowledge, uncertainty and research gaps are assembled across place/time, even if ordinary research remains competitive on any one case?

This is a **coverage/corpus value experiment**, not an Atlas product experiment.

## Scope of the claim

The experiment may support only a bounded conclusion about a sampled global index.

It may **not** establish that:
- the project has captured all historical slavery;
- absence of evidence is evidence of absence;
- polity coverage represents stateless/small-scale societies;
- English-language/digitized scholarship is globally representative;
- a larger database/UI/platform is justified.

“Comprehensive” in this experiment means only: **systematically researched across a declared sampling frame with gaps and uncertainty preserved**.

## Strongest external baseline

The baseline is not a blank search box.

It includes:
- *The Cambridge World History of Slavery*;
- *The Palgrave Handbook of Global Slavery throughout History*;
- Enslaved.org when its person/event/source data are relevant;
- SlaveVoyages when voyage/trade data are relevant;
- specialist secondary literature;
- bounded primary/source-native evidence where it helps;
- ordinary structured notes/tables/GIS/search and a strong general-purpose model.

The baseline may use any of those competently.

## Phase 1 — freeze the place/time sample

Use the exact pinned Cliopatria source already accepted by M1/M2:

- repository: `Seshat-Global-History-Databank/cliopatria`
- commit: `ad28a691b7c07c1fca89d0e0636d324667d2a258`
- asset SHA-256: `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`
- 13,765 features

The sampling frame is independent of slavery evidence.

### Anchor source-years

Cliopatria's own source-native convention is used solely for sampling:

- -500 = 500 BCE
- 500 = 500 CE
- 1300 = 1300 CE
- 1800 = 1800 CE

No Atlas year normalization is needed because this step only asks which upstream rows are active at an upstream source year.

### Geographic sampling sectors

A row's geometry bounding-box midpoint is used only to assign it to a coarse sampling sector. This midpoint is **not** a historical centroid and creates no Atlas geography claim.

Six disjoint sectors:

- **A — northern/wider Americas:** longitude < -30 and latitude >= 0
- **B — southern Americas:** longitude < -30 and latitude < 0
- **C — southern/wider Africa sector:** -30 <= longitude < 60 and latitude < 30
- **D — Europe / northern West-Eurasia sector:** -30 <= longitude < 60 and latitude >= 30
- **E — central/southern/eastern Asia sector:** 60 <= longitude < 100
- **F — eastern Asia / Pacific sector:** longitude >= 100

These are sampling bins, not historical regions.

### Candidate filter

For each year × sector cell:
- `Type == POLITY`;
- `Components` empty, avoiding composite rows as sample targets;
- name does not start with `(`;
- `FromYear <= anchor <= ToYear`;
- geometry available.

`MemberOf` is not used to infer political hierarchy during sampling.

### Deterministic selection

Seed:

`COV-001|ac73a560|cliopatria-ad28a691|2026-09-23`

For every candidate compute SHA-256 of:

`seed|anchor_year|sector|row_ordinal|Name|FromYear|ToYear`

Select the lexicographically smallest digest.

The script must:
- verify the exact source SHA-256 before parsing;
- preserve the source row ordinal and native values;
- emit candidate count and selected row per stratum;
- record an empty stratum as `sampling_gap` rather than silently replacing it.

The generated sample JSON must be committed **before any slavery/coercion research begins**.

Minimum viability: at least 18 of the 24 strata must contain a valid sampled target. If fewer than 18 are valid, revise the sampling frame before historical research; do not backfill after looking at slavery evidence.

## Phase 2 — bounded research packet per sampled cell

Each valid cell gets a deliberately small **coverage profile**, not a full Atlas research case.

### Source ladder

1. major global baseline: Cambridge and/or Palgrave where relevant;
2. specialist secondary scholarship targeted to the sampled place/time;
3. primary/source-native material only where needed to establish a bounded event, term, legal rule, date or location;
4. structured specialist datasets such as Enslaved.org or SlaveVoyages where their actual scope fits.

### Research stopping rule

A cell may stop when:
- a bounded defensible profile and its main qualification are supported by specialist scholarship; or
- after the declared source ladder the evidence remains inconclusive/inaccessible.

Do not inflate source count for its own sake.

Default maximum per cell:
- 2 global-synthesis items;
- up to 4 specialist secondary items;
- up to 2 primary/source-native/dataset items.

Exceed the cap only when a source conflict cannot otherwise be represented; document why.

### Mini-index fields

The smallest useful row/profile must preserve:

- sample cell ID;
- source-native sampled polity label/row locator;
- anchor year;
- research coverage outcome;
- strongest bounded territorial-practice proposition, if any;
- strongest proposition that must **not** be asserted;
- legal/state evidence, separately;
- external/network participation evidence, separately;
- terminology/category qualification;
- temporal scope/precision;
- evidence locus vs permissible inference extent;
- evidence classes present;
- major disagreement/limiting evidence;
- exact sources/locators;
- whether Cambridge gives direct / adjacent / no usable coverage;
- whether Palgrave gives direct / adjacent / no usable coverage;
- whether a specialist structured dataset materially helps;
- unresolved issues.

Allowed research outcomes:
- `bounded_supported`
- `researched_inconclusive`
- `materially_disputed`
- `insufficient_access`

There is no historical-absence outcome.

No new P0–P4 value is assigned.

## Phase 3 — freeze the mini-index

After all valid sampled cells are researched:
- freeze the index;
- record exact source URLs/versions/access dates;
- do not improve individual rows while evaluating downstream queries unless a factual error is found;
- factual repairs must be logged and the affected evaluation rerun.

## Phase 4 — fixed coverage/query tasks

Evaluate the strongest baseline versus the frozen mini-index on these six tasks:

### Q1 — sampled anchor-year overview
For every sampled cell, what is the strongest defensible territorial-practice proposition at/around the anchor year, and which cells must remain inconclusive?

### Q2 — law versus practice
Across the sample, where does legal/state evidence differ materially from what can be asserted about observed territorial practice?

### Q3 — participation versus territorial inference
Across the sample, where is slave-trade/captive/network participation evidenced but insufficient by itself for a territorial-practice claim?

### Q4 — category/translation limits
Which sampled cells contain a terminology or category problem that materially limits direct comparison under a generic “slavery” label?

### Q5 — global-synthesis coverage
Which sampled cells are directly covered by Cambridge/Palgrave, which are only adjacent, and which require specialist follow-up before even a bounded profile is defensible?

### Q6 — unresolved coverage map
After the declared source ladder, which sampled cells remain inconclusive, disputed or access-limited, and why?

## Negative controls

The index is **not** supposed to replace specialist research.

### N1 — deep-context control
For one deterministically selected valid sample cell, ask a narrow historiographical “why/how” question drawn from its specialist literature. The specialist narrative baseline is expected to equal or beat the index.

### N2 — specialized-data control
Use SlaveVoyages for a bounded voyage/traffic question within its actual scope. The mini-index is expected to lose to the specialized database on quantitative/voyage detail.

If the mini-index appears to beat specialist tools on these controls, inspect for baseline crippling or overclaim.

## Evaluation states

For each task/probe use:

- **direct** — answer is explicit;
- **traceable** — recoverable through explicit links without reconstructing the research;
- **reconstructive** — answer requires material new source synthesis;
- **unavailable** — cannot be established within the declared evidence;
- **misleading** — artifact encourages a materially false inference.

Evaluate separately:
- coverage-state visibility;
- source/provenance recovery;
- uncertainty/abstention;
- law/practice/participation separation;
- cross-cell aggregation;
- temporal/spatial scope;
- external source retrievals required after the task begins.

No single score.

## Material-value rule

A mini-index advantage is material on a query only if:
- at least **two information probes** improve over the strongest baseline;
- improvement is not merely prettier formatting;
- no critical probe becomes misleading.

Reduced lookup count alone does not count as value.

The **coverage-corpus thesis survives this pilot** only if:
- at least **3 of the 6 global query tasks** show material value;
- the gains include at least **two different mechanisms** (for example gap/coverage visibility plus provenance/cross-case retrieval);
- neither negative control suggests the index is being treated as a replacement for specialist scholarship;
- the result adversary finds no fatal sample/baseline bias.

## Failure / shrink rule

If the index mostly restates global handbooks or ordinary tables and does not make coverage/gap questions materially more inspectable, preserve the experiment and return to project preservation.

If the mini-index has value but bespoke Atlas machinery is unnecessary, any future work must remain a **small coverage-corpus** question. This experiment cannot reauthorize the old Atlas platform.

A positive result authorizes at most one further bounded corpus-scale test. It does not authorize comprehensive global data collection automatically.
