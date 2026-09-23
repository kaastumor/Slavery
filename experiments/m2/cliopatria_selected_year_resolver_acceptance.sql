-- M2 #121 synthetic rollback-only acceptance for the selected-year resolver.
BEGIN;

INSERT INTO atlas.source(
    source_id,title,author_or_institution,source_type,source_classification
) VALUES (
    '12100000-0000-0000-0000-000000000001',
    'M2 resolver synthetic source','Historical Slavery Atlas test fixture',
    'synthetic','methodology'
);

INSERT INTO atlas.source_version(
    source_version_id,source_id,version_label,url_or_identifier,license_status
) VALUES (
    '12100000-0000-0000-0000-000000000002',
    '12100000-0000-0000-0000-000000000001',
    'm2 synthetic resolver v1','fixture://m2-cliopatria-resolver','test fixture'
);

INSERT INTO atlas.source(
    source_id,title,author_or_institution,source_type,source_classification
) VALUES (
    '12100000-0000-0000-0000-000000000301',
    'M2 synthetic specialist geometry source',
    'Historical Slavery Atlas test fixture',
    'synthetic_specialist',
    'methodology'
);

INSERT INTO atlas.source_version(
    source_version_id,source_id,version_label,url_or_identifier,license_status
) VALUES (
    '12100000-0000-0000-0000-000000000302',
    '12100000-0000-0000-0000-000000000301',
    'm2 synthetic specialist v1',
    'fixture://m2-specialist-geometry',
    'test fixture'
);

INSERT INTO atlas.source_asset(
    source_asset_id,source_version_id,filename_or_object_key,media_type,
    checksum_sha256,storage_location
) VALUES (
    '12100000-0000-0000-0000-000000000003',
    '12100000-0000-0000-0000-000000000002',
    'synthetic.geojson','application/geo+json',
    repeat('1',64),'fixture'
);

INSERT INTO audit.ingest_run(
    ingest_run_id,source_version_id,source_asset_id,status,code_version,notes
) VALUES (
    '12100000-0000-0000-0000-000000000004',
    '12100000-0000-0000-0000-000000000002',
    '12100000-0000-0000-0000-000000000003',
    'completed','synthetic','M2 #121 resolver acceptance'
);

INSERT INTO staging.cliopatria_dataset(
    dataset_key,source_version_id,source_asset_id,ingest_run_id,
    upstream_repository,upstream_release,upstream_commit,upstream_path,
    git_blob_sha1,asset_sha256,feature_count,source_crs,status,loaded_at,notes
) VALUES (
    'm2-synthetic-cliopatria',
    '12100000-0000-0000-0000-000000000002',
    '12100000-0000-0000-0000-000000000003',
    '12100000-0000-0000-0000-000000000004',
    'synthetic','synthetic','synthetic','synthetic.geojson',
    repeat('a',40),repeat('1',64),13,'EPSG:4326','completed',now(),
    'Synthetic hierarchy fixture only'
);

INSERT INTO raw.raw_record(
    raw_record_id,ingest_run_id,record_type,source_native_id,raw_payload,checksum_sha256
)
SELECT
    ('12100000-0000-0000-0001-' || lpad(n::text,12,'0'))::uuid,
    '12100000-0000-0000-0000-000000000004',
    'cliopatria_feature',
    n::text,
    jsonb_build_object('fixture_ordinal',n),
    repeat('2',64)
FROM generate_series(1,13) n;

INSERT INTO staging.cliopatria_feature(
    dataset_key,source_row_ordinal,raw_record_id,source_feature_id,
    name_raw,type_raw,from_year_raw,to_year_raw,member_of_raw,components_raw,
    seshat_id_raw,wikidata_raw,wikipedia_raw,geom
) VALUES
('m2-synthetic-cliopatria',1,'12100000-0000-0000-0001-000000000001','1',
 'RootPolity','POLITY',1,200,'','ChildPolity;NestedComposite','','','','SRID=4326;POLYGON((0 0,4 0,4 4,0 4,0 0))'),
('m2-synthetic-cliopatria',2,'12100000-0000-0000-0001-000000000002','2',
 'ChildPolity','POLITY',1,200,'RootPolity','','','','','SRID=4326;POLYGON((0 0,1 0,1 1,0 1,0 0))'),
('m2-synthetic-cliopatria',3,'12100000-0000-0000-0001-000000000003','3',
 'NestedComposite','POLITY',1,200,'RootPolity','NestedChild','','','','SRID=4326;POLYGON((1 0,2 0,2 1,1 1,1 0))'),
