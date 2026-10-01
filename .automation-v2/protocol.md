# Automation control v2 — bounded native pilot

Contract: AUTOMATION_CONTROL_V2_20261001. This operational branch is not accepted application state or a second task queue. BACKLOG and existing issues/PRs continue to own all substantive work. Never merge this branch into main. Existing project gates remain binding. This implementation coordinates compliant scheduled workers; GitHub permissions do not forbid an unrelated identity from bypassing it.

## Entry and eligibility
Read the exact control branch ref, then fetch state.json and controller.py at that SHA under .automation-v2/. Verify contract/repository and actual Python execution. Run controller.py with saved JSON state and request files. No Python/controller access means read-only inspection and a changed capability blocker, no project mutation. A prompt cannot select a model, enforce cost or prove host termination.
Before a claim, inspect live BACKLOG, main, pending PRs and existing owner receipts. Resume first; honor interactive owners and older task runs that may not use this protocol. Unknown pending inventory blocks intake. Broad allocation at most once per Amsterdam date. No useful delta => NO_CHANGE without changing control state or adding comments. A changed real blocker may earn one bounded reconciliation stage, ending BLOCKED or WAITING_EXTERNAL.

## Atomic publication
Every transition uses the controller, then:
1. Fetch control ref H and the commit/tree for H; read state at H.
2. Build a blob for candidate state and a tree preserving H's other entries.
3. Create a commit with EXACTLY ONE parent H. Never add a second parent, merge or rebase a losing claim.
4. update_ref(branch_name="automation/control-v2-20261001", sha=candidate, force=false).
5. Independently read ref and state back. Success response alone is not ownership.
For sibling commits from the same H, only one fast-forward can win. A rejected claim is a lost race: reread, report BUSY/NO_CHANGE and stop. An ambiguous update requires readback before one bounded transient retry; never force. Preserve preexisting state on every failure.

## Owning a stage
Use stable repository + public issue number + stage name + fixed input SHA + contract identity. Attempt IDs are separate. claim increments generation and grants a 30-minute lease; start moves CLAIMED to ACTIVE. Publish/read back each. Target 20 minutes including checkpoint (advisory host bound), one coherent stage. Before EACH effect reread state/ref and fence owner_attempt, generation and lease. Interactive/older workers remain an additional owner check.
Publish an intent with stable operation ID, allowed action, target ref and expected head before branch/PR/issue effects. Only isolated branch edits, draft PR preparation, canonical issue checkpoints and reads are allowed. Main writes, merges, DB writes, deployment, deletion, purchases, contacts and private-source transfers remain prohibited. Protect the actual target revision too; never force it.
After effects, independently inspect exact output and call verified. Never replay an ambiguous operation; inspect actual artifacts and stable receipt markers. Verified effects survive CHECKPOINTED resume and cannot be reissued under the same ID. One stage has at most eight effects; batch changes.

## Finish and recovery
Write one meaningful receipt to its existing public owner, deduplicated by contract/stage key/operation marker; verify readback. finish records COMPLETE/CHECKPOINTED/BLOCKED/FAILED_RETRYABLE/WAITING_EXTERNAL/NEEDS_REVIEW, receipt URL, actual checks and next action. Execution completion never means accepted, merged, human-approved or historically admitted. Telemetry unavailable => UNKNOWN.
Resume CHECKPOINTED with a new generation, same fixed stage/input and retained verified effects. Two identical failed stages stop retries until a real prerequisite changes. Unchanged gates remain quiet. dependency_changed=true needs actual new re-entry evidence OR an explicitly recorded, separately eligible nonconflicting alternative; never an elapsed timer.
An expired CLAIMED/ACTIVE lease returns RECONCILE_EXPIRED, not permission to steal. Read outputs; if actual host termination and safe effect reconciliation cannot be established, stop mutations and report NEEDS_REVIEW. Do not silently reset the state. This pilot has no independently verified unattended crash-takeover backend.

## Bounded memory
Max 8 KiB and 16 receipt refs. Before index exhaustion, compact only COMPLETE old receipts. Independently read back the exact pre-compaction state at its immutable control commit SHA; pass its GitHub blob URL to compact. Unresolved and current-stage receipts remain. archive_ref links the preceding complete state, which retains earlier archive links. Before any later claim, reconcile the proposed key against archives/canonical receipts and set archive_checked=true only after that check. If safe compaction or deduplication is unavailable, stop intake; never discard unresolved evidence. Do not change controller code, schedules, enabled roles, models or budgets from a scheduled invocation.
