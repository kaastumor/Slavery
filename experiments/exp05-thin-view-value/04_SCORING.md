# EXP-05 scoring

Frozen criteria come from `00_PROTOCOL.md`. No scoring rule was changed after lane
execution.

## Task scores

| Task | Lane | Frozen distinctions | Uncertainty / abstention | Provenance recoverable | Overclaims | Artifacts/pages | Interaction steps | Material advantage? |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: | --- |
| T1 temporal + spatial | A packets | 9/9 | preserved | yes, separate source table | 0 | 4 | 4 | baseline |
| T1 temporal + spatial | B portable | 9/9 | preserved | yes, target/source tables | 0 | 2 | 2 | **yes vs A** |
| T1 temporal + spatial | C thin Atlas | 9/9 | preserved | yes, integrated target detail | 0 | 1 | 6 | **no vs B** |
| T2 network + territory | A packets | 9/9 | preserved | yes, separate source table | 0 | 4 | 4 | baseline |
| T2 network + territory | B portable | 9/9 | preserved | yes, target/source tables | 0 | 2 | 2 | **yes vs A** |
| T2 network + territory | C thin Atlas | 9/9 | preserved | yes, integrated target detail | 0 | 1 | 6 | **no vs B** |
| T3 category + dependency | A packets | 9/9 | preserved | yes, separate source table | 0 | 4 | 4 | baseline |
| T3 category + dependency | B portable | 9/9 | preserved | yes, target/source tables | 0 | 2 | 2 | **yes vs A** |
| T3 category + dependency | C thin Atlas | 9/9 | preserved | yes, integrated target detail | 0 | 1 | 6 | **no vs B** |

“9/9” means all three preregistered distinctions for each of the three cases in that
task were retained. It is a task checklist, not a historical confidence score.

## B versus A

**B materially improves all 3/3 tasks.**

The improvement is not new historical truth. It is a lower comparison/recovery burden:
- one aligned target table replaces three differently structured narrative packets;
- one source-relation table exposes source family/dependency;
- the same correctness, abstention and provenance boundary survives;
- logical navigation drops from four artifacts/lookups to two per task.

This supports the **portable corpus/package** as the useful working comparison form.

## C versus strongest of A/B

**C materially improves 0/3 tasks under the frozen rule.**

C does several things well:
- one browser page contains the whole research surface;
- research stage, frame and temporal state are readable;
- target detail puts claim, abstention, category mapping, geometry warning and
  source/version/dependency together;
- the navigation map did not create false historical geometry;
- no overclaim or missing abstention was observed.

However:
- the task answers are the same as B;
- no additional correctness or uncertainty preservation appears;
- provenance is more pleasant to inspect, but not materially more recoverable than the
  explicit target-id/source-family join in B;
- each three-case task requires six browser interactions versus two logical artifact
  lookups in B;
- the map itself contributes no new historical inference on the frozen tasks.

The one-page versus two-artifact advantage is therefore treated as a readability/
presentation benefit, not enough to outweigh the interaction burden and qualify as a
material task advantage.

## Decision-rule application

Frozen rule:
- C needs material advantage on >=2/3 tasks to earn continued derived-view investment.

Observed:
- B > A: **3/3**
- C > max(A,B): **0/3**
- dangerous UI-induced overclaim: **0**

Protocol branch reached:

> **B improves but C does not → retain the corpus/method and stop application
> expansion beyond maintenance.**

This does not remove the thin preview. It remains a useful safe inspection surface.
It means no richer application/UI horizon is justified from EXP-05.
