# Historical Slavery Atlas — Project Charter

## Purpose

Preserve the Historical Slavery Atlas's globally scoped, time-aware **historical evidence method, curated artifacts and audit trail** after H2 failed to demonstrate enough repeatable value to justify continued active Atlas expansion. Future development is trigger-bound rather than assumed.

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

HC-003 narrowed the hypothesis to **auditable evidence corpus + thin atlas**. H2 then tested that hypothesis and did not meet the pre-registered project-value threshold.

The durable project result is therefore:

- domain methodology and adversarial fixtures;
- claim/source/version provenance conventions;
- preserved corpus/research examples and immutable historical releases;
- historical geography/query experiments and tested failure cases;
- reproducible audit/release history;
- the H2 baseline/corpus/thin-view comparison, including its negative result.

The current web/API preview and thin-view experiments are preserved demonstrations, not an active product roadmap.

No active Atlas development horizon exists after HC-004 / D-063.

### Implementation architecture

PostgreSQL/PostGIS, MapLibre, GitHub Actions, Supabase/API serving, JSON/GeoJSON and the current web stack are implementation choices. They remain contingent.

No implementation technology defines the project’s contribution. If a materially smaller artifact preserves the demonstrated contribution, shrinking is a valid outcome.

## Current central question

Can the atlas make historically diverse evidence genuinely more inspectable and comparable than a conventional map, spreadsheet, source catalogue, or ordinary narrative synthesis **without manufacturing false precision, false absence, false equivalence, or false territorial generalization**?

## North star

A user should be able to select a place/time and understand the strongest defensible current atlas claim, its scope and limits, the relevant evidence and contrary evidence, and the distinction between:

- territorial practice;
- legal/state regime;
- external/network participation;
- research coverage;
- historical geometry.

The map is a navigation and comparison surface over the evidence system. It is not itself the source of historical truth.

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

### H3 — No active research-expansion horizon

The former globally balanced evidence-expansion candidate is **not authorized**. More records are not a remedy for a failed value threshold.

It may be reconsidered only after explicit new authorization tied to a concrete value hypothesis and bounded cost model. A real external research/user need or simpler-baseline failure is one valid trigger; a preregistered methodological objective such as bias-resistant systematic coverage may also be valid if it tests a workflow not already rejected by COV-002.

### H4 — Preservation, not a product horizon

Preservation is the resting state, not a new feature roadmap.

Maintain reconstructibility, security and integrity of the existing artifacts when needed. Do not create public-product, contribution-platform or infrastructure work merely to keep the project active.

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

The broader systematic-coverage thesis remains open and untested. No successor experiment or corpus-expansion horizon is currently authorized.

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

### COV-003 — tiered systematic coverage architecture (active bounded experiment)

ADV-001 / D-068 established that COV-002 stopped only the tested row-by-row workflow, not every possible systematic-coverage architecture.

COV-003 / #155 is explicitly authorized to test one alternative:
- broad C0 target/research-state registration without slavery inference;
- compact C1 evidence only for a frozen research subset;
- selective C2 depth only when a preregistered escalation rule earns it;
- source-centric batch research;
- versioned/as-of maintenance rather than continuous mutation.

The experiment uses 24 new targets but researches only 12 at C1 and at most 3 at C2. Record count itself is not a success metric.

No result automatically authorizes comprehensive ingestion or the former Atlas product.

At every horizon boundary, review evidence for **and against** the thesis, compare the strongest baseline, consider whether the artifact can shrink, and explicitly choose **continue / simplify / redirect / stop** before creating the next horizon.
