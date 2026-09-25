# Post-v2 Lithuania/Karnak delta review — result

**Issue:** #278  
**Mode:** review / release  
**Disposition:** **KEEP_REVIEWED_DELTA_SEPARATE**  
**Canonical historical release:** v0.6.1 unchanged  
**Independent historical review:** 0

## Row review

### Grand Duchy of Lithuania — 1300 CE

**`ACCEPT_INTERNAL_REVIEW`**

The bounded positive survives:
an unfree household/slavery category is supportable in grand-ducal court/domain
structures around the 1300 horizon.

Acceptance does not imply:
- exact-year statutory precision;
- all captives became slaves;
- ordinary dues/labour were slavery;
- uniform practice or prevalence across the Grand Duchy;
- later serfdom existed unchanged at 1300.

### Temple of Amun at Karnak — 1000 BCE

**`ACCEPT_INTERNAL_REVIEW`**

The bounded **researched-inconclusive** selected-anchor state survives.

Accepted evidence state:
- New Kingdom Amun/Karnak captive/enslaved labour: supported earlier context;
- near-anchor Amun institutional continuity: supported;
- near-anchor subordinate/service/property context: supported;
- Temple-of-Amun human slave/unfree labour around 1000 BCE: unresolved.

Internal acceptance does not convert the last item into a positive claim or historical
absence.

## Source reconciliation

The frozen v2 lineage reconstructs to **133** relations.

Delta:
- Lithuania: 5 source relations;
- Karnak: 7 source relations;
- total: 12.

QC:
- missing source-version refs: 0;
- missing independence groups: 0;
- missing claim-fitness fields: 0;
- exact source-version overlap with v2: 0;
- Lithuania ↔ Karnak exact source-version overlap: 0.

The two existing v2 cross-target exact-version dependencies remain unchanged.

## Candidate gate

**KEEP_REVIEWED_DELTA_SEPARATE.**

This is a positive review result, not a HOLD.

A new immutable candidate is not created because:
- v2 is still coherent;
- the two rows add no cumulative source conflict;
- no publication/consumer/canonical trigger exists;
- v3 would not change the current release/publication ceiling;
- a reviewed delta preserves the evidence without package-version churn.

No fixed row-count threshold is introduced.

## Durable state

Reviewed delta membership:
- `R1:P:1300:D:r1`
- `R1:N:karnak_amun_m1000`

Base candidate remains:
`post-r1-cumulative-review-v2-overnight`

Nothing in this review changes:
- canonical v0.6.1;
- v2 candidate files;
- R1 review state;
- P-levels;
- historical-practice geometry;
- schema/ontology;
- database/API/frontend;
- public release state.

## Reopen integration

Integrate the reviewed delta into a future successor candidate only when cumulative
packaging changes a real decision or workflow, such as a publication/downstream
consumer need, a meaningful later reviewed batch, or a dependency/reconciliation
problem.
