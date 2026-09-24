# EXP-02 — Minimum Sufficient Evidence Packet

Issue: #205  
Parent: #183  
Depends on: #203 R1.8 artifact freeze  
Date: 2026-09-24  
Stage: pre-registered; execution blocked until R1.8 freezes the artifact  
External participants: none  
Production implementation authorized: no

## Question

What is the smallest representation that preserves the safety and reconstructibility properties that survived R1?

This experiment does not ask whether users want the system.

It asks whether the current evidence packet contains unnecessary structure and whether the surviving core can travel through ordinary formats without needing a bespoke application.

## Why this is the right internal-only question

The project currently knows that its method catches internal errors.

It does not know that external users value it, and external validation is explicitly deferred.

Without external people, the project must not manufacture adoption evidence.

The highest-value internal work is therefore subtractive:
- identify unique versus redundant field families;
- test whether the same safeguards survive in smaller artifacts;
- reduce dependence on application-specific representation;
- create better evidence for a later product-form decision.

## Red team of the experiment

### Attack 1 — circular correctness scoring

Using R1's own historical conclusions as gold truth would only show that R1 agrees with itself.

Correction: score structural invariants and recoverability, not historical truth.

### Attack 2 — serialization tautology

Copying every field into Markdown and declaring success proves nothing.

Correction: each portable format must preserve fixed review tasks and safety invariants with fewer or flatter structures.

### Attack 3 — ablation bias

If an invariant is defined by a field name, removing that field is guaranteed to fail.

Correction: test whether the underlying distinction remains recoverable from the remaining packet, not whether the original key name survives.

### Attack 4 — hidden historical re-interpretation

An ablation result could tempt us to rewrite claims or merge ontology dimensions.

Correction: no historical classification, ontology or schema becomes canonical from this experiment.

### Attack 5 — app-vs-file category error

Showing that a Markdown packet preserves information does not prove a UI is worthless.

Correction: the result may only strengthen or weaken the hypothesis that a smaller/portable artifact is sufficient for the current internal contract.

## Frozen corpus

Use the R1 candidate after #203 freezes it.

Primary set:
- all 19 reviewed C1 packets;
- all 45 source relations.

Coverage/non-absence checks:
- all 77 frozen targets.

No new historical research.

## Candidate ablations

Test one family at a time:

A. proposition / abstention  
B. evidence locus / inference extent  
C. temporal precision / display rule  
D. law-practice and network-territorial notes  
E. source version / locator / independence group  
F. review / access / coverage fields  
G. research-state / non-absence distinctions

## Portable representations

P1 — compact Markdown evidence packet  
P2 — flat target table plus separate source table  
P3 — canonical JSON reference

No graph database, bespoke viewer or new service is allowed.

## Fixed invariants

A representation or ablation passes only if all relevant invariants remain recoverable:

1. strongest permitted claim is distinguishable from prohibited overclaim;
2. temporal precision is explicit;
3. evidence locus and inference extent are not silently conflated;
4. law/practice and network/territorial boundaries survive where relevant;
5. exact source/version/locator remains recoverable;
6. shared source-family dependency remains visible;
7. review/access limitations remain explicit;
8. unresearched/inconclusive/held/C0 do not become absence;
9. geometry state cannot strengthen the historical claim;
10. candidate/non-canonical/internal-review boundary remains expressible.

## Result labels

- STRUCTURALLY REQUIRED
- REDUNDANT IN CURRENT FROZEN SET
- FORMAT-SPECIFIC
- AMBIGUOUS / NEEDS MANUAL REVIEW

Redundant means only redundant for these fixed invariants on the frozen R1 set. It does not authorize schema deletion.

## Decision rule

SIMPLIFY CANDIDATE:
a field family can be removed or collapsed across the frozen set without losing any invariant.

PRESERVE CORE:
removing the field family causes a distinct invariant to become unrecoverable or materially ambiguous.

PORTABLE CORE SURVIVES:
Markdown and/or flat tables preserve all fixed invariants without application-specific logic.

PORTABILITY FAILS:
at least one essential invariant requires structure not representable safely in the boring format.

## Exit

Produce:
- ablation matrix;
- portable-format comparison;
- smallest surviving packet proposal;
- explicit unresolved/ambiguous list;
- no canonical schema change.

After EXP-02, stop and re-evaluate project form again.

No automatic successor.
