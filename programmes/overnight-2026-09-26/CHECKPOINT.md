# Overnight programme checkpoint — terminal handoff

**Controller issue:** #291  
**Substantive stages:** 1–7 complete  
**Stage 8:** final QC/handoff prepared; completion requires this final PR to merge,
then the exact `NIGHT_STAGE_8_COMPLETE` marker and issue closure  
**Candidate:** `post-r1-cumulative-review-v3-cross-frame`  
**Next horizon:** #297 — EXP-15 neutral node-site C0 qualification  
**Canonical release:** v0.6.1 unchanged  
**Independent historical review:** 0

## Final disposition

**NIGHT_PROGRAMME_COMPLETE** after the final merge/marker/closure gate.

The scheduler created for the mistaken future date has been disabled. The work was
executed interactively instead.

## Post-merge closure

1. record `NIGHT_STAGE_8_COMPLETE` exactly once;
2. close #291 as completed;
3. reconcile the private execution ledger to Runs 1–8 terminal DONE with no pending
   GitHub reconciliation;
4. verify no programme PR remains open.
