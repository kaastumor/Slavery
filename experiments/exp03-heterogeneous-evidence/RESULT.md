# EXP-03 — Heterogeneous Evidence Stress Test — Result

**Issue:** #211
**Date:** 2026-09-24
**Canonical historical release:** v0.6.1 unchanged
**External participants:** none
**Disposition:** **CORE REQUIRES EXTENSION**

## Question

Does the portable reviewed evidence core from EXP-02 remain sufficient when applied to fresh, structurally heterogeneous historical research?

## Result

The portable architecture survives:

> reviewed research state → immutable portable evidence package → replaceable presentation adapters

The exact EXP-02 minimum field set does not survive unchanged.

Six fresh cases can still be represented in a manifest + flat target table + flat source-relation table, but safe reconstruction now requires two small semantic extensions:

### Target / claim level
- historical_terms
- category_mapping_status
- category_mapping_note

### Source relation level
- evidence_role
- claim_fitness

Mixed spatial states also confirm the existing warning that package-level geometry hoisting is valid only for a uniform release. A mixed release needs per-target geometry state/role.

## Fresh historical research completed

1. Classical Athens, c. 400 BCE — bounded-supported institutional slavery; archive-density positive control; no prevalence inference.
2. Mamluk Cairo, c. 1300 CE — bounded-supported multiple slavery forms plus Cairo-local captive forced labour; military-slave category not generalized to all slavery.
3. Tenochtitlan, c. 1500 CE — bounded-supported tlacotli/tlatlacotin institution with explicit historically specific category mapping and colonial-source mediation.
4. Joseon Korea, c. 1700 CE — sale/status-control practices supported; umbrella slavery/serfdom classification materially disputed.
5. Zanzibar Town / port, c. 1850 CE — territorial slavery plus slave-trade network and a partial anti-export legal regime coexist; law/network/practice remain separate.
6. British India, 1843–1850 — exact legal delegalization in 1843 plus regionally continued practices; no uniform post-1843 territorial practice state inferred.

## Machine-readable packet

- 6 target rows
- 17 source relations
- 14 independence groups
- 3 repeated dependency groups:
  - mexico-salazar-tlacotli
  - joseon-classification-debate
  - india-major-delegalization

Validation confirmed all required old and new target/source fields are present.

## Why the extension is necessary

### Source role / claim fitness

Direction and decisiveness are insufficient.

A treaty or statute can strongly support a legal proposition while being unfit to prove compliance or practice cessation.

A transaction document can strongly support a bounded transaction while being unfit to establish polity-wide prevalence or an umbrella classification.

A rhetorical primary text can attest presence while being unfit as a prevalence survey.

These are not presentation details. They constrain what an adapter is allowed to infer.

### Historical terminology / category mapping

Tenochtitlan and Joseon falsify a packet that stores only a normalized comparative label.

Tlacotli/tlatlacotin and nobi carry historically specific distinctions and translation/classification disputes. Flattening those distinctions would allow a map/table/API to strengthen the reviewed claim silently.

South Asian and Mamluk cases reinforce the same pattern.

## What did NOT fail

- bounded proposition / abstention;
- evidence locus / inference extent;
- temporal state;
- source version / locator / independence group;
- language/access limitation;
- coverage confidence;
- non-absence research states;
- law/practice separation;
- network/territorial separation;
- portable flat artifacts;
- replaceable-view architecture.

## What is not authorized by this result

- no canonical schema migration;
- no reinterpretation of v0.6.1;
- no public release;
- no universal taxonomy engine;
- no automatic P-level/intensity derivation;
- no new service/database/UI;
- no external participant work.

## Adversarial result

The extension survived attacks that it was merely better prose, redundant with source direction, overfit to Joseon, or evidence for a universal new taxonomy.

The smallest defensible change remains:
- explicit historical terminology/category mapping;
- explicit source role/claim fitness;
- per-target geometry state when a release is spatially mixed.

## Final disposition

**CORE REQUIRES EXTENSION.**

The project should preserve the portable-core architecture and amend the release/interchange contract, not expand the platform.
