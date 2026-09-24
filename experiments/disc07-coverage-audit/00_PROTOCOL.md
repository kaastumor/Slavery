# DISC-07 — cross-dimensional coverage audit

**Issue:** #245  
**Primary gate:** method / research-design discovery  
**Status:** preregistered before matrix generation  
**Base commit:** `d0604dba1ec2fa4ca2d5ab1e33b50de79e3bfca3`

## 1. Question

Do the current R1 target-frame balance gates and manual registry inspection hide a
**cross-dimensional research-design concentration** that becomes visible only when the
frozen target universe is audited jointly across chronology, frame class, polity
sampling sector and research/QA state?

This is a research-coverage audit only. A sparse/unresearched cell never means historical
absence, low prevalence or weak evidence.

## 2. Frozen universe

All **77 targets** in:
`programmes/r1/r1_candidate_target_registry.json`

Frozen registry blob:
`cec379246221d166db3830845566311077596862`

Do not add, remove or reclassify targets because of matrix results.

## 3. Baseline

Existing controls:
- frozen target registry;
- `programmes/r1/target_frame.json` marginal balance checks;
- explicitly preserved polity sampling gaps;
- existing manual horizon-selection/reconciliation notes;
- current research-state and QA fields.

The audit must compare against what those controls already make explicit.

## 4. Experimental matrices

Non-visual tables only.

### A — chronology × frame class × research state

Use the frozen target anchor and `effective_frame_class`.
Keep exact anchors in the raw table and aggregate only into transparent audit bands when
needed for readability.

### B — polity chronology × neutral sampling sector × research state

Use only rows with a frozen `sampling_sector` A–F.
Do not reinterpret sectors as named modern regions.

### C — frame class × QA/research state

Cross-tab:
- effective frame class;
- `c1_review_complete`;
- `planned_c1_unresearched_ready`;
- `c0_registered_unresearched`;
- held states;
- QA state / frame limitation.

## 5. Test tasks

1. Does a joint matrix expose at least one material concentration/gap not already
   explicit in current marginal balance checks/manual docs?
2. Would that finding change or materially qualify a future target-frame or horizon
   decision?
3. Does the matrix merely restate known sector gaps or total research-state counts?
4. Does the audit create an invalid temptation to interpret target sparsity as historical
   absence or archive density as prevalence?

## 6. Frozen discriminator

**SURVIVES** if at least one material cross-dimensional blind spot is not already
explicit in the baseline and would change or materially qualify a future target-frame /
horizon decision.

**NARROW** if the matrices add useful QA/reconciliation visibility but no
decision-changing blind spot.

**REJECT** if they only restate current balance gates/manual knowledge.

No threshold change after matrix generation.

## 7. Adversarial attacks

Assume the audit is misleading and attack for:
- target-frame sparsity → historical absence;
- archive/source density → prevalence;
- subjective region labels;
- immutable R1 release state being mistaken for live post-R1 experiment state;
- marginal balance being confused with joint balance;
- visualization/product creep from a simple QA table.

## 8. Complexity boundary

No historical/slavery subject research. No target substitution. No registry mutation.
No inferred absence. No new geography ontology. No visualization/frontend. No schema,
database or service work. No canonical/public release.

EXP-08 remains paused; Qi — 500 BCE remains frozen/unstarted.

## 9. Freeze rule

Do not generate or score the matrices until this protocol/universe freeze is merged.
