#!/usr/bin/env python3
"""Apply an exact reviewed geometry artifact through Supabase Management API.

D-050 production executor: validates the immutable artifact/registry, performs
production preflight checks, and inserts only registry rows marked "promote".
It never regenerates geometry or mutates atlas.geometry.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
from typing import Any

from promote_geometry_artifact import PromotionError, validate_artifact, sha256


def management_query(project_ref: str, token: str, query: str) -> Any:
    url = f"https://api.supabase.com/v1/projects/{project_ref}/database/query"
    request = urllib.request.Request(
        url,
        data=json.dumps({"query": query}, separators=(",", ":")).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "historical-slavery-atlas-geometry-promotion/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise PromotionError(
            f"Supabase Management API query failed HTTP {exc.code}: {body[:2000]}"
        ) from exc
    except urllib.error.URLError as exc:
        raise PromotionError(f"Supabase Management API query failed: {exc}") from exc


def rows_from_response(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("result", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    raise PromotionError(f"unexpected query response shape: {type(payload)}")


def sql_text(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def uuid_sql(value: str) -> str:
    return sql_text(value) + "::uuid"


def ids_for_action(rows: list[dict[str, Any]], action: str) -> list[str]:
    return [str(row["geometry_id"]) for row in rows if row["action"] == action]


def build_preflight_sql(plan: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    artifact = plan["artifact"]
    ids = ",\n    ".join(uuid_sql(str(row["geometry_id"])) for row in rows)
    return f"""
select 'fabric' as kind, fabric_id::text as id,
       content_sha256 as detail1, active::text as detail2
from cartography.land_fabric
where active
union all
select 'policy', policy_id, generator_kind, active::text
from cartography.geometry_render_policy
where policy_id={sql_text(plan["policy_id"])}
union all
select 'source', geometry_id::text, review_status::text, st_npoints(geom)::text
from atlas.geometry
where geometry_id in ({ids})
union all
select 'cache', geometry_id::text, policy_id, st_npoints(geom)::text
from cartography.render_geometry_cache
where fabric_id={sql_text(artifact["land_fabric_id"])}
  and policy_id={sql_text(plan["policy_id"])}
  and geometry_id in ({ids})
