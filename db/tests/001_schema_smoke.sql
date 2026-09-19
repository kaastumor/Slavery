-- Foundation smoke tests. Run after migrations 0001-0011.
-- Any raised exception means the foundation schema is not accepted.

DO $$
DECLARE
    missing text;
BEGIN
    SELECT string_agg(name, ', ')
    INTO missing
    FROM (VALUES
        ('atlas.source'),
        ('atlas.source_version'),
        ('atlas.actor'),
        ('atlas.spatial_entity'),
        ('atlas.geometry'),
        ('atlas.claim'),
        ('atlas.claim_source'),
        ('atlas.voyage'),
        ('atlas.voyage_owner'),
        ('audit.ingest_run'),
        ('audit.research_coverage_assessment'),
        ('audit.research_coverage_source'),
        ('atlas.external_participation_claim')
    ) AS required(name)
    WHERE to_regclass(name) IS NULL;

    IF missing IS NOT NULL THEN
        RAISE EXCEPTION 'Missing required relations: %', missing;
    END IF;
END $$;

DO $$
BEGIN
    IF atlas.make_year_range(0,0) IS DISTINCT FROM int4range(0,1,'[)') THEN
        RAISE EXCEPTION '1 BCE range conversion failed';
    END IF;
    IF NOT (atlas.make_year_range(0,0) @> 0) OR (atlas.make_year_range(0,0) @> 1) THEN
        RAISE EXCEPTION 'Historical year containment failed at BCE/CE boundary';
    END IF;
    IF atlas.make_year_range(NULL,NULL) IS NOT NULL THEN
        RAISE EXCEPTION 'Unknown/unknown time must be NULL, not unbounded all-time';
    END IF;
    IF NOT (atlas.make_year_range(NULL, 10) @> -1000) THEN
        RAISE EXCEPTION 'Open lower bound failed';
    END IF;
    IF NOT (atlas.make_year_range(10, NULL) @> 1000) THEN
        RAISE EXCEPTION 'Open upper bound failed';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'postgis') THEN
        RAISE EXCEPTION 'PostGIS extension missing';
    END IF;
END $$;

DO $$
DECLARE
    n integer;
BEGIN
    SELECT count(*) INTO n
    FROM pg_indexes
    WHERE schemaname = 'atlas'
      AND indexname IN ('geometry_geom_gist','geometry_valid_years_gist','claim_valid_years_gist','spatial_relation_valid_years_gist');
    IF n <> 4 THEN
        RAISE EXCEPTION 'Expected 4 core GiST indexes, found %', n;
    END IF;
END $$;
