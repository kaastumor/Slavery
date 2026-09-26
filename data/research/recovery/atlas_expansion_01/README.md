# Atlas Expansion 01 — recovery-first intake

Issue: #332  
Canonical public release while this work is in review: **v0.7.0 unchanged**

## Why recovery comes first

The canonical v0.7.0 public surface is deliberately small. The live research database
contains materially more reviewed historical work, including reviewed mapped claims
that were excluded from the conservative Gate-4/5 release.

The first expansion checkpoint therefore does **not** begin by researching only new
famous cases. It first reconciles the existing reviewed state into the current
post-M1 methodology.

At inventory freeze:

- v0.7.0 public materialization: 16 displayed entities / 18 territorial-practice claims;
- live research database: 56 spatial entities / 82 claims / 60 territorial-practice claims;
- reviewed, published, mapped claims outside v0.7.0:
  - **R0 direct recovery:** 8 claims / 7 entities;
  - **R1 prototype reconciliation:** 6 claims / 6 entities;
  - **R2 special/disputed review:** 3 claims / 2 entities.

The machine-readable IDs are frozen in `recovery_inventory.json`.

## R0 — direct recovery

These are reviewed published claims with reviewed resolved geometry and ordinary
`classification_status=reviewed`:

- Kanesh / Kültepe;
- Hittite central Anatolia (two distinct practice claims);
- Neo-Babylonian Babylonia;
- Mauryan Empire;
- Qin Empire;
- Western Han China;
- Baekje.

They may enter a next-release candidate after exact membership/source/geometry QC.
Existing P-level values are legacy metadata and are **not** newly derived.

## R1 — prototype reconciliation

These mapped claims predate the current post-M1 research contract and require a bounded
source/dependency replay before admission:

- Old Babylonian Uruk;
- New Kingdom Egypt;
- Zhengzhou Shang City — captive-taking claim;
- Neo-Assyrian Nineveh;
- Classical Athens;
- Roman Empire — early Principate.

Rome is the first replay. The new
`roman_early_principate_slavery_v2.json` package keeps the strong positive slavery
classification but does not copy the legacy P4 into a new post-M1 claim.

## R2 — special/disputed review

Mapped geometry does not settle a contested classification:

- Achaemenid Persis/Elam royal economy;
- Zhengzhou Shang City — disputed slavery interpretation.

These remain separate from direct recovery.

## Net-new weak-region intake already staged

Four previously reviewed but never ingested weak-region cases are staged separately:

- Funan;
- Hawaiian Islands / kauwā dependency;
- Southern Maya Lowlands captive-taking/incorporation;
- Songo Mnara.

All new claims have `practice_level=null`.

Songo Mnara also contains the first new mapped locus: an authoritative UNESCO World
Heritage component point. It is explicitly a site/evidence locator, **not** a slavery
practice polygon or Swahili-coast extent.

## Next checkpoint

1. CI-validate the recovery/intake packages.
2. Ingest the reviewed unpublished packages into PostgreSQL without publishing them.
3. Reconcile the remaining R1 prototype cases.
4. Freeze a bounded v0.8.0 candidate membership containing v0.7.0 plus accepted
   recovery/intake additions.
5. Red-team source dependence, claim scope, geometry overlap and release leakage before
   any public promotion.

Public v0.7.0 remains immutable throughout this work.
