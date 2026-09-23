# R1.1 — Core Contract v1 Adversary

**Programme:** R1 / #159  
**Target:** `03_CORE_CONTRACT_V1.md` + validator + fixtures  
**Disposition:** **SURVIVES AFTER SMALL CORRECTIONS**

## Attack 1 — C1 can be syntactically complete but evidentially empty

Initial validator required a `sources` field but did not require at least one recoverable evidence relation.

A row with `sources=[]` could therefore pass some structural checks.

**Correction:**
- C1/C2 candidate rows require at least one source relation;
- a positive historical proposition requires at least one decisive source relation that is not `context_only` or `review_required`.

**Disposition:** corrected.

---

## Attack 2 — `production_grade` can become a prestige label

The contract already says claim-fitness is not venue prestige, but the risk remains operationally important.

**Correction:**
- fixture/reviewer guidance must define `production_grade` only as “fit for this bounded claim under current review”;
- source independence and evidence direction remain separate required review concepts;
- multiple production-grade relations may still share one independence group.

No numerical source-quality score is introduced.

**Disposition:** survives.

---

## Attack 3 — positive proposition is ambiguous for inconclusive rows

An inconclusive row can have a bounded proposition such as:
> “the reviewed packet establishes a later sale but not target-year territorial practice.”

That proposition is positive as a bounded evidence statement even though the classification outcome is inconclusive.

**Correction:**
- validator must not infer “positive history” merely from `classification_outcome=classified`;
- evidence relations are required for all C1/C2 rows;
- release review determines whether a proposition is historical-positive, limiting, or research-state synthesis.

**Disposition:** survives.

---

## Attack 4 — C0 claims can hide in free-text notes

No simple validator can prove that arbitrary notes contain no historical claim.

**Correction:**
- candidate C0 export has a deliberately narrow field set;
- free-form C0 historical interpretation is prohibited;
- C0 notes may concern identity, geometry, sampling, access or research workflow only.

Machine validation catches known claim fields; adversarial sampling catches semantic leakage.

**Disposition:** survives with review control.

---

## Attack 5 — `coverage_confidence` could become another pseudo-probability

**Correction:**
- coverage confidence remains qualitative and research-process specific;
- no numeric probability;
- no mechanical effect on historical classification;
- it must be explained when `limited` or worse.

**Disposition:** survives.

---

## Attack 6 — tier labels may duplicate canonical DB lifecycle states

True.

C0/C1/C2 are programme/release research tiers, not replacements for:
- claim `review_status`;
- `publication_status`;
- research-stage vocabulary.

**Correction:**
Contract states the mapping explicitly and forbids treating C2 as “more true.”

**Disposition:** survives.

---

## Attack 7 — C2 trigger list can expand indefinitely

**Correction:**
- a new trigger requires a concrete R1/COV fixture and a decision-log change;
- ordinary uncertainty alone does not force C2 if C1 can state it safely;
- fame/source volume never trigger C2.

**Disposition:** survives.

---

## Attack 8 — source-quality escalation could make every limited-access row C2

Not every access limitation changes claim safety.

**Correction:**
- `access_limited` is not automatically C2;
- C2 triggers when the limitation makes a decisive proposition unsafe, leaves a material disagreement unresolved, or blocks recovery of a source relation;
- otherwise preserve limitation in C1.

**Disposition:** survives.

---

## Attack 9 — dependency tracking might attach sources to rows rather than claims

That would recreate entity-level evidence.

**Correction:**
- dependency table keys through claim/evidence relation;
- row/target is reachable from claim, not the evidence owner;
- one source may support one claim and only contextualize another.

**Disposition:** survives.

---

## Attack 10 — release validator could become a shadow schema

**Correction:**
- validator checks portable release invariants only;
- it does not define database normalization;
- DB schema remains governed by existing data-model/migration decisions;
- no migration follows from Core Contract v1.

**Disposition:** survives.

---

## Attack 11 — exact source version may be impossible for some historical works

For books/articles, an exact reviewed edition/scan/DOI state may be enough even when no local asset exists.

**Correction:**
- `source_version_ref` means exact reviewed version identity in the project registry;
- local mirroring is optional and rights-dependent;
- stable citation metadata + locator may satisfy recovery.

**Disposition:** survives.

---

## Attack 12 — release-safe versus publication-safe remains distinct

Internal adversarial review is not independent review.

**Correction:**
- Core Contract v1 is sufficient for an R1 candidate research release;
- public/canonical promotion can impose stronger review gates;
- review labels remain explicit.

**Disposition:** survives.

---

# Final verdict

**SURVIVES AFTER SMALL CORRECTIONS.**

Core Contract v1 is hard enough to freeze for R1 because:
- every major rule maps to a real fixture or existing canonical method;
- it adds no new infrastructure;
- it does not overwrite the database schema;
- it preserves unknown/disagreement rather than scoring them away;
- the known Chandela/Zhu/network/geometry/release failures are first-class guards.

Remaining uncertainty belongs to actual R1 research and review, not further contract design.

Proceed to R1.2 target-frame freeze after applying the validator corrections and decision-log entry.
