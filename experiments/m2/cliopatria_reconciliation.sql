-- M2 #119 full-corpus reconciliation for the exact pinned Cliopatria v0.2.0 asset.
-- Fail closed if ingestion, raw preservation or publication isolation drift.

DO $$
DECLARE
    v_dataset_key constant text :=
        'cliopatria:v0.2.0-duplicate:ad28a691b7c07c1fca89d0e0636d324667d2a258';
    v_ingest_run uuid;
    v_count bigint;
BEGIN
    SELECT ingest_run_id INTO v_ingest_run
    FROM staging.cliopatria_dataset
    WHERE dataset_key = v_dataset_key
      AND status = 'completed'
      AND upstream_repository = 'Seshat-Global-History-Databank/cliopatria'
      AND upstream_release = 'v0.2.0-duplicate'
      AND upstream_commit = 'ad28a691b7c07c1fca89d0e0636d324667d2a258'
      AND upstream_path = 'cliopatria.geojson.zip'
      AND git_blob_sha1 = 'cefab0f4b622e2e7fb3daf68d4f461f83991204c'
      AND asset_sha256 = 'd01ae3a20d358cc5d54f69d9d725d390767d9c8759ac89ad6f90c58d106f3370'
      AND feature_count = 13765
      AND source_crs = 'EPSG:4326';

    IF v_ingest_run IS NULL THEN
        RAISE EXCEPTION 'pinned Cliopatria dataset metadata is missing or mismatched';
    END IF;

    SELECT count(*) INTO v_count
    FROM raw.raw_record
    WHERE ingest_run_id = v_ingest_run
      AND record_type = 'cliopatria_feature';
    IF v_count <> 13765 THEN
        RAISE EXCEPTION 'raw Cliopatria row count %, expected 13765', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key;
    IF v_count <> 13765 THEN
        RAISE EXCEPTION 'staging Cliopatria row count %, expected 13765', v_count;
    END IF;

    SELECT count(DISTINCT name_raw) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key;
    IF v_count <> 1633 THEN
        RAISE EXCEPTION 'distinct Cliopatria names %, expected 1633', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key AND type_raw = 'POLITY';
    IF v_count <> 13380 THEN
        RAISE EXCEPTION 'POLITY rows %, expected 13380', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key AND type_raw = 'RELATION';
    IF v_count <> 385 THEN
        RAISE EXCEPTION 'RELATION rows %, expected 385', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND type_raw NOT IN ('POLITY','RELATION');
    IF v_count <> 0 THEN
        RAISE EXCEPTION 'unexpected source-native Type rows %', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND ST_GeometryType(geom) = 'ST_Polygon';
    IF v_count <> 6531 THEN
        RAISE EXCEPTION 'Polygon rows %, expected 6531', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND ST_GeometryType(geom) = 'ST_MultiPolygon';
    IF v_count <> 7234 THEN
        RAISE EXCEPTION 'MultiPolygon rows %, expected 7234', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key AND geom IS NULL;
    IF v_count <> 0 THEN
        RAISE EXCEPTION 'null geometries %, expected 0', v_count;
    END IF;

    IF (SELECT min(from_year_raw) FROM staging.cliopatria_feature WHERE dataset_key=v_dataset_key) <> -3400
       OR (SELECT max(to_year_raw) FROM staging.cliopatria_feature WHERE dataset_key=v_dataset_key) <> 2024 THEN
        RAISE EXCEPTION 'source-native year extent drifted';
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND (from_year_raw < 0 OR to_year_raw < 0);
    IF v_count <> 1106 THEN
        RAISE EXCEPTION 'rows with negative source year %, expected 1106', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND from_year_raw < 0 AND to_year_raw > 0;
    IF v_count <> 39 THEN
        RAISE EXCEPTION 'rows crossing numeric zero %, expected 39', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND (from_year_raw = 0 OR to_year_raw = 0);
    IF v_count <> 6 THEN
        RAISE EXCEPTION 'rows with zero endpoint %, expected 6', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND from_year_raw > to_year_raw;
    IF v_count <> 0 THEN
        RAISE EXCEPTION 'invalid source ranges %, expected 0', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key AND nullif(member_of_raw,'') IS NOT NULL;
    IF v_count <> 2656 THEN
        RAISE EXCEPTION 'MemberOf-present rows %, expected 2656', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key AND nullif(components_raw,'') IS NOT NULL;
    IF v_count <> 1722 THEN
        RAISE EXCEPTION 'Components-present rows %, expected 1722', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND nullif(member_of_raw,'') IS NOT NULL
      AND nullif(components_raw,'') IS NOT NULL;
    IF v_count <> 80 THEN
        RAISE EXCEPTION 'nested composite rows %, expected 80', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature
    WHERE dataset_key = v_dataset_key
      AND nullif(member_of_raw,'') IS NOT NULL
      AND member_of_raw LIKE '%;%';
    IF v_count <> 86 THEN
        RAISE EXCEPTION 'multiple-MemberOf rows %, expected 86', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM staging.cliopatria_feature f
    JOIN raw.raw_record r ON r.raw_record_id = f.raw_record_id
    WHERE f.dataset_key = v_dataset_key
      AND (
        r.raw_payload->'properties'->>'Name' IS DISTINCT FROM f.name_raw
        OR r.raw_payload->'properties'->>'Type' IS DISTINCT FROM f.type_raw
        OR r.raw_payload->'properties'->>'MemberOf' IS DISTINCT FROM f.member_of_raw
        OR r.raw_payload->'properties'->>'Components' IS DISTINCT FROM f.components_raw
        OR NULLIF(r.raw_payload->'properties'->>'FromYear','')::integer IS DISTINCT FROM f.from_year_raw
        OR NULLIF(r.raw_payload->'properties'->>'ToYear','')::integer IS DISTINCT FROM f.to_year_raw
      );
    IF v_count <> 0 THEN
        RAISE EXCEPTION 'raw/staging source-value mismatches %', v_count;
    END IF;

    SELECT count(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema='staging'
      AND table_name='cliopatria_feature'
      AND column_name IN ('spatial_entity_id','polity_id','geometry_id');
    IF v_count <> 0 THEN
        RAISE EXCEPTION 'raw Cliopatria staging incorrectly contains atlas identity columns';
    END IF;

    SELECT count(*) INTO v_count
    FROM information_schema.views
    WHERE table_schema='publish'
      AND (table_name ILIKE '%cliopatria%' OR view_definition ILIKE '%cliopatria%');
    IF v_count <> 0 THEN
        RAISE EXCEPTION 'Cliopatria raw/staging rows leaked into publish views';
    END IF;
END $$;

SELECT
    d.dataset_key,
    d.feature_count,
    count(*) FILTER (WHERE f.type_raw='POLITY') AS polity_rows,
    count(*) FILTER (WHERE f.type_raw='RELATION') AS relation_rows,
    count(DISTINCT f.name_raw) AS distinct_names,
    min(f.from_year_raw) AS source_min_year,
    max(f.to_year_raw) AS source_max_year
FROM staging.cliopatria_dataset d
JOIN staging.cliopatria_feature f USING (dataset_key)
WHERE d.dataset_key='cliopatria:v0.2.0-duplicate:ad28a691b7c07c1fca89d0e0636d324667d2a258'
GROUP BY d.dataset_key,d.feature_count;
