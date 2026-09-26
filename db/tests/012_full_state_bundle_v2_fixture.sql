-- Disposable Gate-3 full-state bundle v2 fixture.

insert into atlas.source(
  source_id,title,author_or_institution,source_type,source_classification,notes
) values (
  '71000000-0000-4000-8000-000000000001'::uuid,
  'Gate3 v2 fixture source','CI','fixture','secondary_specialist','Disposable fixture'
);

insert into atlas.source_version(
  source_version_id,source_id,version_label,url_or_identifier,license_status,redistribution_status
) values (
  '71000000-0000-4000-8000-000000000002'::uuid,
  '71000000-0000-4000-8000-000000000001'::uuid,
  'fixture-v1','https://example.invalid/gate3-v2','test-only','test-only'
);

insert into atlas.spatial_entity(
  spatial_entity_id,entity_type_code,canonical_name,display_name,from_year,to_year,review_status
) values (
  '71000000-0000-4000-8000-000000000003'::uuid,
  'polity','Gate3 Fixture Polity','Gate3 Fixture Polity',1200,1400,'reviewed'
);

insert into atlas.polity(spatial_entity_id,polity_type,notes) values (
  '71000000-0000-4000-8000-000000000003'::uuid,
  'fixture','Disposable fixture'
);

insert into atlas.geometry(
  geometry_id,spatial_entity_id,from_year,to_year,geometry_source_version_id,
  geometry_source_native_id,resolution_method,accuracy_status,geom,review_status
) values (
  '71000000-0000-4000-8000-000000000004'::uuid,
  '71000000-0000-4000-8000-000000000003'::uuid,
  1200,1400,
  '71000000-0000-4000-8000-000000000002'::uuid,
  'gate3-v2-geometry','fixture','specialist',
  st_geomfromtext('POLYGON((1 1, 2 1, 2 2, 1 2, 1 1))',4326),
  'reviewed'
);

insert into atlas.actor(
  actor_id,actor_type_code,canonical_name,display_name,review_status
) values (
  '71000000-0000-4000-8000-000000000005'::uuid,
  'person','Gate3 Fixture Actor','Gate3 Fixture Actor','reviewed'
);

insert into atlas.actor_name(
  actor_name_id,actor_id,name_text,name_type,source_version_id,is_preferred
) values (
  '71000000-0000-4000-8000-000000000006'::uuid,
  '71000000-0000-4000-8000-000000000005'::uuid,
  'Gate3 Fixture Actor','canonical',
  '71000000-0000-4000-8000-000000000002'::uuid,true
);

insert into atlas.claim(
  claim_id,claim_kind_code,from_year,to_year,summary,confidence,
  review_status,publication_status,notes
) values
(
  '71000000-0000-4000-8000-000000000007'::uuid,
  'territorial_practice',1300,1300,
  'Gate3 territorial fixture','high','reviewed','unpublished','Disposable fixture'
),
(
  '71000000-0000-4000-8000-000000000008'::uuid,
  'voyage_owner',1300,1300,
  'Gate3 ownership fixture','high','reviewed','unpublished','Disposable fixture'
);

insert into atlas.territorial_practice_claim(
  claim_id,spatial_entity_id,practice_type_code,practice_level,
  coverage_state_code,classification_status,notes
) values (
  '71000000-0000-4000-8000-000000000007'::uuid,
  '71000000-0000-4000-8000-000000000003'::uuid,
  'slavery_enslavement',NULL,'classified','fixture','P-level deliberately NULL'
);

insert into atlas.claim_source(
  claim_source_id,claim_id,source_version_id,evidence_role,
  independence_group,claim_fitness,directness,direction,locator,notes
) values
(
  '71000000-0000-4000-8000-000000000009'::uuid,
  '71000000-0000-4000-8000-000000000007'::uuid,
  '71000000-0000-4000-8000-000000000002'::uuid,
  'fixture support','gate3-fixture','direct','direct','supports','fixture:claim','Disposable'
),
(
  '71000000-0000-4000-8000-00000000000a'::uuid,
  '71000000-0000-4000-8000-000000000008'::uuid,
  '71000000-0000-4000-8000-000000000002'::uuid,
  'fixture ownership','gate3-fixture','direct','direct','supports','fixture:owner','Disposable'
);

insert into atlas.voyage(
  voyage_id,source_dataset,source_native_voyage_id,primary_source_version_id,
  vessel_name,year_arrived,year_status,review_status
) values (
  '71000000-0000-4000-8000-00000000000b'::uuid,
  'gate3_fixture','G3-1',
  '71000000-0000-4000-8000-000000000002'::uuid,
  'Gate3 Fixture Vessel',1300,'documented','reviewed'
);

