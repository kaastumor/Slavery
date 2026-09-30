# Historical Slavery Atlas — Way of Working

## Default evidence loop

For consequential work use:

**Question → smallest useful proposal → adversarial attack → experiment/implementation → evidence → decision → permanent regression where warranted → sanitation → project-state reconciliation**

Do not substitute activity for progress. Green CI proves implementation behaviour; it does not prove historical usefulness, architectural correctness or project value.

## Evidence before project identity

Start from the phenomenon and the decision-relevant research question, not from protecting
the current Atlas, corpus, taxonomy or implementation.

Keep these questions separate:
1. what historical/research problem actually exists?
2. what contribution does this project make beyond competent existing practice?
3. what is the smallest project form that preserves that contribution?
4. what implementation, if any, is needed to support that form?

A useful historical problem does not prove a bespoke product is needed. A useful corpus
does not prove a richer application is needed. A working implementation does not earn
continued expansion by existing.

## Continuation and mode selection

The project is proactive, but **activity is not a scheduling requirement**.

After a bounded item completes, reconcile the evidence and choose the next justified
**mode of work**, not automatically the next experiment:

1. **discovery** — resolve a material uncertainty about method, representation or value;
2. **execution** — apply an accepted method within its demonstrated scope;
3. **consolidation** — reconcile overlapping batches, claims, sources and review state;
4. **review/release** — assemble and gate a coherent candidate;
5. **maintenance** — preserve, correct or reopen released/settled work on explicit triggers.

Choose by contribution to the project goal, evidence quality, focus, review capacity and
complexity. Elapsed time alone is not a stop rule, but neither is unused time a reason to
invent work.

Keep WIP at **one active priority across workers**. For #369 intake, D-124 permits
bounded read-only qualification within that priority while one owner controls the
canonical mutation stream. WIP=1 does not require a continuous chain of experiments.

A method may become **operational within a declared scope** when it supports that task,
its known failure modes have controls, and no unresolved method question blocks ordinary
use. Routine execution then uses the method without re-testing its strategic value.
Reopen only for a demonstrated failure, changed task, consequential scale pressure,
changed evidence or concrete interoperability/publication need.

A no-work state is legitimate when discovery, execution, consolidation, review/release
and maintenance are all either complete, unjustified or genuinely blocked.

## Canonical ownership

For every consequential fact, identify one canonical owner.

Current project ownership is deliberately small:

- **current priority + mode:** repository-root `BACKLOG.md`;
- **within-item unfinished work:** the active protocol/checkpoint;
- durable task evidence: GitHub issues and pull requests;
- accepted methodology/architecture decisions: `08_DECISIONS_LOG.md`;
- assumptions, material risks, value evidence and health decisions: `25_PROJECT_HEALTH.md`;
- canonical historical releases: immutable release artifacts/manifests;
- source observations: source/version/raw lineage;
- reviewed atlas interpretation: reviewed claim/evidence structures;
- presentation: derived map/API/publication layers.

`README.md` and `01_PROJECT_STATUS.md` are summaries/pointers. They must not own the
next action or compete with `BACKLOG.md`.

When an accepted amendment changes an operative rule, record **what it supersedes, where
it applies and its release effect**. Newer prose does not silently override a frozen
programme/release contract.

Derived layers may reference canonical truth but must not silently become competing truth stores.

## Delivery flow, WIP and readiness

For bounded delivery horizons use a lean Kanban-style flow:

`READY -> IN PROGRESS -> PR/REVIEW -> DONE`

Default WIP is **1 active priority across workers**. The item may be discovery, execution,
consolidation, review/release or maintenance. Do not start a second canonical mutation
item while the first has an open branch/PR or unresolved repository-caused CI failure.
For #369 intake only, read-only qualification within the active priority may continue
under the following D-124 contract; it does not create another repository/DB writer.

### #369 intake fast path (D-124)

