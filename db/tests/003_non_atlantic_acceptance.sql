-- Non-Atlantic schema acceptance fixtures drawn from evidence already present in canonical v0.6.1.
-- Test-only: everything is rolled back. These rows do NOT become canonical atlas data.
-- The fixtures deliberately do not translate legacy S/P/D/RI coverage codes into P0-P4.

BEGIN;

-- Exact workbook source URLs, represented as test-only source versions.
INSERT INTO atlas.source(source_id, title, source_type, source_classification, notes) VALUES
('10000000-0000-4000-8000-000000000001', 'v0.6.1 fixture source — Carolingian Empire', 'scholarship', 'secondary', 'Test fixture sourced from v0.4.7 Evidence'),
('10000000-0000-4000-8000-000000000002', 'v0.6.1 fixture source — Mycenaean Greece', 'scholarship', 'secondary', 'Test fixture sourced from v0.4.9 Evidence'),
('10000000-0000-4000-8000-000000000003', 'v0.6.1 fixture source — Shang China', 'scholarship', 'secondary', 'Test fixture sourced from v0.4.9 Evidence'),
('10000000-0000-4000-8000-000000000004', 'v0.6.1 fixture source — Indus Civilization', 'scholarship', 'secondary', 'Test fixture sourced from v0.4.9 Evidence'),
('10000000-0000-4000-8000-000000000005', 'v0.6.1 fixture source — Ottoman Middle East', 'scholarship', 'secondary', 'Test fixture sourced from v0.4.7 Evidence'),
('10000000-0000-4000-8000-000000000006', 'v0.6.1 fixture source — Anshan / Elam', 'scholarship', 'secondary', 'Test fixture sourced from v0.4.9 Evidence'),
('10000000-0000-4000-8000-000000000007', 'v0.6.1 fixture source — Peruvian Amazon', 'institutional study', 'secondary', 'Test fixture sourced from v0.4.7 Evidence');

INSERT INTO atlas.source_version(source_version_id, source_id, version_label, url_or_identifier, notes) VALUES
('11000000-0000-4000-8000-000000000001', '10000000-0000-4000-8000-000000000001', 'v0.6.1 referenced web state', 'https://www.cambridge.org/core/books/abs/cambridge-world-history-of-slavery/slavery-in-the-carolingian-empire/0839B9865AE0551A900206FEA94A60BD', 'Exact URL from canonical workbook'),
('11000000-0000-4000-8000-000000000002', '10000000-0000-4000-8000-000000000002', 'v0.6.1 referenced web state', 'https://ajaonline.org/book-review/639/', 'Exact URL from canonical workbook'),
('11000000-0000-4000-8000-000000000003', '10000000-0000-4000-8000-000000000003', 'v0.6.1 referenced web state', 'https://www.cambridge.org/core/books/violence-kinship-and-the-early-chinese-state/violence-and-shang-civilization/0CC7BBDF8C61D567EE49A706A0011CA2', 'Exact URL from canonical workbook'),
('11000000-0000-4000-8000-000000000004', '10000000-0000-4000-8000-000000000004', 'v0.6.1 referenced web state', 'https://www.harappa.com/answers/there-any-indication-slavery-or-ritual-human-sacrifice-ivc', 'Exact URL from canonical workbook'),
('11000000-0000-4000-8000-000000000005', '10000000-0000-4000-8000-000000000005', 'v0.6.1 referenced web state', 'https://www.cambridge.org/core/books/abs/cambridge-world-history-of-slavery/ottoman-slavery-and-abolition-in-the-nineteenth-century/854C54336AF6B048CD2FD56A566D3406', 'Exact URL from canonical workbook'),
('11000000-0000-4000-8000-000000000006', '10000000-0000-4000-8000-000000000006', 'v0.6.1 referenced web state', 'https://www.cambridge.org/core/journals/iraq/article/abs/gudeas-iranian-slaves-an-anatomy-of-transregional-forced-mobility/0174663296EB743D7387E7C64FA91DF7', 'Exact URL from canonical workbook'),
('11000000-0000-4000-8000-000000000007', '10000000-0000-4000-8000-000000000007', 'v0.6.1 referenced web state', 'https://www.ilo.org/publications/forced-labor-timber-extraction-peruvian-amazon', 'Exact URL from canonical workbook');

