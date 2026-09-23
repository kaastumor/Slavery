# Wide-angle Project Review — #123

**Project:** Historical Slavery Atlas  
**Repository:** `kaastumor/Slavery`  
**Review date:** 2026-09-23  
**Base main:** `5f1972eb5634461e8eb18386cff75ef40b73c849`  
**Status:** ACTIVE REVIEW — no direction chosen yet

This record is the durable evidence trail for issue #123. It is a horizon review, not a feature plan. Completion of any implementation gate does not imply continuation.

## Review method

Dependency-ordered chunks:

1. repository reality;
2. project thesis/value;
3. foundation/ownership;
4. GitHub/CI/automation/sanitation;
5. adversarial/evaluation quality;
6. external precedents/practice;
7. competing project identities;
8. shrinkage and repairs;
9. final direction.

Each chunk records evidence before a final disposition is allowed.

---

## Chunk 1 — Repository reality

### Snapshot

- canonical branch: `main` at review start `5f1972eb5634461e8eb18386cff75ef40b73c849`;
- open substantive issues: #123 (this review), parent #116, blocked #43, blocked #26;
- open pull requests: none at review start;
- latest M2 integration/adversarial work is merged;
- foundation CI and MVP availability monitor are green at review start;
- repository tree: 379 entries;
- no tracked large-file problem: largest tracked blob is ~363 KB;
- approximately 100 remote branches are visible; many are merged historical topic/auto branches;
- GitHub reports `main.protected=false`; the connected integration cannot read/administer the protected-branch endpoint and repository rulesets returned none.

### Canonical-owner agreement

After the preparatory conformance pass (#143/#144), the current owner documents agree on:

- v0.6.1 remains the immutable canonical historical data release;
- `mvp-preview-ancient-v2` remains non-canonical;
- M2 implementation/adversarial gate is complete;
- #123 is the sole current substantive boundary;
- no H2 expansion, production M2 migration, global geography publication or successor canonical release is authorized before this review.

No competing live project manifest remains.

### Stale / accumulated state

1. **Backlog history is too large for its stated role.**  
   `BACKLOG.md` is canonical execution order but retains long completed P0/P1 narratives. Historical evidence is useful, but much of this belongs in issues/decisions/audits rather than the live queue.

2. **Remote branch accumulation is real.**  
   Old `arch/*`, `auto/*`, `fix/*`, `docs/*`, `feat/*` branches substantially exceed what a short-lived-branch model implies. This is repository hygiene debt, not project knowledge.

3. **Frontend dependency resolution is not lockfile-reproducible.**  
   `web/package.json` pins direct versions, but no tracked `web/package-lock.json` exists. CI/deploy workflows run `npm install --package-lock-only` and then `npm ci`, which resolves transitive dependency state afresh per run.

4. **GitHub Actions are version-tag pinned, not commit-SHA pinned.**  
   This is ordinary practice but weaker supply-chain reproducibility than the project applies to historical datasets/QGIS/Natural Earth. Whether to harden must be proportional to actual project stakes.

5. **Only one scheduled workflow exists:** `MVP Availability Monitor`, every 15 minutes.  
   `MVP Self Heal` is event-triggered from monitor failure and can restart the Supabase project. These are operationally meaningful and must be judged against the current non-user-critical preview horizon, not retained automatically.

6. **No workflow writes commits to main.**  
   Workflows may deploy Pages, mutate external Supabase state in tightly scoped production-promotion/self-heal paths, or write incident issues. Production geometry promotion is triggered only by a specific execution-request path on main.

7. **Generated output is mostly artifact-scoped, not Git-scoped.**  
   Pages snapshots and browser/geometry review packs are retained as Actions artifacts; tracked geometry pilots/fixtures are bounded evidence rather than bulk generated build state.

### Repository-size / sanitation result

- no unexpectedly large tracked blob;
- canonical workbook binary is excluded;
- backups/build outputs are excluded except keep-files;
- sanitation blocks common secret/key/env/dump/cache/merge-marker failure modes;
- sanitation currently does **not** enforce a generic tracked-file size ceiling or local-user path pattern.

### Chunk-1 provisional pressure carried forward

- backlog should likely shrink after the final review;
- old branches should be pruned when an administrative path is available;
- frontend lockfile reproducibility deserves a concrete repair;
- 15-minute monitoring + automatic project restart may be disproportionate for a non-canonical preview with no meaningful user base;
- branch protection is not present according to the branch API and should not be assumed.

**Checkpoint:** repository reality established. No final project direction inferred from this chunk.
