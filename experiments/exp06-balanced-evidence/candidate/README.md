# EXP-06 Candidate v1

**Status:** non-canonical research candidate  
**Gate:** issue #227 — PUBLISH_CANDIDATE / HOLD_NO_RELEASE / REWORK  
**Historical source commit:** `16906affed159722cf940e6723401c7ab4e5d9f4`  
**Canonical historical release:** **v0.6.1 remains unchanged**

This directory freezes the completed EXP-06 six-case evidence tranche as a candidate
for human-facing publication.

It is **not** a new canonical data release and does not mutate the R1 reviewed candidate
registry.

## Candidate contents

- `targets_extended.csv` — exact frozen EXP-06 portable target rows;
- `source_relations.csv` — exact frozen EXP-06 claim/source relations;
- `QC_SUMMARY.md` — candidate QC and release-boundary checks;
- `UNRESOLVED_ISSUES.md` — material limitations carried into review;
- `manifest.json` — exact identity, counts and SHA-256 checksums.

The browser surface is generated separately as
`web/public/data/exp06-candidate.json` and rendered by
`web/exp06-candidate.html`.

## Research states

The six rows intentionally do not collapse to a positive/negative binary:

- **3 bounded internally researched:** Later Maya/Mayapán, Mongol Yam, Khmer capital/core;
- **1 researched inconclusive:** Yaghan internal practice at 1800;
- **2 under review:** Chámpa polity identity at 500 CE and exact Haryanka chronology at 500 BCE;
- **0 independently historically reviewed.**

Under review and researched inconclusive do **not** mean absence.

## Map semantics

The candidate map is context/navigation only.

Markers:
- are fixed-size reference locators;
- do not define historical territory;
- do not define practice extent;
- do not encode P0–P4 or prevalence;
- do not use source counts as intensity.

No historical practice polygon is materialized.

## Release decision

Only issue #227 may decide:

- **PUBLISH_CANDIDATE** — publish this explicitly non-canonical candidate;
- **HOLD_NO_RELEASE** — preserve the exact candidate but do not publish it;
- **REWORK** — fix only concrete release-blocking defects and rerun the gate.

No candidate decision changes canonical v0.6.1.
