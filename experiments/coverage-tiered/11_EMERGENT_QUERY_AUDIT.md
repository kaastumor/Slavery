# COV-003 — Emergent Query Audit

**Issue:** #155  
**Status:** exploratory only; cannot rescue a failed core architecture.

Candidate questions were generated only after C0/C1/C2 were frozen. A counted question must:
- require >=8 targets and >=2 batches/cohorts;
- not duplicate COV-001/002 T1–T6;
- use existing experiment metadata/evidence only;
- produce a falsifiable answer;
- alter a methodology or research-priority decision;
- not merely report one field count.

## EQ-1 — Does historiographic coherence predict shared-source reuse better than coarse map-sector membership?

### Why this question exists only after COV-003

COV-003 has three batches selected by the same neutral stratum method but with very different internal historical coherence:

- `-500:F`: four contemporaneous eastern-Chinese states;
- `-500:E`: four contemporaneous Mahājanapada targets;
- `1300:E`: Kathmandu, Chandela, Hanthawaddy and Myinsaing — same coarse longitude sector and anchor, but different historiographies.

### Answer

- `-500:F`: two shared specialist sources materially inform 4/4 C1 cells.
- `-500:E`: two shared specialist sources materially inform 4/4 C1 cells.
- `1300:E`: no shared specialist source safely informs >=3/4.

**Falsifiable pattern in this sample:** source reuse tracks historical/historiographic coherence more closely than coarse geographic sector alone.

### Methodological consequence

If a later batch experiment is ever authorized, it should preregister batches using an independent historical/source-domain coherence rule rather than longitude sector alone.

This cannot be reconstructed directly from an ordinary row matrix without rebuilding source-to-cell dependencies and batch provenance.

**Counts as nontrivial emergent query: YES.**

---

## EQ-2 — Does shared-source reuse create correlated error/review risk?

### Cross-target evidence

The `-500:F` batch reused the same early-China packet across Yan, Zhu, Lu and Cao.

C2 escalation of Zhu found that the compact C1 wording was temporally too loose:
- the strongest concrete legal material in one shared source is later Qin evidence;
- earlier Zhou status terminology is less secure than a generic “slavery established” phrase suggests.

Because the shared framing fed four rows, the correction is not logically Zhu-only.

### Answer

**Yes in this batch.** One shared-source framing issue creates a next-release review dependency across all four linked C1 rows.

### Methodological consequence

Source reuse must be represented as a dependency graph:

`source packet -> dependent rows -> review propagation`

Source-centric batching therefore has two sides:
- fewer unique sources / more reuse;
- correlated revision risk.

This changes the architecture: batch source dependencies must be first-class review metadata if systematic coverage grows.

An ordinary row matrix with copied citations does not directly expose this propagation structure.

**Counts as nontrivial emergent query: YES.**

---

## EQ-3 — Should target identity/time validation precede subject research?

### Cross-cohort evidence

COV-002's 12-row expansion encountered three targets that failed before the slavery question:
- New Netherland at 1800;
- medieval Kingdom of Georgia at 1800;
- Western Regions protectorate at 500.

COV-003 then preregistered a cheap identity/time check on six targets and found:
- Later Zhou at -500 — mismatch;
- Xu at -500 — ambiguous;
- four valid-at-anchor cases.

These cohorts use different selection ranks and were frozen independently.

### Answer

The recurrence of target-frame failures across both cohorts means subject-first research can waste effort or attach claims to the wrong historical object.

### Methodological consequence

Future coverage architecture should order work:

**C0 identity/time validation -> C1 subject research -> selective C2 depth**

rather than treating identity validation as a cleanup step after historical interpretation.

This is a methodological priority decision, not a claim that the observed fractions estimate a global defect rate.

**Counts as nontrivial emergent query: YES.**

## Candidate rejected from counting

“Which C1 targets have direct Cambridge/Palgrave coverage?”

Useful, but already part of the preregistered coverage/bias audit and too close to an existing field count. It is not counted as emergent value.

## Emergent-query disposition

**3 nontrivial exploratory queries survive.**

They add methodological value in three different directions:
1. batch design;
2. correlated source-review risk;
3. research-order / identity QA.

This satisfies the STRONG-SURVIVE emergent-query *component*, but cannot override the failed strong batch-economy criterion.
