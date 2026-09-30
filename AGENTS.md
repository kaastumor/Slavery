# Repository agent guide

Current `main` owns accepted repository state; open pull requests/issues are pending
work, and CI is verification evidence. The governed research database owns canonical
research data; immutable release packages own published versions. Repository-root `BACKLOG.md` owns the active priority; do not create a second
queue, roadmap or mutable handoff.

Start with `docs/PROJECT_INSTRUCTIONS.md`, `docs/23_PROJECT_CHARTER.md`,
`docs/24_WAY_OF_WORKING.md` and `docs/25_PROJECT_HEALTH.md`, then read the active
protocol/checkpoint and only the methodology or architecture files relevant to the
task. For scheduled work, `docs/automation/hourly-worker.md` is binding.

Codex is the primary environment for repository-native implementation, verification
and pull-request work. ChatGPT may support sponsor discussion, exploration, research
and strategic reasoning. Neither chat output nor a scheduled-worker packet is accepted
truth until it has been reconciled into the repository through the normal evidence,
review and CI gates.

Preserve WIP=1 for the canonical mutation stream and inspect active ownership before
editing. For the #369 intake programme, bounded read-only qualification may run in
parallel under D-124; it creates candidates, never accepted research or permission to
write. Routine implementation may proceed autonomously within the accepted contract;
escalate genuine sponsor, evidence, credential, publication or irreversible gates.

Do not promote methodology, schema, historical data, geometry or a release merely
because a draft or newer artifact exists. Preserve historical releases and keep
research, reviewed, published and canonical state separate.

Run the smallest relevant local checks and repository sanitation before opening a
short-lived pull request. A `GITHUB_RECONCILIATION_PENDING` packet is an input for
interactive reconciliation, never permission to apply its conclusions blindly.

## Bounded execution entry

Repository map: `db/` schema/migrations/tests; `tools/` and `scripts/` validation;
`web/` Vite/TypeScript/MapLibre; `data/`, `release/`, `experiments/`, `reviews/`
research and versioned artifacts; `docs/` methodology and decisions.

Use [docs/24_WAY_OF_WORKING.md](docs/24_WAY_OF_WORKING.md) for bounded autonomy, model routing, timeboxes,
recovery and authorization. Use [task capsules](docs/automation/TASK_TEMPLATE.md),
[verification commands](docs/automation/VERIFICATION.md) and the
[schedule activation gate](docs/automation/SCHEDULED_TASK_TEMPLATE.md).
Purpose and invariants stay in the existing charter; current work stays in BACKLOG and
its active checkpoint; durable decisions stay in the existing decision records.

Repeat critical project constraints in each task. Inspect before editing; make the smallest
coherent change; verify the actual outcome and diff; report checks run/skipped honestly.
No merge, deploy, publication, deletion, production/credential change, purchase or external
contact without explicit scoped authorization. A ready PR is pending, not accepted.
