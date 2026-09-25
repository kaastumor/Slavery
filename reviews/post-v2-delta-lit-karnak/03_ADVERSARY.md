# Post-v2 Lithuania/Karnak delta — internal adversarial review

**Issue:** #278  
**Mode:** review / release  
**Review type:** internal replay; not independent historical review  
**New historical/source research:** none  
**Frozen base:** `c4d5d11f273e9ceed7e4215fbf9d7c195221fddc`

## Attack 1 — Lithuania is really a broad-period reconstruction, not a 1300 observation

Correct.

The EXP-09 packet does not claim an exact-year roster or statute. Its positive basis is
a specialist reconstruction placing a separately identified unfree household/slave
population in grand-ducal court structures across the late thirteenth and fourteenth
centuries.

The packet also excludes:
- ordinary tribute/labour obligations;
- later 1529 statutory categories and mature serfdom;
- whole-polity prevalence.

**Disposition:** `ACCEPT_INTERNAL_REVIEW`.

The temporal formulation is already narrow enough: institutional presence **around the
1300 horizon**, not an invented exact-year event.

## Attack 2 — Lithuania's raid/captive evidence inflates capture into slavery

Rejected.

The packet explicitly treats the near-anchor Jeroschin raid episode as capture/forced
movement context. Nikžentaitis is used to show that captive treatment changed over
time and blocks `captive = slave` as a default rule.

The positive claim rests on the separately identified court unfree-household category.

**Disposition:** survives.

## Attack 3 — Lithuania generalizes one court structure to the Grand Duchy

Rejected after scope review.

The target row limits inference to institutional presence in **at least part of the
grand-ducal court/domain economy** and explicitly notes uneven direct ducal control.

No polity-wide prevalence or practice polygon follows.

**Disposition:** survives.

## Attack 4 — Lithuania source independence is overstated

Rejected.

- Jeroschin / Peter of Dusburg remains one chronicle family.
- VLE explicitly derives category history from Jurginis 1960.
- later Dambrauskaitė evidence is a temporal negative control, not an independent
  anchor attestation.

The positive result does not depend on source counts.

**Disposition:** survives.

## Attack 5 — Karnak should be positive because New Kingdom Amun captive labour is strong

Rejected.

That is exactly the temporal-leakage trap EXP-11 was designed to test.

The packet establishes:
- earlier New Kingdom target-positive captive/enslaved labour;
- near-anchor Amun institutional continuity;
- near-anchor subordinate/service/property context.

It does not establish continuity of a specific slave/unfree labour institution through
the New Kingdom → Third Intermediate transition.

**Disposition:** `ACCEPT_INTERNAL_REVIEW` for the researched-inconclusive selected
anchor state.

## Attack 6 — Karnak's `bꜣk.w` or foreign population should resolve the status

Rejected.

The Banishment Stela context is political/service/exile and its terminology is
polysemous. The Asiatic domestic population at Karnak has no securely identified
slave/property status in the reviewed evidence.

Neither source permits:
- `bꜣk.w = slave` automatically;
- foreign/Asiatic = slave.

**Disposition:** survives.

## Attack 7 — Amun-priestly perpetual-service transactions prove temple labour

Rejected.

The packet preserves institution/owner/locus distinctions. Muhs's clearest perpetual
service transaction concerns Amun-priestly family/property context and personnel linked
to Abydos; it is not silently converted into Temple-of-Amun workforce evidence.

**Disposition:** survives.

## Attack 8 — Karnak's inconclusive row should stay outside reviewed material

Rejected under established project semantics.

Internal review validates a bounded evidence state, not only a positive slavery
classification. The Karnak packet is complete, reconstructible, explicit about what
would reopen the claim, and does not use inconclusive as absence.

This is the same review principle already applied to Great Zimbabwe, Yaghan, Qi,
Ifugao and Kokand.

**Disposition:** `ACCEPT_INTERNAL_REVIEW`.

## Attack 9 — the two rows may hide source overlap with v2 or each other

Deterministic reconciliation found:
- v2 source lineage reconstructs to **133** relations;
- delta adds **12** relations;
- 0 missing source-version refs;
- 0 missing independence groups;
- 0 missing claim-fitness fields;
- 0 exact source-version overlaps between the delta and v2;
- 0 cross-target exact source-version overlaps between Lithuania and Karnak.

The two known v2 cross-row overlaps remain unchanged.

**Disposition:** survives.

## Attack 10 — every accepted delta should generate a successor candidate

Rejected.

An immutable candidate is a coherent review/release artifact, not a rolling mirror of
every internally reviewed row.

Here:
- v2 remains coherent and reconstructible;
- no publication, consumer or canonical-release trigger exists;
- the two reviewed rows have no dependency conflict with v2;
- their reviewed status can be preserved as a bounded delta without rewriting v2;
- building another multi-file immutable package would add version/package churn without
  changing release readiness or publication ceiling.

This is not a numeric threshold such as “two rows are too few.” The trigger is
**decision/release value**.

**Disposition:** `KEEP_REVIEWED_DELTA_SEPARATE`.

## Final disposition

Per row:
- Lithuania 1300 — `ACCEPT_INTERNAL_REVIEW`;
- Karnak 1000 BCE — `ACCEPT_INTERNAL_REVIEW`.

Candidate gate:
**`KEEP_REVIEWED_DELTA_SEPARATE`**.

The delta is reviewed and source-reconstructible. It does not mutate v2 and does not
create v3.

Reopen integration when a materially useful consolidation/release trigger exists, for
example:
- another coherent reviewed batch that makes cumulative state materially easier to
  consume/release;
- a concrete publication or downstream consumer need;
- a source/dependency conflict requiring cumulative reconciliation;
- an explicit canonical/release evaluation.

Independent historical review remains 0.
