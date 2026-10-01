# Continuous validation contract

CONTINUOUS_VALIDATION_V1_20261001 extends observation and existing hourly workers until the sponsor pauses them. Project gates and WIP=1 remain authoritative. No substantive progress is required from a gated project. The observer is read-only except for its private status Page.

## Worker run receipt

At actual entry capture an actual UTC epoch start and unique attempt ID. At exit, including NO_CHANGE/GATED, execute continuous.py `record` with the latest same-SHA controller.py, existing run-ledger.json (or `initial(repository)` only when independently confirmed absent), and these exact fields:

`run_id`, `task_id`, `started_at`, `finished_at`, `outcome`, `canonical_owner`, `main_head`, `control_ref`, `checks`, `evidence_kind`.

`task_id` must match the saved task; evidence_kind is WORKER_SELF_REPORT. outcome is NO_CHANGE/GATED/BUSY/COMPLETED/CHECKPOINTED/BLOCKED/FAILED/NEEDS_REVIEW. COMPLETED means a worker stage ended, never scientific/product acceptance. canonical_owner is a verified own-repository issue/pull URL or null. main_head/control_ref are actual public Git SHAs read during this run. Checks are only the predefined check labels actually completed; leave unperformed checks out. No free-text/source/paths/model/private metadata is accepted. Over 25 minutes requires FAILED or NEEDS_REVIEW. Never fabricate a missing timestamp, host execution or positive check.

Publish only .automation-v2/run-ledger.json, retaining all other tree entries, with EXACTLY one parent equal to the observed control ref; force=false and independently read back the file at the resulting ref. Recheck state before publishing: do not write while another live/expired claim exists or an operation is unresolved. A lost sibling CAS stops this publication; independently inspect, do not rebase/force/retry blindly. Report RECEIPT_WRITE_CONFLICT/UNAVAILABLE in the task result. A successful control write is not itself a run receipt. This final bounded operational receipt is the only exception to the old NO_CHANGE-without-writes rule; unchanged runs still make no project changes or repeated issue comments. Keep run_id stable across retry; exact replay is idempotent, changed replay refuses. Latest 24 entries are retained; older entries remain in Git commit parents, which are the audit history, not a second task queue.

## Observer

Every hour, read exact refs/states/ledgers and current canonical gates. Fetch controller.py, continuous.py and test_continuous.py at one exact control SHA; execute `python -m unittest test_continuous` in an isolated temporary directory. Report actual PASS/FAIL or TEST_RUNTIME_UNAVAILABLE; never substitute prose. Compute health with real enabled/end flags and actual owner issue closure. Detect stale blockers, receipt gaps over two hours, expired claims, unresolved effects, duplicates, disabled/finite schedules, repeated failures and near-full control indexes. Tests and quiet gate checks never count as substantive stages.

Worker self-reports are separate from native host telemetry. Without host run history, scheduled-start percentage/host completion remain UNVERIFIED. Model/usage/cost and hard ceilings remain UNVERIFIED unless actual telemetry exposes them. Timers, last_run_time and CI are insufficient substitutes. No autonomous crash takeover is accepted from an expiry test.

Write hourly readbacks, alerts, checks actually run and next action to the existing private status Page. Keep a current three-project table and rolling latest 24 hourly windows; only trim a window after its archived content is retained on the audit Page with readback. Deduplicate UTC hour. Notify changed material failures, recovery or real sponsor decisions; no repeated quiet notifications. Observer may not mutate repos, repair claims, launch workers, change configuration, merge, deploy, access private manuscripts or contact others.
