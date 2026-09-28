# Repository agent guide

Treat current `main`, open pull requests/issues and current CI as the accepted project
state. Repository-root `BACKLOG.md` owns the active priority; do not create a second
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

Preserve WIP=1 and inspect active ownership before editing. Routine implementation may
proceed autonomously within the accepted contract; escalate genuine sponsor, evidence,
credential, publication or irreversible gates.

Do not promote methodology, schema, historical data, geometry or a release merely
because a draft or newer artifact exists. Preserve historical releases and keep
research, reviewed, published and canonical state separate.

Run the smallest relevant local checks and repository sanitation before opening a
short-lived pull request. A `GITHUB_RECONCILIATION_PENDING` packet is an input for
interactive reconciliation, never permission to apply its conclusions blindly.
