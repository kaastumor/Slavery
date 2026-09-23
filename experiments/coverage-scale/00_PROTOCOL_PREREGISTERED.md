# COV-002 — Scale / Reuse Economics Protocol

**Issue:** #151  
**Authorized:** 2026-09-23  
**Base main:** `41ee6bf05de8332e1e1645a1d60ad6f60dc1a34d`  
**State:** setup only until adversarial review passes  
**Canonical historical release:** v0.6.1 unchanged

## Question

COV-001 established that a flat coverage corpus can add reusable cross-cell value.

COV-002 asks:

> Does that value grow faster than the research, review and update burden when the corpus becomes materially larger?

This is the final automatically permitted corpus-scale experiment under D-065. It does not authorize bulk global research.

## What is being compared

The experiment deliberately compares **three boring artifacts**.

### F — full coverage row

The complete COV-001 row shape:
- outcome;
- strongest bounded / unsupported propositions;
- practice;
- law/state;
- network;
- terminology;
- temporal scope;
- evidence locus / inference extent;
- evidence classes;
- limiting evidence;
- handbook coverage;
- access/language limits;
- full source direction/role metadata;
- unresolved issues.

### R — compact coverage register

Only the fields needed by the value that survived COV-001:

- cell ID / target / anchor;
- coverage outcome;
- one bounded conclusion;
- one required abstention;
- law/practice divergence note, if material;
- network/territorial-inference note, if material;
- Cambridge coverage;
- Palgrave coverage;
- unresolved/gap reason;
- source links;
- access/language warning.

No full ontology, evidence-direction table or duplicated prose.

### M — strongest ordinary matrix

A competent conventional table:
- cell ID;
- target/year;
- research status;
- concise conclusion;
- caveat/notes;
- citations.

M is allowed to learn from COV-001. It is not frozen in a deliberately weaker form.

## Scale cohort

COV-001 has 25 researched cells.

COV-002 adds **12 deterministic polity-year cells**, producing 37 researched cells if all are viable.

The expansion cohort is selected from the same pinned Cliopatria source without reference to slavery evidence.

### Selection rule

1. Reuse COV-001's four anchor years and six sectors.
2. Consider only strata with at least two eligible polity candidates.
3. Rank the eligible strata by SHA-256:
   `COV-002-STRATUM|cell_id`
4. Take the first 12 strata.
5. Within each selected stratum, reproduce the COV-001 candidate ranking but select **rank 2** rather than rank 1.
6. Preserve source-native row ordinal/name/interval/IDs.
7. If fewer than 12 rank-2 cells can be produced, stop and revise before historical research.

This creates a larger cohort without choosing historically famous slavery cases.

No additional non-polity expansion is added. The four COV-001 non-polity challenge rows remain part of the combined corpus and therefore remain visible in reuse tests.

## Research rule for 12 new cells

Use the same bounded source ladder and source budget as COV-001.

Allowed outcomes:
- bounded_supported
- researched_inconclusive
- materially_disputed
- insufficient_access

No historical-absence state. No P0–P4.

The 12 rows are researched once into F. R and M are mechanically derived from the same frozen evidence; neither gets better sources.

## Review-surface proxy

COV-002 does not pretend field count equals human hours.

It records an observable maintenance proxy:

- populated scalar fields requiring review;
- source/citation objects requiring review;
- manually written cross-field notes;
- duplicate propositions across artifacts;
- files/artifacts requiring synchronization.

For each representation compute:
- median review atoms per row;
- total review atoms at 25 and 37 rows;
- growth factor from 25→37.

This is **review surface**, not elapsed time.

## Reuse tasks

Run at corpus sizes:
- N=25 (COV-001 only);
- N=31 (first 6 new cohort rows);
- N=37 (all 12 new rows).

Fixed tasks:

### T1 — law/practice divergence
Which cells have legal/state evidence that differs materially from what can be asserted about practice?

### T2 — network/territorial boundary
Which cells contain network/trade/captive-movement evidence that must not substitute for territorial-practice inference?

