# 100/100 released geo recovery tranche 4 — Sogdiana / Samarkand legal context

**Issue:** #383  
**Parent:** #369  
**Reviewed against main:** `eee51caa6569e3b433af60bc9a7a33f5e04622ed`  
**Attempt:** `ATLAS100-PROC-20260930T1341Z-SOGDIANA-02`

## Result

**ACCEPTED_STAGING — LIVE PREFLIGHT REQUIRED**

This review closes the source, stable-identity and geometry-role analysis for the released Sogdiana claim. It does not authorize a database write or claim, P-level, release, publication or serving-channel change.

## Released identity

- claim: `63dda32b-6c3e-4b3e-9c5a-36596e6cdc1b`
- target spatial entity: `a6718e1f-5683-48f4-90fb-cc35ad263ba5`
- practice type: `slavery_enslavement`
- released interval: 709–710 CE / `[709,711)`
- v0.8.1 target geometry: unresolved and preserved

## Historical evidence and dependence

Reuse existing source version `cc49573e-8621-43d2-b054-a496c66cdcc8`: Ilya Yakubovich, “Sogdian marriage contract,” *Encyclopaedia Iranica*.

Relevant locators:

- opening discussion: Nov. 3–4 were found at Mount Mugh, are dated to the tenth regnal year of Tarkhun (ca. 709–710), and were likely concluded in Samarkand;
- Nov. 3 lines 11–17: slave, hostage, prisoner and dependent are distinct legal contingencies;
- Nov. 4 lines 7–15: the groom undertakes not to sell Chat, give her as hostage or tribute, or place her under another's protection.

The geometry recovery adds no independent historical attestation. Oxford Invisible East is a later catalogue/edition lineage, not a second witness.

## Chronology discrepancy

Oxford Invisible East lists Nov. 3 and Nov. 4 as dated **27 April 711**, citing Livshits 2015, pp. 17–37. The released claim follows Yakubovich's ca. 709–710 chronology.

This tranche does not adjudicate or silently normalize that difference. It preserves the immutable released interval and requires the catalogue discrepancy to remain explicit in any rehearsal or later implementation.

## Geometry disposition

UNESCO World Heritage component `603rev-001` identifies the **Afrosiab Archaeological Area** as ancient Samarkand and gives:

- N 39°40′0″
- E 66°58′60″
- normalized WGS84 point: `POINT(66.9833333 39.6666667)`
- component area: 229 ha

Proposed role:

- semantic role: `claim_evidence_locus_probable_contract_setting`
- accuracy: `specialist`
- label: **Afrosiab / ancient Samarkand — probable 709–710 legal context**
- one link to the exact released claim
- role text: **probable Samarkand legal-context locus; contract location inferred by specialist editor**

The coordinate is the official component anchor. It is not the exact Foundation Hall, building, room or contract-execution point.

## Findspot separation

Mount Mugh remains the document findspot only. It is not substituted for Samarkand and does not establish territorial prevalence or a Sogdiana practice extent.

## Repository/release preflight

The immutable v0.8.1 authority bundle contains the released claim and no evidence locus for it. It contains no matching UNESCO maps URL, `603rev-001` identifier or Afrosiab string.

The governed live database was not readable in this run. Current live collision/reuse state for the UNESCO source, locus entity and claim-locus link is therefore **UNKNOWN**, not absent.

## Expected later disposable delta

- +1 spatial entity
- +1 geometry source + source version, subject to live reuse check
- +1 reviewed point geometry
- +1 claim-evidence-locus link
- +0 claims
- +0 claim-source relations
- +0 practice polygons
- +0 P-level/release/publication/serving changes
- existing unresolved target geometry preserved

## Explicit abstentions

- no Sogdiana polygon or regional centroid;
- no UNESCO property boundary as claim geometry;
- no exact-site claim;
- no Mount Mugh substitution;
- no overwrite of unresolved target geometry;
- no P2 strengthening;
- no silent chronology reconciliation.

## Next gate

Run a fresh governed Postgres/PostGIS read-only collision/source/release preflight. Only if exact identities and reuse rules pass may a disposable, rollback-verified, exact-no-op PostGIS rehearsal be prepared.

A live write remains separately sponsor-gated.
