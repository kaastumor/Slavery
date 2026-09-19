-- v0.6.1 reconciliation tests. Run only after the controlled workbook seed has been migrated.
-- Expected values come from the canonical v0.6.1 Atlantic sheets plus the four global evidence sheets.

DO $$
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n FROM atlas.voyage;
    IF n <> 8 THEN RAISE EXCEPTION 'Expected 8 voyages, found %', n; END IF;

    SELECT count(*) INTO n FROM atlas.actor;
    IF n <> 11 THEN RAISE EXCEPTION 'Expected 11 real actors after dropping the fake unknown-owner identity, found %', n; END IF;

    SELECT count(*) INTO n FROM atlas.voyage_owner;
    IF n <> 12 THEN RAISE EXCEPTION 'Expected 12 voyage-owner/status rows including one missing-owner row, found %', n; END IF;

    SELECT count(*) INTO n FROM atlas.voyage_owner WHERE actor_id IS NOT NULL;
    IF n <> 11 THEN RAISE EXCEPTION 'Expected 11 actor-linked owner relations, found %', n; END IF;

    SELECT count(*) INTO n FROM atlas.voyage_owner WHERE relationship_status = 'missing_owner' AND actor_id IS NULL;
    IF n <> 1 THEN RAISE EXCEPTION 'Expected exactly one explicit missing-owner row, found %', n; END IF;

    SELECT count(*) INTO n FROM audit.v061_source_map;
    IF n <> 17 THEN RAISE EXCEPTION 'Expected 17 legacy source mappings, found %', n; END IF;

    SELECT count(DISTINCT legacy_evidence_id) INTO n FROM audit.v061_evidence_claim_map;
    IF n <> 29 THEN RAISE EXCEPTION 'Expected 11 Atlantic evidence IDs + 18 positive/disputed global evidence rows to map to claims, found %', n; END IF;
END $$;

DO $$
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n FROM atlas.voyage v JOIN atlas.voyage_owner vo ON vo.voyage_id = v.voyage_id
    WHERE v.source_native_voyage_id = '557' AND v.source_dataset = 'Trans-Atlantic' AND vo.relationship_status = 'missing_owner' AND vo.actor_id IS NULL;
    IF n <> 1 THEN RAISE EXCEPTION 'Orestes missing-owner control failed'; END IF;
END $$;

DO $$
DECLARE val text;
BEGIN
    SELECT flag_documented INTO val FROM atlas.voyage WHERE source_native_voyage_id = '36144' AND source_dataset = 'Trans-Atlantic';
    IF val IS DISTINCT FROM 'U.S.A.' THEN RAISE EXCEPTION 'Westmoreland raw carrier value changed: %', val; END IF;
END $$;

DO $$
DECLARE c integer; s text;
BEGIN
    SELECT disembarked_count, disembarked_status INTO c, s FROM atlas.voyage WHERE source_native_voyage_id = '35181' AND source_dataset = 'Trans-Atlantic';
    IF c IS NOT NULL THEN RAISE EXCEPTION 'Fredensborg disembarked_count must remain NULL pending reconciliation'; END IF;
    IF s IS DISTINCT FROM 'Needs source reconciliation' THEN RAISE EXCEPTION 'Fredensborg unresolved status changed: %', s; END IF;
END $$;

DO $$
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n FROM atlas.actor_attribute_claim aac JOIN atlas.claim c ON c.claim_id = aac.claim_id
    WHERE aac.attribute_type_code = 'nationality_political_identity' AND aac.value_text = 'French' AND c.review_status = 'reviewed';
    IF n <> 1 THEN RAISE EXCEPTION 'Expected one reviewed French nationality positive-control claim, found %', n; END IF;
END $$;

DO $$
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n FROM audit.v061_evidence_claim_map;
    IF n <> 39 THEN RAISE EXCEPTION 'Expected 17 Atlantic + 22 global evidence-to-claim mappings after semantic split, found %', n; END IF;
    SELECT count(*) INTO n FROM audit.v061_evidence_claim_map WHERE legacy_evidence_id = 'E-011';
    IF n <> 5 THEN RAISE EXCEPTION 'E-011 should support five Martha co-owner claims, found %', n; END IF;
    SELECT count(*) INTO n FROM audit.v061_evidence_claim_map WHERE legacy_evidence_id = 'E-003';
    IF n <> 2 THEN RAISE EXCEPTION 'E-003 should split into commercial-role and business-base claims, found %', n; END IF;
    SELECT count(*) INTO n FROM audit.v061_evidence_claim_map WHERE legacy_evidence_id = 'E-006';
    IF n <> 2 THEN RAISE EXCEPTION 'E-006 should support corporate-jurisdiction and Fredensborg ownership claims, found %', n; END IF;
END $$;

DO $$
DECLARE u text; n integer;
BEGIN
    SELECT sv.url_or_identifier INTO u FROM atlas.voyage v JOIN atlas.source_version sv ON sv.source_version_id = v.primary_source_version_id
    WHERE v.source_native_voyage_id = '35181' AND v.source_dataset = 'Trans-Atlantic';
    IF u IS DISTINCT FROM 'https://www.slavevoyages.org/voyage/35181/variables' THEN RAISE EXCEPTION 'Fredensborg exact source URL was substituted or lost: %', u; END IF;
    SELECT count(*) INTO n FROM audit.qc_issue WHERE issue_code = 'V061_SOURCE_REGISTRY_GAP' AND object_identifier = 'https://www.slavevoyages.org/voyage/35181/variables';
    IF n <> 1 THEN RAISE EXCEPTION 'Expected one Fredensborg source-registry-gap QC issue, found %', n; END IF;
