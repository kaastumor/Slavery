# Uzbekistan 2019 / Mauritania 2009 modern-context source review — 2026-10-01

**Disposition:** frozen source candidates for future `modern_proxy / navigation_context` review. Repository review only; no governed geometry promotion, historical claim change, release selection, publication or numerator increment. Internal self-review is not independent historical review.

## Source selection and exact provenance

Pinned Natural Earth repository: `nvkelso/natural-earth-vector`, commit `ca96624a56bd078437bca8184e78163e5039ad19`.

The preferred `geojson/ne_10m_admin_0_countries.geojson` exists at that commit: Git blob `5ebc66e25fc1af01edaebe9375c546655e04cf1e`, 13,287,234 bytes. Its metadata is recoverable, but its bytes are not available through this session: the GitHub fetch response exceeds the 8,388,608-byte transport cap, the file reader returns empty content, and shell network access is unavailable. No 1:10m Uzbekistan feature, ordinal or fingerprint is claimed. This is an access limitation, not rejection of the upstream geometry.

Retain the sponsor-permitted, independently frozen 1:110m fallback:

- Asset: `geojson/ne_110m_admin_0_countries.geojson`.
- Git blob: `1e6ab74c7042f97013be69ceec798be8e1aff27d`.
- Saved source bytes: **838,726**; recomputed Git SHA-1 matches the blob exactly.
- Asset SHA-256: `6866c877d39cba9c357620878839b336d569f8c662d3cfab4cb1dbe2d39c977f`.
- 177 features; exact source-native feature objects are retained in the two adjacent GeoJSON files, without property/coordinate normalization.
- Upstream `VERSION` at this commit is **5.2.0-pre**. Do not relabel this Admin-0 asset as 5.1.1 merely because that label is used for the Atlas land fabric.
- Pinned `LICENSE.md` declares the data public domain. Redistribution of these source feature extracts is permitted.
- Ordinal, identifiers, byte/fingerprint rules and QC are frozen in the adjacent JSON review record.

