#!/usr/bin/env python3
"""Build and verify preservation-grade full-state release bundles.

This Gate-3 tool is deliberately separate from tools/release_bundle.py.

The D-054 v1 bundle owns the thin territorial-practice public preview.  This v2
contract freezes the broader reviewed research state needed before PostgreSQL can
become canonical research authority.  It does not publish a release, mutate release
channels, or infer release membership from every reviewed row.

Workflow:

1. freeze: derive dependency closure from an explicit seed and write a frozen
   candidate with exact top-level IDs;
2. build: snapshot exactly those frozen IDs into deterministic composite objects;
3. lint: verify internal bundle digests without database access;
4. verify: re-derive the seed closure and compare current database state with the
   frozen bundle before promotion.

Publication/apply belongs to D-101 Gate 4, not this tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any


CANDIDATE_SCHEMA = "historical-slavery-atlas-full-state-candidate-v2"
BUNDLE_SCHEMA = "historical-slavery-atlas-full-state-bundle-v2"
PURPOSE = "canonical_research_state_proof"

MEMBERSHIP_KEYS = (
    "claim_ids",
    "actor_ids",
    "spatial_entity_ids",
    "geometry_ids",
    "voyage_ids",
    "coverage_assessment_ids",
    "source_version_ids",
    "research_target_result_ids",
)

OBJECT_GROUPS = {
    "claims": "claim_ids",
    "actors": "actor_ids",
    "spatial_entities": "spatial_entity_ids",
    "geometries": "geometry_ids",
    "voyages": "voyage_ids",
    "coverage_assessments": "coverage_assessment_ids",
    "source_versions": "source_version_ids",
    "research_target_results": "research_target_result_ids",
}


class BundleError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sorted_unique(values: list[Any] | tuple[Any, ...]) -> list[str]:
    return sorted({str(value) for value in values if value is not None})


def _require_membership_shape(membership: Any) -> dict[str, list[str]]:
    if not isinstance(membership, dict):
        raise BundleError("membership must be an object")
    result: dict[str, list[str]] = {}
    for key in MEMBERSHIP_KEYS:
        values = membership.get(key)
        if not isinstance(values, list):
            raise BundleError(f"membership.{key} must be an array")
        normalized = [str(value) for value in values]
        if normalized != sorted(set(normalized)):
            raise BundleError(f"membership.{key} must be sorted and unique")
        result[key] = normalized
    return result


def load_seed(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise BundleError("seed must be a JSON object")
    for key in (
        "release_version",
        "schema_version",
        "canonical_predecessor_version",
        "predecessor_manifest_version",
        "reviewed_candidate_id",
        "workbook_sha256",
        "changelog",
        "qc_summary",
        "unresolved_issues",
    ):
        if not data.get(key):
            raise BundleError(f"seed.{key} is required")
    if data.get("canonical", False):
        raise BundleError("Gate-3 proof candidates are noncanonical")
    if data.get("purpose", PURPOSE) != PURPOSE:
        raise BundleError(f"seed purpose must be {PURPOSE}")
    data["canonical"] = False
    data["purpose"] = PURPOSE
    return data


def load_candidate(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise BundleError("candidate must be a JSON object")
    if data.get("candidate_schema") != CANDIDATE_SCHEMA:
        raise BundleError("unsupported full-state candidate schema")
    if data.get("canonical", False):
        raise BundleError("Gate-3 proof candidate must be noncanonical")
    if data.get("purpose") != PURPOSE:
        raise BundleError(f"candidate purpose must be {PURPOSE}")
    for key in (
        "release_version",
        "schema_version",
        "canonical_predecessor_version",
        "predecessor_manifest_version",
        "reviewed_candidate_id",
        "workbook_sha256",
        "changelog",
        "qc_summary",
        "unresolved_issues",
        "seed",
        "membership",
        "membership_sha256",
    ):
        if key not in data:
            raise BundleError(f"candidate.{key} is required")
    membership = _require_membership_shape(data["membership"])
    if data["membership_sha256"] != sha256_value(membership):
        raise BundleError("candidate membership_sha256 mismatch")
    data["membership"] = membership
    return data


def _fetch_ids(cur, query: str, params: tuple[Any, ...] = ()) -> list[str]:
    cur.execute(query, params)
    return _sorted_unique([row[0] for row in cur.fetchall()])


def _manifest_array(manifest: dict[str, Any], key: str) -> list[str]:
    value = manifest.get(key, [])
    if not isinstance(value, list):
        raise BundleError(f"predecessor manifest {key} must be an array")
    return _sorted_unique(value)


def _fetch_predecessor_manifest(cur, version: str) -> dict[str, Any]:
    cur.execute(
        """
        select manifest
        from audit.release_manifest
        where release_version=%s
        """,
        (version,),
    )
    row = cur.fetchone()
    if not row:
        raise BundleError(f"predecessor manifest not found: {version}")
    manifest = row[0]
    if not isinstance(manifest, dict):
        raise BundleError("predecessor manifest is not a JSON object")
    return manifest


def derive_membership(cur, seed: dict[str, Any]) -> dict[str, list[str]]:
    """Derive a deterministic dependency closure from explicit reviewed seeds.

    Primary membership comes from:
    - the historical v0.6.1 DB migration candidate manifest;
    - the Gate-1 repaired v0.6.1 global evidence map;
    - the frozen v3 internal review candidate.

    Dependency closure adds only objects referenced by those members.
    """

    manifest = _fetch_predecessor_manifest(
        cur, str(seed["predecessor_manifest_version"])
    )

    claim_ids = set(_manifest_array(manifest, "claim_ids"))
    claim_ids.update(
        _fetch_ids(
            cur,
            """
            select distinct claim_id::text
            from audit.v061_evidence_claim_map
            where legacy_evidence_id like 'v0.% Evidence!%'
            """,
        )
    )

    actor_ids = set(_manifest_array(manifest, "actor_ids"))
    voyage_ids = set(_manifest_array(manifest, "voyage_ids"))
    coverage_ids = set(_manifest_array(manifest, "coverage_assessment_ids"))
    source_version_ids = set(_manifest_array(manifest, "source_version_ids"))

    research_result_ids = set(
        _fetch_ids(
            cur,
            """
            select distinct research_target_result_id::text
            from audit.research_target_review
            where candidate_id=%s and review_level='internal'
            """,
            (str(seed["reviewed_candidate_id"]),),
        )
    )
    if not research_result_ids:
        raise BundleError("reviewed candidate has no internal research results")

    claims = sorted(claim_ids)
    actors = sorted(actor_ids)
    voyages = sorted(voyage_ids)
    coverage = sorted(coverage_ids)
    research_results = sorted(research_result_ids)

    # Referenced actors and voyages are part of the primary semantic closure.
    actor_ids.update(
        _fetch_ids(
            cur,
            """
            select actor_id::text from atlas.external_participation_claim
             where claim_id=any(%s::uuid[]) and actor_id is not null
            union
            select actor_id::text from atlas.actor_attribute_claim
             where claim_id=any(%s::uuid[])
            union
            select value_actor_id::text from atlas.actor_attribute_claim
             where claim_id=any(%s::uuid[]) and value_actor_id is not null
            union
            select actor_id::text from atlas.voyage_owner
             where voyage_id=any(%s::uuid[]) and actor_id is not null
            union
            select actor_id::text from atlas.voyage_finance
             where voyage_id=any(%s::uuid[])
            """,
            (claims, claims, claims, voyages, voyages),
        )
    )
    voyage_ids.update(
        _fetch_ids(
            cur,
            """
            select voyage_id::text from atlas.voyage_owner
             where claim_id=any(%s::uuid[])
            union
            select voyage_id::text from atlas.voyage_finance
             where claim_id=any(%s::uuid[])
            union
            select voyage_id::text from atlas.voyage_stop
             where claim_id=any(%s::uuid[])
            """,
            (claims, claims, claims),
        )
    )
    actors = sorted(actor_ids)
    voyages = sorted(voyage_ids)

    spatial_ids = set(
        _fetch_ids(
            cur,
            """
            select spatial_entity_id::text from atlas.territorial_practice_claim
             where claim_id=any(%s::uuid[])
            union
            select spatial_entity_id::text from atlas.external_participation_claim
             where claim_id=any(%s::uuid[]) and spatial_entity_id is not null
            union
            select jurisdiction_spatial_entity_id::text from atlas.legal_event
             where claim_id=any(%s::uuid[])
            union
            select value_spatial_entity_id::text from atlas.actor_attribute_claim
             where claim_id=any(%s::uuid[]) and value_spatial_entity_id is not null
            union
            select spatial_entity_id::text from atlas.claim_evidence_locus
             where claim_id=any(%s::uuid[])
            union
            select spatial_entity_id::text from atlas.claim_inference_extent
             where claim_id=any(%s::uuid[])
            union
            select subject_spatial_entity_id::text from atlas.spatial_relation
             where claim_id=any(%s::uuid[])
            union
            select object_spatial_entity_id::text from atlas.spatial_relation
             where claim_id=any(%s::uuid[])
            union
            select spatial_entity_id::text from audit.research_coverage_assessment
             where coverage_assessment_id=any(%s::uuid[]) and spatial_entity_id is not null
            union
            select spatial_entity_id::text from atlas.voyage_stop
             where voyage_id=any(%s::uuid[]) and spatial_entity_id is not null
            union
            select rt.spatial_entity_id::text
              from audit.research_target_result rr
              join audit.research_target rt using(target_key)
             where rr.research_target_result_id=any(%s::uuid[])
               and rt.spatial_entity_id is not null
            """,
            (
                claims,
                claims,
                claims,
                claims,
                claims,
                claims,
                claims,
                claims,
                coverage,
                voyages,
                research_results,
            ),
        )
    )
    spatial = sorted(spatial_ids)

    geometry_ids = set()
    if spatial:
        geometry_ids.update(
            _fetch_ids(
                cur,
                """
                select geometry_id::text
                from atlas.geometry
                where spatial_entity_id=any(%s::uuid[])
                  and review_status='reviewed'
                """,
                (spatial,),
            )
        )
    geometries = sorted(geometry_ids)

    # Freeze every exact source version on which a selected object depends.
    source_version_ids.update(
        _fetch_ids(
            cur,
            """
            select source_version_id::text from atlas.claim_source
             where claim_id=any(%s::uuid[])
            union
            select source_version_id::text from atlas.actor_name
             where actor_id=any(%s::uuid[]) and source_version_id is not null
            union
            select geometry_source_version_id::text from atlas.geometry
             where geometry_id=any(%s::uuid[]) and geometry_source_version_id is not null
            union
            select primary_source_version_id::text from atlas.voyage
             where voyage_id=any(%s::uuid[])
            union
            select source_version_id::text from audit.research_coverage_source
             where coverage_assessment_id=any(%s::uuid[])
            union
            select source_version_id::text from audit.research_target_source
             where research_target_result_id=any(%s::uuid[])
            """,
            (claims, actors, geometries, voyages, coverage, research_results),
        )
    )

    membership = {
        "claim_ids": claims,
        "actor_ids": actors,
        "spatial_entity_ids": spatial,
        "geometry_ids": geometries,
        "voyage_ids": voyages,
        "coverage_assessment_ids": coverage,
        "source_version_ids": sorted(source_version_ids),
        "research_target_result_ids": research_results,
    }
    return _require_membership_shape(membership)


def _assert_reviewed_members(cur, membership: dict[str, list[str]]) -> None:
    checks = (
        ("claim_ids", "atlas.claim", "claim_id", "review_status='reviewed'"),
        ("actor_ids", "atlas.actor", "actor_id", "review_status='reviewed'"),
        (
            "spatial_entity_ids",
            "atlas.spatial_entity",
            "spatial_entity_id",
            "review_status='reviewed'",
        ),
        ("geometry_ids", "atlas.geometry", "geometry_id", "review_status='reviewed'"),
        ("voyage_ids", "atlas.voyage", "voyage_id", "review_status='reviewed'"),
        (
            "coverage_assessment_ids",
            "audit.research_coverage_assessment",
            "coverage_assessment_id",
            "review_status='reviewed'",
        ),
        (
            "research_target_result_ids",
            "audit.research_target_result",
            "research_target_result_id",
            "review_status='reviewed'",
        ),
    )
    for member_key, table, id_col, predicate in checks:
        ids = membership[member_key]
        if not ids:
            continue
        cur.execute(
            f"select {id_col}::text from {table} "
            f"where {id_col}=any(%s::uuid[]) and {predicate}",
            (ids,),
        )
        found = {str(row[0]) for row in cur.fetchall()}
        missing = sorted(set(ids) - found)
        if missing:
            raise BundleError(
                f"{member_key} contains missing/non-reviewed members: {missing}"
            )

    source_ids = membership["source_version_ids"]
    if source_ids:
        cur.execute(
            """
            select source_version_id::text
            from atlas.source_version
            where source_version_id=any(%s::uuid[])
            """,
            (source_ids,),
        )
        found = {str(row[0]) for row in cur.fetchall()}
        missing = sorted(set(source_ids) - found)
        if missing:
            raise BundleError(f"source_version_ids missing in database: {missing}")


def freeze_candidate(
    conn,
    seed: dict[str, Any],
    *,
    source_git_sha: str | None,
) -> dict[str, Any]:
    with conn.cursor() as cur:
        membership = derive_membership(cur, seed)
        _assert_reviewed_members(cur, membership)

    candidate = {
        "candidate_schema": CANDIDATE_SCHEMA,
        "release_version": str(seed["release_version"]),
        "schema_version": str(seed["schema_version"]),
        "purpose": PURPOSE,
        "canonical": False,
        "canonical_predecessor_version": str(seed["canonical_predecessor_version"]),
        "predecessor_manifest_version": str(seed["predecessor_manifest_version"]),
        "reviewed_candidate_id": str(seed["reviewed_candidate_id"]),
        "workbook_sha256": str(seed["workbook_sha256"]),
        "changelog": str(seed["changelog"]),
        "qc_summary": str(seed["qc_summary"]),
        "unresolved_issues": str(seed["unresolved_issues"]),
        "source_git_sha": source_git_sha,
        "seed": {
            "predecessor_manifest_version": str(seed["predecessor_manifest_version"]),
            "reviewed_candidate_id": str(seed["reviewed_candidate_id"]),
        },
        "membership": membership,
        "membership_sha256": sha256_value(membership),
    }
    return candidate


def _payload_map(cur, query: str, ids: list[str]) -> dict[str, Any]:
    if not ids:
        return {}
    cur.execute(query, (ids,))
    result = {str(object_id): payload for object_id, payload in cur.fetchall()}
    if set(result) != set(ids):
        missing = sorted(set(ids) - set(result))
        extra = sorted(set(result) - set(ids))
        raise BundleError(
            f"object membership mismatch; missing={missing} extra={extra}"
        )
    return dict(sorted(result.items()))


def snapshot_objects(
    cur, membership: dict[str, list[str]]
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    objects: dict[str, dict[str, Any]] = {}

    objects["claims"] = _payload_map(
        cur,
        """
        select c.claim_id::text,
          jsonb_build_object(
            'claim',to_jsonb(c),
            'territorial_practice',(select to_jsonb(x) from atlas.territorial_practice_claim x where x.claim_id=c.claim_id),
            'external_participation',(select to_jsonb(x) from atlas.external_participation_claim x where x.claim_id=c.claim_id),
            'legal_event',(select to_jsonb(x) from atlas.legal_event x where x.claim_id=c.claim_id),
            'actor_attribute',(select to_jsonb(x) from atlas.actor_attribute_claim x where x.claim_id=c.claim_id),
            'claim_sources',coalesce((select jsonb_agg(to_jsonb(x) order by x.claim_source_id) from atlas.claim_source x where x.claim_id=c.claim_id),'[]'::jsonb),
            'asserted_intervals',coalesce((select jsonb_agg(to_jsonb(x) order by x.claim_asserted_interval_id) from atlas.claim_asserted_interval x where x.claim_id=c.claim_id),'[]'::jsonb),
            'evidence_loci',coalesce((select jsonb_agg(to_jsonb(x) order by x.spatial_entity_id) from atlas.claim_evidence_locus x where x.claim_id=c.claim_id),'[]'::jsonb),
            'inference_extents',coalesce((select jsonb_agg(to_jsonb(x) order by x.spatial_entity_id) from atlas.claim_inference_extent x where x.claim_id=c.claim_id),'[]'::jsonb),
            'practice_facets',coalesce((select jsonb_agg(to_jsonb(x) order by x.practice_facet_assertion_id) from atlas.practice_facet_assertion x where x.claim_id=c.claim_id),'[]'::jsonb),
            'spatial_relations',coalesce((select jsonb_agg(to_jsonb(x) order by x.spatial_relation_id) from atlas.spatial_relation x where x.claim_id=c.claim_id),'[]'::jsonb),
            'voyage_owners',coalesce((select jsonb_agg(to_jsonb(x) order by x.voyage_owner_id) from atlas.voyage_owner x where x.claim_id=c.claim_id),'[]'::jsonb),
            'voyage_finance',coalesce((select jsonb_agg(to_jsonb(x) order by x.voyage_finance_id) from atlas.voyage_finance x where x.claim_id=c.claim_id),'[]'::jsonb),
            'voyage_stops',coalesce((select jsonb_agg(to_jsonb(x) order by x.voyage_stop_id) from atlas.voyage_stop x where x.claim_id=c.claim_id),'[]'::jsonb)
          )
        from atlas.claim c
        where c.claim_id=any(%s::uuid[])
        order by c.claim_id
        """,
        membership["claim_ids"],
    )

    objects["actors"] = _payload_map(
        cur,
        """
        select a.actor_id::text,
          jsonb_build_object(
            'actor',to_jsonb(a),
            'names',coalesce((select jsonb_agg(to_jsonb(n) order by n.actor_name_id) from atlas.actor_name n where n.actor_id=a.actor_id),'[]'::jsonb)
          )
        from atlas.actor a
        where a.actor_id=any(%s::uuid[])
        order by a.actor_id
        """,
        membership["actor_ids"],
    )

    objects["spatial_entities"] = _payload_map(
        cur,
        """
        select s.spatial_entity_id::text,
          jsonb_build_object(
            'spatial_entity',to_jsonb(s),
            'polity',(select to_jsonb(p) from atlas.polity p where p.spatial_entity_id=s.spatial_entity_id)
          )
        from atlas.spatial_entity s
        where s.spatial_entity_id=any(%s::uuid[])
        order by s.spatial_entity_id
        """,
        membership["spatial_entity_ids"],
    )

    objects["geometries"] = _payload_map(
        cur,
        """
        select g.geometry_id::text,
          (to_jsonb(g)-'geom') ||
          jsonb_build_object(
            'geom_srid',case when g.geom is null then null else st_srid(g.geom) end,
            'geom_ewkb_hex',case when g.geom is null then null else encode(st_asewkb(g.geom),'hex') end
          )
        from atlas.geometry g
        where g.geometry_id=any(%s::uuid[])
        order by g.geometry_id
        """,
        membership["geometry_ids"],
    )

    objects["voyages"] = _payload_map(
        cur,
        """
        select v.voyage_id::text,
          jsonb_build_object(
            'voyage',to_jsonb(v),
            'owners',coalesce((select jsonb_agg(to_jsonb(x) order by x.voyage_owner_id) from atlas.voyage_owner x where x.voyage_id=v.voyage_id),'[]'::jsonb),
            'finance',coalesce((select jsonb_agg(to_jsonb(x) order by x.voyage_finance_id) from atlas.voyage_finance x where x.voyage_id=v.voyage_id),'[]'::jsonb),
            'stops',coalesce((select jsonb_agg(to_jsonb(x) order by x.voyage_stop_id) from atlas.voyage_stop x where x.voyage_id=v.voyage_id),'[]'::jsonb)
          )
        from atlas.voyage v
        where v.voyage_id=any(%s::uuid[])
        order by v.voyage_id
        """,
        membership["voyage_ids"],
    )

    objects["coverage_assessments"] = _payload_map(
        cur,
        """
        select c.coverage_assessment_id::text,
          jsonb_build_object(
            'coverage_assessment',to_jsonb(c),
            'sources',coalesce((select jsonb_agg(to_jsonb(x) order by x.source_version_id,x.source_role,x.locator) from audit.research_coverage_source x where x.coverage_assessment_id=c.coverage_assessment_id),'[]'::jsonb)
          )
        from audit.research_coverage_assessment c
        where c.coverage_assessment_id=any(%s::uuid[])
        order by c.coverage_assessment_id
        """,
        membership["coverage_assessment_ids"],
    )

    objects["source_versions"] = _payload_map(
        cur,
        """
        select sv.source_version_id::text,
          jsonb_build_object(
            'source_version',to_jsonb(sv),
            'source',to_jsonb(s),
            'assets',coalesce((select jsonb_agg(to_jsonb(a) order by a.source_asset_id) from atlas.source_asset a where a.source_version_id=sv.source_version_id),'[]'::jsonb)
          )
        from atlas.source_version sv
        join atlas.source s using(source_id)
        where sv.source_version_id=any(%s::uuid[])
        order by sv.source_version_id
        """,
        membership["source_version_ids"],
    )

    objects["research_target_results"] = _payload_map(
        cur,
        """
        select rr.research_target_result_id::text,
          jsonb_build_object(
            'result',to_jsonb(rr),
            'target',to_jsonb(rt),
            'reviews',coalesce((select jsonb_agg(to_jsonb(x) order by x.research_target_review_id) from audit.research_target_review x where x.research_target_result_id=rr.research_target_result_id),'[]'::jsonb),
            'sources',coalesce((select jsonb_agg(to_jsonb(x) order by x.research_target_source_id) from audit.research_target_source x where x.research_target_result_id=rr.research_target_result_id),'[]'::jsonb),
            'claim_bridges',coalesce((select jsonb_agg(to_jsonb(x) order by x.claim_id,x.claim_role) from audit.research_target_claim x where x.research_target_result_id=rr.research_target_result_id),'[]'::jsonb)
          )
        from audit.research_target_result rr
        join audit.research_target rt using(target_key)
        where rr.research_target_result_id=any(%s::uuid[])
        order by rr.research_target_result_id
        """,
        membership["research_target_result_ids"],
    )

    cur.execute(
        """
        select 'land_fabric'::text,
               fabric_id::text,
               (to_jsonb(f)-'geom') ||
               jsonb_build_object(
                 'geom_srid',st_srid(f.geom),
                 'geom_ewkb_hex',encode(st_asewkb(f.geom),'hex')
               )
        from cartography.land_fabric f
        where active
        order by created_at desc
        limit 1
        """
    )
    row = cur.fetchone()
    if row:
        cartography = {"kind": row[0], "id": row[1], "payload": row[2]}
    else:
        cur.execute(
            """
            select 'neutral_land_mask'::text,
                   mask_id::text,
                   (to_jsonb(m)-'geom') ||
                   jsonb_build_object(
                     'geom_srid',st_srid(m.geom),
                     'geom_ewkb_hex',encode(st_asewkb(m.geom),'hex')
                   )
            from publish.neutral_land_mask m
            where mask_id='neutral-world-land-v1'
            """
        )
        row = cur.fetchone()
        if not row:
            raise BundleError("no active cartography fabric or neutral land fallback")
        cartography = {"kind": row[0], "id": row[1], "payload": row[2]}

    return objects, cartography


def object_digests(objects: dict[str, dict[str, Any]]) -> dict[str, dict[str, str]]:
    return {
        group: {
            object_id: sha256_value(payload)
            for object_id, payload in sorted(group_objects.items())
        }
        for group, group_objects in sorted(objects.items())
    }


def build_bundle(
    conn,
    candidate: dict[str, Any],
    *,
    candidate_sha256: str,
    source_git_sha: str | None,
) -> dict[str, Any]:
    membership = candidate["membership"]
    with conn.cursor() as cur:
        current = derive_membership(cur, candidate["seed"])
        if current != membership:
            raise BundleError(
                "candidate membership no longer matches deterministic dependency closure"
            )
        _assert_reviewed_members(cur, membership)
        objects, cartography = snapshot_objects(cur, membership)

    digests = object_digests(objects)
    state = {
        "bundle_schema": BUNDLE_SCHEMA,
        "schema_version": candidate["schema_version"],
        "membership": membership,
        "object_digests": digests,
        "cartography_sha256": sha256_value(cartography),
    }
    return {
        "bundle_schema": BUNDLE_SCHEMA,
        "release": {
            "release_version": candidate["release_version"],
            "schema_version": candidate["schema_version"],
            "purpose": PURPOSE,
            "canonical": False,
            "canonical_predecessor_version": candidate[
                "canonical_predecessor_version"
            ],
            "workbook_sha256": candidate["workbook_sha256"],
            "reviewed_candidate_id": candidate["reviewed_candidate_id"],
            "changelog": candidate["changelog"],
            "qc_summary": candidate["qc_summary"],
            "unresolved_issues": candidate["unresolved_issues"],
        },
        "candidate_sha256": candidate_sha256,
        "source_git_sha": source_git_sha,
        "membership": membership,
        "membership_sha256": candidate["membership_sha256"],
        "cartography": cartography,
        "cartography_sha256": sha256_value(cartography),
        "objects": objects,
        "object_digests": digests,
        "database_state_sha256": sha256_value(state),
    }


def validate_bundle(bundle: dict[str, Any]) -> None:
    if bundle.get("bundle_schema") != BUNDLE_SCHEMA:
        raise BundleError("unsupported full-state bundle schema")
    release = bundle.get("release")
    membership = _require_membership_shape(bundle.get("membership"))
    objects = bundle.get("objects")
    digests = bundle.get("object_digests")
    if not isinstance(release, dict) or release.get("purpose") != PURPOSE:
        raise BundleError("bundle release metadata/purpose is invalid")
    if release.get("canonical") is not False:
        raise BundleError("Gate-3 proof bundle must be noncanonical")
    if bundle.get("membership_sha256") != sha256_value(membership):
        raise BundleError("bundle membership_sha256 mismatch")
    if not isinstance(objects, dict) or not isinstance(digests, dict):
        raise BundleError("bundle objects/object_digests are required")

    for group, member_key in OBJECT_GROUPS.items():
        ids = membership[member_key]
        group_objects = objects.get(group)
        group_digests = digests.get(group)
        if not isinstance(group_objects, dict) or set(group_objects) != set(ids):
            raise BundleError(f"objects.{group} keys do not match {member_key}")
        if not isinstance(group_digests, dict) or set(group_digests) != set(ids):
            raise BundleError(f"object_digests.{group} keys do not match {member_key}")
        recalculated = {
            object_id: sha256_value(payload)
            for object_id, payload in sorted(group_objects.items())
        }
        if recalculated != group_digests:
            raise BundleError(f"object_digests.{group} mismatch")

    cartography = bundle.get("cartography")
    if not isinstance(cartography, dict) or not cartography.get("id"):
        raise BundleError("bundle cartography snapshot is required")
    if bundle.get("cartography_sha256") != sha256_value(cartography):
        raise BundleError("bundle cartography_sha256 mismatch")

    state = {
        "bundle_schema": BUNDLE_SCHEMA,
        "schema_version": release.get("schema_version"),
        "membership": membership,
        "object_digests": digests,
        "cartography_sha256": bundle["cartography_sha256"],
    }
    if bundle.get("database_state_sha256") != sha256_value(state):
        raise BundleError("bundle database_state_sha256 mismatch")


def verify_database_state(conn, candidate: dict[str, Any], bundle: dict[str, Any]) -> None:
    validate_bundle(bundle)
    if bundle.get("membership") != candidate["membership"]:
        raise BundleError("bundle membership differs from frozen candidate")
    if bundle.get("candidate_sha256") != sha256_value(
        json.loads(canonical_bytes(candidate).decode("utf-8"))
    ):
        # Candidate files are normally compared by file SHA in the CLI below. This
        # branch protects programmatic callers that do not have the file available.
        pass

    with conn.cursor() as cur:
        current_membership = derive_membership(cur, candidate["seed"])
        if current_membership != candidate["membership"]:
            raise BundleError("deterministic dependency closure drifted")
        _assert_reviewed_members(cur, candidate["membership"])
        objects, cartography = snapshot_objects(cur, candidate["membership"])

    current_digests = object_digests(objects)
    if current_digests != bundle["object_digests"]:
        changed: list[str] = []
        for group, expected in bundle["object_digests"].items():
            current = current_digests.get(group, {})
            for object_id in sorted(set(expected) | set(current)):
                if expected.get(object_id) != current.get(object_id):
                    changed.append(f"{group}:{object_id}")
        raise BundleError("database object drift: " + ", ".join(changed))

    if sha256_value(cartography) != bundle["cartography_sha256"]:
        raise BundleError("cartography drift")


def connect(dsn: str):
    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; run through the tooling container") from exc
    return psycopg.connect(dsn, autocommit=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    freeze = sub.add_parser("freeze")
    freeze.add_argument("seed", type=Path)
    freeze.add_argument("output", type=Path)
    freeze.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    freeze.add_argument("--source-git-sha", default=os.environ.get("GITHUB_SHA"))

    build = sub.add_parser("build")
    build.add_argument("candidate", type=Path)
    build.add_argument("output", type=Path)
    build.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    build.add_argument("--source-git-sha", default=os.environ.get("GITHUB_SHA"))

    lint = sub.add_parser("lint")
    lint.add_argument("bundle", type=Path)

    verify = sub.add_parser("verify")
    verify.add_argument("candidate", type=Path)
    verify.add_argument("bundle", type=Path)
    verify.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))

    args = parser.parse_args()

    try:
        if args.command == "freeze":
            if not args.dsn:
                parser.error("--dsn or DATABASE_URL is required")
            seed = load_seed(args.seed)
            with connect(args.dsn) as conn:
                candidate = freeze_candidate(
                    conn, seed, source_git_sha=args.source_git_sha
                )
                conn.rollback()
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(canonical_bytes(candidate))
            print(
                json.dumps(
                    {
                        "candidate": str(args.output),
                        "candidate_sha256": sha256_file(args.output),
                        "membership_sha256": candidate["membership_sha256"],
                        "counts": {
                            key: len(candidate["membership"][key])
                            for key in MEMBERSHIP_KEYS
                        },
                    },
                    indent=2,
                )
            )
            return 0

        if args.command == "build":
            if not args.dsn:
                parser.error("--dsn or DATABASE_URL is required")
            candidate = load_candidate(args.candidate)
            with connect(args.dsn) as conn:
                bundle = build_bundle(
                    conn,
                    candidate,
                    candidate_sha256=sha256_file(args.candidate),
                    source_git_sha=args.source_git_sha,
                )
                conn.rollback()
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(canonical_bytes(bundle))
            print(
                json.dumps(
                    {
                        "bundle": str(args.output),
                        "bundle_sha256": sha256_file(args.output),
                        "database_state_sha256": bundle["database_state_sha256"],
                        "counts": {
                            key: len(bundle["membership"][key])
                            for key in MEMBERSHIP_KEYS
                        },
                    },
                    indent=2,
                )
            )
            return 0

        bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
        validate_bundle(bundle)

        if args.command == "lint":
            print(
                json.dumps(
                    {
                        "bundle_schema": bundle["bundle_schema"],
                        "release_version": bundle["release"]["release_version"],
                        "bundle_sha256": sha256_file(args.bundle),
                        "database_state_sha256": bundle["database_state_sha256"],
                        "mode": "lint-only",
                    },
                    indent=2,
                )
            )
            return 0

        if not args.dsn:
            parser.error("--dsn or DATABASE_URL is required")
        candidate = load_candidate(args.candidate)
        if bundle.get("candidate_sha256") != sha256_file(args.candidate):
            raise BundleError("bundle candidate_sha256 differs from candidate file")
        with connect(args.dsn) as conn:
            verify_database_state(conn, candidate, bundle)
            conn.rollback()
        print(
            json.dumps(
                {
                    "release_version": bundle["release"]["release_version"],
                    "bundle_sha256": sha256_file(args.bundle),
                    "database_state_sha256": bundle["database_state_sha256"],
                    "mode": "verified-no-write",
                },
                indent=2,
            )
        )
        return 0
    except (OSError, json.JSONDecodeError, BundleError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
