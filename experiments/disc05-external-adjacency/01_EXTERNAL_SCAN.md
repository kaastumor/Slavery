# DISC-05 external adjacency scan

## Result

The scan found several useful external precedents, but **no reason to reopen the old
feature queue**. The strongest opportunities are methodological and interchange-oriented.

The highest-information next question is whether the current portable evidence packet
loses material information about **inference provenance**: which premises and reasoning
steps produced an atlas conclusion, and what other conclusions should be reconsidered
when a premise changes.

That question is selected for one bounded successor experiment. No new ontology,
graph database or production feature is authorized.

---

## D5-01 — explicit inference provenance

**External precedent**

CIDOC **CRMinf** models argumentation and inference making. Its current model includes
an `I5 Inference Making` class whose purpose is to trace conclusions back through
premises and reasoning logic, including the effect of knowledge revision on later
beliefs.

King's College London's **Factoid Prosopography Ontology** uses source-derived
assertions/factoids as the central historical unit. A factoid is a structured
interpretation of what a historical source says, linked to the exact source citation.
It also distinguishes the date when an assertion/source was made from the date to which
the assertion refers.

Sources:
- https://cidoc-crm.org/crminf
- https://cidoc-crm.org/extensions/crminf/html/CRMinf_v1.2.1.html
- https://www.kcl.ac.uk/factoid-prosopography/fpo-factoids
- https://www.kcl.ac.uk/factoid-prosopography/fpo-sources
- https://pase.ac.uk/about/research-methodology/

**Observed project friction**

R1 adversarial replay produced real corrections caused by:
- temporal projection;
- target/context evidence joins;
- external/network evidence becoming internal practice;
- status overstatement;
- source-dependency normalization.

Current packets preserve the final proposition, abstention, source relation direction,
claim fitness and dependency groups. They do not necessarily preserve one explicit,
portable object saying **these premises + this reasoning step produced this conclusion**.

**Strongest current baseline**

Current target/source tables + packet prose + dependency groups.

**Transfer mechanism**

A minimal inference ledger could make reasoning dependencies explicit without adopting
CIDOC CRM, RDF or a graph database.

**Transfer risk**

CRMinf is deliberately general and ontology-heavy relative to this project. A separate
inference layer could merely duplicate prose and increase review burden.

**Cheap falsifier**

Replay a small set of already-corrected R1/EXP cases. Encode only:
- conclusion;
- premise source-relation / prior-claim IDs;
- short reasoning rule/justification;
- review state.

If the current packet lets a reviewer reconstruct the same dependency/revision impact
without ambiguity, reject the new abstraction.

**Disposition:** **DISCOVERY CANDIDATE — SELECTED NEXT**

---

## D5-02 — research-coverage / evidence-gap audit

**External precedent**

Evidence and Gap Maps use pre-specified, systematic evidence searches and map the
distribution of available evidence and gaps separately from outcome/effect direction.
A 2024 methods review emphasizes explicit framework design, filters, update practice
and stakeholder/use considerations.

**Seshat** provides a closer global-history comparison. It separates present, absent,
unknown, inferred states, uncertainty ranges and expert disagreement, while attaching
narrative coding rationales and scholarly sources.

Sources:
- https://doi.org/10.1002/cesm.12096
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4750281/
- https://seshat-db.com/methods/
- https://seshat-db.com/codebook

**Observed project friction**

The Atlas already insists that research coverage is not historical prevalence, but
horizon selection still relies partly on manual balancing across region, chronology,
frame and prior coverage.

**Strongest current baseline**

Frozen registry + research state + language/access notes + manual expected-information-
gain comparison.

**Transfer mechanism**

Use an evidence-gap-style **coverage audit**, not a slavery map: target frame × period ×
region × research state × access/language/source-tradition. Ask whether it exposes a
selection blind spot that current manual inspection misses.

**Transfer risk**

Evidence-gap terminology can imply that an unresearched cell is a true knowledge gap.
Historical archives also have survival/access biases unlike intervention-study
literatures. Seshat's `inferred absent` convention directly conflicts with this
project's non-absence rule and must not transfer.

**Cheap falsifier**

Generate one non-visual matrix from the existing registry. Compare the next-horizon
choice produced with and without it. If it changes no decision and reveals no hidden
coverage concentration, keep the current baseline.

**Disposition:** **DISCOVERY CANDIDATE — not selected while D5-01 has higher correctness leverage**

---

## D5-03 — standard portable research packaging

**External precedent**

**Frictionless Data Package** provides a small, human-editable JSON descriptor for a
collection of files, with Tabular Data Package/Table Schema for CSV structure.

**RO-Crate 1.3** packages research data and contextual metadata in a JSON-LD metadata
document and can describe local/remote resources, creators, software and provenance.

Sources:
- https://specs.frictionlessdata.io/guides/data-package/
- https://specs.frictionlessdata.io/tabular-data-package/
- https://www.researchobject.org/ro-crate/specification
- https://www.researchobject.org/ro-crate/specification/1.3/introduction.html

**Observed project friction**

EXP-02/EXP-06 already produce a custom manifest + flat CSVs + Markdown + checksums.
That is structurally close to an established data-package pattern.

**Strongest current baseline**

Existing deterministic manifest/checksum package. It already works.

