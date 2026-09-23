-- M2 #121 full pinned-corpus selected-year acceptance.
-- Expected values were observed in successful GitHub Actions run 35877196416
-- against the exact Cliopatria asset pinned by D-059/#119.

DO $$
DECLARE
    v_dataset constant text :=
        'cliopatria:v0.2.0-duplicate:ad28a691b7c07c1fca89d0e0636d324667d2a258';
    r record;
    actual_baseline integer;
    actual_relations integer;
    actual_composites integer;
    actual_suppressed integer;
    actual_unresolved integer;
    actual_source_year integer;
    n bigint;
BEGIN
    FOR r IN
        SELECT * FROM (VALUES
            (-13, -14, 44, 1, 0, 0, 0),
            (0,    -1, 44, 1, 0, 0, 0),
            (1,     1, 45, 1, 0, 0, 0),
            (369, 369, 51, 1, 0, 0, 0),
            (1000,1000,107,1, 6,25, 0),
            (2024,2024,190,0, 3, 5, 0)
        ) AS x(
            atlas_year, source_year, baseline_count, relation_count,
            composite_count, suppressed_count, unresolved_count
        )
    LOOP
        actual_source_year := staging.m2_cliopatria_source_year(r.atlas_year);

        SELECT
            count(*)::integer,
            count(*) FILTER (WHERE hierarchy_status='resolved_polity_composite')::integer,
            coalesce(sum(suppressed_component_count),0)::integer,
            count(*) FILTER (WHERE hierarchy_status='unresolved_hierarchy')::integer
        INTO actual_baseline,actual_composites,actual_suppressed,actual_unresolved
        FROM staging.m2_cliopatria_polity_baseline(r.atlas_year)
        WHERE dataset_key=v_dataset;

        SELECT count(*)::integer INTO actual_relations
        FROM staging.m2_cliopatria_relation_layer(r.atlas_year)
        WHERE dataset_key=v_dataset;

        IF actual_source_year <> r.source_year
           OR actual_baseline <> r.baseline_count
           OR actual_relations <> r.relation_count
           OR actual_composites <> r.composite_count
           OR actual_suppressed <> r.suppressed_count
           OR actual_unresolved <> r.unresolved_count THEN
            RAISE EXCEPTION
                'selected-year drift for atlas year %: source %, baseline %, relations %, composites %, suppressed %, unresolved %; expected %, %, %, %, %, %',
                r.atlas_year,
                actual_source_year,actual_baseline,actual_relations,
                actual_composites,actual_suppressed,actual_unresolved,
                r.source_year,r.baseline_count,r.relation_count,
                r.composite_count,r.suppressed_count,r.unresolved_count;
        END IF;
    END LOOP;

    -- D-059 BCE/CE boundary: six observed bridge rows resolve at -1 and their
    -- next positive rows resolve at +1; source-native zero is never queried.
    SELECT count(*) INTO n
    FROM staging.m2_cliopatria_polity_baseline(0)
    WHERE dataset_key=v_dataset
      AND cliopatria_source_year=-1
      AND name_raw IN (
          'Yuezhi','Parthian Empire','Indo-Greeks',
          'Indo-Scythians','Judea','Roman Empire'
      )
      AND to_year_raw=0;
    IF n <> 6 THEN
        RAISE EXCEPTION 'BCE boundary bridge rows %, expected 6', n;
    END IF;

    SELECT count(*) INTO n
    FROM staging.m2_cliopatria_polity_baseline(1)
    WHERE dataset_key=v_dataset
      AND cliopatria_source_year=1
      AND name_raw IN (
          'Yuezhi','Parthian Empire','Indo-Greeks',
          'Indo-Scythians','Judea','Roman Empire'
      )
      AND from_year_raw=1;
    IF n <> 6 THEN
        RAISE EXCEPTION 'CE boundary successor rows %, expected 6', n;
    END IF;

    -- Representative real ancient case.
    SELECT count(*) INTO n
    FROM staging.m2_cliopatria_polity_baseline(369)
    WHERE dataset_key=v_dataset
      AND name_raw='Baekje'
      AND source_row_ordinal=1478
      AND from_year_raw=347
      AND to_year_raw=391
      AND hierarchy_status='resolved_top_polity';
    IF n <> 1 THEN
        RAISE EXCEPTION 'Baekje 369 source-row resolution drifted';
    END IF;

    -- Default baseline remains POLITY-only, duplicate-free and explicitly raw.
    SELECT count(*) INTO n
    FROM staging.m2_cliopatria_polity_baseline(369)
    WHERE dataset_key=v_dataset
      AND type_raw='RELATION';
    IF n <> 0 THEN
        RAISE EXCEPTION 'RELATION rows leaked into default polity baseline';
    END IF;

    SELECT count(*) INTO n
    FROM (
        SELECT source_row_ordinal,count(*)
        FROM staging.m2_cliopatria_polity_baseline(369)
        WHERE dataset_key=v_dataset
        GROUP BY source_row_ordinal
        HAVING count(*)>1
    ) d;
    IF n <> 0 THEN
        RAISE EXCEPTION 'duplicate selected-year source candidates observed';
    END IF;

    SELECT count(*) INTO n
    FROM staging.m2_cliopatria_polity_baseline(369)
    WHERE dataset_key=v_dataset
      AND baseline_state <> 'raw_unapproved_global_baseline';
    IF n <> 0 THEN
        RAISE EXCEPTION 'raw baseline acquired non-raw approval state';
    END IF;

    IF staging.m2_cliopatria_source_year(0)=0
       OR staging.m2_cliopatria_source_year(-13)=-13 THEN
        RAISE EXCEPTION 'D-059 source-year translation regressed';
    END IF;
END $$;

SELECT 'M2 complete pinned Cliopatria selected-year acceptance passed' AS result;
