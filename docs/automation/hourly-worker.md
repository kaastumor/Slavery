# Autonomous evidence worker

This runbook does not enable or change a schedule. Before each saved-task migration,
use [SCHEDULED_TASK_TEMPLATE.md](SCHEDULED_TASK_TEMPLATE.md); repeat the project's
critical constraints in the saved prompt. New scheduled research defaults to **20 minutes,
one bounded item**, followed by an honest checkpoint. Existing saved tasks require
separate manual testing and approval before configuration changes.

Use [TASK_TEMPLATE.md](TASK_TEMPLATE.md) and [VERIFICATION.md](VERIFICATION.md).
The canonical operating policy owns routing, retry, deduplication, memory and authorization.
Merge/deploy/publication and other consequential actions require explicit scoped sponsor
authorization; a green PR is READY_FOR_REVIEW, not automatic permission to merge.

Repository: `kaastumor/Slavery`. Active issue and next action: root `BACKLOG.md`.
WIP: one active priority across workers. Operating rules: D-090, D-091, D-092, D-096.

## Verified autonomous handoff

Use one designated executor for the current WIP. Prefer that executor to read the
input, execute the bounded task, save the result and verify its durable receipt.
Separate producers require a working consumer and approved delivery route first.
Keep issues/PRs/BACKLOG as owners; do not introduce another queue.

A comment/readback test proves only that operation. Verify branch/PR writes, local
execution, browser observations and private persistence when the selected task
requires them. A prompt cannot grant access, select a model or enforce a budget.
Test one real existing-result handoff and one substantive recovery cycle before
claiming end-to-end operation. Use the scheduled-task contract for activation and
cost review; timer activation alone is not acceptance.

A new explicit sponsor-authorized contract may replace a historical campaign's
read-only envelope. Actual permission or automatic-approval denial still stops the
affected operation: never switch tools, credentials or destinations to evade it.
Without a permitted durable route, stop new intake and report the capability gap.

Resume pending results before producing another. Record exact task/input/output
revision and a separate attempt identity; verify saved bytes or readback and the
consumer disposition. Receipt is not substantive acceptance. Default new
unacknowledged-output capacity is one; unknown legacy backlog blocks new intake,
not explicitly selected recovery of an existing item. Inspect open work and its
latest checkpoint before treating stale main/PR text as unfinished execution.

## Scheduled execution boundary

Scheduled workers treat GitHub as read-only whenever their execution credential cannot
write. If an approved durable packet route is available, they may complete bounded
research, reconciliation or QC and emit one `GITHUB_RECONCILIATION_PENDING` packet
instead of repeatedly attempting the same impossible mutation. This fallback is
valid only when a designated permitted consumer can actually process the route. If no durable route is
available, stop new intake and report that prerequisite; do not treat missing GitHub
write permission alone as a substantive project block.

Each pending packet must preserve enough information for an interactive Codex session
to verify and land it without reconstructing chat or scheduler history:

- worker lane, run time and canonical Git head/release observed at start;
- exact target, temporal/spatial scope and proposed disposition;
- exact sources/versions/locators and dependency or independence notes;
- claim, geometry and publication boundaries, including uncertainty/HOLD state;
- deduplication comparison against accepted repository and database state;
- intended repository/database changes, checks and release effect;
- a stable packet identity or content fingerprint when available.

The designated consumer owns reconciliation. With explicit scoped sponsor
authorization and verified capability, it may be interactive or scheduled for
repository evidence and reviewable PR work. It must compare the packet with current
`main`, open work and live authority, then apply ordinary evidence/review gates.
Database, release and public-channel mutations retain their separate authorization
gates; receipt alone never authorizes them. Already-complete pending packets are not
reissued or reprocessed merely because the scheduled worker runs again. A genuine
evidence, source, credential or safety gate may still be reported as `BLOCKED`; lack of
scheduled GitHub write permission alone may not.

## Entry and execution

1. Inspect current main, open PRs/issues and CI. Resume existing work before opening
   another branch. Check ownership; do not overwrite another worker's changes.
2. Read `BACKLOG.md`, `docs/discovery/DISCOVERY_EXECUTION.md`, and the active
   protocol/checkpoint. On first entry read project instructions and charter.
   Load additional method/source files only as needed for the chosen action.
3. Execute the next discriminating action under the appropriate evidence gate.
   `docs/discovery/RUN_PROMPT.md` is the shared continuation prompt. Use existing
   experiment contracts; do not create duplicate forms just to satisfy this guide.
   New permanent abstractions require existing-class/external-baseline first refusal
   and a meaningful negative boundary before adoption.
4. Preserve an honest checkpoint, reconcile the next action, and batch a coherent PR.
   A partial packet can merge with explicit scoped authorization while the active issue remains open. Close an issue
   only when its own acceptance criteria are met.

## Continuity and boundaries

After a bounded item completes, reconcile it and select the next justified **mode**
under D-096: discovery, execution, consolidation, review/release, maintenance, or no
justified work. WIP=1 does not require another experiment. Do not invent work if the
useful modes are complete, blocked or unjustified. Evidence quality, focus, review
capacity and complexity take priority. A timebox ends this run with a checkpoint;
elapsed time alone does not terminate the research question or project.

Historical source/method constraints in `docs/PROJECT_INSTRUCTIONS.md` remain binding.
Internal critique is not independent review. Green CI is not historical/editorial
approval. Discovery does not authorize production features, canonical schema/data
promotion, participant outreach or sensitive modern-person coverage. Existing
external-review deferral remains; no automatic recruitment or new services.

## Verification and cost

Local relevant checks and sanitation first. Short-lived PR; required relevant CI must
pass before merge. Known documentation/research text changes use lightweight checks;
code, SQL, workflow, dependency and unknown paths retain the database gate. Use normal
scoped CI; do not dispatch unrelated workflows or rerun unchanged passing jobs.
Weekly/manual preview monitoring remains. Do not alter scheduler cadence/model merely
because this runbook changes. When active state changes, reconcile `BACKLOG.md` and
the active checkpoint; README/status update only for material milestones and do not own
the exact next action.

## End-of-run report

State evidence gained, actual disposition, material limits, checks and next exact
step. A handoff must let the next session resume without reconstructing chat history.
Research volume, new hypotheses, commits and elapsed time are not success metrics.
