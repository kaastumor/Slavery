# Historical Slavery Atlas — Way of Working

## Default evidence loop

For consequential work use:

**Question → smallest useful proposal → adversarial attack → experiment/implementation → evidence → decision → permanent regression where warranted → sanitation → project-state reconciliation**

Do not substitute activity for progress. Green CI proves implementation behaviour; it does not prove historical usefulness, architectural correctness or project value.

## Canonical ownership

For every consequential fact, identify one canonical owner.

Current project ownership is deliberately small:

- execution queue: repository-root `BACKLOG.md`;
- durable task evidence: GitHub issues and pull requests;
- accepted methodology/architecture decisions: `08_DECISIONS_LOG.md`;
- assumptions, material risks, value evidence and health decisions: `25_PROJECT_HEALTH.md`;
- canonical historical releases: immutable release artifacts/manifests;
- source observations: source/version/raw lineage;
- reviewed atlas interpretation: reviewed claim/evidence structures;
- presentation: derived map/API/publication layers.

Derived layers may reference canonical truth but must not silently become competing truth stores.

## Delivery flow, WIP and readiness

For bounded delivery horizons use a lean Kanban-style flow:

`READY -> IN PROGRESS -> PR/REVIEW -> DONE`

Default WIP is **1 per autonomous worker**. Do not start a second work item while the first has an open branch/PR or unresolved repository-caused CI failure.

### Definition of Ready

A work item is ready when:
- its parent goal/horizon is explicit;
- dependencies are complete;
- the question and smallest acceptance slice are bounded;
- acceptance criteria and material non-goals are explicit;
- required source/data/permissions are available;
- completion does not require an unmade project-level decision.

### Definition of Done

A delivery item is done when:
- the smallest acceptance slice is complete;
- the adversarial finding has a disposition;
- relevant focused tests and sanitation pass;
- normal CI is green;
- provenance/reproducibility metadata is preserved where material;
- PR is merged;
- issue is closed;
- canonical project state is reconciled only when evidence actually changed it.

A discovery item is done when the bounded question has durable evidence and one explicit disposition. Discovery completion does not imply production implementation.

### Release gates

Technical completion, usability acceptance, historical review and canonical publication are separate gates.

Never promote one because another passed.

## Adversarial dispositions

Every material adversarial finding receives exactly one disposition:

- **survives** — the proposal remains justified after a credible attack;
- **revise** — a real weakness changes the design;
- **reject** — the proposal is not justified;
- **park** — potentially useful, but not justified now;
- **experiment** — uncertainty is best resolved by a discriminating test.

An adversarial review that never changes anything is suspicious.

Prefer real historical/source cases where feasible. Synthetic fixtures are appropriate for exact failure modes and regression coverage, but do not establish historical usefulness.

Preserve negative controls, ambiguity, disagreement, abstention, parity and failed experiments rather than optimizing them away.

## Evidence classes

Keep epistemically different things explicit:

- **source evidence** — primary/source-native material;
- **specialist scholarship** — historical interpretation/synthesis;
- **deterministic observation** — reproducible code/database/GIS result;
- **statistical estimate** — quantified estimate with assumptions;
- **heuristic** — rule useful for operation but not historical fact;
- **model inference** — output from an AI/statistical model;
- **atlas interpretation** — reviewed project synthesis;
- **user/author assertion** — supplied claim not independently verified;
- **suggestion** — possible next step, not evidence.

Never silently promote one evidence class into another.

## Complexity and strongest-baseline rule

Use the smallest architecture that answers the current question.

A new dependency, service, database, queue, vector store, framework or provider needs a concrete failure of the strongest simpler baseline recorded in the relevant issue/decision. Prefer standard/existing repository capabilities first.

The baseline must be competent: specialist literature + notes, ordinary tables/GIS, ordinary search, a strong general-purpose model, and small scripts/notebooks are legitimate competitors.

If the simpler workflow performs materially as well, record **parity** rather than manufacturing a project advantage.

## Experiments

A non-trivial active experiment records:

- question;
- smallest discriminating test;
- strongest credible alternative;
- expected evidence;
- success signal;
- failure signal;
- state: **idea / active / survives / revise / reject / park**.

If an active experiment survives two Project Health Checks without new evidence, it must be accepted, rejected, parked, or given one concrete next discriminating test.

Implementation success is not project-value evidence.

## Method maturity

Analytical/automation capability must not be promoted merely because its code works.

Where relevant use this maturity ladder:

- **idea** — plausible but not relied upon;
- **experimental** — implemented enough to attack;
- **validated_for_view** — safe for bounded analytical/public display with limitations visible;
- **validated_for_automation** — repeated evidence supports unattended use within the stated scope and failure behaviour;
- **retired** — disproven, superseded or no longer worth maintaining.

A useful method may remain permanently experimental or view-only.

