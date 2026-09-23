# COV-001 — Revised Coverage-Value Protocol

**Issue:** #148  
**Setup adversary:** `02_SETUP_ADVERSARY.md` → **REVISE**  
**State:** setup valid; historical execution begins only after the sample JSON is generated and committed

## Central question

Can a **small, systematically assembled historical coverage corpus** provide practical value that the strongest combination of global handbooks, specialist resources and ordinary notes does not provide directly?

The tested value is:
- coverage visibility;
- gap/uncertainty visibility;
- provenance recovery;
- cross-place/time retrieval;
- avoiding repeated reconstruction.

It is **not**:
- better historical interpretation than specialists;
- prettier mapping;
- a new database platform;
- proof of global completeness.

## Experimental artifact

Use the smallest possible artifact:

- one plain CSV or JSON table for machine-readable rows;
- one human-readable Markdown profile/evidence log;
- source links/locators;
- no PostgreSQL migration;
- no public API;
- no map/frontend;
- no new dependency/service.

If value survives, it belongs to the **corpus concept**, not automatically to the Atlas architecture.

## Sample

### Primary frame — 24 deterministic polity-year strata

Use `select_sample.py` unchanged.

Exact source pin:
- Cliopatria commit `ad28a691b7c07c1fca89d0e0636d324667d2a258`
- SHA-256 `d01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370`

Four source-native anchor years:
- 500 BCE
- 500 CE
- 1300 CE
- 1800 CE

Six coarse sampling sectors A–F.

The generated sample is frozen before slavery research.

At least 18/24 strata must be valid. Empty strata remain sampling gaps and are never converted into historical-absence evidence.

### Frame-bias challenge — 4 non-polity contexts

Fixed before research:

- NP-01 — Central Australian interior, c. 1800 CE
- NP-02 — New Guinea Highlands, c. 1800 CE
- NP-03 — North American Great Plains, c. 1300 CE
- NP-04 — Upper Amazon / western Amazonia, c. 1300 CE

These are deliberately broad research contexts. Exact local scope must be tightened by scholarship during research without pretending a modern region is one historical society.

They test whether the corpus can honestly represent:
- non-state/stately mismatch;
- poor written-source survival;
- archaeology/ethnohistory;
- terminology mismatch;
- researched-inconclusive outcomes.

## Baseline conditions

Three baseline forms are legitimate:

### B0 — global-resource baseline
Cambridge + Palgrave + relevant specialist structured resources.

### B1 — strongest ordinary research
Specialist literature/search + ordinary notes/table/GIS/general model.

### B2 — plain ordinary matrix
A competent spreadsheet/CSV with sample ID, short conclusion and citations, but **without** the project's special coverage/provenance fields.

B2 prevents the experiment from claiming that “having rows in a table” is itself novel.

## Research rules

For every polity or non-polity cell:

1. identify what the global syntheses actually cover;
2. identify specialist scholarship for the bounded target;
3. check contrary/limiting interpretation;
4. use primary/source-native evidence only for bounded facts where helpful;
5. separate:
   - territorial/social practice;
   - legal/state regime;
   - external/network participation;
   - research coverage;
6. preserve classification/terminology problems;
7. preserve temporal/spatial uncertainty;
8. stop with `researched_inconclusive` or `insufficient_access` rather than filling a gap by inference.

### Source budget

Default maximum:
- 2 global synthesis entries;
- 4 specialist secondary items;
- 2 primary/source-native/structured-data items.

A conflict may justify more; the row must say why.

## Coverage row

Minimum fields:

- `cell_id`
- `frame` = polity | non_polity_challenge
- `anchor_year`
- sampled target / region label
- `coverage_outcome`:
  - bounded_supported
  - researched_inconclusive
  - materially_disputed
  - insufficient_access
- strongest bounded proposition
- strongest prohibited/unsupported proposition
- territorial practice summary
- legal/state summary
- network/participation summary
- terminology/category qualification
- temporal scope/precision
- evidence locus
- inference extent
- evidence classes
- contrary/limiting evidence
- Cambridge coverage = direct | adjacent | none | inaccessible
- Palgrave coverage = direct | adjacent | none | inaccessible
- specialist structured-data relevance
- language/access limitation
- sources/locators
- unresolved issues

No historical-absence state. No P0–P4.

### Direct / adjacent / none rule

For Cambridge/Palgrave:

- **direct** — sampled target/society and relevant period are substantively treated;
- **adjacent** — region/period treatment materially helps but the target is not itself treated;
- **none** — no usable target-level context found in the resource;
- **inaccessible** — coverage cannot be assessed because relevant material cannot be inspected.

## Frozen user-facing tasks

The six global tasks remain:

1. What is the strongest defensible sampled place/time overview, including cells that must remain unresolved?
2. Where does legal/state evidence diverge from what can be said about practice?
3. Where is participation/network evidence insufficient for territorial inference?
4. Where do terminology/category problems materially limit direct comparison?
5. Which cells receive direct/adjacent/no usable global-handbook coverage and require specialist follow-up?
6. Which cells remain disputed, inconclusive or access-limited after the source ladder, and why?

These tasks are frozen before research.

## Negative controls

### N1 — deep specialist context
After the sample is frozen, deterministically choose one valid cell. Ask one narrow historiographical why/how question based on its literature.

Expected:
specialist narrative >= coverage index.

### N2 — specialized quantitative data
Ask a bounded SlaveVoyages question about voyage/traffic detail inside its documented scope.

Expected:
SlaveVoyages > coverage index.

A mini-index “win” on these controls triggers adversarial review for overclaim/baseline failure.

## Evaluation procedure

Where practical, use isolated fresh runs:

### External/baseline evaluator
Receives:
- frozen sample IDs;
- task;
- strongest baseline resources;
- no mini-index.

### Index evaluator
Receives:
- frozen mini-index;
- task;
- may follow index source links;
- no hidden research notes.

If fresh-run isolation is unavailable, mark the evaluation non-independent.

### Probe states

- direct
- traceable
- reconstructive
- unavailable
- misleading

Judge:
- coverage-state visibility;
- provenance;
- abstention/uncertainty;
- law/practice/participation separation;
- cross-cell aggregation;
- temporal/spatial scope;
- number of new external source retrievals.

Lookup reduction alone is never sufficient.

## Material-value gate

A query shows material corpus value only if:
- at least two **information** probes improve over B0/B1/B2;
- improvement is not merely formatting;
- no critical probe becomes misleading.

COV-001 survives only if:
- >= 3 of 6 global tasks show material value;
- gains span >= 2 mechanisms;
- non-polity challenge cells remain representable without false state/absence inference;
- N1 and N2 behave as negative controls;
- result adversary finds no fatal sampling/baseline bias.

## Interpretation of outcomes

### Fail
Global handbooks + ordinary research/matrix are materially as useful.

Action:
return to **IDLE / PRESERVATION**. Preserve the experiment.

### Narrow survive
The coverage corpus helps, but only as a plain structured reference.

Action:
at most one further bounded test of corpus-scale reuse/maintenance. No Atlas platform revival.

### Strong survive
The sampled corpus materially improves several real cross-place/time tasks while preserving uncertainty and provenance.

Action:
still only one bounded next corpus experiment. “Build the complete world corpus” remains unauthorized until scale/maintenance is tested.

## Hard exclusions

COV-001 cannot authorize:
- M2 production migration;
- H3 bulk research;
- new public Atlas release;
- frontend/map expansion;
- vector/search/RAG/graph infrastructure;
- contributor platform;
- automatic research workers;
- a claim of historical completeness.
