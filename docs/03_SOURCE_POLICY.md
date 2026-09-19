# Source Policy

## 1. Primary versus secondary sources

Do not rank all primary sources above all secondary sources. Their evidentiary roles differ.

### Primary sources are especially useful for

- existence of a specific transaction, event, legal rule, person, ship, sale, tax, court case, status term, census entry, ownership relation, or dated practice
- contemporary terminology and administrative categories
- precise dates and locations when provenance is sound

### Primary-source limitations

- survival bias: some societies, states and institutions left far more records than others
- archive bias: state, commercial, legal and elite institutions are overrepresented
- genre bias: a sale contract, law code, inscription, travel account and court record each show different slices of reality
- exceptional-event bias: unusual cases may survive because they were litigated, recorded or sensational
- category mismatch: historical terms do not always map cleanly to modern slavery categories
- selection bias: a modern researcher may unknowingly choose only the easiest or most famous surviving records

### Secondary scholarship is especially useful for

- classification of ambiguous historical status
- prevalence and structural significance
- continuity and change over time
- interpreting terminology in its historical context
- reconciling contradictory primary sources
- placing isolated records into a larger social, economic or legal system
- identifying historiographical disputes and alternative interpretations

### Secondary-source limitations

- dependence on an uneven primary archive
- national, imperial, linguistic or disciplinary archive preferences
- historiographical fashions and inherited categories
- citation cascades where many works ultimately rely on the same evidence
- presentist category projection
- overgeneralization from a local archive to a larger polity or period

## 2. Source hierarchy is claim-dependent

For a claim such as "a sale occurred at X on date Y," a primary transaction record may be the strongest evidence.

For a claim such as "slavery was structurally important across polity X during period Y," synthesis by specialist scholarship is normally necessary; a collection of surviving sales cannot by itself establish prevalence.

## 3. Independence rule

Count independent evidentiary bases, not citations.

Five articles repeating one archival example are not five independent attestations. Conversely, an inscription, court record and independent administrative archive may provide genuinely distinct evidentiary bases even when later scholarship discusses all three.

## 4. Archive-density bias safeguard

Never allow well-digitized, easily searchable or Western/Atlantic archives to produce visually stronger prevalence merely because more rows can be ingested.

Track at least:

- source count
- source family
- independence relationship
- coverage state
- source type
- research effort / audit state

These metadata may affect confidence and coverage display, but not automatically P-level.

## 5. Source registry minimum fields

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

## 6. Source versions

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

## 7. Source assets and raw preservation

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

## 8. Claim-level citation rule

Evidence attaches to a specific claim through `CLAIM_SOURCE`.

Each link should record where relevant:

- exact `source_version_id`
- evidence role
- supports / challenges / qualifies
- directness
- independence group
- page, table, archival reference, record ID or other locator
- interpretation notes

A source that supports one attribute of an actor or polity does not automatically support every other attribute.
