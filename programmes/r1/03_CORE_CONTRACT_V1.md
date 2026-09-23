# Historical Slavery Atlas — Core Contract v1

**Programme:** R1 / issue #159  
**Status:** frozen R1 release-method contract after setup adversary  
**Scope:** research/release semantics; **not** a PostgreSQL schema replacement  
**Canonical historical data release:** v0.6.1 remains unchanged

## 0. Purpose

Core Contract v1 defines the minimum semantics a new R1 research/release artifact must preserve.

It consolidates existing project methodology plus failure modes demonstrated in M1/M2 and COV-001→004.

It does **not** create:
- a new universal ontology;
- a new intensity scale;
- a new database architecture;
- an exhaustive slavery taxonomy.

Where this contract is silent, the existing canonical method/source/geography/release documents remain authoritative.

---

# 1. Research tiers

The tier is a **research/release workflow state**, not a historical property.

## C0 — registered target / research state

A C0 target may record:
- target identity;
- source-native identity and source version;
- target type / sampling frame;
- temporal frame;
- spatial frame;
- identity-validation state;
- geometry state;
- research stage;
- reviewed-through date/release id.

A C0 target MUST NOT assert:
- slavery presence;
- slavery absence;
- legal status;
- territorial practice;
- prevalence;
- external/network participation.

Required interpretation when subject research is not performed:

> Registered target; historical slavery/coercion research not yet performed.

Canonical mapping:
- `research_stage = not_researched` or another non-complete workflow state;
- `classification_outcome = unassessed`.

C0 is not a historical negative.

## C1 — compact bounded research

A C1 target is a reviewed synthesis sufficient for bounded comparison.

Required:
- `research_stage`;
- `classification_outcome`;
- strongest bounded proposition;
- strongest required abstention;
- target temporal frame;
- positive temporal applicability semantics where any claim applies;
- temporal precision/certainty;
- evidence locus;
- inference extent;
- source-quality state for decisive source relations;
- exact source/version references;
- source direction where materially relevant;
- law/practice distinction where material;
- network/territorial distinction where material;
- language/access limitation;
- coverage confidence;
- review state;
- reviewed-through/release id.

C1 may legitimately end:
- classified;
- disputed;
- inconclusive.

Inconclusive is not absence.

## C2 — selective deep review

C2 is required only when a material risk or dispute warrants deeper interpretation.

Escalation triggers:
1. unresolved historiographical disagreement;
2. category/translation ambiguity;
3. temporal back-projection risk;
4. spatial/generalization risk;
5. law/practice ambiguity;
6. network/territorial ambiguity;
7. target identity or geometry uncertainty that changes interpretation;
8. decisive positive proposition depends on a source whose claim fitness is below production grade;
9. adversarial/QC reviewer escalation;
10. source-dependency correction affecting multiple claims.

C2 adds, where needed:
- richer source role/direction/directness;
- source-independence analysis;
- source-native terminology;
- terminology/category reasoning;
- contrary/limiting evidence;
- generalization basis;
- detailed temporal/spatial inference reasoning;
- explicit review propagation.

C2 is not a prestige label and is never triggered by fame or documentation volume alone.

---

# 2. Historical dimensions that remain separate

The release must not collapse:
- territorial practice;
- legal/state status;
- external/network participation;
- research coverage;
- historical geometry.

These dimensions may coexist, conflict, or remain independently unknown.

No single “total slavery” field is permitted.

Legacy P0–P4 may be reproduced only for releases that already contain it. R1 must not derive a new P-level.

---

# 3. Research stage and classification outcome

Use the existing post-M1 separation.

## Research stage
Examples:
- `not_researched`
- `source_identified`
- `under_review`
- `review_complete`

## Classification outcome
Examples:
- `unassessed`
- `classified`
- `disputed`
- `inconclusive`

A review-complete row may be disputed or inconclusive.

Do not use workflow progress as a historical result.

---

# 4. Bounded proposition and abstention

Every C1/C2 synthesis must state:

## Strongest bounded proposition
The strongest historical statement the reviewed evidence package supports.

## Strongest required abstention
The most important tempting inference that the package does **not** support.

The abstention is part of the release semantics, not optional prose.

Examples:
- a slave sale does not prove widespread territorial practice;
- a law code does not quantify compliance/prevalence;
- network participation does not prove territorial practice;
- a later ethnography does not automatically establish an earlier institution;
- sacrifice/captivity does not automatically establish slave status.

---

# 5. Source relation contract

Evidence is claim-specific.

Each decisive evidence relation must be recoverable to an exact `SOURCE_VERSION` where version identity matters.

Record where relevant:
- source/version identity;
- source classification;
- evidence role;
- direction = `supports | challenges | qualifies | context`;
- directness;
- independence group;
- locator;
- interpretation/limitation note;
- claim-fitness/source-quality state.

## Claim-fitness / source-quality state

Allowed R1 values:
- `production_grade`
- `usable_with_limitation`
- `context_only`
- `access_limited`
- `review_required`

Meaning is **fitness for the specific bounded claim**, not prestige of venue.

A positive bounded proposition may not depend solely on:
- `context_only`;
- `review_required`.

A positive proposition relying on `usable_with_limitation` must receive adversarial replay.

Source quality, evidence direction and source independence are separate concepts.

---

# 6. Primary / secondary roles

Primary/source-native evidence is especially suited to:
- events;
- transactions;
- laws;
- inscriptions;
- terminology;
- dates;
- locations.

