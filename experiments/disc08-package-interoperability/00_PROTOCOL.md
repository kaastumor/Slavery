# DISC-08 — portable-package interoperability benchmark

**Issue:** #250  
**Primary gate:** method / release-interchange discovery  
**Status:** preregistered before descriptor construction  
**Base commit:** `d567f25dfcb0efeda2eed8f4be7d5cc0a921a960`

## 1. Question

Does an established packaging standard materially improve the already-working portable
candidate boundary, or would it merely duplicate the Atlas custom manifest while losing
safety/review semantics?

## 2. Frozen subject

Use exactly **EXP-06 Candidate v1**:

`experiments/exp06-balanced-evidence/candidate/`

Candidate identity:
- `candidate_id = exp06-candidate-v1`;
- non-canonical `PUBLISH_CANDIDATE`;
- 6 target rows;
- 36 source-relation rows;
- canonical historical release remains `v0.6.1`.

The candidate files and their Git blob SHAs are frozen in
`01_PACKAGE_FREEZE.json`. The existing `manifest.json` additionally freezes SHA-256
content identity, artifact role, release effects and review-gate state.

Do not move, copy, rewrite, normalize or regenerate candidate files for compatibility.

## 3. External baselines

### Frictionless Data Package v1 — first/simple baseline

Pinned official specifications, accessed 2026-09-25:
- Data Package v1: https://specs.frictionlessdata.io/data-package/
- Data Resource v1: https://specs.frictionlessdata.io/data-resource/
- Tabular Data Resource v1: https://specs.frictionlessdata.io/tabular-data-resource/

Relevant standard capabilities to test:
- package/resource enumeration;
- generic metadata;
- tabular schema declaration;
- file size/hash metadata;
- local or fully-qualified resource locations.

Relevant constraint:
- Frictionless v1 local resource paths must be siblings/children of the descriptor;
  absolute paths and parent `../` paths are forbidden.

That matters because the existing Atlas manifest intentionally links:
- `../RESULT.md`;
- `../CHECKPOINT.md`;
- `../../../web/public/data/exp06-candidate.json`.

The benchmark must not silently drop those artifacts.

### RO-Crate 1.3 — conditional richer comparator

Pinned official specification:
- RO-Crate 1.3 Recommendation: https://w3id.org/ro/crate/1.3
- published 2026-06-22;
- current long-term release at freeze time.

RO-Crate is **not automatically executed**. It becomes eligible only if the
Frictionless result fails specifically on research-object/provenance structure and a
richer comparator could change the final standards decision.

## 4. Strongest current baseline

The current custom `manifest.json` already preserves:
- candidate/status/release identity;
- exact target/source counts;
- release-effect guards;
- artifact path + SHA-256 + Atlas-specific artifact role;
- review-gate state/disposition;
- links to target/source tables, research result/checkpoint and browser bundle.

The candidate package is deterministic and already approved for non-canonical
publication.

## 5. Experimental representation

Construct only **disposable benchmark descriptors** outside the frozen candidate
directory.

Frictionless arm:
1. standards-only package descriptor;
2. standard resource metadata for all representable artifacts;
3. Tabular Data Resource/Table Schema metadata for the two CSVs where feasible;
4. SHA-256 identity in standard hash fields where feasible.

Two path modes may be inspected:
- local/sibling-child semantics without relocating files;
- fully-qualified commit-pinned URLs where needed to represent resources outside the
  candidate directory.

A descriptor that relies on Atlas-specific extension keys must be labelled
**custom extension**, not counted as standards-only interoperability.

## 6. Benchmark tasks

Compare current manifest versus Frictionless on:

1. **Resource discovery** — can a generic consumer enumerate the candidate resources?
2. **Tabular validation** — do the CSVs gain useful schema/column/type validation?
3. **Integrity** — can SHA-256 identity be preserved?
4. **Reconstructibility** — can the complete reviewed candidate boundary be recovered,
   including linked result/checkpoint/browser artifacts?
5. **Semantic safety** — are release-effect guards, artifact roles and review-state
   meaning preserved without Atlas-specific custom fields?
6. **Maintenance cost** — how many extra maintained metadata atoms/files are required?
7. **Interoperability gain** — what concrete generic validation/consumer capability is
   added that the current manifest does not provide?

## 7. Frozen discriminator

**ADOPT / REUSE**
only if Frictionless adds a material generic validation/interoperability capability
while preserving all safety-critical candidate semantics with less or comparable
custom maintenance.

**NARROW REUSE**
if it materially improves only the tabular CSV boundary but cannot replace the
package-level manifest.

**REJECT AS DEFAULT**
if it mainly duplicates the current manifest, loses safety/provenance semantics, or
requires Atlas-specific extensions that erase the claimed interoperability gain.

**RO-CRATE COMPARATOR AUTHORIZED**
only if Frictionless fails specifically on research-object/provenance structure and a
RO-Crate test could change the package-standard decision.

No threshold changes after descriptor construction.

## 8. Adversarial attacks

Assume standards adoption is unnecessary and attack for:
- “standard” being treated as automatically better;
- custom extension keys being counted as interoperability;
- silent loss of outside-directory artifacts;
- schema validation being confused with historical validation;
- checksum compatibility without semantic-role compatibility;
- duplicate descriptors drifting from the existing manifest;
- remote URL mode reducing standalone portability;
- version-locking without demonstrated benefit.

## 9. Complexity boundary

No historical/slavery subject research. No mutation/copy/move of EXP-06 candidate
files. No schema/ontology migration. No canonical/public release change. No frontend,
API, database or service work. No production dependency.

EXP-08 remains paused; Qi — 500 BCE remains frozen/unstarted.

## 10. Freeze rule

Do not construct or score any Frictionless/RO-Crate descriptor until this protocol and
package freeze are merged.
