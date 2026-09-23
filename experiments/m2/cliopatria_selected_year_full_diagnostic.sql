\pset tuples_only on
\pset format unaligned

WITH requested(atlas_year,label) AS (
    VALUES
        (-13,'14 BCE'),
        (0,'1 BCE'),
        (1,'1 CE'),
        (369,'369 CE'),
        (1000,'1000 CE'),
        (2024,'2024 CE')
),
stats AS (
    SELECT
        y.atlas_year,
        y.label,
        staging.m2_cliopatria_source_year(y.atlas_year) AS cliopatria_source_year,
        b.baseline_count,
        b.unresolved_hierarchy_count,
        b.composite_candidate_count,
        b.suppressed_component_count,
        r.relation_count
    FROM requested y
    CROSS JOIN LATERAL (
        SELECT
            count(*)::integer AS baseline_count,
            count(*) FILTER (WHERE hierarchy_status='unresolved_hierarchy')::integer
                AS unresolved_hierarchy_count,
            count(*) FILTER (WHERE hierarchy_status='resolved_polity_composite')::integer
                AS composite_candidate_count,
            coalesce(sum(suppressed_component_count),0)::integer
                AS suppressed_component_count
        FROM staging.m2_cliopatria_polity_baseline(y.atlas_year)
    ) b
    CROSS JOIN LATERAL (
        SELECT count(*)::integer AS relation_count
        FROM staging.m2_cliopatria_relation_layer(y.atlas_year)
    ) r
),
boundary_examples AS (
    SELECT *
    FROM (
        SELECT
            b.atlas_year,b.cliopatria_source_year,b.name_raw,b.source_row_ordinal,
            b.from_year_raw,b.to_year_raw,b.hierarchy_status
        FROM staging.m2_cliopatria_polity_baseline(0) b
        WHERE b.name_raw IN (
            'Roman Empire','Yuezhi','Parthian Empire','Indo-Greeks',
            'Indo-Scythians','Judea'
        )
        UNION ALL
        SELECT
            b.atlas_year,b.cliopatria_source_year,b.name_raw,b.source_row_ordinal,
            b.from_year_raw,b.to_year_raw,b.hierarchy_status
        FROM staging.m2_cliopatria_polity_baseline(1) b
        WHERE b.name_raw IN (
            'Roman Empire','Yuezhi','Parthian Empire','Indo-Greeks',
            'Indo-Scythians','Judea'
        )
    ) q
),
baekje_raw AS (
    SELECT
        f.source_row_ordinal,
        f.name_raw,
        f.type_raw,
        f.from_year_raw,
        f.to_year_raw,
        f.member_of_raw,
        r.resolved_source_row_ordinal,
        r.hierarchy_status,
        r.hierarchy_depth
    FROM staging.cliopatria_feature f
    CROSS JOIN LATERAL staging.m2_cliopatria_resolve_polity_row(
        f.dataset_key,
        f.source_row_ordinal,
        staging.m2_cliopatria_source_year(369)
    ) r
    WHERE f.name_raw='Baekje'
      AND f.type_raw='POLITY'
      AND f.source_years @> staging.m2_cliopatria_source_year(369)
),
modern_samples AS (
    SELECT name_raw,source_row_ordinal,from_year_raw,to_year_raw,hierarchy_status,
           suppressed_component_count
    FROM staging.m2_cliopatria_polity_baseline(2024)
    ORDER BY name_raw,source_row_ordinal
    LIMIT 12
),
invariants AS (
    SELECT jsonb_build_object(
        'requested_source_zero_count',
        (SELECT count(*) FROM stats WHERE cliopatria_source_year=0),
        'duplicate_candidate_keys_369',
        (
            SELECT count(*)
            FROM (
                SELECT dataset_key,source_row_ordinal,count(*)
                FROM staging.m2_cliopatria_polity_baseline(369)
                GROUP BY dataset_key,source_row_ordinal
                HAVING count(*)>1
            ) d
        ),
        'relation_rows_in_default_baseline_369',
        (
            SELECT count(*)
            FROM staging.m2_cliopatria_polity_baseline(369)
            WHERE type_raw='RELATION'
        ),
        'non_raw_baseline_state_369',
        (
            SELECT count(*)
            FROM staging.m2_cliopatria_polity_baseline(369)
            WHERE baseline_state <> 'raw_unapproved_global_baseline'
        )
    ) AS value
)
SELECT jsonb_pretty(
    jsonb_build_object(
        'schema_version','m2-cliopatria-selected-year-diagnostic-v1',
        'stats',(SELECT jsonb_agg(to_jsonb(stats) ORDER BY atlas_year) FROM stats),
        'boundary_examples',coalesce(
            (SELECT jsonb_agg(to_jsonb(boundary_examples) ORDER BY atlas_year,name_raw)
             FROM boundary_examples),
            '[]'::jsonb
        ),
        'baekje_369',coalesce(
            (SELECT jsonb_agg(to_jsonb(baekje_raw) ORDER BY source_row_ordinal)
             FROM baekje_raw),
            '[]'::jsonb
        ),
        'modern_2024_samples',coalesce(
            (SELECT jsonb_agg(to_jsonb(modern_samples) ORDER BY name_raw)
             FROM modern_samples),
            '[]'::jsonb
        ),
        'invariants',(SELECT value FROM invariants)
    )
);
