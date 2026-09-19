# Source Policy

## 1. Purpose of the source policy

The Historical Slavery Atlas is an evidence-synthesis project. Its task is to collect and digest existing historical evidence and scholarship into transparent claims, not to replace the work of specialist historians with ad hoc interpretation by the project.

The atlas therefore uses both:

- **primary/source-native evidence**, which anchors bounded historical facts
- **specialist secondary scholarship**, which interprets classification, significance, continuity, prevalence and contested terminology

Neither class automatically outranks the other for every historical question.

## 2. Primary versus secondary sources

### Primary sources are especially useful for

- existence of a specific transaction, event, legal rule, person, ship, sale, tax, court case, status term, census entry, ownership relation, inscription, or dated practice
- contemporary terminology and administrative categories
- precise dates and locations when provenance is sound
- bounded evidence that can later be interpreted in a larger historical context

### Primary-source limitations

- survival bias: some societies, states and institutions left far more records than others
- archive bias: state, commercial, legal and elite institutions are overrepresented
- genre bias: a sale contract, law code, inscription, travel account and court record each show different slices of reality
- exceptional-event bias: unusual cases may survive because they were litigated, recorded or sensational
- rhetorical/ideological bias: an inscription, ethnography or law may describe ideals, categories or political claims rather than ordinary practice
- transmission bias: some ancient texts survive only through later quotation, copying, translation or redaction
- category mismatch: historical terms do not always map cleanly to modern slavery categories
- selection bias: a modern researcher may unknowingly choose only the easiest or most famous surviving records

### Secondary scholarship is especially useful for

- classification of ambiguous historical status
- prevalence and structural significance
- continuity and change over time
- interpreting terminology in its historical context
- evaluating reliability and representativeness of primary sources
- reconciling contradictory primary evidence
- placing isolated records into a larger social, economic or legal system
- identifying historiographical disputes and alternative interpretations
- determining whether an apparent contradiction is still considered historically consequential

### Secondary-source limitations

- dependence on an uneven primary archive
- national, imperial, linguistic or disciplinary archive preferences
- historiographical fashions and inherited categories
- citation cascades where many works ultimately rely on the same evidence
- presentist category projection
- overgeneralization from a local archive to a larger polity or period
- outdated interpretation when newer specialist work materially revises the evidence

## 3. Source hierarchy is claim-dependent

For a claim such as "a sale occurred at X on date Y," a primary transaction record may be the strongest evidence.

For a claim such as "slavery existed as a recognized institution in polity X," primary legal, administrative, epigraphic or transactional evidence may establish the underlying fact, while specialist scholarship helps interpret the historical category.

For a claim such as "slavery was structurally important across polity X during period Y," synthesis by specialist scholarship is normally necessary; a collection of surviving sales cannot by itself establish prevalence.

The project should therefore ask **what proposition a source is capable of supporting**, not whether the source is simply "primary" or "secondary."

## 4. Historical synthesis and conflicting sources

Conflicting sources should be preserved, but they should also be interpreted.

The atlas should follow ordinary historical source criticism and the treatment of the issue in relevant specialist scholarship. Relevant considerations include:

- date and proximity to the events
- source provenance and transmission
- author perspective and purpose
- genre
- original terminology and translation
- whether the source concerns law, rhetoric, social practice or an exceptional event
- independence from other evidence
- geographic/temporal scope
- corroboration
- how relevant specialist historians evaluate the conflict

### Do not use automatic dispute logic

The following pattern is not acceptable:

```
Source A says X
Source B says not-X
therefore atlas = disputed / blank
```

Instead:

1. preserve both sources
2. determine what each actually establishes
3. consult the relevant specialist historiography
4. record the best-supported synthesis
5. attach contrary evidence as `challenges` or `qualifies`
6. use `disputed` only when a material disagreement remains unresolved in credible specialist scholarship

The atlas is allowed to have a working designation while also showing that contrary historical evidence exists.

## 5. Specialist scholarship is the interpretive backbone, not a substitute archive

The atlas should not attempt to independently resolve major historical controversies from raw primary material when specialist scholarship already exists.

For broad classification questions, prefer relevant specialists with demonstrated subject-area engagement over generic summaries.

Where possible, preserve the relationship between specialist interpretation and the primary/source-native evidence on which it rests.

The preferred pattern is:

```
bounded primary evidence
    +
specialist interpretation
    +
limiting / challenging evidence
    ↓
claim-specific atlas synthesis
```

This does not mean secondary scholarship is copied uncritically. Competing scholarship, age of interpretation, source dependence and evidentiary limitations should remain visible.

## 6. Independence rule

Count independent evidentiary bases, not citations.

Five articles repeating one archival example are not five independent attestations.

Conversely, an inscription, court record and independent administrative archive may provide genuinely distinct evidentiary bases even when later scholarship discusses all three.

Two modern articles analyzing the same excavated archive may belong to the same independence group for prevalence assessment even if they make different interpretive contributions.

## 7. Archive-density bias safeguard

Never allow well-digitized, easily searchable or Western/Atlantic archives to produce visually stronger prevalence merely because more rows can be ingested.

Track at least:

- source count
- source family
- independence relationship
- coverage state
- source type
- research effort / audit state

These metadata may affect confidence and coverage display, but not automatically P-level.

## 8. Source registry minimum fields

Every reusable conceptual source should have:

- `source_id`
- title / name
- author or institution where known
- source type
- primary / secondary / methodology / dataset classification
- language where relevant
- geographic scope
- temporal scope
- independence notes
- reliability / limitation notes

Claims should cite an exact `SOURCE_VERSION`, not merely the conceptual source when version/edition/snapshot identity matters.

## 9. Source versions

Use a separate `SOURCE_VERSION` for the exact edition, database release, web snapshot, archival item/version or other concrete evidentiary state.

Track where applicable:

- `source_version_id`
- `source_id`
- version / edition / dataset release label
- publication or creation date
- URL, DOI, archive identifier or other stable locator
- access/retrieval date for web/database resources
- licensing / terms status
- redistribution status
- notes about changes, completeness or limitations

Never silently merge versions.

Examples:

- Seshat legacy Equinox slavery variables must retain the Equinox identity.
- A current Seshat/Polaris snapshot is not automatically equivalent to the historical dataset from which a variable was taken.
- SlaveVoyages documented versus imputed fields must remain distinguishable.

## 10. Source assets and raw preservation

Where legally and practically permitted, preserve the exact downloaded/imported source asset or dataset snapshot.

Store an optional `SOURCE_ASSET` record with:

- source version
- filename/object key
- media type
- checksum, preferably SHA-256
- storage location
- redistribution status

Do not assume every article, book, archive image or proprietary dataset may be mirrored or redistributed. When local storage is not permitted or practical, preserve citation metadata, stable locators and claim-level page/section/record locators instead.

For structured bulk datasets, preserve source-native values separately from normalized interpretation. A normalization correction must not erase the original field value.

## 11. Claim-level citation rule

Evidence attaches to a specific claim through `CLAIM_SOURCE`.

Each link should record where relevant:

- exact `source_version_id`
- evidence role
- `supports` / `challenges` / `qualifies` / `context`
- directness
- independence group
- page, table, archival reference, record ID or other locator
- interpretation notes

A source that supports one attribute of an actor or polity does not automatically support every other attribute.

A source marked `challenges` does not automatically negate the claim. It records evidence that must be considered in the synthesis.
