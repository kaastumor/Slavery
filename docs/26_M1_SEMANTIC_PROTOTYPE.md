# M1 semantic split prototype

**Gate:** #100  
**Atomic task:** #102  
**Status:** experimental; not canonical methodology or schema  
**Baseline:** v0.6.1 and the current P0–P4 representation remain unchanged

## Question

What is the smallest model that avoids mixing evidentiary configuration, historical characterization, research workflow, epistemic outcome, event/process occurrence, and simultaneous practice facets?

## Smallest proposal

Do not replace the universal `CLAIM`, provenance model, territorial/external/legal layer separation, or current release. Add semantic dimensions *beside* the legacy fields in a future-compatible representation:

1. **Evidence basis** — how the evidence package is configured, e.g. `isolated_attestation`, `recurrent_attestation`, `specialist_synthesis`, `mixed`.
2. **Historical characterization** — what the reviewed synthesis says about historical structure, e.g. `unassessed`, `bounded_occurrence`, `recurrent`, `institutional`, `widespread_structurally_major`.
3. **Research stage** — project workflow only: `not_researched`, `source_identified`, `under_review`, `review_complete`.
4. **Classification outcome** — epistemic result only: `unassessed`, `classified`, `disputed`, `inconclusive`.
5. **Assertion form** — whether the historical predicate is a `practice_or_status` or a bounded `event_or_process`. Event/process claims do not by themselves imply enduring territorial practice.
6. **Practice facets** — zero or more typed concept assertions, each carrying a dimension (`status`, `function`, `property_legal`, `transmission`, `process`) and a concept code. A headline legacy practice type may remain for compatibility but is not the sole analytical vocabulary.

This is deliberately additive. It can be represented in JSON/relational child rows without changing existing identifiers or deleting P0–P4.

## Compatibility with P0–P4

P0–P4 remains a **legacy summary**, not a value to mechanically derive from the prototype dimensions.

- P1 often corresponds to an isolated evidence basis plus a bounded historical characterization, but no automatic mapping is valid.
- P2 often corresponds to recurrent evidence and/or recurrent characterization, but evidence count alone remains insufficient.
- P3/P4 chiefly express institutional/structural characterization and still require specialist synthesis.
- P0 remains an explicit legacy reviewed no-usable-classification state; it is not absence and must not be inferred from `inconclusive`.
- `NULL` remains no legacy P-level assessment.

Migration, if later justified, should dual-read/dual-write explicit reviewed mappings and preserve the original P-level. No backfill may infer new dimensions from a P-level alone.

## Adversary and alternatives

| Attack / simpler alternative | Disposition | Evidence / consequence |
| --- | --- | --- |
| Keep P0–P4 and improve legend wording | **reject** | M1-A01 shows one ordered field mixes evidence configuration with historical structure; sorting/filtering remains semantically ambiguous. |
| Keep one `coverage_state` and treat disputed/inconclusive as terminal workflow stages | **reject** | M1-A02 requires `review_complete + disputed` and `review_complete + inconclusive` to coexist. |
| Put secondary practice characteristics in notes | **reject** | Hittite status, property/pricing and function become non-queryable and force a false single-category choice (M1-A06). |
| Create a large new subtype/table hierarchy for every concept now | **park** | The fixture only demonstrates need for separable facets, not a mature exhaustive taxonomy or SQL migration. |
| Split evidence basis from historical characterization | **revise** | Required by M1-A01; the prototype makes both independently testable and leaves P-level untouched. |
| Split research stage from classification outcome | **revise** | Required by M1-A02; orthogonal fields preserve simultaneous truths. |
| Add assertion form for bounded event/process versus practice/status | **revise** | Baekje 369 demonstrates that a capture/distribution event is a different predicate from enduring territorial practice (M1-A05). |
| Preserve claim-specific evidence directions | **survives** | Mauryan counterevidence already works; no parallel evidence architecture is needed. |
| Preserve unresolved geometry behavior | **survives** | Late Classic Maya already avoids invented territorial certainty; #102 does not alter it. |

## Real-case discriminating examples

### Baekje 369

Prototype representation: `assertion_form=event_or_process`, evidence basis `isolated_attestation`, historical characterization `bounded_occurrence`, with process facets such as captive-taking/enslavement/distribution only where the reviewed evidence supports them. The legacy one-year P1 can remain unchanged. A query for enduring territorial practice can now exclude a pure event without reading notes.

### Hittite central Anatolia

Prototype representation can retain a headline slavery/enslavement label while separately recording supported facets for status/category, property/legal pricing, economic function such as herding, and status flexibility/transmission where evidenced. These are simultaneous characteristics rather than mutually exclusive replacements.

### Reviewed but disputed/inconclusive cases

`research_stage=review_complete` can coexist with `classification_outcome=disputed` or `inconclusive`. This removes the workflow/outcome collision without changing provenance or publication state.

## Decision

**Revise experimentally.** The smallest additive six-dimension prototype discriminates the #101 failures without a schema migration or canonical-methodology change. The fixture/tests define invariants rather than claiming a final vocabulary. Exhaustive taxonomy design and SQL implementation are intentionally parked until the integrated M1 gate determines whether this model survives alongside #103 and #104.

No historical case is reinterpreted or republished by this prototype. Canonical release v0.6.1 and the public preview remain unchanged.
