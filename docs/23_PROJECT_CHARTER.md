# Historical Slavery Atlas — Project Charter

## Purpose

Build and extend the Historical Slavery Atlas as a globally scoped, time-aware **historical evidence method + compact auditable Atlas**, while requiring every increment beyond the core to earn itself against the strongest simpler baseline. Broad platform expansion remains stopped. Work proceeds through **one active priority** whose mode is chosen from discovery, execution, consolidation, review/release, or maintenance; no mode is automatic.

The project is an evidence-synthesis and data-curation system. It does not claim that one universal category can make all forms of coercion equivalent, and it does not replace specialist historical scholarship.

## Four distinct questions

### Problem

Historical evidence about slavery, slavery-like systems, coerced labour and dependency is distributed across periods, regions, source traditions and analytical vocabularies. Conventional maps, spreadsheets and narrative syntheses can make it difficult to compare place/time claims while keeping provenance, uncertainty, research coverage, legal/practice distinctions and changing historical geography visible.

### Contribution

The project’s claimed contribution is **not** “a map plus a database.” It is a traceable comparison layer that can keep unlike evidentiary dimensions separate while still allowing place/time inspection across a global corpus.

That contribution is only justified where it materially improves on the strongest simpler workflow in:

- traceability;
- temporal/spatial uncertainty;
- distinction between unknown / inconclusive / negative;
- separation of law, practice, participation, coverage and geometry;
- reproducibility;
- comparison without false equivalence;
- public inspectability.

### Project / product form

The best-supported project form after R1 and EXP-02 is:

> **portable reviewed evidence core + replaceable Atlas/map/table views**

The project remains the **Historical Slavery Atlas**. “Atlas” describes a geographic/time-aware inspection and publication mode; it does not require the historical evidence model to be owned by a bespoke web application.

The durable project contribution currently lies in:
- domain methodology and adversarial fixtures;
- bounded proposition / abstention discipline;
- claim/source/version provenance;
- temporal/spatial inference guards;
- source-family dependency;
- research-state / non-absence semantics;
- preserved corpus/research examples and immutable historical releases;
- reproducible audit/release history.

The legacy web/API preview and thin-view experiments remain preserved demonstrations rather than the product roadmap.

H2 and COV-004 weakened bespoke-interface advantage. R1 preserved the tiered evidence/release method. EXP-02 then showed that the frozen R1 safety/reconstructibility contract survives in a package manifest + flat target/source tables + optional Markdown packets.

That result changes the default architecture boundary, not the canonical historical schema.

### Implementation architecture

PostgreSQL/PostGIS remains valid research/curation infrastructure for relational integrity, imports, provenance, geometry, review state and release reconstruction.

MapLibre, APIs, JSON/GeoJSON, static tables and the current web stack are replaceable presentation/serving choices.

The preferred boundary is now:

> **reviewed research state → immutable portable evidence package → one or more presentation adapters**

No implementation technology defines the project’s contribution. A map, API or web application must consume the evidence contract rather than silently become its owner.

EXP-02 does not authorize schema migration, database deletion, or a CSV-first rewrite.

## Current central question

Can a portable, auditable historical evidence core support useful place/time inspection and comparison—through maps or other views—better than the strongest ordinary workflow **without manufacturing false precision, false absence, false equivalence, or false territorial generalization**?

## North star

A user should be able to select a place/time and understand the strongest defensible current atlas claim, its scope and limits, the relevant evidence and contrary evidence, and the distinction between:

- territorial practice;
- legal/state regime;
- external/network participation;
- research coverage;
- historical geometry.

The map is one navigation and comparison surface over the evidence system. It is not itself the source of historical truth, and no presentation adapter may strengthen the underlying evidence claim.

## Strongest boring baseline

The project must justify its complexity against a competent simpler workflow:

1. specialist literature + source notes;
2. a spreadsheet/ordinary relational table of claims and citations;
3. a conventional GIS layer or static map;
4. ordinary search or a strong general-purpose model used competently over those materials;
5. small scripts/notebooks where needed.

Do not cripple this baseline so the atlas can “win.”