('m2-synthetic-cliopatria',4,'12100000-0000-0000-0001-000000000004','4',
 'NestedChild','POLITY',1,200,'NestedComposite','','','','','SRID=4326;POLYGON((1 0,1.5 0,1.5 .5,1 .5,1 0))'),
('m2-synthetic-cliopatria',5,'12100000-0000-0000-0001-000000000005','5',
 'RelationMember','POLITY',1,200,'(Alliance)','','','','','SRID=4326;POLYGON((5 0,6 0,6 1,5 1,5 0))'),
('m2-synthetic-cliopatria',6,'12100000-0000-0000-0001-000000000006','6',
 '(Alliance)','RELATION',1,200,'','RelationMember;ParentA','','','','SRID=4326;POLYGON((5 0,8 0,8 2,5 2,5 0))'),
('m2-synthetic-cliopatria',7,'12100000-0000-0000-0001-000000000007','7',
 'AmbiguousChild','POLITY',1,200,'ParentA;ParentB','','','','','SRID=4326;POLYGON((7 0,7.5 0,7.5 .5,7 .5,7 0))'),
('m2-synthetic-cliopatria',8,'12100000-0000-0000-0001-000000000008','8',
 'ParentA','POLITY',1,200,'','','','','','SRID=4326;POLYGON((7 0,8 0,8 1,7 1,7 0))'),
('m2-synthetic-cliopatria',9,'12100000-0000-0000-0001-000000000009','9',
 'ParentB','POLITY',1,200,'','','','','','SRID=4326;POLYGON((8 0,9 0,9 1,8 1,8 0))'),
('m2-synthetic-cliopatria',10,'12100000-0000-0000-0001-000000000010','10',
 'MissingParentChild','POLITY',1,200,'DoesNotExist','','','','','SRID=4326;POLYGON((9 0,10 0,10 1,9 1,9 0))'),
('m2-synthetic-cliopatria',11,'12100000-0000-0000-0001-000000000011','11',
 'BoundaryPolity','POLITY',-2,0,'','','','','','SRID=4326;POLYGON((0 5,1 5,1 6,0 6,0 5))'),
('m2-synthetic-cliopatria',12,'12100000-0000-0000-0001-000000000012','12',
 'BoundaryPolity','POLITY',1,2,'','','','','','SRID=4326;POLYGON((0 5,2 5,2 6,0 6,0 5))'),
('m2-synthetic-cliopatria',13,'12100000-0000-0000-0001-000000000013','13',
 'QuarantinedPolity','POLITY',1,200,'','','','','','SRID=4326;POLYGON((11 0,12 0,12 1,11 1,11 0))');

INSERT INTO atlas.spatial_entity(
    spatial_entity_id,entity_type_code,canonical_name,review_status
) VALUES
('12100000-0000-0000-0000-000000000101','polity','RootPolity atlas target','reviewed'),
('12100000-0000-0000-0000-000000000102','polity','Quarantined atlas target','reviewed');

INSERT INTO atlas.geometry(
    geometry_id,spatial_entity_id,from_year,to_year,geometry_source_version_id,
    geometry_source_native_id,resolution_method,accuracy_status,geom,review_status
) VALUES
('12100000-0000-0000-0000-000000000201',
 '12100000-0000-0000-0000-000000000101',50,150,
 '12100000-0000-0000-0000-000000000302',
 'specialist-accepted-201',
 'Synthetic explicitly accepted specialist replacement','specialist',
 'SRID=4326;POLYGON((0 0,10 0,10 10,0 10,0 0))','reviewed'),
('12100000-0000-0000-0000-000000000202',
 '12100000-0000-0000-0000-000000000102',50,150,
 '12100000-0000-0000-0000-000000000302',
 'specialist-quarantined-202',
 'Synthetic quarantined specialist candidate','specialist',
 'SRID=4326;POLYGON((11 0,15 0,15 4,11 4,11 0))','reviewed');

INSERT INTO staging.m2_cliopatria_entity_match(
    dataset_key,source_row_ordinal,spatial_entity_id,match_status,notes
) VALUES
('m2-synthetic-cliopatria',1,'12100000-0000-0000-0000-000000000101','reviewed_match','synthetic explicit match'),
('m2-synthetic-cliopatria',13,'12100000-0000-0000-0000-000000000102','reviewed_match','synthetic explicit match');