Specialist scholarship is normally required for:
- historical classification;
- prevalence;
- continuity;
- structural significance;
- terminology interpretation;
- representativeness;
- historiographical disagreement.

Neither source class is universally superior.

A collection of primary attestations does not mechanically establish prevalence.

---

# 7. Source independence and archive-density guard

Citation count is not independent support.

Track dependence where multiple works rely on:
- the same primary source;
- the same dataset;
- the same prior synthesis;
- the same archive slice.

Never allow:
- source count;
- voyage count;
- document count;
- archive density;
- digitization density

to mechanically set historical prevalence or intensity.

Sampling/research density is a research-coverage property only.

---

# 8. Language / access / coverage confidence

Every C1/C2 must record:
- languages actually used/searched where known;
- material language or archive gaps;
- access limitations;
- `coverage_confidence` for the research process.

Coverage confidence is separate from historical classification confidence.

A row may be:
- historically classified;
- but research coverage limited.

`inconclusive` never claims literature exhaustion.

---

# 9. Temporal contract

Keep separate:
1. outer query window;
2. positive temporal applicability;
3. temporal precision/certainty.

A broad date range is not continuous historical truth.

Alternative dates do not fill the interval between them.

An open terminus does not create indefinite continuity.

Selected-year truth must evaluate positive applicability semantics, not simple range membership.

Preserve source-native date wording where historically material.

---

# 10. Spatial contract

Keep separate:
- spatial/target identity;
- historical jurisdiction/control;
- evidence locus;
- inference extent;
- geometry representation;
- geometry certainty/provenance.

Geometry availability never authorizes historical generalization.

Allowed release geometry states include:
- exact/accepted historical;
- specialist historical;
- approximate historical;
- modern proxy;
- point/site;
- route/network;
- fuzzy region;
- unresolved/no geometry.

Any proxy/approximation must be explicit.

A route is not territorial practice.

A site is not a polity.

A containing polygon is not an inference basis.

Neutral world land remains visible.

---

# 11. Event/process versus enduring practice

A bounded:
- capture;
- sale;
- transfer;
- enslavement;
- raid;
- transaction

may be a strong historical claim without establishing:
- recurrence;
- institution;
- prevalence;
- structural significance;
- enduring territorial practice.

Assertion form must remain recoverable.

---

# 12. Faceted practice concepts

Do not force status, function, legal powers, transmission and process into one mutually exclusive code.

Where needed, preserve independent facets such as:
- status/condition;
- function/context;
- property/legal powers;
- transmission/exit;
- process.

Vocabulary grows only when a real research case requires it.

Source-native terms remain preserved and are not mechanically translated into atlas categories.

---

# 13. Actor identity / roles

Actor identity remains separate from historical role.

Never infer nationality/political identity from:
- vessel flag;
- registration;
- port;
- residence;
- business base;
- surname;
- company jurisdiction.

Unknown remains unknown until independently evidenced.

---

# 14. Research coverage

Research coverage is project metadata, not evidence of historical prevalence.

C0/C1/C2 and review state may be exposed as transparency layers.

A missing or unresearched claim must never render as historical absence.

---

# 15. Source-to-claim dependency

Every released historical proposition must be traceable:

`SOURCE_VERSION -> evidence relation -> CLAIM -> target -> release`

Where one source/source packet materially informs multiple claims, all dependents must be recoverable.

A material source correction creates explicit review propagation.

No graph database is required; a flat dependency table is sufficient for R1.

---

# 16. Release immutability and supersession

Published/candidate release snapshots are immutable.

New evidence creates:
- a new review task;
- updated claim/research state in a later release;
- supersession linkage where appropriate.

Old releases are not rewritten.

Queries and Atlas views must bind to one release/as-of state.

---

# 17. Review states

Minimum R1 review labels:
- `draft`
- `internally_reviewed`
- `internally_adversarially_reviewed`
- `independently_reviewed`
- `published`
- `superseded`
- `rejected_or_withdrawn` where required.

Do not imply independent review when only internal/adversarial replay occurred.

---

# 18. R1 candidate publication gates

A C1 positive proposition cannot enter the candidate release if:
- decisive source relation is `context_only` or `review_required`;
- target identity is unresolved in a way that changes the proposition;
- temporal applicability is inferred only from an outer query window;
- inference extent exceeds evidence locus without reviewed generalization basis;
- law or network evidence is being used as territorial practice without independent support;
- required abstention is missing;
- source/version cannot be recovered.

A C2 row may remain unresolved if the disagreement/uncertainty is explicit and release-safe.

---

# 19. Required adversarial replay

For R1 candidate release:
- at least 50% of C1 rows;
- 100% of C2 rows;
- 100% of positive claims with only one decisive source;
- 100% of positive claims using `usable_with_limitation`.

If material-error rate in the first half of replayed C1 exceeds 10%:
- expand replay to 100% of C1;
- run a release-wide scan for the repeated error class.

---

# 20. Atlas presentation contract

The default R1 Atlas surface is:
- neutral world outline;
- historical/non-polity geometry where defensible;
- ordinary point/route/fuzzy/unresolved symbology;
- selected-year applicability;
- C0 research state visible;
- bounded proposition + abstention;
- citations;
- release/review state.

Do not build bespoke Atlas machinery unless a real R1 friction ticket earns a bounded feature test.

---

# 21. “Rock hard” definition

Core v1 does not claim immutable historical truth.

For R1, “rock hard” means:

> provenance, uncertainty, inference boundaries, dependencies, research state and revision history are explicit enough that later correction can occur without corrupting what the release previously said.

That is the durability target.
