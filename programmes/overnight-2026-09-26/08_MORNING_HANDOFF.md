# Corrected morning handoff — Historical Slavery Atlas

**Controller:** #291  
**Campaign:** eight-stage overnight programme completed interactively after the
scheduling-date error  
**Final disposition after green final merge:** **NIGHT_PROGRAMME_COMPLETE**

## What the campaign accomplished

### 1–2. EXP-14 Trans-Saharan 1300

Result: **BOUNDED_SUPPORTED**.

The target now has direct evidence bridging enslaved status to actual movement through
the network: Ibn Battuta's 1353 northbound caravan carried 600 female slaves from the
central Sudan toward Morocco.

The claim remains bounded:
- direct route evidence is strongest in the mid-fourteenth century;
- specialist synthesis places the slave-trading system across the broader medieval
  period spanning 1300;
- no exact-1300 volume;
- no annualization of 600;
- no all-route uniformity;
- no territorial-slavery inference from network participation.

PR #295 merged and #290 closed.

### 3. EXP-10-derived programme closure

All four neutrally qualified EXP-10 rows now have subject outcomes:
- Karnak 1000 BCE — researched-inconclusive;
- Tōdai-ji 800 — bounded-supported near-anchor legally non-free status;
- Sápmi 1600 — bounded-supported state coercion; internal slavery unresolved;
- Trans-Saharan 1300 — bounded-supported network participation.

The method discriminated between cases rather than mechanically producing a positive or
negative result. No schema/ontology extension was needed.

### 4. Source/dependency reconciliation

Five post-v2 rows were reconciled:
- Lithuania;
- Karnak;
- Sápmi;
- Tōdai-ji;
- Trans-Saharan.

Result:
- 33 post-v2 source relations;
- 0 missing source versions;
- 0 missing independence groups;
- 0 missing claim-fitness fields;
- 0 exact post-v2 source-version overlaps with v2;
- 0 exact cross-target overlaps among the five post-v2 rows.

### 5. Cumulative internal review

Result: **FIVE_ROW_INTERNAL_REVIEW_PASS**.

All five bounded evidence states receive `ACCEPT_INTERNAL_REVIEW`.

Acceptance does not mean five positive slavery classifications:
- Karnak remains inconclusive at the selected anchor;
- Sápmi remains dimensionally bounded coercion rather than internal-slavery evidence.

Independent historical review remains **0**.

### 6. D-099 packaging gate

Result: **BUILD_SUCCESSOR_CANDIDATE**.

The earlier small deltas correctly remained separate. Five reconciled reviewed rows plus
closure of EXP-10 now make cumulative packaging useful rather than version churn.

New candidate:
`post-r1-cumulative-review-v3-cross-frame`

Counts:
- 26 members;
- 21 internally accepted bounded evidence states;
- 5 HOLDs;
- 166 source relations;
- 2 preserved exact cross-target dependencies;
- 0 independent historical reviews.

Candidate v2 remains immutable.

### 7. Next horizon

Frozen as #297 / **EXP-15 neutral node-site C0 qualification**:
- Samarkand 1400;
- Timbuktu 1500;
- Tenochtitlan 1500.

This is qualification only. No slavery/coercion subject research has begun.

## What did not change

- canonical historical release remains **v0.6.1**;
- no P-level changed;
- no historical-practice geometry was promoted;
- no R1 reviewed state changed;
- no schema/ontology/database/API/frontend change;
- no public release was made;
- no independent review was claimed;
- the five existing v2 HOLD rows remain HOLD.

## Next WIP

#297 — EXP-15 neutral node-site qualification tranche.

The next action is neutral identity/chronology/frame/spatial qualification of the three
frozen nodes. Subject slavery/coercion research remains outside that issue.