- One integration owner controls the active batch, its branch/PR, manifest, review
  decisions and all repository/DB writes. No overlapping writer or competing admission
  batch is allowed. Up to four workers may qualify distinct candidates read-only when
  the owner has review capacity. Each worker owns one bounded item per run; scheduled
  timeboxes and packet rules remain in force. Stop new scouting at eight unacknowledged
  packets or sooner if review debt grows faster than it closes.
- Screen a bounded 20-40 candidate pool from the existing #369 funnel before fresh
  discovery. In the owning issue or existing review artifact, record a stable candidate
  key, source/version pointer, input revision and one disposition:
  `ACCEPT_FOR_BATCH`, `NEEDS_DEEP_REVIEW`, `HOLD` or `DUPLICATE`, with a reason.
  `ACCEPT_FOR_BATCH` means eligible for full case review, not admitted data or a 100/100
  numerator increment. Preserve rejected, duplicate and HOLD evidence.
- Select an initial routine batch of at most five cases; later batches may contain up
  to ten when the owner can review every case and the previous batch has been
  reconciled. These are caps, not quotas. Route material category, chronology,
  identity, source-independence, overlap, provenance or geometry-role ambiguity to
  deep review. An exception joins a batch only after its own dispute is resolved and
  the manifest is reviewed again. Do not favor easy-to-map or archive-dense regions.
- Each admitted case needs its own stable identity, substantive claim review,
  exact source-version/locator and dependency record, bounded or explicitly uncertain
  time/place, review outcome, and independent geometry-role decision. HOLD and
  unresolved geometry remain explicit. A valid historical case without defensible
  case-linked geometry cannot enter the geo numerator. No P-level follows from
  document, voyage or citation counts.
- Prepare one coherent PR for the batch review, exact manifest/driver and disposable
  rehearsal. Pin case keys, source versions, expected inserts/reuse and zero-effect
  boundaries to a manifest digest. Focused CI must check collisions, identity,
  provenance, geometry role, expected deltas, unchanged replay, rollback and receipt
  completeness. Human review owns historical meaning and source independence.
- Merge the reviewed preparation only with scoped authorization. A later production
  authorization may cover the entire **exact manifest**, not changed members or SQL.
  Immediately before one guarded transaction, recheck current main, schema, live
  identities/source reuse, release membership and serving state. Drift aborts. A
  mismatch in any case rolls back the whole batch; removal or repair makes a newly
  reviewed manifest requiring fresh authorization. Record generated IDs, per-case
  results, exact before/after deltas and independent post-write readback in one
  receipt/control-state PR before the next canonical mutation batch. After commit,
  correction requires a separately reviewed compensating action, never an overwrite
  of immutable release history.
- Research ingestion does not authorize successor selection, publication or public
  cutover. Those remain separate gates. Keep cross-batch identity/source/review
  reconciliation before sustained scaling or release. Do not enable or alter a saved
  schedule merely by changing this policy.

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
- PR is merged with explicit scoped authorization; otherwise the worker reports READY_FOR_REVIEW and delivery acceptance remains pending;
- the owning issue reflects its own acceptance state; a partial delivery may merge while the issue remains open;
- canonical project state is reconciled only when evidence actually changed it;
- `BACKLOG.md` and the active checkpoint agree before merge when priority/progress changed;
- summary files are updated only for a material milestone and link back to the canonical owner rather than duplicating the exact next action.

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

## Complexity budget and strongest-baseline rule

Use the smallest project form that answers the current question.

A permanent addition must prevent a demonstrated failure or serve a concrete task better
than the existing arrangement. This applies to more than software:

- **methodology/rules:** routine cases inherit accepted controls; new mandatory steps need a demonstrated failure;
- **metadata/schema:** every maintained field owns a distinct information responsibility; derive duplicated information where possible;
- **standards/adapters:** optional adapters stay optional until a real workflow earns their maintenance;
- **automation:** each persistent workflow owns one distinct responsibility;
- **documentation:** one mutable owner per fact; summaries point to it;
- **review:** new intake must remain within actual reconciliation/review capacity.