**Transfer mechanism**

Benchmark the existing candidate against:
1. a Frictionless descriptor as the simpler standard;
2. RO-Crate only if richer research-object provenance adds something material.

**Transfer risk**

Standards can add metadata duplication and version dependency without improving
reconstructibility. Frictionless v2 is under active development; avoid binding a
canonical release to a moving profile without demonstrated benefit.

**Cheap falsifier**

Wrap one existing candidate without changing its files. If validation/interoperability
does not improve enough to replace custom manifest logic, reject adoption.

**Disposition:** **BENCHMARK / REUSE CANDIDATE; not next**

---

## D5-04 — historical place/time interchange

**External precedent**

World Historical Gazetteer's **Linked Places Format (LPF)** supports temporally scoped
names, geometries, types and relations, multiple geometries, uncertain dates,
provenance and source citations.

**PeriodO** stores *definitions* of historical periods rather than pretending period
names have one universal meaning. Entries require a name, temporal bounds, geographic
association and citable source; textual source expressions coexist with structured
temporal approximations.

Sources:
- https://docs.whgazetteer.org/content/v4/data-model/contributions.html
- https://github.com/LinkedPasts/linked-places-format
- https://perio.do/technical-overview/

**Observed project friction**

The Atlas repeatedly separates spatial identity from geometry, source-native labels
from normalized identity, temporal applicability from precision, and modern proxies
from historical extents.

**Strongest current baseline**

Current spatial identity + historical jurisdiction + geometry provenance model.

**Transfer mechanism**

Use LPF/PeriodO as interchange/reference benchmarks for historical identity and period
definitions, not as owners of slavery evidence.

**Transfer risk**

LPF is place-centric and cannot represent this project's claim/evidence semantics.
PeriodO is a period-definition gazetteer, not a polity chronology truth service.
Networks and fuzzy community frames may not fit cleanly.

**Cheap falsifier**

Map one site, one changing polity and one fuzzy/community or network target to
LPF/PeriodO. Record exactly what is preserved/lost.

**Disposition:** **LEARN FROM / REUSE WHERE FIT; no replacement architecture**

---

## D5-05 — exact source selectors / annotations

**External precedent**

The W3C Web Annotation Data Model can target a specific segment of a source using
selectors and can carry motivation/provenance while remaining implementation-neutral.

Source:
- https://www.w3.org/TR/annotation-model/

**Observed project friction**

Current source relations use URL + free-text locator. PDFs, HTML pages and editions
sometimes make those locators brittle.

**Strongest current baseline**

Versioned source identity + locator string + asset hash where available.

**Transfer mechanism**

Use a structured selector only when it materially improves recoverability of a cited
passage.

**Transfer risk**

Most historical sources are not stable web resources and the repository deliberately
does not copy restricted assets. Selector machinery could be more brittle than page/
section locators.

**Cheap falsifier**

Test five existing locators across PDF page, HTML section and text-fragment cases.

**Disposition:** **PARK until locator-recovery failures recur**

---

## D5-06 — trigger-based evidence maintenance

**External precedent**

Living systematic-review guidance says continuous updating is justified only when the
question matters for decisions, new evidence is likely to emerge, and new evidence is
likely to change conclusions. Guidance also defines reasons to retire living status.

Sources:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7542271/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12018299/
- https://ebm.bmj.com/content/early/2023/03/16/bmjebm-2022-112100
- https://doi.org/10.1016/j.jclinepi.2026.112504

**Observed project friction**

D-088 correctly prevents arbitrary idle, but that does not mean every completed
historical claim should be re-searched continuously. COV-002 already found weak
maintenance-economy evidence.

**Strongest current baseline**

Immutable releases + explicit reopening triggers + bounded new-source checks.

**Transfer mechanism**

Use living-review logic to sharpen *claim-specific update triggers*: active surveillance
only where new scholarship is plausibly frequent and decision-changing.

**Transfer risk**

Historical evidence changes far more slowly and heterogeneously than clinical evidence;
scheduled searching could create archive-density bias and needless work.

**Cheap falsifier**

Apply update-trigger criteria to ten existing reviewed claims. If almost none warrant
active monitoring, keep trigger-based reopening and reject recurring surveillance.

**Disposition:** **LEARN FROM; supports current trigger-based direction rather than a new system**

---

## Cross-candidate selection

D5-01 ranks highest by expected information gain because:
- it targets a repeated correctness failure already observed in project adversarial
  review;
- it can be tested entirely on existing frozen evidence;
- a negative result confirms the current minimal packet;
- a positive result can be implemented as a tiny portable relation, not infrastructure;
- external standards provide a mature first-refusal benchmark.

D5-02 is the best follow-on if horizon-selection bias becomes the next uncertainty.
D5-03 is a low-risk interoperability benchmark but is less likely to change historical
correctness. D5-04 is valuable mainly as reuse/interchange. D5-05 lacks demonstrated
pain. D5-06 mostly validates existing trigger-based maintenance.

## Selected successor

Freeze one **inference-chain stress test** using already-researched cases with known
material corrections. Compare the current packet against a minimal CRMinf/FPO-inspired
ledger. Do not adopt CRMinf, RDF, a graph database or a new schema unless the test
demonstrates information loss in the current baseline.
