# Cross-batch source reconciliation

**Issue:** #257  
**Mode:** consolidation  
**Historical subject research:** none

## Scope

Compared source relations from:
- R1 reviewed rows;
- EXP-04;
- EXP-06;
- EXP-07 qualification;
- EXP-08 completed research.

Exact identity comparison used only:
- `source_version_ref`;
- `independence_group`.

No fuzzy source-title or author matching was promoted to identity.

## Counts

- R1: **45** source relations
- EXP-04: **57**
- EXP-06: **36**
- EXP-07: **15**
- EXP-08: **20**
- total inspected relations: **173**

## Exact cross-origin source overlap

Exactly one cross-experiment source/version overlap was recovered:

- source/version: `doi:10.3406/asean.2013.2272:2013`
- title: *New insights into ‘les interminables listes nominatives d’esclaves’*
- independence group: `angkor-personnel-corpus`
- EXP-04 target: `R1:N:angkor_1200` — Angkor — 1200 CE
- EXP-06 target: `R1:P:1300:F:r1` — Khmer Empire — 1300 CE

The same source family is therefore **not independent evidence across those two rows**.

This is not a claim conflict:
- EXP-04 is a near-anchor Angkor/site-node claim;
- EXP-06 uses 1296–1297 Angkor/Yasodharapura evidence to support a capital/core claim while explicitly withholding empire-wide uniformity.

The correct reconciliation is shared dependency + separate target/anchor inference extent.

## Target-ID overlap

No R1 reviewed target ID is reused by EXP-04/06/08.

Four exact target IDs occur across EXP-07 and EXP-08:
- Great Zimbabwe — 1400;
- Māori communities in Aotearoa — 1700;
- Nobatia — 500 CE;
- Qi — 500 BCE.

These are not competing historical claims:
- EXP-07 owns identity/anchor/frame qualification;
- EXP-08 extends that qualification with subject research for Great Zimbabwe, Māori and Nobatia;
- Qi remains qualification-complete but EXP-08 subject research is frozen/unstarted.

No later artifact silently rewrites the earlier qualification decision.

## Limits

This reconciliation proves only **exact identifier/dependency overlap**.

Potential hidden aliases may remain where:
- the same work is cited through different editions/DOIs/URLs;
- source titles vary;
- a modern synthesis silently reuses an older evidentiary chain without the same independence-group label.

Project rules prohibit inferring those aliases without evidence. A future review may normalize them when a concrete dependency is demonstrated.

## Disposition

**Cross-batch source state is coherent enough for a review tranche.**

One shared Angkor/Khmer source family must remain explicit during any cumulative review.
No evidence justifies new source-identity infrastructure or a graph layer.
