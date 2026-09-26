# Overnight controller — 2026-09-26 → 2026-09-27

**Issue:** #291  
**Controller:** one scheduled task, eight hourly occurrences  
**Canonical source:** GitHub `main` + issue #291 marker comments  
**Canonical release:** v0.6.1 unchanged

## Recovery algorithm

On every occurrence:

1. Read current GitHub `main`, BACKLOG, issue #291, all #291 comments, open PRs/issues
   and branches relevant to the programme.
2. Ignore stale assumptions from the scheduled prompt where GitHub differs.
3. Determine the lowest missing exact marker:
   `NIGHT_STAGE_1_COMPLETE` … `NIGHT_STAGE_8_COMPLETE`.
4. Resume that stage from any existing branch/PR/checkpoint. Never duplicate an
   unfinished stage.
5. Complete at least one durable stage when possible. If capacity remains and the next
   stage is contiguous and safe, continue into it. This catch-up rule is deliberate.
6. Write the exact stage marker to #291 only after that stage's done-gate is durable.
7. For CI: one inspection plus at most one bounded follow-up. If still pending, leave
   a precise checkpoint and let the next occurrence resume.
8. Do not create background promises. Finish what can be finished in the occurrence.

## Stage map

1. EXP-14 Trans-Saharan subject packet on one branch.
2. EXP-14 adversarial replay + sanitation + cheap CI + merge + close #290.
3. EXP-10-derived programme closure retrospective/inventory.
4. Five-row post-v2 source/dependency reconciliation.
5. Five-row adversarial cumulative internal review.
6. D-099-compliant packaging gate; merge cumulative review/gate branch.
7. Next-horizon allocation review; freeze at most one horizon if justified.
8. Final QC, BACKLOG reconciliation, morning handoff, final disposition and issue closure.

See issue #291 for exact acceptance criteria and boundaries.

## CI budget

Target <=3 PR cycles total:
- EXP-14 research;
- cumulative review/gate;
- allocation/final handoff.

Text-only research/review changes should use the cheap path introduced by PR #281.
PostGIS is not justified for these programme artifacts.

## Final-run safety

If the final scheduled occurrence arrives with missing earlier markers:
- continue from the lowest missing stage;
- do not fabricate markers;
- write Stage 8 handoff only after truthfully recording incomplete/blocking state;
- use `NIGHT_PROGRAMME_REWORK_REQUIRED` or `NIGHT_PROGRAMME_HOLD` when appropriate.

A missed automation occurrence therefore delays work but does not corrupt stage order.