INSERT INTO staging.m2_geometry_precedence(
    geometry_id,spatial_entity_id,decision_status,from_year,to_year,decision_note
) VALUES
('12100000-0000-0000-0000-000000000201',
 '12100000-0000-0000-0000-000000000101',
 'accepted_specialist_override',50,150,
 'Synthetic D-055 accepted case-specific specialist override'),
('12100000-0000-0000-0000-000000000202',
 '12100000-0000-0000-0000-000000000102',
 'quarantined',50,150,
 'Synthetic quarantine: existence of specialist candidate must not create precedence');

DO $$
DECLARE
    n bigint;
    v_status text;
    v_suppressed integer;
    v_choice text;
    v_geom uuid;
    v_baseline_source_version uuid;
    v_chosen_source_version uuid;
    v_chosen_source_native_id text;
BEGIN
    IF staging.m2_cliopatria_source_year(-13) <> -14
       OR staging.m2_cliopatria_source_year(0) <> -1
       OR staging.m2_cliopatria_source_year(1) <> 1 THEN
        RAISE EXCEPTION 'D-059 atlas/source-year translation failed';
    END IF;

    SELECT count(*) INTO n
    FROM staging.m2_cliopatria_polity_baseline(100)
    WHERE dataset_key='m2-synthetic-cliopatria';
    IF n <> 7 THEN
        RAISE EXCEPTION 'synthetic baseline count %, expected 7', n;
    END IF;

    SELECT hierarchy_status,suppressed_component_count
      INTO v_status,v_suppressed
    FROM staging.m2_cliopatria_polity_baseline(100)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='RootPolity';
    IF v_status <> 'resolved_polity_composite' OR v_suppressed <> 3 THEN
        RAISE EXCEPTION 'POLITY nested/component suppression failed: %, %',v_status,v_suppressed;
    END IF;

    IF EXISTS (
        SELECT 1 FROM staging.m2_cliopatria_polity_baseline(100)
        WHERE dataset_key='m2-synthetic-cliopatria'
          AND name_raw IN ('ChildPolity','NestedComposite','NestedChild')
    ) THEN
        RAISE EXCEPTION 'suppressed POLITY components leaked into baseline';
    END IF;

    SELECT hierarchy_status INTO v_status
    FROM staging.m2_cliopatria_polity_baseline(100)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='RelationMember';
    IF v_status <> 'relation_membership_retained' THEN
        RAISE EXCEPTION 'RELATION membership incorrectly suppressed polity: %',v_status;
    END IF;

    IF EXISTS (
        SELECT 1 FROM staging.m2_cliopatria_polity_baseline(100)
        WHERE dataset_key='m2-synthetic-cliopatria'
          AND name_raw='(Alliance)'
    ) THEN
        RAISE EXCEPTION 'RELATION row leaked into default polity baseline';
    END IF;

    SELECT count(*) INTO n FROM staging.m2_cliopatria_relation_layer(100)
    WHERE dataset_key='m2-synthetic-cliopatria';
    IF n <> 1 THEN
        RAISE EXCEPTION 'optional relation layer count %, expected 1',n;
    END IF;

    SELECT hierarchy_status INTO v_status
    FROM staging.m2_cliopatria_polity_baseline(100)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='AmbiguousChild';
    IF v_status <> 'unresolved_hierarchy' THEN
        RAISE EXCEPTION 'multiple POLITY parents were guessed instead of unresolved';
    END IF;

    SELECT hierarchy_status INTO v_status
    FROM staging.m2_cliopatria_polity_baseline(100)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='MissingParentChild';
    IF v_status <> 'unresolved_hierarchy' THEN
        RAISE EXCEPTION 'missing parent reference was guessed instead of unresolved';
    END IF;

    SELECT count(*) INTO n
    FROM staging.m2_cliopatria_polity_baseline(0)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='BoundaryPolity'
      AND source_row_ordinal=11
      AND cliopatria_source_year=-1;
    IF n <> 1 THEN
        RAISE EXCEPTION 'atlas year 0 did not resolve through source year -1';
    END IF;

    SELECT count(*) INTO n
    FROM staging.m2_cliopatria_polity_baseline(1)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='BoundaryPolity'
      AND source_row_ordinal=12
      AND cliopatria_source_year=1;
    IF n <> 1 THEN
        RAISE EXCEPTION 'atlas year 1 did not resolve source year 1';
    END IF;

    IF EXISTS (
        SELECT 1 FROM staging.m2_cliopatria_polity_baseline(0)
        WHERE dataset_key='m2-synthetic-cliopatria'
          AND cliopatria_source_year=0
    ) THEN
        RAISE EXCEPTION 'source-native year zero was queried as an atlas year';
    END IF;

    SELECT
        geometry_choice_status,
        chosen_geometry_id,
        baseline_source_version_id,
        chosen_geometry_source_version_id,
        chosen_geometry_source_native_id
      INTO
        v_choice,
        v_geom,
        v_baseline_source_version,
        v_chosen_source_version,
        v_chosen_source_native_id
    FROM staging.m2_cliopatria_geometry_candidates(100)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='RootPolity';
    IF v_choice <> 'accepted_specialist_override'
       OR v_geom <> '12100000-0000-0000-0000-000000000201'::uuid THEN
        RAISE EXCEPTION 'accepted specialist override did not outrank raw baseline';
    END IF;
    IF v_baseline_source_version <> '12100000-0000-0000-0000-000000000002'::uuid
       OR v_chosen_source_version <> '12100000-0000-0000-0000-000000000302'::uuid
       OR v_chosen_source_native_id <> 'specialist-accepted-201' THEN
        RAISE EXCEPTION
            'chosen specialist provenance was not separated from baseline provenance';
    END IF;

    SELECT
        geometry_choice_status,
        chosen_geometry_id,
        baseline_source_version_id,
        chosen_geometry_source_version_id,
        chosen_geometry_source_native_id
      INTO
        v_choice,
        v_geom,
        v_baseline_source_version,
        v_chosen_source_version,
        v_chosen_source_native_id
    FROM staging.m2_cliopatria_geometry_candidates(100)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='QuarantinedPolity';
    IF v_choice <> 'raw_cliopatria_baseline' OR v_geom IS NOT NULL THEN
        RAISE EXCEPTION 'quarantined specialist candidate incorrectly gained precedence';
    END IF;
    IF v_baseline_source_version <> '12100000-0000-0000-0000-000000000002'::uuid
       OR v_chosen_source_version IS NOT NULL
       OR v_chosen_source_native_id IS NOT NULL THEN
        RAISE EXCEPTION 'quarantined candidate leaked chosen specialist provenance';
    END IF;

    SELECT geometry_choice_status,chosen_geometry_id
      INTO v_choice,v_geom
    FROM staging.m2_cliopatria_geometry_candidates(160)
    WHERE dataset_key='m2-synthetic-cliopatria'
      AND name_raw='RootPolity';
    IF v_choice <> 'raw_cliopatria_baseline' OR v_geom IS NOT NULL THEN
        RAISE EXCEPTION 'specialist override leaked outside accepted interval';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM information_schema.views
        WHERE table_schema='publish'
          AND view_definition ~* '(m2_cliopatria|cliopatria_feature)'
    ) THEN
        RAISE EXCEPTION 'resolver prototype leaked into publish views';
    END IF;
