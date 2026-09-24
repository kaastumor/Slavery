# DISC-08 benchmark — portable package interoperability

**Issue:** #250  
**Subject:** exact frozen `exp06-candidate-v1`  
**Historical research:** none  
**Package mutation:** none

## Result

**NARROW REUSE.**

Frictionless Data Package v1 earns a useful but bounded role for the **tabular
interchange/validation edge**. It does not replace the Atlas package manifest.

RO-Crate 1.3 was conditionally inspected because Frictionless's remaining failure was
research-object/provenance structure. RO-Crate describes the research-object boundary
more naturally, but it still does not replace the Atlas's safety-critical release
semantics without project/domain-specific meaning. It therefore does not earn default
adoption either.

## Frictionless arm

Artifact:
`frictionless/datapackage.json`

The standards-only descriptor represents all nine resources already named by the Atlas
manifest using commit-pinned HTTPS URLs. This avoids the v1 prohibition on parent
(`../`) local paths without moving any frozen file.

### 1. Resource discovery — PASS / real gain

A generic Data Package consumer can enumerate the nine resources from one standard
`resources` array.

The current Atlas manifest can of course do the same for Atlas-aware code, but it is not
a generic package vocabulary. This is a genuine interoperability difference.

### 2. Tabular validation — PASS / material narrow gain

The two CSV resources are declared as `tabular-data-resource` with inline Table Schema:
- 21 target columns; primary key `target_id`;
- 16 source-relation columns; composite primary key `target_id + source_id`.

This adds a standards-level declaration of expected headers/types/keys. The current
custom manifest preserves file identity and counts but does not itself express a generic
table schema.

This is the strongest reason for **NARROW REUSE**.

All fields are deliberately typed as strings in the benchmark. DISC-08 does not invent
stronger domain types from current CSV text.

### 3. Integrity — PASS

Frictionless Data Resource v1 supports a standard `hash` field and allows the
algorithm name to prefix the digest. All nine frozen SHA-256 values can therefore be
represented as `sha256:<digest>`.

No integrity advantage over the current Atlas manifest exists; this is interoperability,
not stronger integrity.

### 4. Reconstructibility — PASS with portability trade-off

The complete nine-resource boundary can be enumerated if the three artifacts outside
the candidate directory are represented by fully-qualified, commit-pinned URLs.

A pure local attached package cannot preserve the current structure without moving/
copying files because Data Resource v1 forbids parent `../` paths.

Therefore:
- full boundary: standards-compliant through remote URLs;
- standalone local portability in the current repository layout: weaker than the custom
  manifest;
- moving files to satisfy the standard is prohibited and unnecessary.

### 5. Semantic safety — FAIL as manifest replacement

Standards-only Frictionless has no project-understood structured equivalent for:
- `canonical_release_change = false`;
- `r1_review_state_change = false`;
- `p_level_assignment = false`;
- `historical_geometry_promotion = false`;
- `database_or_api_change = false`;
- Atlas artifact roles such as `release_gate_decision`;
- allowed/current review-gate dispositions.

These can be:
- mentioned in description text; or
- represented using additional custom metadata properties.

Neither makes them generic Frictionless semantics. The frozen protocol explicitly bars
counting custom extension keys as interoperability gain.

The custom Atlas manifest therefore remains safety-authoritative.

### 6. Maintenance cost — mixed / additive

A Frictionless sidecar adds:
- one descriptor;
- 9 resource declarations;
- 37 field declarations;
- two primary-key declarations.

If maintained manually this is a significant drift surface.

If generated from the package/CSV headers, most cost is mechanical—but then the custom
Atlas manifest still remains and the Frictionless descriptor is an optional adapter,
not the owning package contract.

### 7. Generic capability — PASS narrowly

Material generic capability:
- standard resource enumeration;
- standard CSV schema/key declaration;
- compatibility with Frictionless-aware consumers/validators.

Not demonstrated:
- better historical validation;
- better release-safety enforcement;
- less Atlas-specific metadata;
- lower total maintenance if made mandatory.

No Frictionless runtime library was available in the execution environment and outbound
package installation was unavailable. The benchmark therefore verifies the descriptor
against the pinned v1 specification rather than claiming an executed third-party-tool
validation. This limits tool-ecosystem evidence but not the structural comparison.

## RO-Crate conditional comparator

Artifact:
`ro-crate/ro-crate-metadata.json`

The trigger for the richer comparator was met: Frictionless's main package-level failure
was research-object/provenance semantics.

RO-Crate 1.3 improves the representation in three ways:
- the candidate can be a root `Dataset`;
- all nine URI-addressable resources can be explicit `File` data entities;
- `isBasedOn`, contextual entities and action/provenance patterns provide a richer
  standard research-object vocabulary.

The comparator also carries SHA-256 values through schema.org's `sha256` term.

However, the decisive Atlas safety meanings still remain domain-specific. A generic
RO-Crate consumer can understand that a file is part of a Dataset and that the crate is
based on a source commit; it does not thereby understand that:
- v0.6.1 remains canonical;
- the candidate did not change R1 review state;
- no P-level or geometry promotion occurred;
- PUBLISH_CANDIDATE is a bounded internal release-gate disposition.

Encoding those meanings requires either human-readable artifacts or a domain profile /
custom vocabulary. That reintroduces an Atlas-specific semantic layer.

RO-Crate also adds JSON-LD/entity/provenance complexity that is not justified for the
current small immutable candidate.

**RO-Crate disposition: LEARN FROM / REJECT AS DEFAULT PACKAGE LAYER.**

## Frozen discriminator

- **ADOPT / REUSE:** fail — package-level safety semantics are not replaced.
- **NARROW REUSE:** **pass** — Frictionless materially improves the tabular
  interchange/validation edge.
- **REJECT AS DEFAULT:** pass for both Frictionless as package owner and RO-Crate as a
  mandatory release layer.

Overall disposition: **NARROW REUSE**.

## Practical consequence

Keep:
- custom Atlas `manifest.json` as authoritative package/release contract;
- deterministic SHA-256 package identity;
- existing human QC/review/unresolved artifacts.

Allow:
- a **generated, optional Frictionless descriptor/Table Schema adapter** when an actual
  export/interoperability/validator use case benefits from it.

Do not:
- make Frictionless mandatory for every candidate;
- make RO-Crate mandatory;
- add JSON-LD/RDF infrastructure;
- move candidate files to satisfy a packaging standard;
- treat table-schema validity as historical correctness.

## Reopen triggers

Reconsider stronger standard adoption only if:
1. a real external consumer/depository requires Data Package or RO-Crate;
2. generic table validation catches defects the current builders/tests miss often enough
   to justify a maintained sidecar;
3. cross-tool package exchange becomes a demonstrated workflow rather than a hypothetical
   possibility;
4. a domain profile can replace, not merely duplicate, material Atlas safety semantics.
