# COV-002 — Final Reuse / Scale Evaluation

**Issue:** #151  
**Evaluation independence:** non-independent artifact-behavior test  
**Corpus sizes:** N=25, N=31, N=37

## Fixed-task comparison at N=37

| Task | F full row | R compact register | M ordinary matrix | Disposition |
| --- | --- | --- | --- | --- |
| T1 law/practice divergence | direct | direct | reconstructive across rows | **R = F; R > M** |
| T2 network/territorial boundary | direct | direct | reconstructive across rows | **R = F; R > M** |
| T3 Cambridge/Palgrave coverage | direct | direct | reconstructive from citations/source context | **R = F; R > M** |
| T4 unresolved research | direct | direct | direct via status + caveat | parity |
| T5 bounded overview | direct | direct | direct | parity |
| T6 decisive source recovery | direct + role/direction metadata | direct source links | direct source links | practical parity for fixed question; F retains richer metadata |

R therefore matches F's fixed-task information state on **6/6** tasks. No critical task becomes misleading.

For T6, F's source-role/direction metadata is richer, but the fixed task asks whether the decisive source trail can be recovered without general re-research. R and M preserve direct links, so the extra F metadata does not produce a material task win here.

## Scale behavior

### T1 — law/practice

Rows needing substantive inspection after using the explicit field:
- N=25: F/R 4 matching rows; M requires cross-row rereading of 25 rows.
- N=31: F/R 5; M 31.
- N=37: F/R 8; M 37.

The absolute M rereading burden grows with corpus size; the F/R field remains directly filterable.

### T2 — network/territorial inference

- N=25: F/R 9 matching rows; M rereads 25.
- N=31: F/R 11; M 31.
- N=37: F/R 14; M 37.

Again the explicit distinction remains reusable as N grows.

### T3 — global-handbook coverage

F and R retain explicit Cambridge/Palgrave judgments at every N.

M preserves citations but not whether the global handbooks are direct/adjacent/none/inaccessible for the target. Reconstructing that judgment requires revisiting source context.

The advantage therefore persists at N=37.

### T4 — unresolved research

M's stronger design deliberately includes research status and caveat. It therefore remains competitive with F/R.

**Parity survives from N=25 to N=37.**

## Scaling gate

COV-001's surviving cross-cell tasks were T1–T4.

At N=37:
- T1: R/F materially better than M;
- T2: R/F materially better than M;
- T3: R/F materially better than M;
- T4: parity.

**3/4 survive with material reuse advantage — scaling threshold PASS.**

The advantage does not shrink on more than one task between N=25 and N=37. T1–T3 remain direct/filterable while M's reconstruction surface grows.

## Static representation economy

Pre-maintenance review-surface proxy:

| N | F total atoms | R total atoms | R/F | F median | R median | R/F median |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 25 | 367 | 222 | 60.5% | 14 | 9 | 64.3% |
| 31 | 456 | 275 | 60.3% | 14 | 9 | 64.3% |
| 37 | 547 | 331 | **60.5%** | 15 | 9 | **60.0%** |

The preregistered static threshold was <=70%.

**Static compactness gate: PASS.**

The information-loss audit of all twelve expansion rows found no omitted field classified as safety-critical under the fixed tasks. Source role/direction metadata and evidence-class metadata remain unique to F, but they did not create a material fixed-task difference.

## Maintenance economy

Six deterministic rows were update-tested.

Actual outcomes:
- 3 credible new/contextual sources changed row evidence;
- 3 bounded searches produced no acceptable new specialist source.

For all three material changes:
- F touched 2 review atoms;
- R touched 2 review atoms.

The no-change 0/0 rows are neutral and are not counted as savings.

Preregistered requirement:
> R touches <=70% as many review atoms as F in at least 4/6 update rows.

Observed:
> **0 material update rows met the <=70% threshold.**

**Maintenance-economy gate: FAIL.**

Updates remained local—no widespread contradictory/stale outputs appeared—but the compact register did not demonstrate cheaper evidence maintenance.

## F versus R

For **NARROW SUSTAIN** of the full row, F must materially beat R on at least two independent correctness/provenance/uncertainty tasks or maintenance shocks.

Observed:
- no fixed task gives F a material correctness/uncertainty win;
- F retains richer evidence-role metadata;
- all three material maintenance shocks require the same number of local review atoms in F and R.

**Full-row sustain gate: FAIL.**

## Protocol-level state before adversary

- scale/reuse value over M: **PASS**
- R retains F fixed-task value: **PASS**
- static R review-surface economy: **PASS**
- maintenance-shock economy: **FAIL**
- F earns extra complexity over R: **FAIL**

No positive outcome's complete preregistered gate is satisfied.

The result adversary must therefore decide whether this is a protocol-level STOP or whether a fatal defect invalidates the experiment itself. It may not relax the maintenance threshold after seeing the result.
