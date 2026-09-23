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

### No claim versus legacy P0

No territorial-practice claim means the atlas currently has no usable classification for that place/time.

P0 remains meaningful only as a **legacy compatibility assessment** when an existing reviewed territorial-practice record explicitly says the old P0–P4 framework could not assign P1–P4. It is not the target post-M1 model and must not be inferred from a new inconclusive outcome.

Do not manufacture P0 rows merely to fill the map, and do not backfill the new post-M1 dimensions from a legacy P-level alone.

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

## 5. Territorial-practice semantics after M1

The target model does **not** reduce territorial practice to one universal ordinal intensity.

A reviewed territorial-practice claim may carry independent assessments of:

### Evidence package

- **attestation pattern** — whether the reviewed package is a single bounded attestation, recurrent attestation, multiple independent attestations, mixed/unclear, or still unassessed;
- **interpretive basis** — whether the working interpretation rests principally on source-native/primary evidence, specialist synthesis, a mixed primary-and-specialist package, or remains unassessed.

These are different questions. A specialist synthesis may interpret one attestation, recurrent attestations, or many independent evidentiary bases. Source count does not establish independence.

### Historical characterization

Keep the following dimensions independent because they may be simultaneously true or independently unknown:

- **occurrence pattern** — bounded occurrence, recurrent practice, continuous-period assertion, or unassessed;
- **institutionalization** — whether institutional features are positively supported, or remain unassessed;
- **prevalence scope** — localized, broader, widespread, or unassessed;
- **structural significance** — whether structurally major significance is positively supported, or remains unassessed.

Do not infer one dimension mechanically from another. In particular:

- recurrence does not prove institutionalization;
- institutionalization does not prove widespread prevalence;
- widespread prevalence does not by itself prove structural importance;
- any of these may remain unassessed while another is positively supported.

### Assertion form

Distinguish a bounded **event/process** assertion from an enduring **practice/status** assertion.

A capture, sale, transfer or enslavement event can be strong evidence without, by itself, establishing recurrent or polity-wide territorial practice.

### Legacy P0–P4 compatibility

P0–P4 is retained only to reproduce and interpret historical releases that already use it.

- P0 = explicit reviewed legacy no-usable-P1–P4 classification; not absence.
- P1–P4 retain their historical release meanings.
- NULL = no legacy P-level assessment recorded.
- no new post-M1 dimension may be inferred from P0–P4 alone;
- no new P-level may be mechanically derived from the post-M1 dimensions;
- the future public comparison model must not use P0–P4 as its universal target ordinal.

Historical releases remain immutable. A future release may carry both legacy compatibility values and the new dimensions where each was explicitly reviewed.

## 6. Research stage and classification outcome

The old single coverage_state field mixed workflow progress with epistemic result. The target model keeps them separate.

### Research stage

Research stage describes project workflow only, for example:

- not_researched
- source_identified
- under_review
- review_complete

### Classification outcome

Classification outcome describes the result of synthesis, for example:

- unassessed
- classified
- disputed
- inconclusive

These dimensions are orthogonal. A claim can be review_complete + disputed or review_complete + inconclusive.

Inconclusive does not mean absence and does not mechanically create legacy P0.

The legacy broad audit labels S / P / D / RI and legacy row-level coverage_state values may remain for historical release/migration compatibility, but they are not the target post-M1 analytical model and must not be used to infer historical prevalence.

## 7. Legal status

Store separately from practice level:

- `institutionalized_or_recognized`
- `prohibited_abolished_or_criminalized`
- `mixed_conflicting_or_subnational`
- `unknown`

A legal event must carry time, jurisdiction, source, and scope.

Legal recognition establishes that a category, rule or institution was recognized in that legal context. It does not by itself establish prevalence.

Legal abolition or prohibition does not prove that practice ended immediately.

## 8. Practice concepts are faceted, not one exclusive taxonomy

The atlas must preserve historically meaningful distinctions without forcing unlike properties into one flat exclusive list.

A territorial claim may therefore carry zero or more reviewed **practice facets**. Initial facet dimensions include:

- **status / condition** — e.g. an enslaved or servile status where specialist interpretation supports it;
- **function / context** — e.g. domestic, military, agricultural, herding, sexual exploitation, or other evidenced function;
- **property / legal powers** — e.g. sale, pricing, alienability, ownership-like legal treatment where specifically evidenced;
- **transmission / exit** — e.g. hereditary transmission, status flexibility, manumission/exit conditions where supported;
- **process** — e.g. captive-taking, enslavement, sale, transfer or trafficking processes.

Legacy headline categories such as slavery/enslavement, debt bondage, forced labour, penal labour, corvée, serfdom, military slavery, domestic servitude, captive-taking and slave trading remain useful labels and migration values. They must not be treated as if they all describe the same ontological dimension.

A bounded process such as capture or sale does not automatically establish an enduring status, institutionalization, recurrence or territorial prevalence.

The controlled vocabulary should grow only when a real research case requires a defined concept. M1 establishes the **faceted structure**, not a final exhaustive ontology.

Historical terminology should not be mechanically translated into an atlas facet. Preserve source-native terminology and follow the best-supported specialist interpretation, including ambiguity or disagreement.

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

For claim semantics, distinguish:

- **evidence locus** — the place(s) where the underlying observation/source is anchored;
- **inference extent** — the place(s) over which the reviewed historical assertion is actually justified.

If inference extent is broader than the evidence locus, store a reviewed generalization basis and rationale. Geometry availability, spatial containment, or a convenient polity polygon is never by itself a generalization basis.

## 12. Historical time separates applicability from precision

A broad queryable interval is not the same thing as a historical assertion that a condition held continuously throughout that interval.

The target model keeps at least three temporal concepts distinct:

1. **query window** — outer normalized bounds used to find candidate records efficiently;
2. **applicability semantics** — what dates/intervals are positively asserted, for example a continuous interval, bounded occurrence, alternative dates, an open terminus, or unknown applicability;
3. **temporal precision/certainty** — whether the dating is exact, approximate, broad, disputed, or otherwise uncertain.

Changing precision alone must not change selected-year truth.

Examples:

- competing possible document dates may share one broad query window but must not create continuous presence between those alternatives;
- a broad-period specialist synthesis may support continuous applicability across a period even though its boundary dates are imprecise;
- an approximately dated bounded occurrence remains bounded rather than filling the whole uncertainty envelope.

Normalized integer ranges remain useful retrieval/indexing structures. A selected-year public state must evaluate applicability semantics rather than treating query-window membership as sufficient truth.

Preserve source-faithful date text and uncertainty. Do not invent probability distributions merely because dates are uncertain.

