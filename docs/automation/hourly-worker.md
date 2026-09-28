# Autonomous evidence worker

Repository: `kaastumor/Slavery`. Active issue and next action: root `BACKLOG.md`.
WIP: one active priority across workers. Operating rules: D-090, D-091, D-092, D-096.

## Scheduled execution boundary

Scheduled workers treat GitHub as read-only whenever their execution credential cannot
write. They still complete the bounded research, reconciliation or QC task and emit one
complete `GITHUB_RECONCILIATION_PENDING` packet instead of repeatedly attempting the
same impossible mutation, disabling productive work or treating permission failure as
a substantive project block.

Each pending packet must preserve enough information for an interactive Codex session
to verify and land it without reconstructing chat or scheduler history:

- worker lane, run time and canonical Git head/release observed at start;
- exact target, temporal/spatial scope and proposed disposition;
- exact sources/versions/locators and dependency or independence notes;
- claim, geometry and publication boundaries, including uncertainty/HOLD state;
- deduplication comparison against accepted repository and database state;
- intended repository/database changes, checks and release effect;
- a stable packet identity or content fingerprint when available.

Interactive reconciliation owns any repository, database, release or public-channel
mutation. It must compare the packet with current `main`, open work and live authority,
then apply ordinary evidence/review gates. Already-complete pending packets are not
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
   A partial packet can merge while the active issue remains open. Close an issue
   only when its own acceptance criteria are met.

## Continuity and boundaries

After a bounded item completes, reconcile it and select the next justified **mode**
under D-096: discovery, execution, consolidation, review/release, maintenance, or no
justified work. WIP=1 does not require another experiment. Do not invent work if the
useful modes are complete, blocked or unjustified. Evidence quality, focus, review
capacity and complexity take priority; elapsed time alone is not a stop rule.

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
