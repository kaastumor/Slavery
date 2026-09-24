# EXP-06 Candidate v1

**Status:** **PUBLISH_CANDIDATE approved** — non-canonical research candidate  
**Gate:** issue #227 — decision recorded in `REVIEW_DECISION.md`  
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

Issue #227 returned **PUBLISH_CANDIDATE** after a bounded browser/human-facing review.

The candidate may be deployed through the existing static Pages path as an explicitly
non-canonical research candidate. See `REVIEW_DECISION.md` for the exact reviewed
commit/run/artifact and the bounded rework history.

No candidate decision changes canonical v0.6.1.