INSERT INTO atlas.spatial_entity(spatial_entity_id, entity_type_code, canonical_name, display_name, review_status, notes) VALUES
('20000000-0000-4000-8000-000000000001', 'polity', 'Carolingian Empire', 'Carolingian Empire', 'reviewed', 'Test-only non-Atlantic fixture'),
('20000000-0000-4000-8000-000000000002', 'region', 'Mycenaean Greece (Pylos/Knossos)', 'Mycenaean Greece (Pylos/Knossos)', 'reviewed', 'Workbook evidence target; not forced into a modern-state identity'),
('20000000-0000-4000-8000-000000000003', 'polity', 'Shang China', 'Shang China', 'reviewed', 'Test-only non-Atlantic fixture'),
('20000000-0000-4000-8000-000000000004', 'region', 'Indus Civilization', 'Indus Civilization', 'reviewed', 'Civilization/evidence universe; not a modern-state proxy'),
('20000000-0000-4000-8000-000000000005', 'region', 'Ottoman Middle East', 'Ottoman Middle East', 'reviewed', 'Broad workbook evidence target; not silently reduced to one modern state'),
('20000000-0000-4000-8000-000000000006', 'region', 'Anshan / Elam', 'Anshan / Elam', 'reviewed', 'Broad historical target for c. 2130–2110 BCE fixture'),
('20000000-0000-4000-8000-000000000007', 'region', 'Peruvian Amazon', 'Peruvian Amazon', 'reviewed', 'Non-state regional target from canonical workbook');

INSERT INTO atlas.polity(spatial_entity_id, polity_type, notes) VALUES
('20000000-0000-4000-8000-000000000001', 'historical polity', 'Test fixture only'),
('20000000-0000-4000-8000-000000000003', 'historical polity', 'Test fixture only');

INSERT INTO atlas.geometry(
    geometry_id, spatial_entity_id, from_year, to_year,
    resolution_method, accuracy_status, geom, notes, review_status
) VALUES (
    '21000000-0000-4000-8000-000000000001',
    '20000000-0000-4000-8000-000000000007',
    1900, NULL,
    'unresolved_test_fixture', 'unresolved', NULL,
    'No geometry invented for this acceptance fixture.', 'reviewed'
);

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, summary, review_status, publication_status, notes
) VALUES (
    '30000000-0000-4000-8000-000000000001', 'territorial_practice', 500, 999, '500–999 CE',
    'broad_research_period',
    'Enslavement through trade, self-sale and penal enslavement; household slavery, estate slavery and legal regulation are directly treated in current scholarship.',
    'reviewed', 'unpublished',
    'Canonical workbook coverage code is S; P-level intentionally unassigned in the test fixture.'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status, notes
) VALUES (
    '30000000-0000-4000-8000-000000000001', '20000000-0000-4000-8000-000000000001',
    'slavery_enslavement', NULL, 'reviewed',
    'Strong/map-ready evidence package in legacy audit; no P0–P4 assessment imported from S.',
    'Tests separation of research coverage from practice intensity.'
);
INSERT INTO atlas.claim_source(claim_id, source_version_id, evidence_role, direction) VALUES
('30000000-0000-4000-8000-000000000001', '11000000-0000-4000-8000-000000000001', 'workbook evidence row', 'supports');

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, summary, review_status, publication_status
) VALUES (
    '30000000-0000-4000-8000-000000000002', 'territorial_practice', -1999, -1000, '2000–1001 BCE',
    'broad_research_period',
    'Linear B contains a specific do-e-ro/do-e-ra category, including people belonging to individuals and evidence interpreted as slave purchases. Some slaves of the god had atypical rights, so the status was internally differentiated, but slavery itself is secure.',
    'reviewed', 'unpublished'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status, notes
) VALUES (
    '30000000-0000-4000-8000-000000000002', '20000000-0000-4000-8000-000000000002',
    'slavery_enslavement', NULL, 'reviewed',
    'Direct terminology and some purchase/property evidence; no P-level assigned by the workbook.',
    'Tests bounded deep-history evidence without false P-level precision.'
);
INSERT INTO atlas.claim_source(claim_id, source_version_id, evidence_role, direction) VALUES
('30000000-0000-4000-8000-000000000002', '11000000-0000-4000-8000-000000000002', 'workbook evidence row', 'supports');

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, summary, review_status, publication_status
) VALUES (
    '30000000-0000-4000-8000-000000000003', 'territorial_practice', -1999, -1000, '2000–1001 BCE',
    'broad_research_period',
    'Captive-taking and sacrifice are unequivocal, while interpretation of captives as evidence of a slave society remains disputed.',
    'reviewed', 'unpublished'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status, notes
) VALUES (
    '30000000-0000-4000-8000-000000000003', '20000000-0000-4000-8000-000000000003',
    'captive_taking_incorporation', NULL, 'disputed',
    'Slavery classification disputed; captivity is retained separately.',
    'Legacy D is not translated into a P-level.'
);
INSERT INTO atlas.claim_source(claim_id, source_version_id, evidence_role, direction) VALUES
('30000000-0000-4000-8000-000000000003', '11000000-0000-4000-8000-000000000003', 'workbook evidence row', 'qualifies');

