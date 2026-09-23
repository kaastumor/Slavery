# COV-004 — Falsification Gate Protocol

**Issue:** #157  
**Authorized:** 2026-09-23  
**Base main:** `0b3a2c3f7226c312cdae432d4fb857f9b25839fd`  
**Canonical release:** v0.6.1 unchanged  
**State:** setup only; no new historical research until setup adversary passes

## Purpose

COV-004 is designed to falsify the strongest surviving post-COV-003 claims.

It tests four independent propositions:

A. C1 can safely decide which cases require C2 depth.  
B. C0/C1/C2 works outside polity-year targets.  
C. immutable releases + review propagation handle real later scholarship cleanly.  
D. an Atlas-style spatial/temporal evidence surface can add value beyond a competent register + conventional map baseline.

The experiment must not average these arms into one score.

---

# Arm A — Escalation calibration

## Question

Does the C1→C2 trigger miss cases whose compact row is materially wrong, over-broad or unsafe?

## Frozen population

Use all 12 COV-003 C1 targets.

Already escalated in COV-003:
- Zhu
- Hanthawaddy
- Pañcāla

Previously non-escalated: 9 rows.

## Audit sample

Deep-audit:
- all 3 previously escalated rows; plus
- 6 of the 9 previously non-escalated rows selected by smallest SHA-256 of:
  `COV-004-AUDIT|target_id`

Selection is frozen before any new search.

## Masked review procedure

For each selected row, create a reviewer packet containing only:
- target identity / anchor;
- source citations already known;
- source texts/snippets where accessible;
- geometry/identity metadata needed to understand the target.

Do **not** include:
- C1 outcome;
- C1 bounded conclusion;
- escalation state;
- C2 result.

The review pass must first write:
- strongest bounded conclusion;
- strongest required abstention;
- whether deep review is warranted;
- reason.

Only afterward compare with C1/C2.

This is a masked replay, **not an independent human review**.

## Material error classes

A C1 row is a false negative if masked deep review identifies any of:

- materially different outcome state;
- unsupported temporal back-projection;
- unsupported spatial generalization;
- law/practice conflation;
- network/territorial conflation;
- category/translation error;
- source-quality failure that changes the bounded proposition;
- missing disagreement that materially changes abstention.

Richer prose alone does not count.

## Gate

C1/C2 trigger survives calibration if:
- among the 6 previously non-escalated rows, at most **1** has a material false-negative error; and
- at least **2/3** previously escalated rows still show material value from depth; and
- no unreviewed safety-critical error is found in a non-escalated row that would have produced a misleading public claim.

If >1/6 non-escalated rows materially fail, the current trigger is rejected.

---

# Arm B — Non-polity frame challenge

## Question

Can tiered coverage represent historically important non-polity units without forcing them into political polygons or collapsing network/site/institution evidence into territorial practice?

## Four frame classes

Freeze **3 targets per class** = 12 total.

1. **node/site**
   - port, market, mine, plantation complex, urban site or other bounded place not equivalent to a polity.

2. **institution/estate**
   - monastery, temple estate, royal/elite estate, corporate or religious institution.

3. **mobile/network**
   - caravan/trading network, mobile pastoral/confederated formation, diaspora/trading community, maritime network.

4. **region/community**
   - stateless/segmentary society, frontier zone, cultural region or community not safely represented as one sovereign polity.

## Neutral selection requirement

Specific targets must be chosen from **non-slavery reference sources** after this protocol and setup adversary are frozen.

Allowed candidate-source types:
- Pleiades / WHG / established historical gazetteers;
- scholarly historical atlases / reference works;
- source-independent lists of historical institutions, ports, routes or cultural regions.

Candidate lists must be frozen before slavery/coercion evidence is inspected.

No target may be selected because it is known to have rich slavery evidence.

## Tiering

All 12 get C0.

Exactly 8 get C1:
- two per frame class;
- selected deterministically by SHA-256 within class before subject research.

Exactly 4 remain C0-only.

C2 escalation follows the COV-003 rule with a maximum of **4** total.

## Required non-polity fields

Every target must explicitly state:
- frame_class;
- evidence_locus_type;
- geometry_type;
- geometry_precision;
- whether territorial inference is allowed;
- if not, which inference types are allowed.

Allowed geometry types:
- point;
- bounded area;
- route/network;
- fuzzy region;
- no resolved geometry.

No mobile/network target may be rendered as a filled territorial polygon unless independently justified.

## Gate

Non-polity tiering survives if:
- all 12 can be registered without false territorialization;
- at least 7/8 C1 targets can express their strongest bounded claim without pretending they are polities;
- no more than 1/8 C1 cases requires abandoning the C1 schema entirely;
- any unresolved geometry remains visible as unresolved rather than being proxied silently.

---

# Arm C — Historical time-split update test

## Question

Can the versioned architecture handle **real later scholarship** rather than no-change searches?

## Cutoff

Frozen publication cutoff: **2015-12-31**.