END $$;

-- Invalid: an unreviewed geometry cannot become an accepted specialist override.
INSERT INTO atlas.geometry(
    geometry_id,spatial_entity_id,from_year,to_year,geometry_source_version_id,
    resolution_method,accuracy_status,geom,review_status
) VALUES (
    '12100000-0000-0000-0000-000000000203',
    '12100000-0000-0000-0000-000000000101',50,150,
    '12100000-0000-0000-0000-000000000002',
    'unreviewed synthetic specialist','specialist',
    'SRID=4326;POLYGON((0 0,3 0,3 3,0 3,0 0))','draft'
);

DO $$
DECLARE blocked boolean := false;
BEGIN
    BEGIN
        INSERT INTO staging.m2_geometry_precedence(
            geometry_id,spatial_entity_id,decision_status,from_year,to_year,decision_note
        ) VALUES (
            '12100000-0000-0000-0000-000000000203',
            '12100000-0000-0000-0000-000000000101',
            'accepted_specialist_override',50,150,
            'must fail because geometry is not reviewed'
        );
    EXCEPTION WHEN others THEN
        IF SQLERRM LIKE 'accepted specialist override requires reviewed non-empty exact/specialist geometry%' THEN
            blocked := true;
        ELSE
            RAISE;
        END IF;
    END;
    IF NOT blocked THEN
        RAISE EXCEPTION 'unreviewed specialist geometry was accepted';
    END IF;
END $$;

SELECT
    name_raw,
    hierarchy_status,
    suppressed_component_count,
    geometry_choice_status,
    publication_state
FROM staging.m2_cliopatria_geometry_candidates(100)
WHERE dataset_key='m2-synthetic-cliopatria'
ORDER BY name_raw;

ROLLBACK;
