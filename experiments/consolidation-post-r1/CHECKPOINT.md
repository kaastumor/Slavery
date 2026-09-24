# Cross-batch consolidation checkpoint

**Issue:** #257  
**State:** reconciliation complete; result ready for merge  
**Mode:** consolidation  
**Disposition:** **REVIEW_RELEASE_CANDIDATE**

Artifacts:
- `01_RESEARCH_INVENTORY.csv`
- `01_RESEARCH_INVENTORY_SUMMARY.json`
- `02_SOURCE_RECONCILIATION.md`
- `03_REVIEW_CAPACITY.md`
- `UNRESOLVED_ISSUES.md`
- `RESULT.md`

Key counts:
- 41 unique targets;
- 19 R1 internally adversarially reviewed;
- 12 post-R1 researched internal;
- 5 post-R1 under review;
- 3 qualification-ready unresearched;
- 1 identity/time hold;
- 1 EXP-08 frozen/unstarted;
- 0 independent historical reviews.

Cross-origin exact source overlap:
- one family: `angkor-personnel-corpus` / Lustig & Lustig 2013.

## Next exact mode/action

After merge, close #257 and enter **review/release mode**.

Freeze the 17 post-R1 subject-research target IDs as one cumulative internal review
tranche. Review existing evidence only; do not admit new targets or resume Qi.

Goal: either produce a coherent non-canonical cumulative review candidate or HOLD with
explicit unresolved review debt.
