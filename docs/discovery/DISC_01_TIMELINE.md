# DISC-01 — Timeline interaction versus discrete-anchor baseline

**Issue:** #184  
**Parent:** #183  
**Stage:** pre-registered before precedent review/prototyping  
**Date:** 2026-09-24  
**Production implementation authorized:** no

## Question

Does a richer timeline materially improve a real Historical Slavery Atlas task over the technical MVP's current discrete frozen-anchor navigation plus per-record temporal precision guard?

## Concrete task

A user wants to answer:

> **Across several historically different reviewed cases, what can I safely say at the selected research anchor, and which apparent time differences are only period-level / near-anchor / unknown rather than exact-year evidence?**

The task is deliberately about temporal interpretation, not visual spectacle.

Test cases must include at least:
- Middle Kingdom of Egypt — period-level support;
- Carthage — period-level support;
- Gao — near-anchor / approximate;
- United States 1800 — exact cross-section;
- Chimú — period-level support;
- one selected-year-unknown row such as Teotihuacan.

## Strongest boring baseline

The existing MVP:

1. discrete navigation over frozen research anchors only;
2. target register filtered to the selected anchor;
3. each reviewed target displays one explicit temporal state:
   - exact cross-section;
   - period-level support;
   - near-anchor / approximate;
   - unknown;
   - aggregate / not-applicable;
4. each detail record displays the human-readable temporal guard;
5. source-native BCE display remains separate from Atlas astronomical internal year.

This baseline is intentionally strong. A richer timeline must beat it rather than merely look richer.

## Candidate richer interaction

The smallest candidate concept is **not** a production timeline.

For the experiment only, consider a horizontal temporal overview that could show:
- frozen anchors as discrete positions;
- reviewed targets attached to those anchors;
- temporal-support category encoded directly on each item;
- optional period/near-anchor extents only when already present in reviewed evidence.

No inferred continuous interval may be created from an anchor alone.

## Predeclared kill rule

**REJECT** richer timeline interaction if any of the following holds:

1. it does not materially reduce interpretation/navigation burden on at least **two independent test tasks** compared with the boring baseline;
2. its main benefit is aesthetic or “seeing time” rather than a concrete correctness/comparison gain;
3. it requires fabricating start/end dates or continuous validity intervals not present in R1;
4. it makes period-level or near-anchor evidence look more exact than the baseline;
5. it needs a new timeline library/service/data model merely to reproduce information already clear in the register.

A small result may be **REVISE** rather than reject only if one narrower temporal affordance clearly solves a repeated task while the full timeline does not.

## Evidence collection plan

1. inspect a small set of external timeline/map precedents for interaction patterns and known precision risks;
2. derive the actual frozen anchor/temporal-state distribution from the MVP candidate;
3. run two or more concrete comparison tasks against:
   - A: current discrete-anchor/register baseline;
   - B: a non-production paper/data prototype of richer timeline semantics;
4. record:
   - steps/operations;
   - temporal distinctions exposed;
   - new ambiguity introduced;
   - extra data assumptions required;
5. attack the provisional result for false precision and feature attraction.

## Allowed dispositions

Exactly one final disposition:
- ADOPT_FOR_EXPERIMENT
- REVISE
- REJECT
- PARK

Even ADOPT_FOR_EXPERIMENT does not authorize production implementation.
