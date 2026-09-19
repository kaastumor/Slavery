# Method and Ontology

## 1. What the atlas is — and is not

The Historical Slavery Atlas is an **evidence-synthesis and data-curation project**.

Its purpose is to collect, normalize, reconcile and digest existing historical evidence and scholarship into a transparent spatial-temporal dataset. It is not intended to operate as an independent historical research institute, produce novel historical theories, or settle historiographical controversies through original interpretation.

The normal evidentiary chain is:

```
PRIMARY / SOURCE-NATIVE EVIDENCE
        +
SPECIALIST HISTORICAL SCHOLARSHIP
        ↓
SYNTHESIZED ATLAS DESIGNATION
        ↓
TRANSPARENT CLAIM + PROVENANCE + UNCERTAINTY
```

Primary sources anchor bounded facts such as transactions, laws, inscriptions, terminology, dates, places, status categories and recorded events. Specialist historical scholarship is normally the principal guide for interpreting classification, prevalence, continuity, institutional character and wider historical significance.

Where sources conflict, the atlas follows ordinary historical source criticism and the treatment of the problem in relevant specialist scholarship. The atlas should not create an unresolved designation merely because two sources disagree.

## 2. The atlas is multidimensional

The map must not answer only "did slavery exist here?" A defensible historical representation separates at least four questions:

1. **Territorial practice:** what forms of slavery, servitude, coerced labour, dependency, captive incorporation, or related institutions are evidenced in the territory?
2. **Legal/state regime:** what did law, state institutions, courts, monopolies, prohibitions, or abolition measures recognize or forbid?
3. **External participation:** did people, companies, ports, vessels, financiers, states, or institutions based in or linked to the territory participate in enslavement or slave trading elsewhere?
4. **Research coverage:** how much relevant evidence has this project actually reviewed?

These questions must be stored and visualized independently.

## 3. Unknown is the default when no usable claim exists

If the atlas has no defensible territorial-practice claim for a place and time, the historical condition is **unknown in the atlas**.

Unknown does not mean:

- slavery was absent
- coercion was absent
- the territory was free
- the project searched exhaustively
- surviving evidence does not exist

Research coverage should explain why a claim is missing where possible: for example, not researched, source identified, reviewed but not yet classified, or researched-inconclusive.

A missing positive claim must never be rendered as a negative historical fact.

### No claim versus P0

No territorial-practice claim means the atlas currently has no usable classification for that place/time.

`P0` is stronger and should be used only when a reviewed territorial-practice assessment explicitly records that the evidence package does not currently support a usable P1–P4 classification.

Do not manufacture P0 rows merely to fill the map.

## 4. How the atlas resolves conflicting evidence

Conflicting evidence is normal historical material. It should be preserved, not flattened.

A contradiction between sources does **not** automatically mean the atlas classification becomes `disputed` or receives no designation.

The atlas should synthesize the evidence using the same considerations historians normally use, including:

- contemporaneity and distance from the event
- provenance and transmission history
- genre, purpose and intended audience
- whether historical terminology maps cleanly onto the atlas category
- independence or dependence between sources
- geographic and temporal representativeness
- whether a source describes law, ideology, rhetoric or observed practice
- corroboration from other primary evidence
- the interpretation found in relevant specialist scholarship
- the degree of agreement or disagreement in that scholarship

### Working designation

Where the relevant specialist historiography supports a defensible working interpretation, the atlas records that interpretation as its designation.

Contradictory or limiting evidence remains attached to the claim through evidence directions such as:

- `supports`
- `challenges`
- `qualifies`
- `context`

A challenging source therefore does not disappear merely because the atlas reaches a positive classification.

### When to use `disputed`

Use `disputed` only when a **material historiographical disagreement remains unresolved after synthesis**, and credible specialist interpretations support meaningfully different classifications.

Examples include disagreement over whether a historical status category should be understood as slavery at all, or whether the available evidence supports fundamentally different reconstructions of the institution.

Do not use `disputed` merely because:

- one source contradicts another
- a hostile or external observer used different terminology
- an older interpretation differs from a better-supported later one
- a primary source is ambiguous but specialist scholarship resolves the ambiguity
- some uncertainty remains about scale, chronology or geography