insert into atlas.voyage_owner(
  voyage_owner_id,voyage_id,actor_id,claim_id,raw_owner_text,
  relationship_role,owner_sequence,relationship_status,notes
) values (
  '71000000-0000-4000-8000-00000000000c'::uuid,
  '71000000-0000-4000-8000-00000000000b'::uuid,
  '71000000-0000-4000-8000-000000000005'::uuid,
  '71000000-0000-4000-8000-000000000008'::uuid,
  'Gate3 Fixture Actor','owner',1,'documented','Disposable fixture'
);

insert into audit.research_coverage_assessment(
  coverage_assessment_id,spatial_entity_id,region_label_raw,period_label_raw,
  from_year,to_year,normalized_coverage_state_code,researchability,
  release_version,review_status,publication_status,notes
) values (
  '71000000-0000-4000-8000-00000000000d'::uuid,
  '71000000-0000-4000-8000-000000000003'::uuid,
  'Gate3 Fixture Region','1300 CE',1300,1300,
  'classified','fixture','v0.6.1','reviewed','unpublished','Disposable fixture'
);

insert into audit.research_coverage_source(
  coverage_assessment_id,source_version_id,source_role,locator,notes
) values (
  '71000000-0000-4000-8000-00000000000d'::uuid,
  '71000000-0000-4000-8000-000000000002'::uuid,
  'fixture_source','fixture:coverage','Disposable fixture'
);

insert into audit.research_target(
  target_key,target_label,anchor_label,anchor_year,frame_class,
  spatial_entity_id,origin,review_status
) values (
  'TEST:GATE3:RESULT','Gate3 Fixture Target','1300 CE',1300,'node_site',
  '71000000-0000-4000-8000-000000000003'::uuid,
  'gate3_fixture','reviewed'
);

insert into audit.research_target_result(
  research_target_result_id,target_key,research_stage,research_outcome,
  bounded_proposition,required_abstention,content_sha256,review_status
) values (
  '71000000-0000-4000-8000-00000000000e'::uuid,
  'TEST:GATE3:RESULT','researched_internal','BOUNDED_SUPPORTED',
  'Gate3 fixture proposition','Do not infer beyond fixture',
  repeat('d',64),'reviewed'
);

insert into audit.research_target_review(
  research_target_review_id,research_target_result_id,candidate_id,review_level,
  review_disposition,admitted,review_reason,failure_guards,notes
) values (
  '71000000-0000-4000-8000-00000000000f'::uuid,
  '71000000-0000-4000-8000-00000000000e'::uuid,
  'gate3-v2-reviewed','internal','ACCEPT_INTERNAL_REVIEW',true,
  'Disposable fixture',ARRAY['fixture_guard'],'Test-only'
);

insert into audit.research_target_source(
  research_target_source_id,research_target_result_id,source_version_id,
  source_relation_key,source_version_ref_raw,evidence_role,independence_group,
  claim_fitness,direction_raw,normalized_direction,locator,source_id_raw,decisive,
  access_limitation,accessed_at_text,dependency_note
) values (
  '71000000-0000-4000-8000-000000000010'::uuid,
  '71000000-0000-4000-8000-00000000000e'::uuid,
  '71000000-0000-4000-8000-000000000002'::uuid,
  'fixture-rel','fixture-v1','fixture evidence','gate3-fixture',
  'direct','supports','supports','fixture:target','fixture-source',true,
  'none','2026-09-26','Disposable fixture'
);

insert into audit.research_target_claim(
  research_target_result_id,claim_id,claim_role,notes
) values (
  '71000000-0000-4000-8000-00000000000e'::uuid,
  '71000000-0000-4000-8000-000000000007'::uuid,
  'supports_bounded_result','Disposable fixture'
);

insert into audit.release_manifest(
  release_version,schema_version,status,changelog,qc_summary,unresolved_issues,manifest
) values (
  'gate3-v2-predecessor','0033','draft','fixture','fixture','none',
  jsonb_build_object(
    'claim_ids',jsonb_build_array(
      '71000000-0000-4000-8000-000000000007',
      '71000000-0000-4000-8000-000000000008'
    ),
    'actor_ids',jsonb_build_array('71000000-0000-4000-8000-000000000005'),
    'voyage_ids',jsonb_build_array('71000000-0000-4000-8000-00000000000b'),
    'coverage_assessment_ids',jsonb_build_array('71000000-0000-4000-8000-00000000000d'),
    'source_version_ids',jsonb_build_array('71000000-0000-4000-8000-000000000002')
  )
);

insert into cartography.land_fabric(
  fabric_id,source_name,source_version,source_url,source_commit_sha,source_blob_sha,
  content_md5,content_sha256,active,geom
) values (
  'gate3-v2-land','Gate3 fixture land','fixture-v1',
  'https://example.invalid/gate3-land','fixturecommit','fixtureblob',
  repeat('a',32),repeat('b',64),true,
  st_geomfromtext('MULTIPOLYGON(((0 0, 5 0, 5 5, 0 5, 0 0)))',4326)
);
