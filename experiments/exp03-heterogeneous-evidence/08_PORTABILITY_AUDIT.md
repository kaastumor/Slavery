# EXP-03 — Portability Audit

**Date:** 2026-09-24
**Input:** six frozen fresh historical cases
**Comparison baseline:** EXP-02 minimum packet
**Disposition:** **CORE REQUIRES EXTENSION**

## Executive result

The portable package form survives.

The exact EXP-02 minimum field set does not.

Fresh cases can still be represented as:
- package manifest;
- flat target rows;
- flat source-relation rows;
- optional human-readable packets.

But two semantic families that EXP-02 treated as removable or format-specific are now required to prevent overclaim:

1. source role / claim fitness must return to the portable source relation;
2. historical terminology / category-mapping status must become explicit at target/claim level.

Mixed geometry also confirms that the frozen EXP-02 package-level geometry default cannot be generalized: per-target geometry state/role must be active when geometry states differ.

## EXP-02 fields that survive unchanged

### Bounded proposition + required abstention — SURVIVES

Every case needed both.

The abstention is not boilerplate:
- Athens: no prevalence from archive density;
- Cairo: no military-mamluk-to-all-slavery collapse;
- Tenochtitlan: no universal category equivalence;
- Joseon: no all-nobi-as-slave collapse;
- Zanzibar: export restriction is not abolition;
- British India: delegalization is not disappearance of practice.

### Evidence locus + inference extent — SURVIVES

All six cases depend on it.

Examples:
- Cairo-specific forced labour versus Mamluk-Egypt structural synthesis;
- Tlatelolco/Tenochtitlan capital context versus the wider Mexica Empire;
- local Joseon sale documents versus polity-wide characterization;
- regional post-1843 Indian practice versus a huge colonial jurisdiction.

### Temporal state / display rule — SURVIVES

The anchor cannot safely stand in for temporal precision.

Tenochtitlan relies heavily on post-conquest documentary transmission about pre-conquest categories.
British India has an exact 1843 legal event but a broader 1843–1850 practice question.

### Source version / locator / independence group — SURVIVES

Dependency is materially active:
- the two Salazar articles are one closely related source family;
- Andrades' historiographic account and Lee's critique occupy the same Joseon classification debate;
- Kalb's 2023 delegalization discussion explicitly builds on Major and related scholarship.

Counting them as independent confirmations would be wrong.

### Language/access limitation — SURVIVES

The six cases span Greek/English mediation, Arabic-source mediation, Spanish/Nahuatl source traditions, Korean-language scholarship, English/Omani treaty traditions and multilingual South Asia.

### Coverage confidence / non-absence research state — SURVIVES

Several cases have high confidence for a bounded fact while low confidence for prevalence or territorial uniformity. One scalar confidence would be too coarse if adapters hide the packet text.

### Law/practice and network/territorial notes — SURVIVE

Zanzibar and British India make these mandatory in practice, not optional decoration.

## Fields that EXP-02 omitted but EXP-03 shows are core

### 1. Source role / claim fitness — REINTRODUCE

EXP-02 kept:
- source identity;
- locator;
- independence group;
- direction;
- decisive flag.

That is insufficient for these cases.

A source may be decisive for one proposition and unfit for another:
- the 1845 Zanzibar treaty is decisive for legal scope but cannot prove compliance or end of territorial slavery;
- Act V of 1843 is decisive for court/public-officer legal enforceability but cannot prove practice ended;
- Pseudo-Xenophon attests socially visible slavery at Athens but is not a prevalence survey;
- the 1707 Sangju documents support transactions near the Joseon anchor but not one polity-wide classification.

A direction value such as supports does not encode these limits.

### Minimum extension

Add to portable source relation:
- evidence_role
- claim_fitness

A free-text note is acceptable initially. Do not invent a large ontology until repeated cases justify one.

## 2. Historical terminology / category mapping — ADD

Tenochtitlan and Joseon make this unavoidable.

### Tenochtitlan

Tlacotli/tlatlacotin is historically specific and internally differentiated. Spanish esclavo/siervo translations are evidence about translation history, not proof that every subtype is identical to a modern comparative slavery category.

### Joseon

Nobi is a real historical status family, but scholarship disputes whether all subtypes are best classified as slavery, serfdom or a mixed/differentiated dependency system.

### South Asia

Even explicit slave-language can overlap with service/devotional terminology in some source traditions, while other practices are unequivocally slaveholding.

### Minimum extension

Add target/claim-level fields:
- historical_terms
- category_mapping_status
- category_mapping_note

Suggested minimal mapping states:
- direct_or_well_established
- approximate_historically_specific
- disputed
- not_mapped

These are interpretation controls, not a universal slavery taxonomy.

## Geometry result

### EXP-02 package-level default — DOES NOT GENERALIZE

EXP-02 could hoist unresolved_no_geometry because all 77 targets shared it.

EXP-03 has structurally different cases:
- point/site can be identifiable while historical territorial extent remains unresolved;
- city and polity may be different spatial identities;
- physical island land is not historical jurisdiction;
- a large colonial label such as British India cannot safely use a modern-country proxy.

### Required portable behavior

Keep per-target geometry state when mixed.
At minimum preserve:
- what geometry is actually resolved (point / route / polygon / none);
- what spatial claim it may represent;
- what remains unresolved/proxy.

This confirms D-087's warning and does not require a canonical geometry-schema migration.

## What does NOT need to be added

### New service/database

No. Flat portable artifacts still represent the cases.

### New universal intensity score

No. The heterogeneous cases make that less defensible, not more.

### Automatic category normalization

No. The correct result is explicit mapping uncertainty, not a more aggressive classifier.

### Source counts as confidence/prevalence

No. Athens is the positive control showing why archive richness must not mechanically strengthen practice intensity.

## Net change from EXP-02

Portable core remains small.

Target/claim extension:
- historical terms;
- category mapping status/note.

Source-relation extension:
- evidence role;
- claim fitness.

Geometry:
- reactivate per-target mixed state/role when needed; do not hoist a uniform default across heterogeneous releases.

## Disposition

**CORE REQUIRES EXTENSION.**

The architecture finding survives:

> reviewed research state → immutable portable evidence package → replaceable presentation adapters

But the safe package is slightly richer than the frozen EXP-02 minimum.
