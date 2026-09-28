# Atlas closeout — 2026-09-28

Status: review and correction checkpoint complete; v0.8.2 release remains HOLD.

Inspected PR #363 head `88061d12b5455c5b681d508984af3e444d3f2a4b`, main `d0d16ac2b1580bfb4907446a77ee7c11a0a81d25`, #332 and #360. The four checks on the inspected code head passed. This follow-up adds evidence only. It does not merge, publish, write the database or alter worker schedules.

## Exact database evidence recovered

The available Supabase read connection successfully exported all explicitly selected objects plus active cartography in one SELECT statement at **2026-09-28 21:40:20.691279 UTC**. Membership derives from immutable v0.8.1 plus the eleven frozen additions, two Mycenaean locus points, and only their source dependencies; it does not discover arbitrary reviewed rows.

| Group | Count |
| --- | ---: |
| Claims | 86 |
| Actors | 11 |
| Spatial entities | 63 |
| Geometries | 48 |
| Voyages | 8 |
| Coverage assessments | 99 |
| Source versions | 310 |
| Research target results | 26 |

The predecessor authority file's bytes match its required SHA-256 `0aa4d4fd9e4bacad0e359b655fbe237d1ef758b63fcb984ead9651d2c8181ea5`. The repository's actual `load_predecessor` and `verify_predecessor_objects_preserved` routines pass on the captured data. The only changed predecessor object is Mycenaean claim `8691d038-1683-5331-bccb-e7a189cdd229`, with exactly the selected evidence-locus augmentation. Cartography matches the predecessor exactly.

All eleven selected claims are reviewed, unpublished territorial-practice claims, have the specified target and linked claim sources, a reviewed classification, and NULL practice level. The actual authority selection loader still rejects the HOLD selection, as required.

[Fingerprints](current-state-fingerprints.json) pin every object; [read-only SQL](current-state-diagnostic.sql) records the export query. The full diagnostic snapshot is retained in the accompanying `atlas-closeout-evidence-2026-09-28.zip` archive. Diagnostic database-state fingerprint: `ef6640f409e2fa8cf3c085af8e34f92c87e73ba228ba5f7c984e028552c5d689`. This is **not** an authority bundle, historical source acceptance or release permission. The export gate is satisfied for this observation; rerun exact validation when D-121 is closed and authority is actually frozen.

## Funan delivery reconciled

Read back the complete raw Drive packet `17BDDcq29H1_utucSSXfuSDzb_sNggq2G`: 13,772 bytes; SHA-256 `42d5364220921e0c93e5c713fcee054dae78fc367764f1a15019eda2efc0319b`. PR #363 head above already consumes its bounded Southern Qi wording, Stark/Pelliot locators, shared-testimony qualification and temporal-review warning. **Receipt disposition: received and incorporated into the PR candidate; substantive source acceptance still pending.** The packet's earlier embedded delivery-blocked text is superseded by this verified receipt, not rewritten as if it had never been blocked. Original scheduled-run attempt identity remains unknown; this receipt does not authenticate earlier packets.

## D-121: concrete unresolved provenance

See [provenance checkpoint](d121_checkpoint.md) and [per-geometry inventory](d121_candidate_inventory.json). Exact upstream files were recovered and hashed. The Cliopatria ZIP has no numeric Seshat API IDs: 37 of 38 API-sourced polygons have a unique name/interval comparator, but Maurya API record 15654 spans an interval represented by two ZIP features. Shape/date similarity is insufficient to establish the historical API record binding. Confidence is high in this observed provenance gap; it is not evidence that v0.8.1's geometry is wrong.

Smallest correction: recover the original API response assets or a reviewed source crosswalk, bind every source feature and native interval, and record the parser/calendar conversion. Review the AWMC AD14 temporal proxy and source-specific point-date rationale, including the two new Mycenaean points. Verify against frozen source hashes and exact membership before changing the HOLD flag. Do not substitute already loaded Atlas dates for independent source-native dates.

## Remaining work and acceptance

1. Close D-121 with the evidence above, then rerun the exact authority build and state checks.
2. Complete Funan source/temporal adjudication before treating the proposed intake text as accepted canonical research.
3. Reconcile or explicitly disposition the historical worker backlog in #360. Run 1 inspected 120 marked notes, but original packet revision/checksum/attempt/consumer acknowledgments were absent. This session could not reopen those chats because its browser was signed out; original identities remain UNKNOWN. The already successful synthetic delivery test is not historical backlog acceptance. No further synthetic test or new intake was started.
4. After authority acceptance, materialize the actual successor package and verify its desktop/mobile claim-to-source path. Existing v0.8.1/browser checks do not prove the as-yet unbuilt successor.
5. Obtain scoped approval for merge, DB application or publication when those concrete candidates are ready, as required by AGENTS/WoW. #332 stays active; #360 remains gated.

Red-team check: fresh export does not close source provenance; plausible ZIP matches do not identify API records; delivery acknowledgment is not historical acceptance; a stopped/finished worker is not a reconciled packet; green current-release UI checks are not successor acceptance. No criterion was relaxed to mark Atlas done.