### T3 — global-handbook coverage
Which cells are direct / adjacent / none / inaccessible in Cambridge and Palgrave?

### T4 — unresolved research
Which cells remain inconclusive, disputed, access-limited or structurally unsafe, and why?

### T5 — bounded overview
Give the research outcome and strongest bounded proposition for every cell.

### T6 — source recovery
For each answer in T1–T4, can the decisive source trail be recovered without reopening general web/library search?

## Reuse work units

For each artifact/task record:
- rows that must be inspected;
- fields/notes that must be interpreted;
- source links that must be opened after the task begins;
- manual cross-row classifications created during the query;
- critical misleading omissions.

A direct filter over an explicit field may inspect only matching rows plus the field index/list used to identify them. A prose matrix requiring every row to be reread counts every row inspected.

Do not convert these counts into minutes.

## Maintenance shock

After the 37-row corpus is frozen:

1. Deterministically select six researched rows by SHA-256:
   `COV-002-UPDATE|cell_id`
2. For each selected row, perform **one bounded new-evidence search**:
   - seek one genuinely additional specialist source relevant to the existing claim;
   - record whether it supports, qualifies, challenges or adds no material information.
3. Freeze the update packet before modifying any representation.
4. Apply the same update packet independently to F, R and M.

Record:
- source retrievals;
- row fields/notes touched;
- citations touched;
- downstream task answers that become stale;
- whether the artifact makes the changed inference boundary explicit;
- whether an update can be applied locally or requires broad rereading.

A no-change update is valid and must remain in the sample.

## Negative controls

### N1 — specialist depth
A deterministic row receives one narrow why/how question. Specialist narrative should remain at least as good as F/R/M.

### N2 — specialized quantitative data
SlaveVoyages remains the benchmark for voyage-level quantitative questions.

### N3 — single-cell reading
For one deterministic row, ask only "what can we responsibly say here?" M should be at least competitive with F/R. If full structure wins merely because the task asks for every field, the control fails.

## Evaluation

States:
- direct
- traceable
- reconstructive
- unavailable
- misleading

No aggregate aesthetic score.

### Value-retention test

R is considered to retain COV-001's demonstrated value if, across T1–T6 at N=37:
- it matches F's information state on at least 5/6 tasks;
- no critical task becomes misleading;
- it preserves direct source recovery for T1–T4.

### Economy test

R is materially cheaper in review surface if:
- median review atoms/row <= 70% of F;
- total review atoms at N=37 <= 70% of F;
- maintenance shocks touch <= 70% as many review atoms as F in at least 4/6 update rows;
- no additional general source search is required solely because R dropped a field.

### Scaling test

Coverage-corpus value is considered to compound rather than merely accumulate if:
- at N=37, at least 3/4 surviving COV-001 cross-cell tasks (T1–T4) still show a material reuse advantage over M;
- the advantage does not shrink from N=25 to N=37 on more than one task;
- the number of rows requiring rereading in M grows materially with N while R/F remain direct;
- maintenance shocks do not create widespread stale/contradictory outputs.

## Outcomes

### STOP / preservation
Use if:
- M catches up on most tasks;
- reuse advantage disappears at N=37;
- maintenance burden grows roughly with value;
- or source/update cost dominates.

### REDIRECT — compact coverage register
Use if:
- R retains >=5/6 F task performance;
- R meets the review-surface economy gate;
- R retains scale/reuse advantage over M;
- F shows no repeatable information-quality gain sufficient to justify its extra surface.

### NARROW SUSTAIN — full coverage corpus
Use only if:
- F materially outperforms R on at least two independent tasks or maintenance shocks;
- those gains concern correctness/provenance/uncertainty, not richer prose;
- F still satisfies scaling value over M.

No outcome authorizes the old Atlas platform or unrestricted research expansion.

## Hard exclusions

- no canonical release changes;
- no DB/API/UI/map work;
- no automated mass research;
- no literal completeness claims;
- no archive/source count → practice intensity;
- no inference of absence from missing/inconclusive research.
