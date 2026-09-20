-- Migration 0020: hold adaptive coastal completion pending standard GIS preprocessing.
-- Re-activate the fully populated v3 cache so the public map is internally consistent
-- while the source-family preprocessing pipeline is rebuilt around standard GIS tools.

BEGIN;

UPDATE cartography.geometry_render_policy
SET active = false
WHERE source_url_prefix = 'https://github.com/Seshat-Global-History-Databank/cliopatria';

UPDATE cartography.geometry_render_policy
SET active = true
WHERE policy_id = 'cliopatria-boundary-normalization-v3';

COMMIT;
