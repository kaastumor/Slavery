# MVP Delivery + Discovery Cadence

## Why this exists

The project has moved from broad exploration to a small validated research/release core.

Delivery and discovery remain separate so curiosity cannot silently become product scope.

The technical MVP delivery queue #175–#182 is complete. The active uncertainty is now **external relative value**, not whether more features can be built.

## Lane A — Delivery

Purpose: implement only work already earned by stronger evidence.

Rules:
- WIP 1;
- atomic GitHub issue;
- explicit dependency;
- short-lived branch;
- PR + green CI;
- no scope expansion;
- acceptance evidence required;
- one worker run completes at most one issue.

There is currently no new product-delivery queue.

R1.8 publication / hold / rework remains a separate release decision after sponsor/browser review.

## Lane B — Discovery

Purpose: reduce uncertainty about **user/job/alternative/relative value**, not accumulate feature ideas.

Canonical method:
- `docs/discovery/DISCOVERY_STANDARD_V2.md`.

Governing principle:

> **EXISTING ≠ USELESS. DIFFERENT ≠ VALUABLE. NOVEL ≠ DEMANDED. COMPETITION ≠ VALIDATION. EVIDENCE DECIDES.**

Required sequence:
1. identify user + circumstance + job/progress;
2. identify the real current alternative, including manual work/non-consumption;
3. separate novelty from strategic relevance;
4. formulate relative advantage against that alternative;
5. distinguish difference / importance / behavioural consequence;
6. include switching/adoption friction where relevant;
7. inspect system-level complementarity with the core;
8. label material evidence OBSERVED / SUPPORTED INFERENCE / HYPOTHESIS / UNKNOWN;
9. red-team the opportunity;
10. predeclare the smallest falsifiable experiment.

Rules:
- no production implementation;
- baseline first;
- competitor research establishes alternatives, not automatic rejection or validation;
- commercial/pricing analysis only when a credible customer/economic model exists;
- one bounded uncertainty per experiment;
- prefer behavioural evidence;
- desk research alone cannot create PROMOTION CANDIDATE;
- result must reduce uncertainty.

## Current discovery reset

#184 richer timeline is complete and rejected on relative-value / false-precision grounds.

#198 is now the active wide-lens reassessment.

Until #198 closes:
- #185 search/filter is blocked;
- #186 source-dependency visualization is blocked;
- #187 cross-case comparison view is blocked.

The reassessment may keep/rewrite, park or reject those ideas. Existing issue count creates no entitlement to run them.

## Decision states

- REJECT NOW
- PARK
- DISCOVERY CANDIDATE
- RUN EXPERIMENT
- PROMOTION CANDIDATE

Older discovery terminology remains historical evidence:
- REJECT ≈ REJECT NOW;
- PARK = PARK;
- REVISE ≈ DISCOVERY CANDIDATE;
- ADOPT_FOR_EXPERIMENT ≈ RUN EXPERIMENT.

## Change control

Even PROMOTION CANDIDATE does **not** directly authorize production implementation.

To move from discovery to delivery:
1. stronger evidence must identify a concrete baseline failure or meaningful user advantage;
2. a new bounded delivery issue must be created;
3. acceptance criteria must state how the change beats the baseline;
4. project scope/risk must remain compatible with the charter;
5. if methodology/ontology changes, Decisions Log update is required before canonical adoption.

## Reporting

Discovery completion report:
- user/job tested;
- strongest real alternative;
- evidence labels;
- critical unknown;
- red-team result;
- experiment/disposition;
- what was removed from scope;
- next highest-information uncertainty, if any.

Discovery optimizes information gain, not throughput.
