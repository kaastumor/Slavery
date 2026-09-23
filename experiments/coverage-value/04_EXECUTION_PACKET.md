# COV-001 — Execution and Evaluation Packet

**Issue:** #148  
**Protocol:** `03_PROTOCOL_REVISED.md`

This file exists so the experiment can be executed from repository state without reconstructing hidden chat context.

## Stage A — freeze sample

1. Obtain the exact pinned `cliopatria.geojson.zip`.
2. Run:

```bash
python experiments/coverage-value/select_sample.py \
  cliopatria.geojson.zip \
  --output experiments/coverage-value/sample.json
```

3. Verify:
   - source SHA-256 passes;
   - feature count = 13,765;
   - `viable=true`;
   - >=18 selected polity-year cells.
4. Commit `sample.json`.
5. Do not research slavery/coercion before that commit.

If `viable=false`, stop and revise the sampling frame in a new setup-adversary delta.

## Stage B — create frozen research rows

For each selected cell plus NP-01..NP-04:

1. Copy `coverage_row_template.json`.
2. Research under the source ladder and source budget.
3. Do not infer absence.
4. Leave unsupported fields empty/qualified.
5. Store one JSON row per cell under:
   `experiments/coverage-value/rows/<cell_id>.json`
6. Maintain one human-readable evidence log:
   `experiments/coverage-value/05_EVIDENCE_LOG.md`

After every row is complete, combine them into a plain:
- `mini_index.json`
- `mini_index.csv`

No database import.

## Stage C — freeze ordinary-matrix baseline

Create a competent plain comparison artifact using only:
- cell ID;
- target/year;
- concise conclusion;
- ordinary citation list.

It may use normal spreadsheet/table organization but not the special coverage/layer fields.

Path:
`experiments/coverage-value/06_B2_ORDINARY_MATRIX.md`

Purpose:
prevent the coverage corpus from “winning” merely because it is tabular.

## Stage D — evaluate six fixed user tasks

### Isolation rule

Preferred:
- run external/baseline and index evaluations in separate fresh sessions/agents;
- do not expose the mini-index to the baseline evaluator.

If this cannot be done, mark the comparison `non_independent`.

### Baseline evaluator prompt

Use exactly this intent:

> You are evaluating whether the strongest ordinary historical-research workflow can answer a fixed global coverage question without a preassembled project index. You have the frozen COV-001 sample and may use Cambridge World History of Slavery, Palgrave Handbook of Global Slavery throughout History, Enslaved.org, SlaveVoyages, specialist scholarship, ordinary tables/GIS/search and a strong general-purpose model. Preserve unknown/inconclusive/disputed states. Do not infer territorial practice from trade/network data or legal status. Answer the assigned fixed task, record every external source retrieval, and classify each evaluation probe as direct / traceable / reconstructive / unavailable / misleading. Do not use the COV-001 mini-index.

### Index evaluator prompt

> You are evaluating a frozen COV-001 coverage index. Answer the assigned fixed task from the mini-index first. You may follow explicit source links only when the index itself says verification is required. Preserve all abstentions and scope limits. Record external source retrievals. Classify each evaluation probe as direct / traceable / reconstructive / unavailable / misleading. Do not silently improve the frozen rows.

### Fixed tasks

Use Q1–Q6 verbatim from `03_PROTOCOL_REVISED.md`.

For every task record:

```text
task:
condition: B0/B1/B2 or index
independence: independent | non_independent
coverage_state_visibility:
provenance:
uncertainty_abstention:
layer_separation:
cross_cell_aggregation:
temporal_spatial_scope:
new_external_retrieval_count:
misleading_failure:
notes:
```

## Stage E — negative controls

### N1 deep specialist context

Selection:
- take all valid deterministic polity sample cells;
- sort by SHA-256 of `COV-001-N1|cell_id`;
- choose first cell whose coverage outcome is not `insufficient_access`.

Question selection:
- derive one narrow why/how historiographical question from the first specialist secondary source in that cell;
- freeze the question before evaluation.

Expected:
specialist narrative >= mini-index.

### N2 SlaveVoyages specialized-data control

Fixed question:

> For trans-Atlantic voyages disembarking enslaved people in Jamaica between 1750 and 1800, what does SlaveVoyages allow a researcher to inspect or quantify that a global coverage index should not pretend to replace?

This is a capability comparison, not a request to turn voyage counts into territorial prevalence.

Expected:
SlaveVoyages > mini-index on voyage-level/quantitative detail.

## Stage F — result adversary

Attack at minimum:

- sample-frame bias;
- non-polity adequacy;
- handbook coverage coding;
- language/access bias;
- same-model contamination;
- index-shaped task bias;
- ordinary-matrix parity;
- curation overhead;
- stale-source maintenance;
- absence inference;
- positive-result scope creep.

Every finding gets:
survives / revise / reject / park / experiment.

## Stage G — decision

Apply the pre-registered gate.

Possible project dispositions:

- **FAIL / return to preservation**
- **NARROW SURVIVE / one further bounded corpus-scale test**
- **STRONG SURVIVE / one further bounded corpus-scale test**

There is intentionally no “restart Atlas platform” outcome.
