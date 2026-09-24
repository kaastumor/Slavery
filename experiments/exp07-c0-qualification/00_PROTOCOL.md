# EXP-07 — C0 identity / anchor qualification

**Issue:** #229  
**Status:** preregistered and frozen before subject research  
**Canonical historical release:** v0.6.1 unchanged  
**Registry source:** `programmes/r1/r1_candidate_target_registry.json` @ blob `cec379246221d166db3830845566311077596862`  
**Selection base commit:** `ae977be37e9ba7cd959750f1c32060fafff03324`

## 1. Why this horizon exists

The frozen registry reports 15 rows as `planned_c1_unresearched_ready`. EXP-04
researched eight of those and EXP-06 researched six different rows. The remaining
untouched QA-ready C1 row is Grand Duchy of Lithuania — 1300 CE.

EXP-03 used six heterogeneous cases under experiment-local IDs and does not consume
any of the eight C0 rows frozen below.

Choosing Lithuania solely because it is the last ready row would let execution
convenience and C1 readiness determine the next historical horizon, bypassing the
specific C0-qualification question. Instead, this experiment follows the backlog rule:
when the best next direction lies in C0, qualify identity/anchor first and keep
qualification separate from subject research.

## 2. Discriminating question

Can a deliberately non-Western, structurally diverse C0 sample be converted into
defensible target frames using identity, chronology, frame and spatial-scope evidence
alone, without inspecting slavery/coercion evidence?

This is a qualification test, not a historical-practice test.

## 3. Frozen sample

| Target ID | Target | Anchor | Frozen frame |
| --- | --- | --- | --- |
| R1:N:great_zimbabwe_1400 | Great Zimbabwe | 1400 | node_site |
| R1:N:swahili_1400 | Swahili maritime trade network | 1400 | mobile_network |
| R1:N:maori_1700 | Māori communities in Aotearoa | 1700 | region_community |
| R1:N:ifugao_1700 | Ifugao communities, northern Luzon | 1700 | region_community |
| R1:P:500:C:r1 | Nobatia | 500 CE | polity |
| R1:P:500:E:r1 | Kalabhra Dynasty | 500 CE | polity |
| R1:P:-500:F:r2 | Qi | 500 BCE | polity |
| R1:P:1800:E:r1 | Khanate of Kokand | 1800 CE | polity |

The sample was selected only from frozen registry metadata. No slavery/coercion
source search was used.

Selection pressure:
- prioritize non-Atlantic/non-Western contexts;
- avoid EXP-03/04/06 subject cases and their trigger-bound reopenings;
- include four frame classes;
- include BCE, early historic, medieval/early-modern and 1800 anchors;
- include African, Oceanian, Southeast Asian, South Asian, East Asian and Central
  Asian contexts;
- include both territorial and non-territorial frames;
- do not optimize for expected positive findings.

This is not an outcome quota. Any number of rows may fail qualification.

## 4. Allowed evidence

Qualification may inspect only evidence needed to establish:
- whether the named historical object existed at or defensibly around the anchor;
- whether the target label maps to one polity, site, community-region, network,
  aggregate or another bounded frame;
- whether the anchor is exact, approximate, contested or invalid;
- whether the frozen frame class needs a limitation note;
- whether a defensible spatial scope can be described without modern back-projection;
- exact identity/chronology/source locators and uncertainty.

Specialist political history, archaeology, chronology, gazetteers, historical
geography and source-critical identity scholarship are allowed only for those
questions.

## 5. Explicitly prohibited evidence/search

Until this qualification closes, do not search for or interpret:
- slavery / slave status;
- servitude / dependency as a subject classification;
- forced or compulsory labour;
- captives as slavery evidence;
- slave trading or trafficking;
- prevalence/intensity;
- legal slavery regimes.

Do not assign P-levels, practice classifications, legal-state conclusions or network
participation conclusions. Geometry never strengthens qualification beyond spatial
identity/scope.

## 6. Per-row outputs

Each target must end in exactly one state:

- `QUALIFIED_C1_READY` — identity, anchor and frame are adequate for a later bounded
  subject-research pass;
- `HOLD_IDENTITY_OR_TIME` — target may be real but identity/chronology is too
  uncertain for subject research at the frozen anchor;
- `REJECT_FRAME_INVALID` — frozen object/frame is anachronistic or materially
  invalid;
- `QUALIFICATION_INCONCLUSIVE` — bounded qualification could not resolve the frame.

For every row preserve:
- target ID and frozen source-native values;
- evidence used for identity/anchor only;
- exact source/version/locator;
- temporal and spatial precision;
- frame limitation;
- unresolved questions;
- no absence inference.

## 7. Falsifier / stop rule

The tranche fails as a qualification method if completing it requires inspecting
slavery/coercion evidence to decide whether a target deserves promotion.

A row is held or rejected rather than rescued by subject evidence.

Stop qualification when each row has one permitted outcome and a reproducible
identity/anchor rationale. Do not continue merely to force more rows into C1.

## 8. Complexity boundary

No canonical release or schema change. No R1 reviewed-state mutation. No P-levels.
No historical-practice polygons. No public release. No database/API/frontend work.
No automatic follow-on research.

WIP = 1.

## 9. Successor gate

After qualification:
1. reconcile the eight outcomes;
2. compare only `QUALIFIED_C1_READY` rows by expected information gain;
3. freeze one bounded subject-research horizon;
4. preregister it before any slavery/coercion research begins.

Grand Duchy of Lithuania remains a valid untouched C1 row; it is deferred rather than
rejected.
