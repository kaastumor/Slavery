# Overnight programme checkpoint

**Controller issue:** #291  
**Architecture state:** scheduled-write repair completed before first scheduled run  
**Scheduled GitHub mode:** read-only  
**Private ledger:** persistent connected Google Drive document; interactive write/read-back verified  
**Run state:** Runs 1–8 all `PENDING`  
**Any `IN_PROGRESS` slot:** no  
**Substantive scheduled work performed:** no  
**Canonical release:** v0.6.1 unchanged

## Interactive verification

Interactive GitHub mutation succeeded in the sponsor session. This establishes only
that interactive writes work; scheduled runs are deliberately not allowed to depend on
GitHub mutation.

## Recovery invariant

The next scheduled invocation must:
1. read GitHub canonical state;
2. read the private execution ledger;
3. claim Run 1 as `IN_PROGRESS` in the ledger before any research;
4. stop if that ledger write fails;
5. execute Run 1 only;
6. terminate Run 1 privately and flag GitHub reconciliation pending.

No `NIGHT_STAGE_N_COMPLETE` marker should be written by scheduled context.

## Immediate slot

Run 1 — EXP-14 Trans-Saharan 1300 bounded subject packet.

Do not pre-create later-stage branches or perform scheduled GitHub writes.