A new dependency, service, database, queue, vector store, framework or provider still
needs a concrete failure of the strongest simpler baseline recorded in the relevant
issue/decision. Prefer standard/existing repository capabilities first.

The baseline must be competent: specialist literature + notes, ordinary tables/GIS,
ordinary search, a strong general-purpose model, and small scripts/notebooks are
legitimate competitors.

If the simpler workflow performs materially as well, record **parity** rather than
manufacturing a project advantage. Correctness-critical complexity may still be added;
record why it earns the maintenance cost and what would retire it.

## Abstraction first refusal and compression

Before adding a new ontology category, evidence field, mechanism, research-state class,
workflow class or permanent project abstraction:

1. state the causal/information distinction that would be lost without it;
2. test whether an existing project abstraction can own it without semantic distortion;
3. test the strongest established external concept or ordinary scholarly/research practice;
4. identify a meaningful negative/boundary control that looks similar but should not qualify;
5. prefer **reuse / broaden / merge / reject** over adding a new class when the distinction is not consequential.

Different geography, period, source type, cardinality or presentation does not by itself
justify a new abstraction.

At meaningful synthesis boundaries, run a compression pass when neighbouring classes
start to overlap, singleton classes accumulate, or distinctions increasingly depend on
subtle wording. Preserve the evidence even when labels merge or retire. The goal is the
minimum coherent abstraction set that preserves demonstrated distinctions.

## Experiments

A non-trivial active experiment records:

- question;
- smallest discriminating test;
- strongest credible alternative;
- expected evidence;
- success signal;
- failure signal;
- state: **idea / active / survives / revise / reject / park**.

When freshness matters, also record prior exposure. A case or trap inspected during
development is exposed and must not later be described as fresh/blind evaluation
material. Use genuinely unseen cases for tests whose inference depends on freshness;
exposed cases remain valid regression/supporting evidence.

If an active experiment survives two Project Health Checks without new evidence, it must be accepted, rejected, parked, or given one concrete next discriminating test.

Implementation success is not project-value evidence.

## Method maturity

Analytical/automation capability must not be promoted merely because its code works.

Where relevant use this maturity ladder:

- **idea** — plausible but not relied upon;
- **experimental** — implemented enough to attack;
- **operational_for_scope** — accepted for a declared routine task; use it without re-proving method value unless a reopening trigger occurs;
- **validated_for_view** — safe for bounded analytical/public display with limitations visible;
- **validated_for_automation** — repeated evidence supports unattended use within the stated scope and failure behaviour;
- **retired** — disproven, superseded or no longer worth maintaining.

A useful method may remain permanently experimental or view-only. An
`operational_for_scope` method is not universally validated; its scope and reopening
triggers remain explicit.

## Discovery lane

Use `discovery/DISCOVERY_EXECUTION.md` for execution and gate selection, and
`discovery/RUN_PROMPT.md` for continuation. The modes below are search options,
not a mandatory checklist. Historical evidence, method testing and product value
require distinct conclusions; no automatic transfer of acceptance between them.

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

If continuing, define one discriminating next horizon/experiment and a kill rule. Under D-088, completion of a horizon triggers **selection** of the next high-information bounded experiment; it does not authorize arbitrary implementation or scope expansion.

Record decisions and deltas, not meeting transcripts.

## Reconciliation boundary

After a coherent batch, stop adding cases long enough to reconcile it:
1. synthesize the result, including negative/null findings;
2. reconcile overlapping target identities, claim revisions, source identities /
   dependency groups and review states;
3. reconcile corpus/taxonomy/abstractions only where earned;
4. update the canonical backlog/checkpoint owners;
5. assess whether available review/reconciliation capacity can support further intake;
6. choose the next **mode** under D-096;
7. run one relevant sanitation/CI cycle; prepare a reviewable PR. Merge only with explicit scoped authorization, then resume dependent work from fresh main. Until then preserve the pending checkpoint and do not open competing WIP.

