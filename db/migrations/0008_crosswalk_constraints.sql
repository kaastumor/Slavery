-- Migration 0008: strengthen migration crosswalk invariants discovered during importer implementation.
BEGIN;
ALTER TABLE audit.v061_owner_actor_map DROP CONSTRAINT missing_placeholder_has_no_actor;
ALTER TABLE audit.v061_owner_actor_map ADD CONSTRAINT owner_actor_map_action_consistency CHECK ((migration_action='missing_placeholder_no_actor' AND actor_id IS NULL) OR (migration_action<>'missing_placeholder_no_actor' AND actor_id IS NOT NULL));
COMMIT;
