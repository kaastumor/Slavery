# DISC-06 result — inference-chain stress test

**Disposition:** **REJECT**  
**Issue:** #240  
**Historical subject research:** none  
**Canonical release:** v0.6.1 unchanged

A minimal CRMinf/FPO-inspired premise→reasoning→conclusion ledger was reconstructed for
six already-reviewed cases with known correction mechanisms.

It improved normalization and machine queryability, but failed the frozen success
threshold:
- 0 failure mechanisms gained material information unavailable from the current packet;
- all 6 correction mechanisms were reconstructible from the current packet;
- 15 extra inference rows would create new synchronization/review burden.

The current portable contract therefore remains unchanged.

CRMinf/FPO remain useful conceptual references for adversarial questions about premise,
inference and revision impact. They are **not** adopted as a schema, ontology or
portable-release layer.

Reopen only on a demonstrated revision-propagation/reconstructibility failure, not for
graphability or theoretical elegance.

EXP-08 remains paused; Qi — 500 BCE remains frozen/unstarted.