order by kind, id
""".strip()


def validate_preflight_rows(
    plan: dict[str, Any],
    rows: list[dict[str, Any]],
    database_rows: list[dict[str, Any]],
) -> None:
    artifact = plan["artifact"]
    fabric = [r for r in database_rows if r.get("kind") == "fabric"]
    if len(fabric) != 1:
        raise PromotionError(f"expected one active land fabric, found {len(fabric)}")
    if fabric[0].get("id") != artifact["land_fabric_id"]:
        raise PromotionError("active land fabric ID differs from reviewed artifact")
    if fabric[0].get("detail1") != artifact["land_sha256"]:
        raise PromotionError("active land fabric SHA-256 differs from reviewed artifact")

    policy = [
        r for r in database_rows
        if r.get("kind") == "policy" and r.get("id") == plan["policy_id"]
    ]
    if len(policy) != 1:
        raise PromotionError(f"render policy {plan['policy_id']} missing")
    if policy[0].get("detail1") != "external" or policy[0].get("detail2") != "true":
        raise PromotionError(f"render policy is not active/external: {policy[0]}")

    sources = {
        str(r["id"]): r for r in database_rows if r.get("kind") == "source"
    }
    caches = {
        str(r["id"]): r for r in database_rows if r.get("kind") == "cache"
    }

    for row in rows:
        gid = str(row["geometry_id"])
        source = sources.get(gid)
        if not source:
            raise PromotionError(f"{gid}: source geometry missing")
        if source.get("detail1") != "reviewed":
            raise PromotionError(f"{gid}: source is not reviewed")
        expected_source_npoints = row["metrics"].get("source_npoints")
        if expected_source_npoints is not None:
            if int(source.get("detail2", -1)) != int(expected_source_npoints):
                raise PromotionError(
                    f"{gid}: source vertex count changed "
                    f"database={source.get('detail2')} artifact={expected_source_npoints}"
                )

        cached = caches.get(gid)
        if row["action"] == "promote" and cached:
            raise PromotionError(f"{gid}: target cache row already exists unexpectedly")
        if row["action"] == "preserve_existing_live" and not cached:
            raise PromotionError(f"{gid}: accepted live cache row is missing")
        if row["action"] == "quarantine" and cached:
            raise PromotionError(f"{gid}: quarantined geometry has target cache row")


def geometry_expression(geometry: dict[str, Any], tag: str) -> str:
    payload = json.dumps(geometry, separators=(",", ":"))
    quoted = "$" + tag + "$" + payload + "$" + tag + "$"
    return "st_setsrid(st_geomfromgeojson(" + quoted + "), 4326)"


def build_apply_sql(
    plan: dict[str, Any],
    manifest: dict[str, Any],
    rows: list[dict[str, Any]],
) -> str:
    artifact = plan["artifact"]
    policy_id = plan["policy_id"]
    promotable = [row for row in rows if row["action"] == "promote"]
    if not promotable:
        raise PromotionError("promotion registry contains no promotable rows")

    checks = [
        f"""if not exists (
            select 1 from cartography.land_fabric
            where active
              and fabric_id={sql_text(artifact["land_fabric_id"])}
              and content_sha256={sql_text(artifact["land_sha256"])}
        ) then
            raise exception 'active land fabric does not match reviewed artifact';
        end if;""",
        f"""if not exists (
            select 1 from cartography.geometry_render_policy
            where policy_id={sql_text(policy_id)}
              and active and generator_kind='external'
        ) then
            raise exception 'render policy is not active external';
        end if;""",
    ]

    for row in rows:
        gid = str(row["geometry_id"])
        source_npoints = int(row["metrics"]["source_npoints"])
        checks.append(
            f"""if not exists (
                select 1 from atlas.geometry
                where geometry_id={uuid_sql(gid)}
                  and review_status='reviewed'
                  and st_npoints(geom)={source_npoints}
            ) then
                raise exception '{gid}: reviewed source geometry/count mismatch';
            end if;"""
        )
        predicate = (
            f"geometry_id={uuid_sql(gid)} "
            f"and fabric_id={sql_text(artifact['land_fabric_id'])} "
            f"and policy_id={sql_text(policy_id)}"
        )
        if row["action"] == "promote":
            checks.append(
                f"""if exists (
                    select 1 from cartography.render_geometry_cache where {predicate}
                ) then
                    raise exception '{gid}: target cache row already exists';
                end if;"""
            )
        elif row["action"] == "preserve_existing_live":
            checks.append(
                f"""if not exists (
                    select 1 from cartography.render_geometry_cache where {predicate}
                ) then
                    raise exception '{gid}: accepted existing live row is missing';
                end if;"""
            )
        elif row["action"] == "quarantine":
            checks.append(
                f"""if exists (
                    select 1 from cartography.render_geometry_cache where {predicate}
                ) then
                    raise exception '{gid}: quarantined geometry has target cache row';
                end if;"""
            )

    statements = [
        "begin;",
        "do $promotion_preflight$\nbegin\n"
        + "\n".join("    " + item.replace("\n", "\n    ") for item in checks)
        + "\nend\n$promotion_preflight$;",
    ]

    smooth_iterations = int(manifest["parameters"]["smooth_iterations"])
    created_at = str(manifest["created_at"])

    for row in promotable:
        gid = str(row["geometry_id"])
        metrics = row["metrics"]
        tag = "geo_" + gid.replace("-", "")[:12]
        geom_expr = geometry_expression(row["geometry"], tag)
        statements.append(
            f"""insert into cartography.render_geometry_cache(
    geometry_id, fabric_id, policy_id, geom,
    source_npoints, render_npoints,
    smoothing_iterations, smoothing_hausdorff_m, smoothing_area_delta_pct,
    coastal_recovery_m_used, coastal_extra_area_pct, generated_at
) values (
    {uuid_sql(gid)},
    {sql_text(artifact["land_fabric_id"])},
    {sql_text(policy_id)},
    {geom_expr},
    {int(metrics["source_npoints"])},
    {int(metrics["render_npoints"])},
    {smooth_iterations},
    {float(metrics["hausdorff_m"])},
    {float(metrics["area_delta_pct"])},
    null, null,
    {sql_text(created_at)}::timestamptz
);"""
        )
        verify_tag = "verify_" + gid.replace("-", "")[:12]
        statements.append(
            f"""do ${verify_tag}$