END $$;

DO $$
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n FROM raw.raw_record WHERE record_type = 'v061_workbook_row';
    IF n <> 288 THEN RAISE EXCEPTION 'Expected 288 non-empty workbook rows raw-preserved, found %', n; END IF;
    SELECT count(*) INTO n FROM raw.raw_record WHERE record_type = 'v061_workbook_row' AND source_native_id LIKE 'v0.4.7 Evidence!%';
    IF n <> 13 THEN RAISE EXCEPTION 'Expected 13 raw rows from v0.4.7 Evidence, found %', n; END IF;
    SELECT count(*) INTO n FROM raw.raw_record WHERE record_type = 'v061_workbook_row' AND source_native_id LIKE 'v0.4.8 Evidence!%';
    IF n <> 9 THEN RAISE EXCEPTION 'Expected 9 raw rows from v0.4.8 Evidence, found %', n; END IF;
    SELECT count(*) INTO n FROM raw.raw_record WHERE record_type = 'v061_workbook_row' AND source_native_id LIKE 'v0.4.9 Evidence!%';
    IF n <> 12 THEN RAISE EXCEPTION 'Expected 12 raw rows from v0.4.9 Evidence, found %', n; END IF;
    SELECT count(*) INTO n FROM raw.raw_record WHERE record_type = 'v061_workbook_row' AND source_native_id LIKE 'v0.5.0 Evidence!%';
    IF n <> 14 THEN RAISE EXCEPTION 'Expected 14 raw rows from v0.5.0 Evidence, found %', n; END IF;
END $$;

DO $
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n
    FROM audit.v061_evidence_claim_map
    WHERE legacy_evidence_id LIKE 'v0.% Evidence!%';
    IF n <> 22 THEN RAISE EXCEPTION 'Expected 22 global evidence-to-claim mappings, found %', n; END IF;

    SELECT count(DISTINCT legacy_evidence_id) INTO n
    FROM audit.v061_evidence_claim_map
    WHERE legacy_evidence_id LIKE 'v0.% Evidence!%';
    IF n <> 18 THEN RAISE EXCEPTION 'Expected 18 positive/disputed global evidence rows to map to claims, found %', n; END IF;

    SELECT count(*) INTO n
    FROM audit.research_coverage_source
    WHERE source_role = 'evidence_sheet_source';
    IF n <> 36 THEN RAISE EXCEPTION 'Expected all 36 global evidence rows to retain coverage-source provenance, found %', n; END IF;

    SELECT count(DISTINCT source_version_id) INTO n
    FROM audit.research_coverage_source
    WHERE source_role = 'evidence_sheet_source';
    IF n <> 29 THEN RAISE EXCEPTION 'Expected 29 unique global evidence source versions, found %', n; END IF;
END $;

DO $
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n
    FROM audit.v061_evidence_claim_map m
    JOIN atlas.territorial_practice_claim tpc ON tpc.claim_id = m.claim_id
    WHERE m.legacy_evidence_id LIKE 'v0.% Evidence!%';
    IF n <> 18 THEN RAISE EXCEPTION 'Expected 18 migrated global territorial-practice claims, found %', n; END IF;

    SELECT count(*) INTO n
    FROM audit.v061_evidence_claim_map m
    JOIN atlas.territorial_practice_claim tpc ON tpc.claim_id = m.claim_id
    WHERE m.legacy_evidence_id LIKE 'v0.% Evidence!%'
      AND tpc.practice_level IS NOT NULL;
    IF n <> 0 THEN RAISE EXCEPTION 'Global workbook migration must not auto-assign P0-P4; found % assigned levels', n; END IF;

    SELECT count(*) INTO n
    FROM audit.v061_evidence_claim_map m
    JOIN atlas.external_participation_claim epc ON epc.claim_id = m.claim_id
    WHERE m.legacy_evidence_id LIKE 'v0.% Evidence!%';
    IF n <> 3 THEN RAISE EXCEPTION 'Expected 3 global external-participation claims, found %', n; END IF;

    SELECT count(*) INTO n
    FROM audit.v061_evidence_claim_map m
    JOIN atlas.legal_event le ON le.claim_id = m.claim_id
    WHERE m.legacy_evidence_id LIKE 'v0.% Evidence!%';
    IF n <> 1 THEN RAISE EXCEPTION 'Expected 1 global legal-event claim, found %', n; END IF;
END $;

DO $
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n
    FROM audit.v061_evidence_claim_map
    WHERE legacy_evidence_id = 'v0.4.9 Evidence!5'
      AND mapping_role = 'external_participation:slave_trade_network';
    IF n <> 1 THEN RAISE EXCEPTION 'Anshan/Elam must remain external participation only'; END IF;

    SELECT count(*) INTO n
    FROM audit.v061_evidence_claim_map
    WHERE legacy_evidence_id = 'v0.4.9 Evidence!10'
      AND mapping_role IN (
          'territorial_practice:captive_taking_incorporation',
          'territorial_practice:slavery_enslavement'
      );
    IF n <> 2 THEN RAISE EXCEPTION 'Shang must preserve captive-taking and disputed slavery as two separate mappings'; END IF;
END $;

DO $
DECLARE n integer;
BEGIN
    SELECT count(*) INTO n
    FROM audit.qc_issue
    WHERE issue_code = 'V061_GLOBAL_EVIDENCE_SEMANTIC_MIGRATION_PENDING'
      AND severity = 'blocking'
      AND resolved = false;
    IF n <> 0 THEN RAISE EXCEPTION 'Global evidence semantic-migration blocking issue should be absent after completed migration, found %', n; END IF;
END $;
