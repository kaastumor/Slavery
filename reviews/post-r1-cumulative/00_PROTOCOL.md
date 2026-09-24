# Post-R1 cumulative internal review — protocol

**Issue:** #259  
**Mode:** review / release  
**Status:** membership + inputs frozen before replay  
**Base commit:** `7448a94a38fdb5c4380b3adf91bcedbf7ac84dd5`

## Frozen membership

Exactly 17 post-R1 subject-research targets:

1. `R1:P:-2000:E:r1`
2. `R1:P:-2000:D:r1`
3. `R1:L:COV2:-500:C`
4. `R1:L:1300:B`
5. `R1:L:viking_900`
6. `R1:L:andaman_1800`
7. `R1:N:angkor_1200`
8. `R1:P:1800:C:r1`
9. `R1:L:500:F`
10. `R1:P:-500:E:r1`
11. `R1:P:1300:A:r1`
12. `R1:N:mongol_yam_1300`
13. `R1:N:yaghan_1800`
14. `R1:P:1300:F:r1`
15. `R1:N:great_zimbabwe_1400`
16. `R1:N:maori_1700`
17. `R1:P:500:C:r1`

No substitution or intake.

Excluded:
- all 19 already-reviewed R1 rows;
- EXP-07 qualification-only rows;
- Kalabhra identity/time hold;
- Qi 500 BCE frozen/unstarted.

## Frozen inputs

Repository state is pinned by the base commit above.

Key input blobs:
- consolidation inventory: `e7dd665ffc1da7d275cb9ca86250f063cfac0a88`
- consolidation source reconciliation: `e149067e90572f4e73522ab3e66bb892f6dd78af`
- EXP-04 targets: `bf623c6b32825ceeb789453701cf988c49ee658e`
- EXP-04 sources: `42a594dec6d0663e6233fad1bc8844bc4fef05ea`
- EXP-06 targets: `4190a7a23744375e47d945aa3007ada2c7f230c4`
- EXP-06 sources: `776604b1d39f7a135081a3d7841e289847b18246`
- EXP-08 targets: `819106bf82231d710fb8d6693a9b252ba81a2795`
- EXP-08 sources: `5f666ea3a7ebee05cd667e5fcab7d80e2e071a43`

## Review rule

Review **existing repository evidence only**.

Do not start a new subject/source search to rescue a row. If the existing artifacts are
insufficient, preserve or assign HOLD.

For every target replay:
1. target / frame / anchor identity;
2. bounded proposition versus abstention;
3. temporal applicability and selected-year leakage;
4. evidence locus versus inference extent;
5. territorial versus external/network dimension;
6. status/category mapping;
7. source/version reconstructibility;
8. false independence/dependency;
9. language/access limitation;
10. geometry non-inference;
11. review/publication ceiling.

R1 failure classes remain active:
- temporal leakage;
- target/context leakage;
- network/territorial leakage;
- event/status inflation;
- false source independence.

The shared `angkor-personnel-corpus` source family across Angkor 1200 and Khmer 1300
must be reviewed as one dependency family, not two independent attestations.

## Per-row dispositions

- `ACCEPT_INTERNAL_REVIEW`
- `NARROW_AND_ACCEPT`
- `HOLD_EXISTING_EVIDENCE`
- `REJECT_ARTIFACT`

Existing `under_review` is neither pass nor fail by presumption.

## Tranche disposition

- `CUMULATIVE_NONCANONICAL_CANDIDATE`
- `HOLD_FOR_REVIEW_DEBT`
- `REWORK_EXISTING_ARTIFACTS`

A cumulative candidate may exclude/retain explicit HOLD rows; it must not silently
upgrade them.

## Boundary

No new historical research, new targets, Qi work, P-level assignment, geometry
promotion, schema/ontology change, independent-review claim, public publication or
canonical v0.6.1 change.