begin
    if not exists (
        select 1
        from cartography.render_geometry_cache
        where geometry_id={uuid_sql(gid)}
          and fabric_id={sql_text(artifact["land_fabric_id"])}
          and policy_id={sql_text(policy_id)}
          and st_isvalid(geom)
          and st_srid(geom)=4326
          and st_npoints(geom)={int(metrics["render_npoints"])}
          and st_equals(geom, {geom_expr})
    ) then
        raise exception '{gid}: post-insert exact geometry verification failed';
    end if;
end
${verify_tag}$;"""
        )

    ids = ", ".join(uuid_sql(str(row["geometry_id"])) for row in promotable)
    statements.extend(
        [
            "commit;",
            f"""select geometry_id::text as geometry_id,
       policy_id, fabric_id,
       st_isvalid(geom) as valid,
       st_srid(geom) as srid,
       st_npoints(geom) as render_npoints,
       generated_at
from cartography.render_geometry_cache
where policy_id={sql_text(policy_id)}
  and fabric_id={sql_text(artifact["land_fabric_id"])}
  and geometry_id in ({ids})
order by geometry_id;""",
        ]
    )
    return "\n\n".join(statements) + "\n"


def verify_apply_response(
    rows: list[dict[str, Any]],
    response_rows: list[dict[str, Any]],
) -> None:
    expected = {
        str(row["geometry_id"]): int(row["metrics"]["render_npoints"])
        for row in rows if row["action"] == "promote"
    }
    actual = {str(row.get("geometry_id")): row for row in response_rows}
    if set(actual) != set(expected):
        raise PromotionError(
            f"post-apply rows differ: expected={sorted(expected)} actual={sorted(actual)}"
        )
    for gid, npoints in expected.items():
        row = actual[gid]
        if row.get("valid") is not True:
            raise PromotionError(f"{gid}: stored geometry is not valid")
        if int(row.get("srid", -1)) != 4326:
            raise PromotionError(f"{gid}: stored SRID is not 4326")
        if int(row.get("render_npoints", -1)) != npoints:
            raise PromotionError(
                f"{gid}: render_npoints={row.get('render_npoints')} expected={npoints}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("promotion_plan", type=Path)
    parser.add_argument("artifact_dir", type=Path)
    parser.add_argument("--project-ref", required=True)
    parser.add_argument("--token-env", default="SUPABASE_MANAGEMENT_TOKEN")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    token = os.environ.get(args.token_env)
    if not token:
        parser.error(f"missing token environment variable {args.token_env}")

    try:
        plan, manifest, rows = validate_artifact(args.promotion_plan, args.artifact_dir)
        preflight = rows_from_response(
            management_query(
                args.project_ref,
                token,
                build_preflight_sql(plan, rows),
            )
        )
        validate_preflight_rows(plan, rows, preflight)

        result: dict[str, Any] = {
            "schema_version": "geometry-promotion-receipt-v1",
            "promotion_id": plan["promotion_id"],
            "promotion_plan_sha256": sha256(args.promotion_plan),
            "artifact_manifest_sha256": sha256(
                args.artifact_dir / plan["artifact"]["manifest_file"]
            ),
            "artifact_git_sha": manifest["git_sha"],
            "project_ref": args.project_ref,
            "mode": "database-gated dry run",
            "promotable": ids_for_action(rows, "promote"),
            "quarantined": ids_for_action(rows, "quarantine"),
            "preserve_existing_live": ids_for_action(rows, "preserve_existing_live"),
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }

        if args.apply:
            applied = rows_from_response(
                management_query(
                    args.project_ref,
                    token,
                    build_apply_sql(plan, manifest, rows),
                )
            )
            verify_apply_response(rows, applied)
            result["mode"] = "applied"
            result["applied"] = sorted(ids_for_action(rows, "promote"))
            result["database_result"] = applied

        if args.receipt:
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except PromotionError as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