## Eligible pool

Existing researched COV-001/002/003 rows are eligible if:
- at least one usable source published on or before 2015;
- target identity is not structurally invalid;
- the row can be reconstructed without post-2015 sources.

## Selection

Select **6** eligible rows by smallest SHA-256 of:
`COV-004-TIMESPLIT|cell_id`

Selection is frozen before post-2015 searching.

## Old snapshot reconstruction

For each selected row:
- reconstruct a `2015-as-of` bounded conclusion using only sources <=2015;
- freeze it.

Then search only for scholarship from **2016–2026** using a fixed target query.

Accept the first credible genuinely relevant later specialist source found within the bounded search.

## Update classes

Record:
- no later source found;
- corroborates;
- qualifies;
- challenges;
- changes target identity/time;
- changes source-quality confidence only.

## Gate

Versioned maintenance survives if:
- at least **2/6** rows produce a genuine later-evidence event; otherwise the arm is **inconclusive**, not pass;
- every event can be represented as an explicit review task without silent rewrite of the old snapshot;
- source-to-row dependencies identify every known downstream row affected by a shared source change;
- no cross-cell query silently mixes old and updated states.

No claim about lower historian labour cost is permitted.

---

# Arm D — Atlas re-entry

## Question

Does a minimal Atlas-style spatial/temporal evidence inspector add material value over a **competent ordinary baseline** once tiered evidence and non-polity frames are present?

## Baseline B

The strongest boring baseline is:

- compact C1 research register;
- conventional static map/GIS view using the same resolved geometries;
- ordinary filters by year/frame/outcome;
- citations available from the register.

The baseline may use points, areas, routes and fuzzy-region symbology.

Do not cripple it.

## Atlas A

The smallest Atlas-style inspector may add only evidence semantics that are central to the project:

- selected-year applicability;
- separate visual layers for:
  - territorial practice;
  - legal/state status;
  - network/external participation;
  - research coverage;
  - geometry certainty;
- ability to inspect evidence locus versus inference extent;
- explicit unresolved/approximate geometry;
- source/review state;
- no backend or new production infrastructure.

Implementation must be dependency-light and experimental.

## Data parity

B and A must use the **same frozen rows, sources and geometries**.

The Atlas cannot win by having more historical information.

## Fixed task families

After the non-polity sample is frozen but **before outcomes are evaluated**, instantiate one task from each family:

### D1 — spatial-locus mismatch
Find a case where the evidence locus is narrower/different from the geographic extent one might otherwise infer.

### D2 — network versus territory
Find a case where trade/captive/network participation must not become territorial-practice inference.

### D3 — selected-year / geometry uncertainty
Determine what can safely be shown at a specific year where geometry or identity is approximate/ambiguous.

### D4 — research coverage without false absence
Identify where the corpus is unresearched/inconclusive without making blank space look like “no slavery.”

### D5 — ordinary single-target reading negative control
Answer one simple target question where the map should add little or nothing.

## Evaluation states

For each task:
- direct;
- traceable;
- reconstructive;
- misleading;
- unavailable.

Also record:
- number of cross-references between register and map;
- whether a user must mentally join law/practice/network/geometry layers;
- any false territorialization induced by the visualization.

## Atlas re-entry gate

Atlas A survives if:
- it materially improves at least **2 of D1–D4** over baseline B;
- it introduces **zero** new misleading territorial/spatial inferences;
- D5 remains parity or baseline-favored;
- improvements come from spatial/temporal evidence semantics, not styling.

If it passes, only the **thin Atlas inspection hypothesis** is reopened.

It does not authorize product/platform work.

---

# Overall outcome matrix

Arms remain independent.

## FAIL / SHRINK
Use if:
- Arm A rejects the escalation trigger; or
- Arm B shows the tiered model is polity-bound in a way that cannot be repaired without a new ontology.

This can coexist with an Atlas-arm success.

## METHOD SURVIVE
Use if:
- A and B survive;
- C is pass or inconclusive;
- D fails.

Interpretation: tiered research method survives; Atlas remains unearned.

## ATLAS RE-ENTRY
Use if:
- A and B survive;
- D passes;
- C is pass or inconclusive.

Interpretation: tiered method survives and the **thin Atlas inspection layer** regains a bounded value hypothesis.

## STRONG VALIDATION
Use only if:
- A survives;
- B survives;
- C passes with >=2 real later-evidence events;
- D passes;
- no setup/result adversary identifies a hidden source-quality or false-equivalence failure.

Even STRONG VALIDATION does not authorize comprehensive ingestion or a production Atlas.

---

# Hard exclusions

- v0.6.1 remains canonical;
- no production DB/API/frontend migration;
- no full application rebuild;
- no automated mass research;
- no P0–P4 revival;
- no source-count/prevalence inference;
- no unknown -> absence;
- no actor nationality inference from flag/port/registration;
- no silent modern geometry proxy;
- no non-polity target forced into a polity shape;
- no successor horizon created automatically.
