# Overnight ready-queue — final handoff

Controller: #262  
Final disposition: **OVERNIGHT_CANDIDATE_READY**  
Canonical historical release: **v0.6.1 unchanged**  
Independent historical reviews: **0**  
Automatic publication: **not authorized**

## What was completed

The sponsor-authorized four-case ready queue was carried through the full controller:

1. subject research for all four authorized targets;
2. four-case source/claim reconciliation;
3. frozen internal adversarial cumulative review;
4. integration into a new successor noncanonical candidate;
5. final repository/candidate QC.

No fifth target was added.

## Four case outcomes

### Qi — 500 BCE

**Internally reviewed bounded evidence state.**

Exact Qi territorial slavery/servitude remains **researched-inconclusive**.

The Yue Shifu textual tradition preserves near-anchor evidence of redeemable personal
servitude/dependency, but the principal episode is at Zhongmou during Yan Ying's
journey to Jin and is not promoted into Qi territorial practice. Parallel textual
witnesses remain one dependency family.

### Swahili maritime trade network — 1400

**Internally reviewed network-positive evidence state.**

Persistent medieval slave-trade participation around the 1400 horizon is supported at
the **network** dimension. Kilwa and Songo Mnara provide bounded node-level local
slavery evidence.

Participation by every port, coast-wide territorial prevalence, uniformity and exact
network volume remain unresolved.

### Ifugao communities — 1700

**Internally reviewed exact-anchor inconclusive evidence state.**

Exact-1700 slavery/status remains **researched-inconclusive**.

Later traditional child sale, debt bondage, captivity and slaveholding are supported
context, but early-twentieth-century ethnography is not projected backward to 1700.
Exact-period archaeological hierarchy/social differentiation is not treated as
slave-status proof.

### Khanate of Kokand — 1800

**Internally reviewed exact-anchor inconclusive evidence state.**

Exact-1800 slavery/slave-trade practice remains **researched-inconclusive**.

Kokand-specific slavery and captive enslavement are supported in the early nineteenth
century, but verified 1820s/1830s evidence is not projected backward to 1800.
Bukhara/Khiva evidence is not substituted for Kokand.

## Review result

Stage 6 disposition:
**FOUR_CASE_INTERNAL_REVIEW_PASS**.

Per-row:
- 4 `ACCEPT_INTERNAL_REVIEW`;
- 0 `NARROW_AND_ACCEPT`;
- 0 `HOLD_EXISTING_EVIDENCE`;
- 0 `REJECT_ARTIFACT`.

This means all four **bounded evidence states** survived internal replay. It does not
mean four positive slavery classifications.

## Successor candidate

Candidate:
`reviews/post-r1-cumulative/candidate-v2-overnight/`

State:
- 21 total members;
- 16 internally accepted evidence states;
- 5 explicit HOLD rows;
- 133 source relations by pinned lineage;
- 2 exact cross-target source-version overlaps;
- 0 independent historical reviews.

Predecessor:
`reviews/post-r1-cumulative/candidate/`
(`post-r1-cumulative-review-v1`)

The predecessor remains unchanged.

## Exact unresolved blockers / uncertainties

Preserved predecessor HOLDs:
1. Indus Valley Civilization — 2000 BCE;
2. Hadhramaut — 500 BCE;
3. Cuzco — 1300 CE;
4. Chámpa — 500 CE;
5. Magadha–Haryanka — 500 BCE.

Accepted overnight rows also retain material uncertainty:
- Qi: exact territorial occurrence/status/institution/prevalence unresolved;
- Swahili: every-node participation, coast-wide prevalence and exact volume unresolved;
- Ifugao: exact-1700 status and continuity from later ethnography unresolved;
- Kokand: exact-1800 practice unresolved.

Cross-row exact-version dependencies:
- Angkor 1200 ↔ Khmer 1300: Lustig & Lustig 2013 /
  `angkor-personnel-corpus`;
- Great Zimbabwe 1400 ↔ Swahili 1400: Ibn Battuta Kilwa 1331 /
  Freeman-Grenville translation chain.

These are not independent corroborations across the paired rows.

## Final QC

Final sanitation/reconciliation pass:
- 21 unique member IDs;
- no accepted/HOLD duplicate IDs;
- accepted and HOLD CSV schemas structurally uniform;
- 133 source relations reconstructed;
- 0 missing source/version refs;
- 0 missing independence groups;
- 0 missing claim-fitness fields;
- 0 within-target duplicate exact source versions;
- 2 expected cross-target exact source-version overlaps;
- predecessor core blob identities unchanged;
- one exact completion marker exists for every Stage 1–7 before the final gate.

Stage 7 `foundation-ci` succeeded. The Stage 8 PR must pass its normal cheap
sanitation/Python regression gate before merge.

## Release boundary

Nothing in this programme changes:
- canonical v0.6.1;
- frozen R1 reviewed state;
- P0–P4;
- historical-practice geometry;
- database/API;
- schema/ontology;
- public release status.

No independent historical review is claimed.

## Next justified D-096 mode

**Maintenance / trigger-bound review.**

The project has completed the authorized queue and has a reviewed successor candidate.
Another intake tranche is not automatically justified by remaining capacity.

Reopen active work on a concrete trigger: sponsor-authorized bounded intake,
independent review, a real consumer/publication need, a demonstrated candidate defect,
new evidence satisfying a HOLD/reopen condition, or a production/release requirement.