Those limitations should be preserved without erasing the best-supported designation.

## 5. Practice intensity: P0–P4

### P0 — Unknown / no usable classification
A reviewed assessment concludes that the evidence package does not currently support a usable P1–P4 territorial-practice classification. This does not mean absence.

### P1 — Isolated direct attestation
At least one bounded, credible direct attestation exists, but the evidence package does not establish repetition, institutionalization, or broader structural significance.

### P2 — Recurrent / repeatedly evidenced practice
The evidence package supports recurring practice beyond an isolated event. Multiple independent attestations can support P2, but raw document count is never sufficient by itself. Specialist synthesis may also establish recurrence from an evidence corpus.

### P3 — Systemic / institutional
Specialist interpretation and the underlying evidence strongly support an institutionalized, recurring, legally or socially structured practice extending beyond isolated incidents.

### P4 — Widespread / structurally major
Specialist scholarship supports the practice as widespread, structurally important, or deeply embedded in the relevant political, economic or social system for the mapped period.

### Critical rule
P-level is a synthesis of the historical evidence package and specialist interpretation. It is not calculated mechanically from number of records, surviving documents, voyages, captives, citations, database rows, or archive density.

### Unassigned P-level versus P0
A database `NULL` practice level means that no P0–P4 assessment has yet been recorded for that claim. `P0` is different: it is an explicit reviewed assessment that no usable practice classification is currently available.

A claim may have a positive historical designation while still having `practice_level = NULL` if the existence/classification of the practice is defensible but its intensity has not yet been assessed.

## 6. Coverage state

Use a separate research-process field:

- `not_researched`
- `source_identified`
- `reviewed`
- `classified`
- `disputed`
- `researched_inconclusive`

Coverage state describes the state of the project's research, not historical prevalence.

`researched_inconclusive` means the project actively looked and current evidence is insufficient for a defensible historical claim or classification. It is not absence.

`disputed` should be reserved for a genuine unresolved historiographical or evidentiary dispute relevant to the classification. It should not be the default state for any source conflict.

The legacy broad audit labels S / P / D / RI can remain as high-level project-management summaries, but they must not replace row-level coverage state.

## 7. Legal status

Store separately from practice level:

- `institutionalized_or_recognized`
- `prohibited_abolished_or_criminalized`
- `mixed_conflicting_or_subnational`
- `unknown`

A legal event must carry time, jurisdiction, source, and scope.

Legal recognition establishes that a category, rule or institution was recognized in that legal context. It does not by itself establish prevalence.

Legal abolition or prohibition does not prove that practice ended immediately.

## 8. Practice type taxonomy

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

Historical terminology should not be mechanically translated into one of these categories. The atlas should follow the best-supported specialist interpretation and preserve terminological ambiguity where relevant.

## 9. Evidence is claim-specific

Evidence belongs to a claim, not to an entity as a whole.

Example: a source can establish that a merchant operated in Rotterdam without establishing that merchant's nationality. Another source may establish ownership of a vessel but not financing. A legal text can establish prohibition without establishing compliance.

Each claim therefore needs its own provenance, evidence direction, temporal scope and spatial scope.

Contradictory evidence should normally remain attached to the same historical question through `CLAIM_SOURCE` rather than causing competing narrative rows with no synthesis.

## 10. Identity is separate from historical role

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

## 11. Geography targets are not limited to states

Evidence may concern a polity, province, city, port, region, site, estate, institution or other spatial unit.

Use a generic spatial identity for the target, while preserving `POLITY` as a specific political subtype. Historical jurisdiction/containment must be time-bounded rather than inferred from present-day borders or one timeless parent relationship.

Do not enlarge a narrow evidence target merely because a convenient whole-polity geometry exists.

## 12. Historical time includes precision and uncertainty

A mapped/queryable interval is not the same thing as exact historical dating.

The data model must preserve whether evidence is:

- exactly dated
- approximately dated
- bounded to a broad period/century
- open-ended before/after a terminus
- disputed between alternative dates
- otherwise uncertain

A broad interval used to encode competing possible dates must not be interpreted as evidence continuously applying throughout that entire interval.

The web application may use normalized integer ranges for filtering while still displaying the original historical precision to users.
