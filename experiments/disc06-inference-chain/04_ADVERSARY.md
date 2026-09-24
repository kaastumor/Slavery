# DISC-06 adversarial review

## Attack: the negative result is biased because the cases were already corrected

**True limitation, not a reversal.**

The sample is explicitly exposed regression material. It cannot measure whether a
ledger would prevent an unseen first-pass error.

The experiment instead asks a narrower question: after a real correction has occurred,
does the current packet preserve the reasoning dependency well enough to reconstruct
and maintain it?

On that question, the baseline succeeds.

A future prevention test would require fresh/sealed material and a separate protocol.
The current result must not claim preventive efficacy.

## Attack: explicit edges are inherently new information

They are a new **representation**, but in this sample they encode relations already
stated unambiguously in the baseline fields and correction prose.

The preregistered rule required material information/revision impact, not mere
normalization. Treating every explicit edge as new information would make the test
tautologically favor the ledger.

## Attack: reverse dependency lookup could matter at scale

Plausible, but not demonstrated here.

Current source relations already contain source IDs/versions and independence groups.
A cross-target source-family audit can be performed from those structures. DISC-06
contains no observed missed-update incident that requires a second relation layer.

Keep this as a reopen trigger rather than extrapolating from hypothetical scale.

## Attack: free-text prose is fragile

Also plausible. But the project already has structured fields for the failure classes
that mattered:
- temporal applicability/precision;
- evidence locus/inference extent;
- network/territorial separation;
- source role/claim fitness;
- independence group.

The adversarial correction prose is not carrying the whole safety contract alone.

## Attack: the ledger could replace existing fields rather than duplicate them

Not demonstrated. The seven-field ledger does not contain enough historical semantics
to replace the current packet. Removing existing fields would lose information.

Therefore the tested proposal is additive, and additive review cost counts against it.

## Final adversarial disposition

**REJECT survives attack.**

Do not adopt an explicit inference-ledger abstraction now. Retain CRMinf/FPO as
external conceptual references and the three concrete reopen triggers in the result.
