-- Migration 0027: make registered release artifacts immutable after publication.
-- Completes D-054's immutable bundle provenance guard.

BEGIN;

CREATE TRIGGER release_artifact_immutable
BEFORE INSERT OR UPDATE OR DELETE ON audit.release_artifact
FOR EACH ROW EXECUTE FUNCTION audit.guard_published_release_membership();

COMMIT;
