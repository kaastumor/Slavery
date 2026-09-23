# COV-004 — Setup Adversary

**Issue:** #157  
**Historical research started:** no  
**Disposition:** **REVISE, THEN PROCEED**

This adversary attacks the design before any new historical subject research.

## Attack 1 — Four arms create too many chances to declare victory

**Severity: critical.**

A multi-arm experiment can become a narrative buffet: one positive result offsets three weak ones.

**Repair:**
- arms are independent;
- no aggregate score;
- the overall outcome matrix is frozen;
- Atlas success cannot rescue a failed escalation or non-polity method;
- tiering success cannot rescue a failed Atlas arm.

**Disposition after repair: survives.**

---

## Attack 2 — “Masked” review is not independent

The same project/model has already seen C1/C2 outcomes.

**Severity: high.**

A masked packet reduces direct anchoring but does not create genuine evaluator independence.

**Repair:**
- call it masked replay, not independent review;
- prohibit claims about inter-rater reliability;
- compare only whether the replay finds materially different bounded conclusions;
- if a later independent reviewer becomes available, treat that as stronger evidence, not a requirement for this bounded experiment.

**Disposition: survives with limitation.**

---

## Attack 3 — deep-auditing all escalated cases and only six non-escalated can bias the false-negative rate

**Severity: high.**

The escalated set is selected for difficulty.

**Repair:**
- false-negative calibration uses only the six previously non-escalated rows;
- escalated rows are evaluated separately only for “was escalation useful?”;
- never combine the two denominators.

**Disposition: survives.**

---

## Attack 4 — non-polity classes can be cherry-picked around slavery-rich famous cases

**Severity: critical.**

Choosing Zanzibar, plantations, slave ports, etc. would make the test trivial.

**Repair:**
- freeze candidate lists from non-slavery historical reference sources;
- record the source-native candidate list before subject research;
- deterministic target selection within each class;
- no substitution after slavery evidence is seen.

**Disposition: survives only with strict freeze.**

---

## Attack 5 — frame classes themselves encode an ontology answer

“node/site”, “institution/estate”, “mobile/network”, “region/community” are already a designed taxonomy.

**Severity: medium-high.**

**Repair:**
- treat them as experimental frame classes, not canonical ontology;
- allow a target to fail the class;
- record `frame_class_mismatch` instead of forcing fit;
- no schema canonization from COV-004.

**Disposition: survives.**

---

## Attack 6 — the time-split test can cherry-pick rows with known recent literature

**Severity: critical.**

**Repair:**
- freeze cutoff first;
- select rows deterministically from the eligible pool **before** any 2016–2026 target search;
- eligibility depends only on pre-2016 reconstructibility, not on known later scholarship;
- no replacement if no later source is found.

**Disposition: survives.**

---

## Attack 7 — 2015 is arbitrary

**Severity: medium.**

It could accidentally favor or suppress updates.

**Repair:**
- 2015 is chosen before target selection because it leaves a ten-year later window while allowing mature digital scholarship;
- no claims that it is the optimal cutoff;
- a future replication could use another cutoff.

**Disposition: survives.**

---

## Attack 8 — Atlas tasks are spatial by construction, so the Atlas is guaranteed to win

**Severity: critical.**

This is the most serious threat to the Atlas arm.

**Repair:**
- baseline includes a competent conventional static GIS/map using the same geometries;
- Atlas gets no credit merely for showing locations;
- tasks require evidence-semantic distinctions layered onto spatial/time context;
- D5 is a negative control where map value should be negligible;
- at least 2/4 gains must be **material**, not cosmetic.

**Disposition: survives after repair.**

---

## Attack 9 — Atlas can win by having richer interaction rather than better reasoning

**Severity: high.**

**Repair:**
- both arms use identical evidence and geometry;
- count a win only when the Atlas reduces a real reconstruction step or prevents a misleading inference;
- hover, animation, color and convenience alone do not count.

**Disposition: survives.**

---

## Attack 10 — ordinary baseline is still too weak if it lacks layer-aware symbology

**Severity: critical.**

A competent GIS user can map separate categories.

**Repair:**
- baseline may use conventional layer/symbol conventions for points/areas/routes and outcome;
- baseline may filter by time and frame class;
- the Atlas must earn value specifically from **claim-layer semantics + inference boundaries + research state + geometry certainty** being linked in one inspection path.

**Disposition: survives.**

---

## Attack 11 — forcing non-polity cases onto a map may recreate the very false territorialization the method is meant to avoid

**Severity: critical.**

**Repair:**
- geometry can be point, route, fuzzy region or unresolved;
- no mandatory polygon;
- unresolved geometry is a legitimate visible state;
- any false territorialization is an Atlas-arm failure, not a fix-later item.

**Disposition: survives.**

---

## Attack 12 — D1–D4 can be instantiated after seeing outcomes and cherry-picked

**Severity: critical.**

**Repair:**
- task families are frozen now;
- after non-polity targets are frozen but before historical outcomes are evaluated, instantiate tasks using only target/frame/geometry metadata;
- if no target fits a task family without using slavery evidence, mark the task unavailable rather than selecting post hoc.

**Disposition: survives.**

---

## Attack 13 — old C1 rows have known source-quality problems

Chandela already has a weak source issue; Zhu exposed shared temporal overreach.

**Severity: high.**

**Repair:**
- Arm A is allowed to find and count these;
- known problems are not silently repaired before audit;
- the masked reviewer packet preserves source quality as encountered;
- known COV-003 next-release review items remain eligible failures.

**Disposition: survives.**

---

## Attack 14 — if Arm A fails, the rest of the experiment becomes wasted work

**Severity: medium.**

**Repair:**
- execute A first.
- If escalation calibration fails catastrophically (>2/6 material false negatives or any repeated safety-critical pattern), pause before new non-polity subject research and revise the tiering method.
- If A narrowly fails at 2/6, complete B only if the failure suggests a repairable trigger issue rather than schema collapse.

This creates an early stop.

**Disposition: survives.**

---

## Attack 15 — the Atlas concept is being treated as a sidecar instead of the project’s original hypothesis

**Severity: high.**

The sponsor explicitly warned against abandoning it too early.

**Repair:**
- D is a first-class independent arm, not an optional visualization appendix;
- H2's negative result remains valid for the old thin-view setup;
- COV-004 explicitly tests whether the **new tiered evidence + non-polity geometry model** changes the value proposition;
- if D passes, the thin Atlas hypothesis is reopened even though the old application platform remains stopped.

**Disposition: survives.**

---

# Setup-adversary conclusion

**PROCEED, with sequencing constraints.**

Execution order is frozen:

1. freeze Arm A audit sample;
2. run Arm A masked replay;
3. apply early-stop rule;
4. freeze neutral non-polity candidate lists and deterministic targets;
5. instantiate D1–D5 from target/frame/geometry metadata **before subject outcomes**;
6. run B subject research;
7. freeze time-split eligible pool and six targets before later-source searches;
8. run C;
9. build baseline B and Atlas A from identical frozen evidence/geometry;
10. evaluate D;
11. run a final result adversary;
12. reconcile governance.

No new historical subject research may begin before this file is committed.
