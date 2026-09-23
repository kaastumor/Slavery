-- M2 #121 disposable prototype: selected-year resolver over the complete raw Cliopatria staging corpus.
-- Intentionally NOT a production migration or publish view.

CREATE OR REPLACE FUNCTION staging.m2_cliopatria_source_year(p_atlas_year integer)
RETURNS integer
LANGUAGE sql
IMMUTABLE
PARALLEL SAFE
SET search_path = ''
AS $$
    SELECT CASE WHEN p_atlas_year <= 0 THEN p_atlas_year - 1 ELSE p_atlas_year END;
$$;

COMMENT ON FUNCTION staging.m2_cliopatria_source_year(integer) IS
'D-059 calendar translation: atlas astronomical year <=0 maps to Cliopatria source year atlas_year-1; positive CE years are unchanged. Source integer zero is never queried.';

CREATE TABLE IF NOT EXISTS staging.m2_cliopatria_entity_match (
    dataset_key text NOT NULL,
    source_row_ordinal integer NOT NULL,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    match_status text NOT NULL CHECK (match_status IN ('reviewed_match','unresolved')),
    notes text,
    PRIMARY KEY (dataset_key, source_row_ordinal),
    FOREIGN KEY (dataset_key, source_row_ordinal)
        REFERENCES staging.cliopatria_feature(dataset_key, source_row_ordinal)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS staging.m2_geometry_precedence (
    geometry_id uuid PRIMARY KEY REFERENCES atlas.geometry(geometry_id) ON DELETE RESTRICT,
    spatial_entity_id uuid NOT NULL REFERENCES atlas.spatial_entity(spatial_entity_id) ON DELETE RESTRICT,
    decision_status text NOT NULL CHECK (
        decision_status IN ('accepted_specialist_override','quarantined','rejected')
    ),
    from_year integer NOT NULL,
    to_year integer NOT NULL,
    valid_years int4range GENERATED ALWAYS AS (atlas.make_year_range(from_year,to_year)) STORED,
    decision_note text NOT NULL CHECK (nullif(btrim(decision_note),'') IS NOT NULL),
    CONSTRAINT m2_geometry_precedence_year_order CHECK (from_year <= to_year)
);

CREATE OR REPLACE FUNCTION staging.m2_validate_geometry_precedence()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = ''
AS $$
DECLARE
    v_entity uuid;
    v_review atlas.review_status;
    v_accuracy atlas.geometry_accuracy;
    v_geom_present boolean;
    v_from integer;
    v_to integer;
BEGIN
    SELECT spatial_entity_id, review_status, accuracy_status, geom IS NOT NULL, from_year, to_year
      INTO v_entity, v_review, v_accuracy, v_geom_present, v_from, v_to
    FROM atlas.geometry
    WHERE geometry_id = NEW.geometry_id;

    IF v_entity IS DISTINCT FROM NEW.spatial_entity_id THEN
        RAISE EXCEPTION 'geometry precedence spatial entity must match geometry spatial entity';
    END IF;

    IF NEW.decision_status = 'accepted_specialist_override' THEN
        IF v_review <> 'reviewed'
           OR NOT v_geom_present
           OR v_accuracy NOT IN ('exact','specialist') THEN
            RAISE EXCEPTION
                'accepted specialist override requires reviewed non-empty exact/specialist geometry';
        END IF;
        IF v_from IS NOT NULL AND NEW.from_year < v_from THEN
            RAISE EXCEPTION 'override interval starts before geometry interval';
        END IF;
        IF v_to IS NOT NULL AND NEW.to_year > v_to THEN
            RAISE EXCEPTION 'override interval ends after geometry interval';
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS m2_geometry_precedence_validate
    ON staging.m2_geometry_precedence;
CREATE TRIGGER m2_geometry_precedence_validate
BEFORE INSERT OR UPDATE ON staging.m2_geometry_precedence
FOR EACH ROW EXECUTE FUNCTION staging.m2_validate_geometry_precedence();

CREATE OR REPLACE FUNCTION staging.m2_cliopatria_resolve_polity_row(
    p_dataset_key text,
    p_source_row_ordinal integer,
    p_source_year integer
)
RETURNS TABLE (
    resolved_source_row_ordinal integer,
    hierarchy_status text,
    hierarchy_depth integer,
    hierarchy_path integer[]
)
LANGUAGE plpgsql
STABLE
SET search_path = ''
AS $$
DECLARE
    v_original integer := p_source_row_ordinal;
    v_current integer := p_source_row_ordinal;
    v_member_of text;
    v_type text;
    v_path integer[] := ARRAY[]::integer[];
    v_depth integer := 0;
    v_parent_name text;
    v_match_count integer;
    v_parent_ordinal integer;
    v_parent_type text;
    v_polity_parents integer[];
    v_unresolved boolean;
    v_relation_seen boolean;
BEGIN
    LOOP
        IF v_current = ANY(v_path) THEN
            RETURN QUERY SELECT v_original, 'unresolved_cycle'::text, v_depth, v_path;
            RETURN;
        END IF;
        v_path := array_append(v_path, v_current);

        SELECT f.member_of_raw, f.type_raw
          INTO v_member_of, v_type
        FROM staging.cliopatria_feature f
        WHERE f.dataset_key = p_dataset_key
          AND f.source_row_ordinal = v_current
          AND f.source_years @> p_source_year;

        IF NOT FOUND OR v_type IS DISTINCT FROM 'POLITY' THEN
            RETURN QUERY
            SELECT v_original, 'unresolved_inactive_or_nonpolity'::text, v_depth, v_path;
            RETURN;
        END IF;

        IF nullif(btrim(v_member_of),'') IS NULL THEN
            RETURN QUERY
            SELECT v_current,
                   CASE WHEN v_depth = 0
                        THEN 'resolved_top_polity'
                        ELSE 'resolved_nested_polity'
                   END,
                   v_depth,
                   v_path;
            RETURN;
        END IF;

        v_polity_parents := ARRAY[]::integer[];
        v_unresolved := false;
        v_relation_seen := false;

        FOR v_parent_name IN
            SELECT DISTINCT btrim(x)
            FROM regexp_split_to_table(v_member_of, ';') AS x
            WHERE nullif(btrim(x),'') IS NOT NULL
        LOOP
            SELECT count(*), min(f.source_row_ordinal)
              INTO v_match_count, v_parent_ordinal
            FROM staging.cliopatria_feature f
            WHERE f.dataset_key = p_dataset_key
              AND f.name_raw = v_parent_name
              AND f.source_years @> p_source_year;

            IF v_match_count <> 1 THEN
                v_unresolved := true;
                CONTINUE;
            END IF;

            SELECT f.type_raw
              INTO v_parent_type
            FROM staging.cliopatria_feature f
            WHERE f.dataset_key = p_dataset_key
              AND f.source_row_ordinal = v_parent_ordinal;

            IF v_parent_type = 'POLITY' THEN
                IF NOT (v_parent_ordinal = ANY(v_polity_parents)) THEN
                    v_polity_parents := array_append(v_polity_parents, v_parent_ordinal);
                END IF;
            ELSIF v_parent_type = 'RELATION' THEN
                v_relation_seen := true;
            ELSE
                v_unresolved := true;
            END IF;
        END LOOP;

        IF v_unresolved THEN
            RETURN QUERY
            SELECT v_original, 'unresolved_parent_reference'::text, v_depth, v_path;
            RETURN;
        END IF;

        IF cardinality(v_polity_parents) > 1 THEN
            RETURN QUERY
            SELECT v_original, 'unresolved_multiple_polity_parents'::text, v_depth, v_path;
            RETURN;
        ELSIF cardinality(v_polity_parents) = 1 THEN
            v_current := v_polity_parents[1];
            v_depth := v_depth + 1;
            IF v_depth > 32 THEN
                RETURN QUERY
                SELECT v_original, 'unresolved_hierarchy_depth'::text, v_depth, v_path;
                RETURN;
            END IF;
            CONTINUE;
        ELSE
            RETURN QUERY
            SELECT v_current,
                   CASE WHEN v_relation_seen
                        THEN 'relation_membership_retained'
                        ELSE 'unresolved_empty_membership'
                   END,
                   v_depth,
                   v_path;
            RETURN;
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE FUNCTION staging.m2_cliopatria_polity_baseline(p_atlas_year integer)
RETURNS TABLE (
    atlas_year integer,
    cliopatria_source_year integer,
    dataset_key text,
    source_row_ordinal integer,
    source_feature_id text,
    name_raw text,
    type_raw text,
    from_year_raw integer,
    to_year_raw integer,
    member_of_raw text,
    components_raw text,
    seshat_id_raw text,
    wikidata_raw text,
    wikipedia_raw text,
    geom geometry,
    hierarchy_status text,
    suppressed_component_count integer,
    source_version_id uuid,
    source_asset_id uuid,
    upstream_commit text,
    asset_sha256 text,
    baseline_state text
)
LANGUAGE sql
STABLE
SET search_path = ''
AS $$
    WITH params AS (
        SELECT staging.m2_cliopatria_source_year(p_atlas_year) AS source_year
    ),
    active AS (
        SELECT f.*
        FROM staging.cliopatria_feature f
        CROSS JOIN params p
        WHERE f.type_raw = 'POLITY'
          AND f.source_years @> p.source_year
    ),
    resolved AS (
        SELECT
            a.dataset_key,
            a.source_row_ordinal AS origin_ordinal,
            r.resolved_source_row_ordinal,
            r.hierarchy_status,
            r.hierarchy_depth
        FROM active a
        CROSS JOIN params p
        CROSS JOIN LATERAL staging.m2_cliopatria_resolve_polity_row(
            a.dataset_key,
            a.source_row_ordinal,
            p.source_year
        ) r
    ),
    collapsed AS (
        SELECT
            dataset_key,
            resolved_source_row_ordinal,
            count(*)::integer AS contributor_count,
            bool_or(hierarchy_status LIKE 'unresolved_%') AS unresolved
        FROM resolved
        GROUP BY dataset_key, resolved_source_row_ordinal
    )
    SELECT
        p_atlas_year,
        p.source_year,
        f.dataset_key,
        f.source_row_ordinal,
        f.source_feature_id,
        f.name_raw,
        f.type_raw,
        f.from_year_raw,
        f.to_year_raw,
        f.member_of_raw,
        f.components_raw,
        f.seshat_id_raw,
        f.wikidata_raw,
        f.wikipedia_raw,
        f.geom,
        CASE
            WHEN c.unresolved THEN 'unresolved_hierarchy'
            WHEN c.contributor_count > 1 THEN 'resolved_polity_composite'
            WHEN nullif(btrim(f.member_of_raw),'') IS NOT NULL
                 THEN 'relation_membership_retained'
            ELSE 'resolved_top_polity'
        END AS hierarchy_status,
        greatest(c.contributor_count - 1, 0)::integer AS suppressed_component_count,
        d.source_version_id,
        d.source_asset_id,
        d.upstream_commit,
        d.asset_sha256,
        'raw_unapproved_global_baseline'::text
    FROM collapsed c
    JOIN staging.cliopatria_feature f
      ON f.dataset_key = c.dataset_key
     AND f.source_row_ordinal = c.resolved_source_row_ordinal
    JOIN staging.cliopatria_dataset d ON d.dataset_key = f.dataset_key
    CROSS JOIN params p
    ORDER BY f.name_raw, f.source_row_ordinal;
$$;

CREATE OR REPLACE FUNCTION staging.m2_cliopatria_relation_layer(p_atlas_year integer)
RETURNS TABLE (
    atlas_year integer,
    cliopatria_source_year integer,
    dataset_key text,
    source_row_ordinal integer,
    name_raw text,
    from_year_raw integer,
    to_year_raw integer,
    components_raw text,
    geom geometry,
    source_version_id uuid,
    source_asset_id uuid,
    upstream_commit text,
    asset_sha256 text,
    layer_state text
)
LANGUAGE sql
STABLE
SET search_path = ''
AS $$
    SELECT
        p_atlas_year,
        staging.m2_cliopatria_source_year(p_atlas_year),
        f.dataset_key,
        f.source_row_ordinal,
        f.name_raw,
        f.from_year_raw,
        f.to_year_raw,
        f.components_raw,
        f.geom,
        d.source_version_id,
        d.source_asset_id,
        d.upstream_commit,
        d.asset_sha256,
        'optional_relation_layer_unapproved'::text
    FROM staging.cliopatria_feature f
    JOIN staging.cliopatria_dataset d USING (dataset_key)
    WHERE f.type_raw = 'RELATION'
      AND f.source_years @> staging.m2_cliopatria_source_year(p_atlas_year)
    ORDER BY f.name_raw, f.source_row_ordinal;
$$;

DROP FUNCTION IF EXISTS staging.m2_cliopatria_geometry_candidates(integer);
CREATE FUNCTION staging.m2_cliopatria_geometry_candidates(p_atlas_year integer)
RETURNS TABLE (
    atlas_year integer,
    cliopatria_source_year integer,
    dataset_key text,
    source_row_ordinal integer,
    name_raw text,
    hierarchy_status text,
    suppressed_component_count integer,
    spatial_entity_id uuid,
    geometry_choice_status text,
    chosen_geometry_id uuid,
    chosen_accuracy_status atlas.geometry_accuracy,
    geom geometry,
    baseline_source_version_id uuid,
    baseline_source_asset_id uuid,
    baseline_upstream_commit text,
    baseline_asset_sha256 text,
    chosen_geometry_source_version_id uuid,
    chosen_geometry_source_native_id text,
    publication_state text
)
LANGUAGE sql
STABLE
SET search_path = ''
AS $$
    WITH baseline AS (
        SELECT * FROM staging.m2_cliopatria_polity_baseline(p_atlas_year)
    )
    SELECT
        b.atlas_year,
        b.cliopatria_source_year,
        b.dataset_key,
        b.source_row_ordinal,
        b.name_raw,
        b.hierarchy_status,
        b.suppressed_component_count,
        em.spatial_entity_id,
        CASE
            WHEN em.match_status IS DISTINCT FROM 'reviewed_match'
                THEN 'raw_baseline_identity_unresolved'
            WHEN ov.accepted_count = 1
                THEN 'accepted_specialist_override'
            WHEN ov.accepted_count > 1
                THEN 'raw_baseline_specialist_override_ambiguous'
            ELSE 'raw_cliopatria_baseline'
        END AS geometry_choice_status,
        CASE WHEN ov.accepted_count = 1 THEN ov.geometry_id ELSE NULL END,
        CASE WHEN ov.accepted_count = 1 THEN ov.accuracy_status ELSE NULL END,
        CASE WHEN ov.accepted_count = 1 THEN ov.specialist_geom ELSE b.geom END,
        b.source_version_id AS baseline_source_version_id,
        b.source_asset_id AS baseline_source_asset_id,
        b.upstream_commit AS baseline_upstream_commit,
        b.asset_sha256 AS baseline_asset_sha256,
        CASE WHEN ov.accepted_count = 1 THEN ov.geometry_source_version_id ELSE NULL END,
        CASE WHEN ov.accepted_count = 1 THEN ov.geometry_source_native_id ELSE NULL END,
        'prototype_unapproved'::text
    FROM baseline b
    LEFT JOIN staging.m2_cliopatria_entity_match em
      ON em.dataset_key = b.dataset_key
     AND em.source_row_ordinal = b.source_row_ordinal
    LEFT JOIN LATERAL (
        SELECT
            count(*)::integer AS accepted_count,
            (array_agg(g.geometry_id ORDER BY g.geometry_id))[1] AS geometry_id,
            min(g.accuracy_status::text)::atlas.geometry_accuracy AS accuracy_status,
            CASE WHEN count(*) = 1 THEN (array_agg(g.geom ORDER BY g.geometry_id))[1] ELSE NULL END AS specialist_geom,
            (array_agg(g.geometry_source_version_id ORDER BY g.geometry_id))[1]
                AS geometry_source_version_id,
            (array_agg(g.geometry_source_native_id ORDER BY g.geometry_id))[1]
                AS geometry_source_native_id
        FROM staging.m2_geometry_precedence p
        JOIN atlas.geometry g ON g.geometry_id = p.geometry_id
        WHERE p.spatial_entity_id = em.spatial_entity_id
          AND p.decision_status = 'accepted_specialist_override'
          AND p.valid_years @> p_atlas_year
          AND g.review_status = 'reviewed'
          AND g.geom IS NOT NULL
    ) ov ON true
    ORDER BY b.name_raw, b.source_row_ordinal;
$$;

REVOKE EXECUTE ON FUNCTION staging.m2_cliopatria_source_year(integer) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION staging.m2_validate_geometry_precedence() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION staging.m2_cliopatria_resolve_polity_row(text,integer,integer) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION staging.m2_cliopatria_polity_baseline(integer) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION staging.m2_cliopatria_relation_layer(integer) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION staging.m2_cliopatria_geometry_candidates(integer) FROM PUBLIC;
