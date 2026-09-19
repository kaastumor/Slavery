# Method and Ontology

## 1. The atlas is multidimensional

The map must not answer only "did slavery exist here?" A defensible historical representation separates at least four questions:

1. **Territorial practice:** what forms of slavery, servitude, coerced labour, dependency, captive incorporation, or related institutions are evidenced in the territory?
2. **Legal/state regime:** what did law, state institutions, courts, monopolies, prohibitions, or abolition measures recognize or forbid?
3. **External participation:** did people, companies, ports, vessels, financiers, states, or institutions based in or linked to the territory participate in enslavement or slave trading elsewhere?
4. **Research coverage:** how much relevant evidence has this project actually reviewed?

These questions must be stored and visualized independently.

## 2. Practice intensity: P0–P4

### P0 — Unknown / no usable classification
No defensible practice classification is currently available. This does not mean absence.

### P1 — Isolated direct attestation
At least one bounded, credible direct attestation exists, but the project cannot yet establish repetition, institutionalization, or broader structural significance.

### P2 — Repeated independent attestations
Multiple independent attestations support recurring practice. Independence matters more than raw document count.

### P3 — Systemic / institutional
Evidence strongly supports an institutionalized, recurring, legally or socially structured practice extending beyond isolated incidents.

### P4 — Widespread / structurally major
Scholarship supports the practice as widespread, structurally important, or deeply embedded in the relevant political/economic/social system for the mapped period.

### Critical rule
P-level is an assessment of the evidence package and historical interpretation. It is not calculated mechanically from number of records, surviving documents, voyages, captives, citations, or database rows.

### Unassigned P-level versus P0
A database `NULL` practice level means that no P0–P4 assessment has yet been recorded for that claim. `P0` is different: it is an explicit assessment that no usable practice classification is currently available. Do not coerce disputed, researched-inconclusive, or merely reviewed evidence to P0 just to satisfy a database field.

## 3. Coverage state

Use a separate research-process field:

- `not_researched`
- `source_identified`
- `reviewed`
- `classified`
- `disputed`
- `researched_inconclusive`

`researched_inconclusive` means the project actively looked and current evidence is insufficient for a defensible classification. It is not absence.

The legacy broad audit labels S / P / D / RI can remain as high-level project-management summaries, but they must not replace row-level coverage state.

## 4. Legal status

Store separately from practice level:

- `institutionalized_or_recognized`
- `prohibited_abolished_or_criminalized`
- `mixed_conflicting_or_subnational`
- `unknown`

A legal event must carry time, jurisdiction, source, and scope. Legal abolition does not prove practice ended immediately.

## 5. Practice type taxonomy

Do not collapse the following into one field:

- slavery / enslavement
- chattel/property slavery where specifically evidenced
- hereditary slavery
- debt bondage / debt servitude
- forced labour
- state forced labour
- penal labour
- corvée or compulsory public labour
- serfdom / tied dependency
- domestic servitude
- military slavery
- sexual slavery
- captive-taking / captive incorporation
- slave trading / sale / purchase
- trafficking where historically appropriate
- other slavery-like or servile dependency

The taxonomy can grow, but additions require a definition and decision-log entry.

## 6. Evidence is claim-specific

Evidence belongs to a claim, not to an entity as a whole.

Example: a source can establish that a merchant operated in Rotterdam without establishing that merchant's nationality. Another source may establish ownership of a vessel but not financing. A legal text can establish prohibition without establishing compliance.

Each claim therefore needs its own provenance, confidence, temporal scope and spatial scope.

## 7. Identity is separate from historical role

A person or organization should have one normalized identity even when that actor has multiple historically evidenced roles.

Examples of roles that must remain analytically distinct include:

- owner
- financier
- insurer
- lender
- operator
- shareholder
- official

Do not create a second identity merely because the same actor appears in a different role. Conversely, evidence for one role does not imply another role.

## 8. Geography targets are not limited to states

Evidence may concern a polity, province, city, port, region, site, estate or other spatial unit.

Use a generic spatial identity for the target, while preserving `POLITY` as a specific political subtype. Historical jurisdiction/containment must be time-bounded rather than inferred from present-day borders or one timeless parent relationship.

## 9. Historical time includes precision and uncertainty

A mapped/queryable interval is not the same thing as exact historical dating.

The data model must preserve whether evidence is:

- exactly dated
- approximately dated
- bounded to a broad period/century
- open-ended before/after a terminus
- otherwise uncertain

The web application may use normalized integer ranges for filtering while still displaying the original historical precision to users.
