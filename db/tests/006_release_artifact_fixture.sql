-- Disposable D-054 integration fixture.
insert into atlas.source(
    source_id,title,author_or_institution,source_type,source_classification,notes
) values (
    '11111111-1111-4111-8111-111111111111'::uuid,
    'D-054 fixture source','CI','fixture','primary','Disposable exact-release artifact fixture'
);

insert into atlas.source_version(
    source_version_id,source_id,version_label,url_or_identifier,license_status,redistribution_status
) values (
    '22222222-2222-4222-8222-222222222222'::uuid,
    '11111111-1111-4111-8111-111111111111'::uuid,
    'fixture-v1','https://example.invalid/d054-fixture','test-only','test-only'
);

insert into atlas.spatial_entity(
    spatial_entity_id,entity_type_code,canonical_name,display_name,from_year,to_year,review_status
) values (
    '33333333-3333-4333-8333-333333333333'::uuid,
    'polity','D-054 Fixture Polity','D-054 Fixture Polity',-100,-50,'reviewed'
);

insert into atlas.geometry(
    geometry_id,spatial_entity_id,from_year,to_year,geometry_source_version_id,
    geometry_source_native_id,resolution_method,accuracy_status,geom,review_status
) values (
    '44444444-4444-4444-8444-444444444444'::uuid,
    '33333333-3333-4333-8333-333333333333'::uuid,
    -100,-50,
    '22222222-2222-4222-8222-222222222222'::uuid,
    'fixture-geometry',
    'fixture',
    'specialist',
    st_geomfromtext('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))',4326),
    'reviewed'
);

insert into atlas.claim(
    claim_id,claim_kind_code,from_year,to_year,summary,confidence,
    review_status,publication_status,notes
) values (
    '55555555-5555-4555-8555-555555555555'::uuid,
    'territorial_practice',-90,-80,
    'D-054 exact-artifact integration fixture',
    'high','reviewed','unpublished','Disposable fixture'
);

insert into atlas.territorial_practice_claim(
    claim_id,spatial_entity_id,practice_type_code,practice_level,
    coverage_state_code,classification_status,notes
) values (
    '55555555-5555-4555-8555-555555555555'::uuid,
    '33333333-3333-4333-8333-333333333333'::uuid,
    'slavery_enslavement','P2','classified','fixture','Disposable fixture'
);

insert into atlas.claim_source(
    claim_source_id,claim_id,source_version_id,evidence_role,directness,direction,locator,notes
) values (
    '66666666-6666-4666-8666-666666666666'::uuid,
    '55555555-5555-4555-8555-555555555555'::uuid,
    '22222222-2222-4222-8222-222222222222'::uuid,
    'supports fixture','direct','supports','fixture:1','Disposable fixture'
);

insert into cartography.land_fabric(
    fabric_id,source_name,source_version,source_url,source_commit_sha,source_blob_sha,
    content_md5,content_sha256,active,geom
) values (
    'd054-fixture-land','D-054 fixture land','fixture-v1',
    'https://example.invalid/land','fixturecommit','fixtureblob',
    repeat('a',32),repeat('b',64),true,
    st_geomfromtext('MULTIPOLYGON(((-10 -10, 10 -10, 10 10, -10 10, -10 -10)))',4326)
);
