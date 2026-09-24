# EXP-06 Candidate v1 — Review Decision

**Gate:** #227  
**Disposition:** **PUBLISH_CANDIDATE**  
**Date:** 2026-09-24  
**Canonical historical release:** **v0.6.1 remains unchanged**

## Exact candidate reviewed

Historical source commit:

`16906affed159722cf940e6723401c7ab4e5d9f4`

Candidate browser-review head:

`9d47b4c4be1d10697868205af43f8137f61d1826`

Successful browser review:
- workflow run: `36054132409`
- browser job: `107816768565`
- evidence artifact: `10831472682`
- candidate data: 6 targets / 36 source relations
- research states: 3 bounded internal / 1 researched inconclusive / 2 under review
- independent historical reviews: 0

## Review history

The first browser pass found:
1. a brittle automation assertion caused by CSS uppercase rendering; this was a test
   defect, not missing candidate content;
2. one real usability defect: at 768 px the map and evidence register remained
   side-by-side, making the register unnecessarily cramped.

Authorized rework was limited to that release blocker:
- candidate layout now stacks map and register below 820 px;
- browser assertions compare rendered text robustly.

The exact candidate was then rerun.

## Browser / human-facing review

PASS.

The successful rerun produced:
- zero page errors;
- zero semantic assertion failures;
- desktop overview screenshot;
- narrow-screen/mobile overview screenshot;
- one full-page detail screenshot for each of the six targets.

Visual inspection confirmed:
- the candidate/non-canonical boundary is prominent;
- v0.6.1 is visibly still canonical;
- under-review, researched-inconclusive and bounded-internal states are visually
  distinct;
- Chámpa and Magadha do not read as absence;
- Yaghan is visibly inconclusive rather than negative;
- bounded proposition and required abstention are prominent in target detail;
- evidence locus and inference extent remain separate;
- source/version/dependency information remains inspectable;
- map markers read as fixed navigation/context points, not practice extent;
- the corrected narrow-screen layout is coherent enough for candidate publication.

## Non-blocking observations

- Neutral Natural Earth land remains an external runtime asset, as in the existing
  thin preview. It carries no historical claim.
- The candidate is evidence-dense; this is appropriate for a research candidate and
  is not evidence for general-public usability.
- Historical geometry remains unresolved/reference-only.
- No external or independent historical review has occurred.

## Why PUBLISH_CANDIDATE

No release-blocking defect remains after the bounded responsive-layout repair.

Publishing this candidate adds a stable, inspectable human-facing artifact for the
completed EXP-06 evidence tranche while preserving all material uncertainty. Holding
it would provide little additional protection because the candidate is explicit about
its non-canonical/internal status and does not expose draft data as canonical truth.

## Meaning of publication

**PUBLISH_CANDIDATE means only:**
- preserve the exact candidate package in the repository;
- deploy the candidate page through the existing static Pages path;
- make it available as an explicitly non-canonical research candidate.

It does **not**:
- replace canonical v0.6.1;
- change R1 review state;
- assign P0–P4;
- create reviewed historical geometry;
- establish external demand, usability or independent historical validity.

## Next boundary

After publication and deployment verification, close #227. Historical research may
resume under a separately selected bounded horizon. Candidate publication itself does
not authorize a new product/application horizon.