INSERT INTO audit.research_coverage_assessment(
    coverage_assessment_id, spatial_entity_id, region_label_raw, period_label_raw,
    from_year, to_year, legacy_coverage_code, normalized_coverage_state_code,
    release_version, review_status, publication_status, notes
) VALUES (
    '40000000-0000-4000-8000-000000000001', '20000000-0000-4000-8000-000000000004',
    'South Asia', '3000–2001 BCE', -2999, -2000, 'RI', 'researched_inconclusive',
    '0.6.1-test-fixture', 'reviewed', 'unpublished',
    'Harappan specialists cited in the workbook state there is currently no evidence demonstrating slavery while noting that absence of depiction does not prove absence.'
);

INSERT INTO audit.research_coverage_source(
    coverage_assessment_id, source_version_id, source_role, notes
) VALUES (
    '40000000-0000-4000-8000-000000000001',
    '11000000-0000-4000-8000-000000000004',
    'reviewed_source',
    'Exact source URL from the RI evidence row; this records research coverage, not a positive slavery claim.'
);

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, summary, review_status, publication_status
) VALUES
(
    '30000000-0000-4000-8000-000000000005', 'territorial_practice', 1800, 1899, '1800–1899',
    'broad_research_period',
    'Nineteenth-century Ottoman slavery remained a major institution.',
    'reviewed', 'unpublished'
),
(
    '30000000-0000-4000-8000-000000000006', 'legal_event', 1800, 1899, '1800–1899',
    'broad_research_period',
    'Suppression proceeded piecemeal through restrictions on markets and specific trade routes rather than a single clean abolition date.',
    'reviewed', 'unpublished'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status, notes
) VALUES (
    '30000000-0000-4000-8000-000000000005', '20000000-0000-4000-8000-000000000005',
    'slavery_enslavement', NULL, 'reviewed',
    'Practice persisted while suppression measures developed.',
    'No P-level inferred from the legacy S coverage code.'
);
INSERT INTO atlas.legal_event(
    claim_id, jurisdiction_spatial_entity_id, event_type,
    legal_status_after, instrument_name, scope, effective_date_text, notes
) VALUES (
    '30000000-0000-4000-8000-000000000006', '20000000-0000-4000-8000-000000000005',
    'piecemeal_suppression_restrictions', NULL, NULL,
    'Restrictions on markets and specific trade routes; no single clean abolition date in the workbook evidence statement.',
    '19th century',
    'The fixture intentionally does not invent a single instrument or abolition date.'
);
INSERT INTO atlas.claim_source(claim_id, source_version_id, evidence_role, direction) VALUES
('30000000-0000-4000-8000-000000000005', '11000000-0000-4000-8000-000000000005', 'workbook evidence row — practice', 'supports'),
('30000000-0000-4000-8000-000000000006', '11000000-0000-4000-8000-000000000005', 'workbook evidence row — legal/suppression context', 'supports');

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, temporal_certainty, spatial_precision,
    summary, review_status, publication_status, notes
) VALUES (
    '30000000-0000-4000-8000-000000000007', 'external_participation', -2129, -2109, 'c. 2130–2110 BCE',
    'circa_range', 'approximate', 'regional_network_target',
    'Gudea''s dossier documents an intensive influx of Elamite slaves from Anshan/Fars through capture, purchase, tribute and gifting; this supports network participation but not a full territorial prevalence classification for Elam.',
    'reviewed', 'unpublished',
    'Tests BCE conversion and preserves the workbook caution against territorial overclassification.'
);
INSERT INTO atlas.external_participation_claim(
    claim_id, spatial_entity_id, actor_id, participation_type_code, role_text, notes
) VALUES (
    '30000000-0000-4000-8000-000000000007',
    '20000000-0000-4000-8000-000000000006', NULL,
    'slave_trade_network',
    'Capture, purchase, tribute and gifting network linked to Anshan/Fars',
    'Stored as external/network participation because the workbook explicitly cautions against a full territorial prevalence classification for Elam.'
);
INSERT INTO atlas.claim_source(claim_id, source_version_id, evidence_role, direction) VALUES
('30000000-0000-4000-8000-000000000007', '11000000-0000-4000-8000-000000000006', 'workbook evidence row', 'supports');

