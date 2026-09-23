# M1 semantic split prototype

**Gate:** #100  
**Original task:** #102  
**Corrective task:** #112  
**Status:** experimental; not canonical methodology or schema  
**Prototype:** v2 after integrated adversarial correction  
**Baseline:** v0.6.1 and the current public preview remain unchanged

## Question

What is the smallest model that avoids mixing evidence configuration, historical occurrence/structure, workflow state, epistemic outcome, event/process occurrence, and simultaneous practice facets?

## Correction from v1

The first prototype still overloaded two fields:

- `evidence_basis` mixed attestation pattern with interpretive basis;
- `historical_characterization` mixed occurrence, institutionalization, prevalence, and structural importance.

Those combinations fail because their values can be simultaneously true.

The v2 prototype therefore keeps only orthogonal dimensions.

## Experimental dimensions

### Evidence package

- **attestation_pattern** — `unassessed`, `single_bounded_attestation`, `recurrent_attestation`, `multiple_independent_attestations`, `mixed_or_unclear`
- **interpretive_basis** — `unassessed`, `primary_or_source_native`, `specialist_synthesis`, `mixed_primary_and_specialist`

A specialist synthesis can therefore coexist with any attestation pattern. The atlas does not infer independence merely from source count.

### Historical characterization

- **occurrence_pattern** — `unassessed`, `bounded_occurrence`, `recurrent`, `continuous_period`
- **institutionalization** — `unassessed`, `institutional_features_supported`
- **prevalence_scope** — `unassessed`, `localized`, `broader`, `widespread`
- **structural_significance** — `unassessed`, `structurally_major_supported`

These are independent. A practice can be recurrent and institutional while prevalence remains unassessed; institutionalization does not mechanically imply widespread prevalence or structural importance.

The values are intentionally sparse. M1 establishes the need for independent dimensions, not a mature exhaustive ontology.

### Workflow and epistemic result

- **research_stage** — `not_researched`, `source_identified`, `under_review`, `review_complete`
- **classification_outcome** — `unassessed`, `classified`, `disputed`, `inconclusive`

These remain separate because review completion and an inconclusive/disputed result can coexist.

### Assertion and facets

- **assertion_form** — `practice_or_status` or `event_or_process`
- **practice facets** — zero or more typed concept assertions across `status`, `function`, `property_legal`, `transmission`, and `process`

This preserves the successful #102 distinction between a bounded event such as Baekje 369 and an enduring practice/status claim, while allowing multiple characteristics such as the Hittite status/property/function evidence to coexist.

## Legacy P0–P4 boundary

P0–P4 is retained only as **legacy compatibility data** for existing releases and the current preview.

It is not the target universal ordinal for new comparative semantics.

Rules:

- preserve existing P-level values;
- never derive the new dimensions from P-level alone;
- never derive P0 from `inconclusive`;
- a legacy P0 is valid only when that P0 assessment itself was explicitly reviewed;
- do not automatically derive a new P-level from the new dimensions;
- future serving/UI integration must consume the new semantics before post-M1 data relies on them;
- M1 does not mutate the public preview or canonical v0.6.1.

The current public map can therefore remain reproducible as a legacy preview without defining the future ontology.

## Real-case checks

### Baekje 369

- attestation pattern: single bounded attestation
- interpretive basis: mixed primary + specialist
- occurrence pattern: bounded occurrence
- assertion form: event/process
- institutionalization, prevalence, structural significance: unassessed
- legacy P1 preserved

A large captive count does not become prevalence.

### Hittite central Anatolia

- attestation pattern: recurrent attestation
- interpretive basis: mixed primary + specialist
- occurrence pattern: recurrent
- institutional features: supported
- prevalence: unassessed
- structural significance: unassessed
- legacy P2 preserved

This is the discriminating example: recurrent + institutional are simultaneous truths, so they cannot be values in one enum.

### Reviewed inconclusive

`research_stage=review_complete` + `classification_outcome=inconclusive` does not create P0.

A separate synthetic fixture demonstrates that a legacy P0 may coexist only when it is explicitly reviewed as such.

## Adversarial alternatives

| Alternative | Disposition | Result |
| --- | --- | --- |
| Keep the v1 fields and only rename them | **reject** | Renaming cannot represent recurrent + institutional simultaneously or separate specialist synthesis from attestation pattern. |
| Build a large final ontology now | **park** | M1 proves orthogonality needs, not exhaustive controlled vocabulary content. |
| Replace the universal claim/provenance model | **reject** | Existing claim/evidence/release architecture survives. |
| Keep P0–P4 as the future universal summary | **reject** | Integrated gate showed that ordinal map semantics overstate comparability. |
| Preserve P0–P4 only for legacy compatibility | **survives** | Maintains release reproducibility without forcing future semantics into the old scale. |

## Decision

**Revise → survives at prototype level.**

The v2 dimensions remove the integrated-gate overload without schema migration or new infrastructure. They remain experimental until #105 reruns the integrated attack and #106 completes the Project Health Check.