A feature earns its place only if it materially improves traceability, historical scope, uncertainty handling, reproducibility, comparison, or public usability over that baseline. Integration novelty by itself is not a contribution.

## Success condition

The project succeeds if it can publish useful global historical views in which:

- every substantive public claim is traceable to exact evidence/source versions;
- unknown, disputed, researched-inconclusive and absent are not silently conflated;
- law, practice, participation, coverage and geometry remain analytically separable;
- temporal and spatial uncertainty survive the map/query path;
- large source corpora can be ingested reproducibly without archive density becoming prevalence;
- releases remain reconstructible;
- real users can gain findings, confirmations, contradictions or useful uncertainty that the simpler baseline makes materially harder to obtain.

## Failure / kill conditions

The project should simplify, redirect or stop if repeated evaluation shows that:

- the map mainly re-visualizes information already easier to understand in ordinary sources/tables;
- cross-period comparison systematically creates false equivalence or false precision;
- provenance cannot remain inspectable at useful scale;
- maintenance/infrastructure burden materially exceeds research/user value;
- public presentation cannot communicate uncertainty without misleading users;
- the strongest boring baseline repeatedly reaches practical parity on the project’s claimed contribution;
- the demonstrated value survives in a substantially smaller artifact and the larger system adds little.

Failure of a thesis is valid project evidence.

## Invariants

The existing canonical methodology remains binding unless explicitly superseded. In particular:

- archive/document/voyage density is not territorial prevalence;
- missing evidence is not absence;
- law is not practice;
- external participation is not territorial practice;
- actor nationality/political identity requires independent evidence;
- raw/source-native values and identifiers remain recoverable;
- historical geometry and slavery/coercion evidence are separate;
- draft/reviewed/published/canonical states remain separate;
- canonical releases are immutable;
- comparison does not imply equivalence.

## Explicit non-goals

- ranking societies by a single slavery score;
- automatically inferring P-levels from record counts;
- generating novel historical theory where specialist scholarship already resolves the question;
- replacing all specialist historical GIS with one global source;
- adopting infrastructure because it is fashionable or conventional;
- maximizing record count, issue count, feature count or commit count;
- making the public preview silently become the canonical historical release;
- preserving a larger architecture merely because it has already been built.

## Strategic horizons

The completed horizon descriptions below preserve decisions at their original
boundaries. Their historical idle/authorization statements do not schedule current
work. **D-096** governs current continuation; root `BACKLOG.md` alone owns the current
priority and mode. Discovery execution follows
`docs/discovery/DISCOVERY_EXECUTION.md` only when discovery is the selected mode.

Horizons are hypotheses, not promises.

### H0 — M1 methodology hardening (completed)

