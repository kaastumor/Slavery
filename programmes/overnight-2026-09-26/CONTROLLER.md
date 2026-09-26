# Overnight controller — 2026-09-26 → 2026-09-27

**Issue:** #291  
**Controller:** one scheduled task, eight hourly occurrences  
**Canonical project source:** GitHub `main`  
**Scheduled GitHub mode:** **READ-ONLY**  
**Operational recovery state:** private persistent execution ledger outside Git/CI  
**Canonical release:** v0.6.1 unchanged

## Authority split

### GitHub
Owns accepted:
- governance/project state;
- BACKLOG/current WIP;
- campaign plan;
- issues/PRs;
- accepted checkpoints;
- release/review decisions.

### Private execution ledger
Owns only temporary scheduled-run:
- `PENDING` / `IN_PROGRESS` / terminal status;
- recovery note;
- compact result;
- private artifact pointer;
- `github_reconciliation_pending`;
- optional observed GitHub main SHA.

The ledger never silently supersedes GitHub.

## Scheduled worker contract

On every invocation:

1. Read current GitHub `main`, BACKLOG, issue #291, open PRs/issues and relevant
   branches. GitHub overrides stale task text for accepted state.
2. Read the private execution ledger.
3. If any slot is `IN_PROGRESS`, resume that exact slot.
4. Otherwise select the lowest-numbered `PENDING` slot.
5. **Before substantive work**, durably update the ledger slot to `IN_PROGRESS`.
6. If that ledger write fails, stop before substantive work.
7. Execute **exactly one** bounded slot. Never start a second slot in the same invocation.
8. Scheduled context must not attempt GitHub mutation: no comments, branches, commits,
   PRs, merges, issue state, BACKLOG edits or stage markers.
9. Save substantive/private/source-sensitive output in the authorized private store.
10. End the selected slot in exactly one terminal state:
    `DONE`, `REVISED`, `NO_VALUE`, or `BLOCKED`.
11. Record compact privacy-safe result, artifact pointer if any, and
    `github_reconciliation_pending: true` whenever the result is not represented in
    canonical GitHub.
12. Never repeat a terminal slot.
13. If all fixed slots are terminal, perform no new research.
14. Never create Run 9 or extend the campaign.

## Fixed slot map

1. EXP-14 Trans-Saharan subject packet.
2. EXP-14 adversarial replay + merge-ready reconciliation package.
3. EXP-10-derived programme closure retrospective/inventory.
4. Five-row post-v2 source/dependency reconciliation.
5. Five-row adversarial cumulative internal review.
6. D-099-compliant packaging gate.
7. Next-horizon allocation review; at most one justified future horizon.
8. Final QC + private morning handoff and final programme disposition.

For any stage definition in #291 that mentions GitHub merge/close/comment/marker/update,
the scheduled worker performs the bounded analytical/artifact portion privately and
marks GitHub reconciliation pending.

## Crash / disagreement handling

- Ledger slot `IN_PROGRESS` after a crash is resumed by the next invocation.
- GitHub `main` changes between runs: re-read it and adapt the bounded slot without
  erasing ledger history.
- Ledger/GitHub disagreement: GitHub wins for accepted state; preserve ledger result and
  flag reconciliation rather than replaying work.
- A `NO_VALUE` or invalidating result may narrow later slots. Later slots must still
  be dispositioned in order; they may become `NO_VALUE` or `BLOCKED`, not silently
  skipped or replaced.
- Interactive work during the campaign must inspect the ledger before claiming
  overlapping substantive WIP.

## Interactive reconciliation

A later interactive session:
1. reads current GitHub first;
2. reads the ledger;
3. reconciles terminal runs in order;
4. does not blindly replay private results;
5. preserves negative/parity/no-value findings;
6. writes accepted checkpoints/PRs/BACKLOG changes to GitHub;
7. clears or updates `github_reconciliation_pending`;
8. closes #291 only when actual completion criteria are met.

The legacy `NIGHT_STAGE_N_COMPLETE` comments are interactive reconciliation markers,
not scheduled recovery state.
