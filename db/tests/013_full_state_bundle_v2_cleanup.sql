-- Cleanup disposable Gate-3 full-state bundle v2 fixture.
delete from audit.release_manifest where release_version='gate3-v2-predecessor';
delete from audit.research_target_claim where research_target_result_id='71000000-0000-4000-8000-00000000000e'::uuid;
delete from audit.research_target_source where research_target_result_id='71000000-0000-4000-8000-00000000000e'::uuid;
delete from audit.research_target_review where research_target_result_id='71000000-0000-4000-8000-00000000000e'::uuid;
delete from audit.research_target_result where research_target_result_id='71000000-0000-4000-8000-00000000000e'::uuid;
delete from audit.research_target where target_key='TEST:GATE3:RESULT';
delete from audit.research_coverage_source where coverage_assessment_id='71000000-0000-4000-8000-00000000000d'::uuid;
delete from audit.research_coverage_assessment where coverage_assessment_id='71000000-0000-4000-8000-00000000000d'::uuid;
delete from atlas.voyage_owner where voyage_owner_id='71000000-0000-4000-8000-00000000000c'::uuid;
delete from atlas.voyage where voyage_id='71000000-0000-4000-8000-00000000000b'::uuid;
delete from atlas.claim_source where claim_source_id in (
  '71000000-0000-4000-8000-000000000009'::uuid,
  '71000000-0000-4000-8000-00000000000a'::uuid
);
delete from atlas.territorial_practice_claim where claim_id='71000000-0000-4000-8000-000000000007'::uuid;
delete from atlas.claim where claim_id in (
  '71000000-0000-4000-8000-000000000007'::uuid,
  '71000000-0000-4000-8000-000000000008'::uuid
);
delete from atlas.actor_name where actor_name_id='71000000-0000-4000-8000-000000000006'::uuid;
delete from atlas.actor where actor_id='71000000-0000-4000-8000-000000000005'::uuid;
delete from atlas.geometry where geometry_id='71000000-0000-4000-8000-000000000004'::uuid;
delete from atlas.polity where spatial_entity_id='71000000-0000-4000-8000-000000000003'::uuid;
delete from atlas.spatial_entity where spatial_entity_id='71000000-0000-4000-8000-000000000003'::uuid;
delete from atlas.source_version where source_version_id='71000000-0000-4000-8000-000000000002'::uuid;
delete from atlas.source where source_id='71000000-0000-4000-8000-000000000001'::uuid;
delete from cartography.land_fabric where fabric_id='gate3-v2-land';