M1 (#100) attacked the original semantics, returned REVISE, corrected the displaced overloads, and survived the integrated re-attack. P0–P4 is no longer the target universal comparative ordinal; the accepted prototype keeps evidence, historical structure, workflow/outcome, temporal applicability/precision and spatial locus/extent separable.

### H1 — Semantic/geography integration (completed)

M2 (#116) integrated only the semantics that survived M1, resolved Cliopatria calendar/RELATION behavior, ingested the complete pinned corpus as raw geography infrastructure, and proved selected-year behavior in the real relational architecture without altering v0.6.1 or silently changing the current preview.

Its integrated adversarial gate #122 passed only after corrective cycles. HC-003 then chose **CONTINUE + SIMPLIFY** and removed the full application platform from default status.

### H2 — Value-discrimination pilot (completed)

H2 / #146 compared three difficult historical questions through:
1. strongest competent ordinary research workflow;
2. Atlas corpus/method without bespoke map interaction;
3. smallest dependency-free thin query/visual artifact.

The setup was adversarially revised before research; the result was adversarially challenged and the thin view repaired before final evaluation.

Result:
- corpus/method materially improved the baseline in 1/3 cases;
- thin view materially improved the corpus/method in 0/3 cases;
- the pre-registered two-case threshold therefore failed.

HC-004 / D-063 chose **STOP ACTIVE ATLAS EXPANSION; PRESERVE METHOD/CORPUS/AUDIT ARTIFACTS**.

### H3 — Continuation modes after D-096

The project does **not** require another experiment after every bounded horizon.

At a boundary, compare the next justified **mode of work** against the project goal:

1. **discovery** — a material method/product/representation decision is still uncertain;
2. **execution** — an accepted method can now be applied to bounded historical work;
3. **consolidation** — accumulated batches/claims/sources/review states need reconciliation;
4. **review/release** — a coherent candidate is ready for the applicable gates;
5. **maintenance** — a released/settled scope needs correction, preservation or trigger-based upkeep.

Keep WIP at one active priority. Completion may legitimately lead to any mode above,
including no new work when no mode is justified.

Discovery requires a discriminating uncertainty. Execution does not need to re-prove a
method already accepted for the same declared scope. Reopen settled methods only for a
new failure, changed task, consequential scale pressure, changed evidence, or concrete
consumer/release need.

Root `BACKLOG.md` owns the current mode and priority.

### H4 — Preservation as a capability, not a resting strategy

Preservation/reconstructibility remains mandatory for releases, evidence packets and prior experiment state.

It is not the project's default work mode. When no delivery task is justified, prefer a bounded research/discovery experiment over passive preservation if that experiment can materially change belief.

Do not manufacture infrastructure, features, public-product work or external recruitment merely to remain active.

### Post-H2 bounded value experiment — COV-001 (completed)

COV-001 / #148 tested a distinct thesis without reopening Atlas expansion: whether a plain, systematically assembled global place/time coverage corpus has reusable value in its own right.

Result: **NARROW SURVIVE.**

After a deterministic sample, 25-cell research corpus, fixed queries, negative controls and a result adversary:
- 4/6 global coverage tasks retained material value;
- the gain came from explicit layer boundaries and research-coverage/gap state;
- ordinary matrix presentation reached parity for simple overview;
- specialist narrative remained superior for deep interpretation;
- SlaveVoyages remained superior for voyage-level quantitative analysis.

The surviving artifact is a **flat auditable coverage corpus**, not a new product architecture.

This does not change D-063: the former Atlas application/platform remains stopped.

COV-001 authorizes no automatic successor. At most one future bounded experiment may test whether corpus reuse/value scales faster than research, review and update cost.

### COV-002 — scale/reuse economics (completed)

COV-002 / #151 tested whether the COV-001 coverage-corpus value compounds faster than its research/review/update burden.

Result: **STOP FURTHER AUTOMATIC SCALING.**

The experiment grew the frozen research corpus from 25 to 37 rows and compared:
- full detailed coverage rows;
- a compact coverage register;
- a strong ordinary matrix.

The compact register preserved the full row's fixed-task behavior and reduced static review surface to about 60.5%, while law/practice, network/territorial and handbook-coverage reuse advantages persisted at N=37.

However, the preregistered maintenance-economy gate failed: the three material evidence updates required the same number of local review edits in compact and full forms. The full row also failed to earn its additional routine complexity.

The durable lesson, as narrowed by ADV-001 / D-068, is:
- use the compact coverage-register pattern for demonstrated cross-cell tasks;
- preserve existing full evidence artifacts for audit/research;
- do not automatically continue the tested row-by-row expansion workflow;
- do **not** treat COV-002 as a rejection of tiered, versioned, batch-curated systematic coverage in general.

At the ADV-001 boundary the broader systematic-coverage thesis remained open and untested. COV-003 subsequently tested a tiered architecture and returned TIERED SURVIVE; no successor experiment or corpus-expansion horizon is currently authorized.

### ADV-001 — completeness-inference audit (completed)

ADV-001 / #153 adversarially attacked the inference from COV-002's maintenance-gate failure to the broader claim that systematic comprehensive historical coverage is not justified.

Result: **the broad inference was too strong.**

The audit found:
- scope mismatch between COV-002's stated artifact/reuse-economics target and the broader strategic conclusion;
- a maintenance threshold that became unreachable after three neutral no-change shocks under the adopted scoring rule;
- atom-granularity sensitivity because rich source objects and bare source links counted equally;
- no direct test of batch/source-centric research, periodic/versioned maintenance, long-run scale curves or emergent reference-corpus value;
- a risk that an external-use-case-only trigger recreates demand-density bias.

D-068 therefore narrows the stop to the tested row-by-row workflow. The project remains idle and no new expansion is authorized.

### COV-003 — tiered systematic coverage architecture (completed)

ADV-001 / D-068 left open whether broad systematic coverage could be separated from deep row-by-row research.

COV-003 / #155 tested that architecture.

Result: **TIERED SURVIVE; STRONG SURVIVE rejected.**

The viable experimental form is:
- C0 target/research-state registration without slavery inference;
- C1 compact researched coverage for selected targets;
- selective C2 depth when a predefined ambiguity/risk trigger earns it;
- immutable/as-of releases;
- explicit source-quality and source-dependency review state.

Evidence:
- 24 C0 targets can be represented without treating unresearched as absence;
- 6 identity probes exposed one mismatch and one ambiguity before subject interpretation;
- C1 recovered 4 bounded-supported and 8 researched-inconclusive outcomes;
- shared-source reuse increased structurally from 1.00 to 2.20, but every C1 target still needed target-specific follow-up, so strong batch-economy claims fail;
- C2 materially improved 2/3 escalated targets;
- systematic selection reached targets with no direct Cambridge/Palgrave treatment;
- shared-source correction risk can be localized through source-to-row dependencies.

The architecture is therefore worth preserving as a research method. It is not evidence that comprehensive global ingestion is currently affordable or justified.

No successor horizon is authorized by COV-003.

### COV-004 — final architecture falsification gate (completed)

COV-004 / #157 attacked COV-003 rather than extending it by momentum.

It tested:
- C1/C2 false-negative escalation behavior;
- non-polity coverage;
- real publication-time evidence updates;
- the Atlas concept against a competent conventional map + register.

Result: **METHOD SURVIVE.**

The research method survives with one additional guard:
- source-quality failure itself must trigger deeper review/escalation.

The claim architecture also survived sites, institutions, networks and fuzzy community/region targets without forcing polity semantics.

A 2015→2016–2026 time-split produced three genuine evidence events out of six frozen rows, validating immutable/as-of revision mechanics.

The bespoke Atlas evidence inspector did not materially outperform the competent conventional map/register baseline on any of four frozen map tasks.

This does **not** remove geographic presentation from the project. The strongest boring baseline is itself a small historical atlas.

The best-supported project form after COV-004 is therefore:

> **tiered historical evidence programme + ordinary map/GIS navigation surface**

rather than:
> custom Atlas application/platform.

COV-004 closes the architecture-experiment sequence. Any next horizon should be a real research/release programme or preservation, not COV-005 by default.

### R1 — first real systematic coverage release programme (active; MVP delivery stage)

After COV-004, the sponsor explicitly authorized the project to graduate from architecture experiments into a real bounded research/release programme.

R1's project form is:

> **hardened tiered evidence core + systematic sample release + boring Atlas/map surface**

R1 does not reactivate the former full-platform roadmap.

Binding constraints:
- Core Contract v1 is empirical and fixture-backed;
- C0/C1/C2 are research/release tiers, not historical intensity;
- release ceilings are not quotas;
- candidate release is distinct from independent/public review;
- new features must emerge from repeated real research/release friction;
- no successor release is automatic.

R1 subject research is now frozen at 19 reviewed C1 rows. R1.6 release QC passed with explicit limitations.

D-080 defines R1.7 as the MVP delivery stage:

> **immutable R1 candidate package + neutral world map + explicit geometry/research states + compact evidence register**

After the technical MVP gate, feature ideas return to bounded discovery experiments rather than automatic implementation.

Decisions: D-073, D-080.  
Programme: `programmes/r1/`.  
MVP plan: `docs/mvp/v0.1-plan.md`.

At every horizon boundary, review evidence for **and against** the thesis, compare the strongest baseline, consider whether the artifact can shrink, and explicitly choose **continue / simplify / redirect / stop** before creating the next horizon.
