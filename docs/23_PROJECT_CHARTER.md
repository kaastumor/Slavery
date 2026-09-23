# Historical Slavery Atlas — Project Charter

## Purpose

Build a globally scoped, time-aware **historical evidence corpus and comparison method**, with a thin atlas/query surface where it demonstrably helps a reader inspect **what is claimed, where, when, on what evidence, with what uncertainty, and under which analytical layer** for slavery and related coerced-labour or dependency systems.

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

After HC-003, the working identity is **auditable evidence corpus + thin atlas**.

The durable core is:

- a curated claim/evidence corpus;
- domain methodology and adversarial fixtures;
- reviewed relational research state;
- historical geography/query logic;
- reconstructible release artifacts.

A time-aware map/query/evidence inspector is a **derived inspection surface whose value must be demonstrated**, not the project identity by default.

The current richer web/API preview is preserved as a non-canonical demonstration, not as an automatically expanding product roadmap.

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

### H2 — Value-discrimination pilot (candidate only; not authorized)

The only justified next experiment is a small comparison of three difficult historical questions across:

1. strongest boring/external workflow;
2. Atlas corpus/method without custom map interaction;
3. the smallest thin atlas/query view.

The pilot exists to decide whether the thin atlas adds practical value beyond the corpus/method, and whether either materially outperforms the strongest baseline.

Completion of HC-003 does **not** authorize this horizon automatically.

### H3 — Globally balanced evidence expansion (conditional candidate)

Resume broad research growth only if H2 demonstrates that the corpus/method has material comparative value. Continue prioritizing weak and underrepresented regions/periods before dense archive ingestion dominates.

### H4 — Public research usefulness / preservation (conditional candidate)

Only if prior horizons justify it, improve public inspection, distribution, preservation and contribution workflows. A richer application platform must be re-earned rather than assumed.

At every horizon boundary, review evidence for **and against** the thesis, compare the strongest baseline, consider whether the artifact can shrink, and explicitly choose **continue / simplify / redirect / stop** before creating the next horizon.