INSERT INTO atlas.claim(
    claim_id, claim_kind_code, from_year, to_year, date_text_original,
    temporal_precision, spatial_precision, summary, review_status, publication_status
) VALUES (
    '30000000-0000-4000-8000-000000000008', 'territorial_practice', 1900, NULL, '1900–present',
    'broad_research_period_not_exact_onset', 'regional',
    'ILO studies document enganche recruitment, accumulating debts, threats and coercion in timber extraction.',
    'reviewed', 'unpublished'
);
INSERT INTO atlas.territorial_practice_claim(
    claim_id, spatial_entity_id, practice_type_code, practice_level,
    coverage_state_code, classification_status, notes
) VALUES (
    '30000000-0000-4000-8000-000000000008', '20000000-0000-4000-8000-000000000007',
    'debt_bondage', NULL, 'reviewed',
    'Debt bondage / forced labour evidence in a non-state regional target.',
    'The broad 1900–present workbook period is explicitly marked as a research-period envelope, not an exact onset date.'
);
INSERT INTO atlas.claim_source(claim_id, source_version_id, evidence_role, direction) VALUES
('30000000-0000-4000-8000-000000000008', '11000000-0000-4000-8000-000000000007', 'workbook evidence row', 'supports');

DO $test$
BEGIN
    IF EXISTS (
        SELECT 1 FROM atlas.territorial_practice_claim
        WHERE claim_id IN (
            '30000000-0000-4000-8000-000000000001'::uuid,
            '30000000-0000-4000-8000-000000000002'::uuid,
            '30000000-0000-4000-8000-000000000003'::uuid,
            '30000000-0000-4000-8000-000000000005'::uuid,
            '30000000-0000-4000-8000-000000000008'::uuid
        ) AND practice_level IS NOT NULL
    ) THEN
        RAISE EXCEPTION 'Legacy S/D/other evidence fixtures were mechanically assigned a P-level';
    END IF;

    IF EXISTS (
        SELECT 1 FROM atlas.territorial_practice_claim
        WHERE spatial_entity_id = '20000000-0000-4000-8000-000000000004'::uuid
    ) THEN
        RAISE EXCEPTION 'Indus RI fixture incorrectly produced a positive territorial-practice claim';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM audit.research_coverage_assessment
        WHERE coverage_assessment_id = '40000000-0000-4000-8000-000000000001'::uuid
          AND legacy_coverage_code = 'RI'
          AND normalized_coverage_state_code = 'researched_inconclusive'
    ) THEN
        RAISE EXCEPTION 'RI research-coverage fixture missing or misclassified';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM audit.research_coverage_source
        WHERE coverage_assessment_id = '40000000-0000-4000-8000-000000000001'::uuid
          AND source_version_id = '11000000-0000-4000-8000-000000000004'::uuid
    ) THEN
        RAISE EXCEPTION 'RI research-coverage source provenance is missing';
    END IF;

    IF (SELECT count(*) FROM atlas.claim
        WHERE claim_id IN (
            '30000000-0000-4000-8000-000000000005'::uuid,
            '30000000-0000-4000-8000-000000000006'::uuid
        )) <> 2 THEN
        RAISE EXCEPTION 'Ottoman law/practice fixtures are not independent claim objects';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM atlas.claim
        WHERE claim_id = '30000000-0000-4000-8000-000000000007'::uuid
          AND -2129 <@ valid_years
          AND -2109 <@ valid_years
          AND NOT (-2130 <@ valid_years)
    ) THEN
        RAISE EXCEPTION 'BCE astronomical-year range fixture failed';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM atlas.external_participation_claim e
        WHERE e.claim_id = '30000000-0000-4000-8000-000000000007'::uuid
          AND e.participation_type_code = 'slave_trade_network'
          AND e.spatial_entity_id = '20000000-0000-4000-8000-000000000006'::uuid
    ) THEN
        RAISE EXCEPTION 'External-participation fixture failed for Anshan/Elam';
    END IF;

    IF EXISTS (
        SELECT 1 FROM atlas.territorial_practice_claim
        WHERE spatial_entity_id = '20000000-0000-4000-8000-000000000006'::uuid
    ) THEN
        RAISE EXCEPTION 'Anshan/Elam network participation was incorrectly converted to territorial practice';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM atlas.territorial_practice_claim t
        JOIN atlas.spatial_entity s USING (spatial_entity_id)
        WHERE t.claim_id = '30000000-0000-4000-8000-000000000008'::uuid
          AND s.entity_type_code = 'region'
    ) THEN
        RAISE EXCEPTION 'Non-state spatial target fixture failed';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM atlas.geometry
        WHERE geometry_id = '21000000-0000-4000-8000-000000000001'::uuid
          AND accuracy_status = 'unresolved'
          AND geom IS NULL
    ) THEN
        RAISE EXCEPTION 'Unresolved geometry fixture failed';
    END IF;

    IF EXISTS (
        SELECT 1 FROM publish.claim
        WHERE claim_id::text LIKE '30000000-0000-4000-8000-%'
    ) THEN
        RAISE EXCEPTION 'Unpublished test claims leaked through publish.claim';
    END IF;

    RAISE NOTICE 'Non-Atlantic acceptance fixtures passed';
END
$test$;

ROLLBACK;