**Cross-batch reconciliation is required before sustained scaling or release.**
Experiment-local artifacts may remain useful without automatically becoming one
cumulative current corpus. Promotion requires an explicit reconciled candidate and
publication tier.

If review/reconciliation debt is growing faster than it can be closed, finish that work
before admitting more targets. Internal candidates may remain useful but do not become a
substitute for deferred review.

This prevents both merge-shaped idle and indefinitely growing research/discovery chains.

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

## Bounded autonomous execution and usage

Continue within the accepted mandate without asking the sponsor to invent routine
tasks. At each entry inspect live main, open work, active ownership and the existing
BACKLOG/checkpoint. Resume recoverable work before selecting another question. Use
the project's existing allocation and evidence gates; autonomy does not earn new scope.

One run owns one bounded item. At completion, verify, preserve negative/null evidence,
reconcile once in the existing owner, and identify the next eligible action. Start a
fresh bounded task/context for an independently reviewable chunk; pass a compact
[task capsule](automation/TASK_TEMPLATE.md), not the conversation. Fresh context
is a context-management technique, not proof of independent scientific review.

### Authority and acceptance

Autonomous authority covers in-scope research, analysis, drafts, focused checks and
authorized branch/PR preparation. Merging, deploying, publishing, deleting information,
changing production settings, rotating credentials, purchasing, contacting external
parties, changing the charter/evaluation criteria or creating/changing schedules requires
explicit sponsor authorization for that action or a recorded standing scope.
A general "continue", passing CI or an older generic merge instruction is insufficient.
Do not ask again when valid explicit authorization already covers the action.

A worker may finish at `READY_FOR_REVIEW`, `RECONCILIATION_PENDING`,
`CHECKPOINTED` or `BLOCKED`; none means accepted/merged. Keep the owning issue open
until its acceptance criteria are met. Do not advance a dependent implementation from
unmerged assumptions or open competing WIP. A blocked item may yield to a separately
eligible, nonconflicting alternative under the existing allocation rules; record why.
If none exists, record the missing prerequisite and re-entry trigger, then stop the run.

Repeat critical scope, privacy, evidence and authorization constraints in every capsule.
Before returning, review the actual output/diff against them. AGENTS instructions are
guidance, not an enforced permission boundary; use actual tool permissions and existing
CI/review gates. Never claim that writing this policy configured the runtime.

### Surface and model routing

Select the project mode under D-096. Choose the execution surface and model/effort
separately; record the run's disposition separately from all three. These are routing
recommendations, not configured runtime settings or evidence that a schedule exists.

| Work | Execution surface |
| --- | --- |
| Requirements, task design, prioritization, critique, short answers | Ordinary Chat |
| Substantial research, connected-app work, finished non-code deliverables | Work |
| Primary result is repository inspection/change, tests, review, commit or PR | Codex |

| Work | Model/effort recommendation |
| --- | --- |
| Narrow repeatable work with objective verification | GPT-6 Luna |
| Normal bounded multi-step execution and allocation | GPT-6 Sol Medium |
| Difficult interpretation, architecture, debugging or weak verification | Sol High |
| Exceptional ambiguity, security/concurrency risk or critical review | Sol XHigh when justified |
| Hard decision/review where expected value exceeds additional usage | Astra, explicitly justified |

Choose using ambiguity, blast radius, reversibility, privacy and verification strength,
not task size alone. Record requested and actual model/effort (or `UNKNOWN`). A prompt
cannot switch models: report a mismatch before implementation; do not silently claim
a substitution. Missing access is not a reason to buy more reasoning. Prefer a deterministic
script for mechanical work; do not use Chat to circumvent Work/Codex usage limits.

