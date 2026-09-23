# M2 post-M1 relational semantics prototype

**Gate:** #116  
**Task:** #120  
**Status:** disposable/local PostGIS prototype; not a production migration  
**Canonical release:** v0.6.1 unchanged  
**Public preview:** unchanged

## Question

Can D-058's accepted target semantics live in the real relational model without rewriting legacy v0.6.1 meaning, turning P0–P4 into the new model, or silently changing public selected-year behavior?

## Prototype boundary

The prototype is intentionally implemented under `experiments/m2/`, not `db/migrations/`.

It extends a disposable database after the normal repository migrations. No production migration is applied by #120. No current release, release channel, public view, Edge Function or frontend contract is changed.

The prototype reuses the existing universal CLAIM / TERRITORIAL_PRACTICE_CLAIM architecture rather than introducing a parallel ontology service or replacement claim system.

## Smallest relational additions

### Territorial-practice dimensions

Nullable columns are added to `atlas.territorial_practice_claim` for the D-058 dimensions:

- assertion form;
- attestation pattern;
- interpretive basis;
- occurrence pattern;
- institutionalization;
- prevalence scope;
- structural significance;
- research stage;
- classification outcome.

Legacy rows may keep every one of these columns NULL.

Once a row activates the post-M1 semantic set by supplying `assertion_form`, the complete dimension set must be explicit. A dimension may still be `unassessed`; explicit unassessment is different from silently deriving a value from P0–P4.

No trigger or default derives a new dimension from `practice_level`, and no trigger derives a new P-level from the new dimensions.

The sparse prototype values use CHECK constraints rather than introducing nine permanent vocabulary tables. This is an integration experiment, not a decision that the final controlled vocabularies should be hard-coded.

### Simultaneous practice facets

`atlas.practice_facet_assertion` is a many-row child of a territorial-practice claim.

It permits simultaneous concepts across:

- status;
- function;
- property/legal powers;
- transmission/exit;
- process.

The concept code remains open text with a non-empty constraint because D-058 established the faceted structure but explicitly did not establish a final exhaustive vocabulary.

### Temporal applicability

The existing `CLAIM.from_year/to_year/valid_years` remain the outer retrieval/query envelope.

The prototype adds:

- `CLAIM.temporal_applicability_mode`;
- `CLAIM_ASSERTED_INTERVAL` rows for positively asserted bounded dates/intervals;
- `atlas.post_m1_claim_active_at(claim_id, year)`.

The selected-year predicate first rejects years outside the outer query window, but **never treats query-window membership as sufficient truth**. Positive selected-year truth requires an asserted interval.

Temporal precision is intentionally absent from the predicate. Therefore changing `temporal_precision` alone cannot change selected-year truth.

`unknown` applicability cannot carry a positive interval. `terminus_after` and `terminus_before` do not acquire indefinite positive presence merely from an open terminus; only explicit bounded asserted intervals can make a selected year positive.

### Spatial inference

The prototype adds two generic claim bridges:

- `CLAIM_EVIDENCE_LOCUS` — where the underlying evidence/observation is anchored;
- `CLAIM_INFERENCE_EXTENT` — where the reviewed historical assertion is justified.

If an inference extent is the same spatial entity as an evidence locus, it uses `same_as_locus`.

A different/broader inference extent requires both:

- a reviewed generalization basis other than `same_as_locus`;
- a non-empty generalization rationale.

No geometry ID or containment relation appears in either bridge, so drawable/containing geometry cannot itself create inference extent.

No inference-extent row is also valid: unresolved extent remains representable.

## Real-case fixtures

### Hittite central Anatolia

The existing M1 fixture is representable as:

- recurrent attestation;
- mixed primary + specialist interpretation;
- recurrent occurrence;
- institutional features supported;
- prevalence unassessed;
- structural significance unassessed;
- practice/status assertion;
- legacy P2 preserved;
- four simultaneous status/property/function/transmission facets;
- broad-range precision plus an explicitly reviewed continuous asserted interval.

This proves recurrence and institutionalization need not compete for one enum value.

### Baekje 369

The 369 CE case is represented as:

- single bounded attestation;
- mixed primary + specialist interpretation;
- bounded occurrence;
- event/process assertion;
- institution/prevalence/structural significance unassessed;
- legacy P1 preserved;
- process facets for captive-taking and enslavement/distribution;
- one asserted year.

The large captive count therefore still does not become polity-wide prevalence.

### Silla Village Register

The source row retains the broad 695–819 outer query window for retrieval, while positive applicability is represented only at:

- 695;
- 755;
- 815;
- 818–819.

Thus 700 lies inside `CLAIM.valid_years` but `post_m1_claim_active_at(..., 700)` is false.

The spatial target remains the four register communities. A whole-Silla inference extent is not manufactured.

The Silla fixture does **not** invent the full D-058 characterization set because M1 accepted Silla specifically as a temporal/spatial discriminating case, not as a fully reviewed semantic-dimension assignment. This demonstrates that reviewed temporal/spatial semantics can be added independently while the territorial row still carries legacy compatibility values.

## Adversarial controls

The acceptance SQL rejects:

1. a partially populated post-M1 territorial semantic set;
2. an asserted interval extending outside its claim query window;
3. a positive asserted interval on `unknown` applicability;
4. a broader/different inference extent with no reviewed rationale;
5. a positive applicability mode with no asserted interval.

It also asserts that:

- legacy P2 remains P2 and receives no automatic post-M1 values;
- `classification_outcome=inconclusive` does not create P0;
- Silla's outer uncertainty envelope does not create continuous presence;
- the Hittite simultaneous facet set is representable;
- the existing publish views do not expose the prototype columns/tables.

## Reproduction

After starting the ordinary disposable PostGIS stack and applying normal repository migrations:

```bash
bash ./scripts/db-test-post-m1-semantics.sh
```

The DDL remains in that disposable database; all historical acceptance rows are wrapped in a transaction and end in `ROLLBACK`.

## What #120 does not prove

Passing this prototype does not make the schema canonical.

It does not prove:

- that the sparse vocabularies are final;
- that every historical case has reviewed values for every dimension;
- that the public API/client has been migrated to the new selected-year predicate;
- that post-M1 semantics and the complete Cliopatria resolver work correctly together.

Those are precisely why #121 and the integrated #122 adversarial gate still exist.