Source locators:
- [Pinned 1:110m asset](https://github.com/nvkelso/natural-earth-vector/blob/ca96624a56bd078437bca8184e78163e5039ad19/geojson/ne_110m_admin_0_countries.geojson)
- [Pinned 1:10m asset](https://github.com/nvkelso/natural-earth-vector/blob/ca96624a56bd078437bca8184e78163e5039ad19/geojson/ne_10m_admin_0_countries.geojson)
- [Pinned licence](https://github.com/nvkelso/natural-earth-vector/blob/ca96624a56bd078437bca8184e78163e5039ad19/LICENSE.md)
- [Pinned VERSION](https://github.com/nvkelso/natural-earth-vector/blob/ca96624a56bd078437bca8184e78163e5039ad19/VERSION)

## Case-role review

| Candidate | Exact source feature | Defensible role | Temporal limit |
| --- | --- | --- | --- |
| Uzbekistan 2019 cotton forced labour | Ordinal 6; ADMIN=Uzbekistan; ADM0_A3/ISO_A3=UZB; UN_A3=860; NE_ID=1159321405 | Modern country navigation/context, indexing the reviewed cotton-harvest claim | POP_YEAR=2019 and GDP_YEAR=2019 date statistics, not geometry validity |
| Mauritania 2009 de facto slavery | Ordinal 53; ADMIN=Mauritania; ADM0_A3/ISO_A3=MRT; UN_A3=478; NE_ID=1159321075 | Modern country navigation/context, indexing the bounded UN country-mission finding | POP_YEAR=2019 is ten years later than the mission; no 2009 boundary snapshot verified |

The Uzbekistan proposition concerns the cotton-harvest labour system and monitored local recruitment. The preserved ILO evidence also records the end of systematic central recruitment and major improvement. The polygon must not encode forced-labour distribution, prevalence or uniformity.

Mauritania's official mission finding concerns continued de facto slavery despite legal abolition/criminalization. A country outline is useful for navigating that jurisdictional context; a country-level finding does not make the outline a slavery-practice extent or identify victim/interview locations. This modern feature is **not** a verified contemporary 2009 national boundary. If contemporary geometry is required, this candidate stays unresolved for that purpose until independent boundary-date evidence is obtained.

Both polygons are coarse modern context. No `from_year/to_year` is invented for source geometry. A later implementation must explicitly review the case link and temporal use as navigation context; it may not back-project a modern outline as historical territory. Context display must be visibly separate from any practice fill, preserve the neutral land fabric and expose scale/proxy/date limitations. This review contains no browser or render-alignment acceptance.

## Fresh governed reconciliation and mechanical QC

Read-only PostgreSQL/PostGIS observations on 2026-10-01, against main `161e606ab5909557f7875fd8ddff87b6d1a195fc`:

- Uzbekistan case key `overnight-2026-09-27/uzbekistan/cotton-forced-labour-2019-v2` resolves to claim `2b456d9f-be09-4844-8899-286bd13464cb`, 2019–2019, reviewed/unpublished, one historical source link.
- Mauritania case key `overnight-2026-09-27/mauritania/de-facto-slavery-v2` resolves to claim `7f573935-45c9-4746-ac6a-6afe47bafbdd`, 2009–2009, reviewed/unpublished, one historical source link.
- Legacy proxies `053f546e-089e-4f03-aab7-3d2187c835ce` and `d966c564-f79e-4fc7-9bee-0c5ea4b935e8` remain reviewed `modern_proxy`, with NULL temporal bounds, `johan/world.geo.json` provenance and **zero release-geometry memberships each**.
- Serving remains `v0.8.1-public-mvp-v2`.
- Exact extracted coordinates were passed only to read-only PostGIS expressions: both are valid, non-empty single polygons; Uzbekistan has 54 vertices, Mauritania 39. No table insert/update occurred.

The database checks above are observations, not a complete successor-collision census or authority to write. This review does not claim no other geometry/source row exists. Fresh exact source/identity/link preflight remains required for any implementation.

## Adversarial dispositions

| Attack | Disposition |
| --- | --- |
| Prefer the detailed asset merely because its blob exists | **REVISE:** 1:10m feature bytes cannot be frozen here; retain verified 1:110m |
| Use POP_YEAR as historical boundary validity | **REJECT:** statistical metadata is not boundary chronology |
| Call Mauritania's current outline contemporary to the mission | **REJECT:** modern navigation only; 2009 boundary unverified |
| Treat a country polygon as forced-labour/slavery extent | **REJECT:** both source claims explicitly withhold national prevalence surfaces |
| Count two extracted feature rows immediately | **REJECT:** neither is governed, case-linked/review-promoted or release-selected |
| Silently replace old proxy/release objects | **REJECT:** future reviewed successor logic must preserve old rows and immutable history |

## Remaining distinct-case geometry recoverability

This is a planning ranking from existing accepted/reviewed repository packets, not completed new source research or extra geo acceptance.

| Priority | Case(s) | Recoverability / exact next requirement |
| --- | --- | --- |
| Already prepared, authorization-bound | India 2003–2005; Myanmar 1998; Pakistan 1990s | #374 has claim-linked locus/context work and rehearsal; preserve its exact production gate |
| Source extraction now frozen | Uzbekistan 2019; Mauritania 2009 | Explicit modern-context candidates only; future case-link/temporal/render review, exact preflight and separate production authority |
| Next read-only qualification | Nepal 1998–2001 | Recover exact named far/mid-western fieldwork districts from the 1998/2001 ILO editions, then authoritative source-native district/site locators compatible with that interval |
| Following | Paraguay 2005 | Recover named investigation/ranch-area loci in the Paraguayan Chaco; a Chaco/admin-area context is not all-ranch extent |
| More complex multi-locus review | Bolivia 2004 | Keep Santa Cruz sugar, northern Amazon Brazil-nut and Chaco captive-community settings separate; resolve source-named subnational loci individually |

The ordering of Nepal/Paraguay/Bolivia is a provisional recoverability inference, not a measured source-search result. Nazi Germany is a #374 replacement/reconciliation case, not a ninth distinct addition. Brazil and Peru remain replacement/reconciliation cases; Brazil's Correntes/Corrente identity HOLD is not cleared.

## Effects, gates and re-entry

- Historical-case effect: **0**; existing substantive classifications, dates, source dependence and P-levels unchanged.
- Released geo-numerator effect: **0**. Two frozen source candidates improve reproducibility, but are not two accepted mapped cases.
- Source-native extracts and this review may become canonical **repository review evidence** after the review-only PR is accepted. They do not become governed research geometry or immutable release members.
- The exact five-case D-124 pilot, #370, #374 and #379 production gates stay closed. Any later proxy production write needs its own exact authorization, preflight, reviewed case role, rehearsal and independent readback.
- `v0.8.2` remains D-121 HOLD. Successor selection, release publication and public-serving cutover are separate, closed gates.
- Exact next eligible work: read the source-native Nepal ILO fieldwork locators and qualify bounded subnational navigation/evidence context without creating a national practice polygon or a sixth admission packet.

## Validation boundary

Local focused verification passed: full asset byte count/Git blob/SHA-256, both source-exact feature extractions, unique native IDs and ordinals, exact file/canonical feature fingerprints, bboxes, vertex counts, closed rings and coordinate bounds. Changed-file sanitation and required structure were checked against the live Git tree; the local candidate is a partial snapshot. PostGIS validity was independently evaluated with read-only expressions as recorded above. Full current-main sanitation/Python/database regression checks are owned by exact-head Foundation CI. No browser/render verification or new independent historical review is claimed.