No permanent expensive supervisor. When work is delegated, a short-lived coordinator
can select and accept work using durable state; this policy creates no dispatcher.
Workers keep implementation detail outside that context. Use subagents
only for genuinely independent bounded work or validation; no role-play hierarchy or
recursive delegation by default. One writer per overlapping scope. Use completion
signals/long waits, not repeated polling. Summarize material results and artifact refs;
do not return full worker transcripts to the coordinator.

### Budgets, recovery and memory

- New scheduled research tasks default to **20 minutes and one bounded item per run**.
  Reserve time to checkpoint; at the limit persist partial work and the next exact action.
  The timebox ends execution, not the hypothesis or project. Do not stretch it by spawning
  workers or starting a second run. Other task types require an explicit timebox in their
  approved capsule; do not infer unlimited execution.
- This document does not change existing saved schedules. Before activation, verify that
  their saved prompts, access and runtime settings implement the approved contract.
  If the runtime cannot enforce a limit, label it advisory and test checkpointing.
- Use one retry for a transient operation (two attempts total), within the same timebox.
  Missing permissions/tools/required evidence stop that operation immediately. Inspect
  durable state before retrying an ambiguous write. Never repeat an impossible operation.
- A known non-transient prerequisite blocks its operation immediately. Permitted review,
  reconciliation, read-only handoff and separately eligible nonconflicting work may continue.
  If none remains, report the re-entry trigger and stop this run. Two identical
  initially ambiguous failures on successive runs also block the affected operation.
  Emit one actionable notice and record that block in durable state when available.
  If storage is unavailable, stop new intake until it recovers. Future invocations check
  eligibility before retrying the affected operation. Do not autonomously rewrite/disable schedules.
- Before new intake, inspect pending results and consumer acknowledgments. Deduplicate
  on repository, lane, task ID, input revision and contract version, with a separate attempt
  ID. Revalidate stale inputs before application. Unknown pending state is a recovery gate,
  not permission to generate another packet. Review debt takes priority over new intake.
- Keep existing backlog/issues/PRs as owners, not a new shadow task database. Scheduled
  state must have an approved durable location, a pending-item cap and a bounded resume
  summary (default at most 8 KiB and 20 recent receipt references). Preserve unresolved
  receipts and scientific evidence in the appropriate archive before compacting the index;
  if safe compaction is unavailable, stop intake rather than discard them.
- Store full logs outside the coordinator context in a durable, privacy-appropriate place.
  A receipt records task/input refs, status, output ref, verification, consumer acknowledgment,
  next action, elapsed time and actual usage if exposed. Unknown usage stays `UNKNOWN`;
  label estimates separately. Never put protected source identifiers in public receipts.
- No monetary/credit ceiling is presumed approved. Obtain it before enabling new recurring
  paid work; do not silently buy credits, increase limits or add API services. Account for
  retries, review and repair when assessing cost per verified useful outcome. Operator
  efficiency anecdotes are hypotheses, not promised savings or measured billing reductions.
- No meaningful delta means the defined `NO_CHANGE` result and no discretionary notice.
  Notify for reviewable completion, an actionable blocker, budget exhaustion or a material
  contradiction; do not promise silence if the host always delivers task results.

Use [verification guidance](automation/VERIFICATION.md) for proportionate checks.
Use the [scheduled-task contract](automation/SCHEDULED_TASK_TEMPLATE.md) for manual
testing, approval and the first-three-run calibration. This policy creates no schedules.

### Atlas authority and evidence boundary

GitHub main owns accepted repository/control state. The governed Postgres/PostGIS
research database owns canonical research data; immutable release packages own published
versions. A Git packet or source summary cannot replace database verification or publication
approval. Missing database_read/source-native provenance remains a named gate.

Keep historical claims, source evaluation, ontology, time, geometry and publication tier
separate. Preserve conflicting sources and dependent evidence. Geometry is not historical
proof. Parallel claim/geometry preparation may produce candidates only, followed by the
existing QC, reconciliation and promotion gates. Never synthesize a missing provenance
locator or convert unknown/held data into absence or acceptance.
