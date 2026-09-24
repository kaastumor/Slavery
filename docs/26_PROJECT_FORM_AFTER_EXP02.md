# Project Form After EXP-02

**Issue:** #209  
**Date:** 2026-09-24  
**Input decisions:** D-063, D-073, D-080, D-085, D-086  
**Canonical historical data release:** v0.6.1 unchanged  
**Disposition:** **SIMPLIFY + PRESERVE ATLAS AS VIEW**

## Question

What should the Historical Slavery Atlas now be structurally, after EXP-02 showed that the frozen R1 safety/reconstructibility contract survives in a much smaller portable artifact?

This is a project-form decision.

It is not:
- a schema migration;
- a canonical data release;
- a new research programme;
- a new product-feature horizon;
- external user validation.

## Evidence entering the review

The project now has several converging results:

1. H2 found the corpus/method materially beat the strongest boring baseline in only 1/3 tasks, while the thin view improved the corpus/method in 0/3.
2. COV-004 found the bespoke Atlas evidence inspector did not materially outperform a competent conventional map/register on the frozen map tasks.
3. COV-003/COV-004 and R1 repeatedly preserved value in:
   - bounded proposition / abstention;
   - law/practice separation;
   - network/territorial separation;
   - source dependency;
   - temporal/spatial inference guards;
   - explicit research state;
   - immutable/as-of releases.
4. R1 produced a deterministic candidate without requiring a live evidence API.
5. R1 ended HOLD_NO_RELEASE after its release-integrity defect was repaired.
6. EXP-02 showed that the fixed R1 evidence contract survives in:
   - one package manifest;
   - one flat target table;
   - one flat source-relation table;
   - optional Markdown review packets.
7. EXP-02 did not establish external demand or show that a map is useless.
8. External involvement is intentionally deferred.

## Candidate project forms

### A. Continue current application-centered form

Interpretation:

> keep the web Atlas/application as the primary architectural product and treat the evidence package as an export.

### Attack

This form now has weak evidence.

- H2 did not show repeated thin-view advantage.
- COV-004 did not show custom-inspector advantage over an ordinary map/register.
- EXP-02 shows the safety contract does not depend on application-shaped structure.
- The existing database/web/API stack is substantially more machinery than is needed to preserve the demonstrated core.

### Disposition

**REJECT as the default project form.**

Preserve the existing implementation, but do not make future evidence modelling depend on it.

---

### B. Redirect away from the Atlas entirely

Interpretation:

> rename/reframe the project as a historical evidence method and remove map/Atlas identity from the conceptual model.

### Attack

This overreads EXP-02.

- EXP-02 tested information preservation, not human exploration or geographic usefulness.
- historical geography remains a real separate evidence dimension;
- the charter's place/time inspection goal still makes sense;
- COV-004's strongest boring baseline itself included an ordinary map/register;
- neutral world context and historical geometry remain useful where defensible;
- no experiment showed that geographic navigation itself is harmful or valueless.

### Disposition

**REJECT.**

The map should lose architectural ownership of truth, not disappear.

---

### C. Stop the project and preserve only historical artifacts

Interpretation:

> no project identity beyond archived methodology, corpus and experiments.

### Attack

This is stronger than the evidence permits.

The project has repeatedly falsified application/platform assumptions, but the evidence method itself survived:
- COV-003: tiered method survived;
- COV-004: method survived;
- R1: bounded release process survived;
- EXP-02: portable core survived.

However, no active expansion or product horizon is currently justified.

### Disposition

**PARTIAL.**

Preservation/idle is the correct **current execution state**, but not a conclusion that the project has no durable form or future trigger.

---

### D. Simplify + preserve Atlas as a derived view

Interpretation:

> the historical evidence package owns portable truth/reconstructibility; research infrastructure authors and validates it; maps/tables/web/API are replaceable views over released evidence.

### Attack

Risks:
- 19 reviewed C1 rows are a small set;
- all 77 geometries are unresolved, so some simplifications are release-specific;
- EXP-02 omitted source-role/claim-fitness enrichment from the minimum packet;
- a flat release package may become awkward at materially larger scale;
- no external user evidence establishes that this form is useful.

### What survives the attack

The decision does not require those unknowns to be resolved.

It only states:
- presentation must not own historical truth;
- a portable release/interchange boundary is sufficient for the current demonstrated contract;
- richer authoring infrastructure can remain behind that boundary;
- future mixed-geometry or larger releases may require more fields/structure;
- user value remains an independent unresolved question.

### Disposition

**SURVIVES.**

This is the smallest form consistent with the evidence.

# Adopted project form

## 1. Project identity

The project remains **Historical Slavery Atlas**.

“Atlas” describes a geographic/time-aware inspection and publication mode, not a requirement that the project be architected as a bespoke web application.

## 2. Evidence core

The durable center is the reviewed historical evidence contract:

- target identity and research state;
- bounded proposition;
- required abstention;
- evidence locus;
- inference extent;
- temporal state / display rule;
- law/practice distinction where material;
- network/territorial distinction where material;
- exact source/version/locator;
- source-family dependency;
- access/language limitation;
- coverage confidence;
- explicit non-absence semantics;
- geometry state/policy where relevant.

No presentation surface may silently strengthen these claims.

## 3. Research/curation system

PostgreSQL/PostGIS and the existing normalized repository architecture remain valid **research/curation infrastructure**.

They are useful for:
- relational integrity;
- imports;
- provenance;
- geometry work;
- review state;
- release reconstruction;
- future mixed spatial representations.

They are not required to be the public product runtime or the portable release format.

No migration or deletion is authorized by this decision.

## 4. Release/interchange boundary

For post-R1 work, the preferred architectural boundary is:

> reviewed research state → immutable portable evidence package → one or more presentation adapters

The EXP-02 package is evidence that this boundary is feasible.

It is **not** a canonical replacement schema.

Future releases may add fields when new evidence requires them.

## 5. Presentation adapters

Valid views may include:
- ordinary map/GIS;
- compact evidence register;
- static/interactive Atlas;
- flat tables;
- Markdown packets;
- notebooks/scripts;
- API endpoints if a real consumer requires them.

A view:
- does not own canonical historical truth;
- must preserve claim/research/temporal/geometry distinctions;
- can be replaced without changing the evidence meaning.

## 6. Current execution state

**ACTIVE EVIDENCE RESEARCH.**

D-088 supersedes only D-087's preservation/idle **execution consequence**. The project-form conclusion remains unchanged.

Current active horizon: **#211 / EXP-03 heterogeneous evidence stress test**.

The project should continue through bounded research/discovery rather than return to idle merely because a prior horizon completed. WIP remains 1.

## 7. Continuation and escalation rules

A bounded historical/methodological experiment does not require an external trigger merely to exist. After each horizon:
- reconcile evidence;
- choose the highest-information unresolved question;
- preregister one successor;
- continue if the experiment can materially change belief without unacceptable evidence-quality or complexity cost.

Elapsed time alone is not a stop criterion.

Separate triggers are still required for:
- canonical schema/data migration;
- production/public release;
- major infrastructure;
- external recruitment/participant work;
- sensitive modern-person data;
- other scope changes with materially higher risk.

Those triggers authorize evaluation, not automatic implementation.

# Red-team conclusion

The strongest conclusion is **not**:

> the Atlas is unnecessary.

It is:

> the Atlas must not be the architectural owner of the evidence.

The current evidence supports a portable evidence core with replaceable geographic and non-geographic views.

That is a simplification of architecture and project planning, not a renaming of the project or a canonical schema migration.
