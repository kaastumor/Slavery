import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import postgres from "https://deno.land/x/postgresjs@v3.4.5/mod.js";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  if (req.method !== "GET") return new Response("Method not allowed", { status: 405, headers: corsHeaders });

  const sql = postgres(Deno.env.get("SUPABASE_DB_URL")!, { prepare: false });

  try {
    const places = await sql`
      select
        se.spatial_entity_id,
        se.canonical_name as name,
        se.display_name,
        se.entity_type_code,
        se.notes,
        coalesce((
          select jsonb_agg(
            jsonb_build_object(
              'claim_id', c.claim_id,
              'from_year', c.from_year,
              'to_year', c.to_year,
              'summary', c.summary,
              'review_status', c.review_status,
              'publication_status', c.publication_status,
              'practice_type', t.practice_type_code,
              'practice_level', t.practice_level,
              'coverage_state', t.coverage_state_code,
              'classification_status', t.classification_status,
              'sources', coalesce((
                select jsonb_agg(
                  jsonb_build_object(
                    'title', s.title,
                    'author_or_institution', s.author_or_institution,
                    'source_type', s.source_type,
                    'source_classification', s.source_classification,
                    'version_label', sv.version_label,
                    'url', sv.url_or_identifier,
                    'direction', cs.direction,
                    'locator', cs.locator
                  )
                  order by s.title
                )
                from atlas.claim_source cs
                join atlas.source_version sv on sv.source_version_id = cs.source_version_id
                join atlas.source s on s.source_id = sv.source_id
                where cs.claim_id = c.claim_id
              ), '[]'::jsonb)
            )
            order by c.from_year, c.claim_id
          )
          from atlas.territorial_practice_claim t
          join atlas.claim c on c.claim_id = t.claim_id
          where t.spatial_entity_id = se.spatial_entity_id
            and c.review_status = 'reviewed'
        ), '[]'::jsonb) as claims,
        coalesce((
          select jsonb_agg(
            jsonb_build_object(
              'geometry_id', g.geometry_id,
              'from_year', g.from_year,
              'to_year', g.to_year,
              'accuracy_status', g.accuracy_status,
              'resolution_method', g.resolution_method,
              'source_native_id', g.geometry_source_native_id,
              'geometry', case when g.geom is null then null else st_asgeojson(g.geom)::jsonb end,
              'source_title', gs.title,
              'source_version', gsv.version_label,
              'source_url', gsv.url_or_identifier
            )
            order by g.from_year nulls first, g.geometry_id
          )
          from atlas.geometry g
          left join atlas.source_version gsv on gsv.source_version_id = g.geometry_source_version_id
          left join atlas.source gs on gs.source_id = gsv.source_id
          where g.spatial_entity_id = se.spatial_entity_id
            and g.review_status = 'reviewed'
        ), '[]'::jsonb) as geometries
      from atlas.spatial_entity se
      where se.review_status = 'reviewed'
        and exists (
          select 1
          from atlas.territorial_practice_claim t
          join atlas.claim c on c.claim_id = t.claim_id
          where t.spatial_entity_id = se.spatial_entity_id
            and c.review_status = 'reviewed'
        )
      order by se.canonical_name
    `;

    return new Response(JSON.stringify({
      status: "research_preview",
      data_boundary: "reviewed_atlas_records_not_yet_canonical_public_release",
      date_model: "astronomical_year_numbering",
      places,
    }), {
      headers: {
        ...corsHeaders,
        "content-type": "application/json; charset=utf-8",
        "cache-control": "no-store",
      },
    });
  } finally {
    await sql.end({ timeout: 2 });
  }
});
