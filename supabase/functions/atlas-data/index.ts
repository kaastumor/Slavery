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
    const releases = await sql`
      select release_version, schema_version, manifest
      from audit.release_manifest
      where status='published'
        and manifest->>'purpose'='public_mvp_preview'
      order by created_at desc
      limit 1
    `;

    if (releases.length === 0) {
      return new Response(JSON.stringify({ error: "No published MVP preview release" }), {
        status: 503,
        headers: { ...corsHeaders, "content-type": "application/json; charset=utf-8" },
      });
    }

    const places = await sql`
      with release as (
        select manifest
        from audit.release_manifest
        where status='published'
          and manifest->>'purpose'='public_mvp_preview'
        order by created_at desc
        limit 1
      ),
      release_claim as (
        select jsonb_array_elements_text(manifest->'claim_ids')::uuid as claim_id
        from release
      ),
      released_practice as (
        select t.*
        from publish.territorial_practice_claim t
        join release_claim rc using (claim_id)
      )
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
              'practice_type', c.practice_type_code,
              'practice_level', c.practice_level,
              'coverage_state', c.coverage_state_code,
              'classification_status', c.classification_status,
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
          from released_practice c
          where c.spatial_entity_id = se.spatial_entity_id
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
              'source_url', gsv.url_or_identifier,
              'render_transform', g.render_transform,
              'render_land_mask_id', g.render_land_mask_id
            )
            order by g.from_year nulls first, g.geometry_id
          )
          from publish.map_geometry g
          left join atlas.source_version gsv on gsv.source_version_id = g.geometry_source_version_id
          left join atlas.source gs on gs.source_id = gsv.source_id
          where g.spatial_entity_id = se.spatial_entity_id
            and g.geometry_id::text in (
              select jsonb_array_elements_text(manifest->'geometry_ids')
              from release
            )
        ), '[]'::jsonb) as geometries
      from publish.spatial_entity se
      where exists (
        select 1
        from released_practice c
        where c.spatial_entity_id = se.spatial_entity_id
      )
      order by se.canonical_name
    `;

    const fabrics = await sql`
      select
        fabric_id,
        source_name,
        source_version,
        source_url,
        source_commit_sha,
        source_blob_sha,
        content_md5,
        content_sha256
      from cartography.land_fabric
      where active
      order by created_at desc
      limit 1
    `;

    const release = releases[0];
    const fabric = fabrics[0] ?? null;

    return new Response(JSON.stringify({
      status: "published_preview",
      release_version: release.release_version,
      schema_version: release.schema_version,
      canonical: release.manifest?.canonical ?? false,
      data_boundary: "release_manifest_plus_publish_views",
      date_model: "astronomical_year_numbering",
      cartography: fabric ? {
        fabric_id: fabric.fabric_id,
        source_name: fabric.source_name,
        source_version: fabric.source_version,
        source_url: fabric.source_url,
        source_commit_sha: fabric.source_commit_sha,
        source_blob_sha: fabric.source_blob_sha,
        content_md5: fabric.content_md5,
        content_sha256: fabric.content_sha256,
      } : null,
      places,
    }), {
      headers: {
        ...corsHeaders,
        "content-type": "application/json; charset=utf-8",
        "cache-control": "public, max-age=60",
      },
    });
  } finally {
    await sql.end({ timeout: 2 });
  }
});
