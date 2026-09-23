# MVP Delivery + Discovery Cadence

## Why this exists

The project has moved from broad exploration to a small validated core.

Delivery and discovery are now separate lanes so feature curiosity cannot destabilize the MVP.

## Lane A — Delivery

Purpose: make the already-earned core usable.

Rules:
- WIP 1;
- atomic GitHub issue;
- dependency order;
- short-lived branch;
- PR + green CI;
- no scope expansion;
- acceptance evidence required;
- one worker run completes at most one issue.

Current queue: #175–#182.

## Lane B — Discovery

Purpose: test whether a potential feature deserves a later experiment.

Rules:
- unavailable until technical MVP gate #182 passes;
- no production implementation;
- baseline first;
- precedent research is subtractive;
- kill rule predeclared;
- one bounded question per run;
- result must reduce uncertainty.

Current queue: #184–#187.

## Change control

A discovery result that says ADOPT_FOR_EXPERIMENT still does **not** authorize production implementation.

To move from discovery to delivery:
1. evidence must identify a concrete baseline failure;
2. a new bounded delivery issue must be created;
3. acceptance criteria must state how the feature beats the baseline;
4. project scope/risk must remain compatible with the charter;
5. if the change is methodological/ontological, Decisions Log update is required before canonical adoption.

## Reporting

Worker completion report:
- issue worked;
- PR/merge state;
- tests and CI;
- adversarial disposition;
- blocker if any;
- next eligible issue.

Morning review reports evidence, not issue-count velocity.