## Discovery lane

Directed execution is not the only legitimate work. At appropriate boundaries use discovery deliberately:

- **directed** — attack a known unresolved assumption;
- **orthogonal/sideways** — test the same mechanism in another historical context or adjacent discipline;
- **negative** — try to show the current boring baseline already handles the problem;
- **boundary** — attack evidence/interpretation, provenance/reconstruction, state/time, law/practice or geometry/claim ownership;
- **wild** — look for a qualitatively different case capable of breaking the architecture;
- **meta** — attack the project itself for stale state, workflow creep, dead assumptions or identity drift.

A discovery run should leave durable evidence, a fixture/regression, a hypothesis, a decision, an issue, a subtraction from scope, or a well-supported negative finding.

Discovery does not automatically authorize implementation.

## Precedents and pilots

External research should be subtractive, not a backlog generator.

For a strong precedent choose one explicit disposition:

- **reuse** — use the existing solution;
- **benchmark** — make it part of the stronger baseline;
- **learn from** — borrow the useful method/control;
- **remove from scope** — stop rebuilding what is already adequately solved.

Before creating a permanent service, generic engine, new datastore or automation, ask whether the important uncertainty can be exposed with a manual comparison, fixture, spreadsheet, notebook, prompt or small script.

A manual experiment may justify one technical experiment. A prototype may justify one next horizon. Nothing automatically justifies a platform.

## Reproducibility contract

Once a run produces meaningful analytical/research output, it should be possible to identify, as applicable:

- source/data version;
- checksums;
- Git commit;
- tool/analyzer/model version;
- prompt/configuration version;
- parameters;
- ontology/methodology version;
- timestamp;
- output-schema version.

Do not build a separate experiment platform merely to satisfy this contract. Use Git, manifests, source-version records and existing audit tables until they demonstrably fail.

## Evaluation

Synthetic fixtures prove exact behavior. They do not prove historical usefulness.

Important changes should be evaluated against:

- synthetic known-behavior fixtures;
- independent/public real-world material when appropriate;
- the project's real data early enough to expose domain mismatch;
- the strongest boring baseline in the charter.

Where relevant test construct validity, perturbation behavior, temporal/spatial boundary behavior, source traceability, stability, actual user value and whether a smaller artifact would preserve the demonstrated contribution.

## Project Health Check

Run at meaningful gate/horizon boundaries and whenever a gate grows substantially beyond its expected scope.

Do not produce a single health score.

A health check must ask:

- **north star** — are we still solving the same problem?
- **value** — what durable evidence supports and weakens the project thesis?
- **baseline** — has the strongest boring alternative changed, and where have we reached parity?
- **identity** — compare at least the incumbent project identity, a deliberately smaller identity, and a materially different adjacent identity suggested by evidence;
- **contribution** — are we confusing integration novelty with contribution?
- **evaluation** — can the contribution claim be distinguished experimentally?
- **freshness** — do README, charter, backlog, health state and decisions agree?
- **ownership** — does each consequential fact have one canonical owner?
- **method maturity** — has implementation been analytically/publicly promoted beyond its evidence?
- **complexity** — what machinery can be deleted or parked?
- **precedents** — what existing methods/tools should remove work from our scope?
- **automation/CI** — does every persistent workflow still own a distinct justified responsibility?
- **privacy/reproducibility** — can outputs be safely retained and reconstructed?
- **artifact size** — could the demonstrated contribution survive as a methodology, corpus, convention, notebook, small library/CLI, fixture/evaluation set or simpler site?

Then explicitly choose **continue / simplify / redirect / stop**.

If continuing, define one discriminating next horizon/experiment and a kill rule. Completion of a horizon does not itself authorize the next horizon.

Record decisions and deltas, not meeting transcripts.

## Capability-bound acceptance

Do not weaken acceptance criteria merely because the current session lacks credentials, private infrastructure, manual review, sponsor judgment or another required capability.

Record what passed, what remains, why it could not be executed, and who/environment can execute it. Do not promote the capability until the required evidence exists.

## Resumable chunks

Large audits, research batches and tool-heavy work should end at coherent checkpoints such as:

- evidence pinned;
- failure reproduced;
- decision recorded;
- implementation committed;
- CI verified;
- canonical state reconciled.

The repository should make interruption recoverable without reconstructing hidden chat state.

## Governance deletion rule

Periodically attack the project-management system itself.

Delete or simplify governance, workflows and experiments that become duplicated, ceremonial, stale or more expensive than the failure they prevent. The repository-root `BACKLOG.md` remains the execution queue; GitHub issues hold durable task evidence; `docs/08_DECISIONS_LOG.md` remains the decision record; `docs/25_PROJECT_HEALTH.md` remains the assumptions/risk/value/health owner.

Do not create parallel systems merely to match a template.
