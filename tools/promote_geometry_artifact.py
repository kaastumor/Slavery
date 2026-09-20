#!/usr/bin/env python3
"""Validate and promote an exact reviewed external geometry artifact.

Dry-run is the default. The tool never regenerates geometry: it verifies the
immutable geometry-build artifact and checked-in acceptance registry, then
optionally inserts only approved features into cartography.render_geometry_cache.

atlas.geometry source rows are read-only in this workflow.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any


class PromotionError(ValueError):
    pass


ALLOWED_PROMOTE_SCOPE = {"accepted_exact", "accepted_polity_context"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PromotionError(f"cannot read JSON {path}: {exc}") from exc


def require_file_hash(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise PromotionError(f"{label} missing: {path}")
    actual = sha256(path)
    if actual != expected:
        raise PromotionError(
            f"{label} SHA-256 mismatch: expected={expected} actual={actual} path={path}"
        )


def basename_records(manifest: dict[str, Any], key: str) -> dict[str, dict[str, Any]]:
    return {
        Path(str(row["path"])).name: row
        for row in manifest.get(key, [])
        if isinstance(row, dict) and row.get("path")
    }


def feature_map(path: Path) -> dict[str, dict[str, Any]]:
    payload = load_json(path)
    if payload.get("type") != "FeatureCollection":
        raise PromotionError(f"{path} is not a GeoJSON FeatureCollection")
    result: dict[str, dict[str, Any]] = {}
    for feature in payload.get("features", []):
        geometry_id = (feature.get("properties") or {}).get("geometry_id")
        if not geometry_id:
            raise PromotionError(f"feature without properties.geometry_id in {path}")
        geometry_id = str(geometry_id)
        if geometry_id in result:
            raise PromotionError(f"duplicate geometry_id {geometry_id} in {path}")
        if not feature.get("geometry"):
            raise PromotionError(f"candidate {geometry_id} has null geometry in {path}")
        result[geometry_id] = feature
    return result


def decision_map(path: Path) -> dict[str, dict[str, Any]]:
    payload = load_json(path)
    result: dict[str, dict[str, Any]] = {}
    for row in payload.get("features", []):
        geometry_id = row.get("geometry_id")
        if not geometry_id:
            continue
        geometry_id = str(geometry_id)
        if geometry_id in result:
            raise PromotionError(f"duplicate decision geometry_id {geometry_id} in {path}")
        result[geometry_id] = row
    return result


def validate_artifact(
    plan_path: Path,
    artifact_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    plan = load_json(plan_path)
    if plan.get("schema_version") != "geometry-promotion-plan-v1":
        raise PromotionError("unsupported promotion-plan schema")

    artifact = plan.get("artifact") or {}
    manifest_path = artifact_dir / str(artifact.get("manifest_file", "artifact_manifest.json"))
    require_file_hash(
        manifest_path,
        str(artifact.get("manifest_sha256", "")),
        "artifact manifest",
    )
    manifest = load_json(manifest_path)

    if manifest.get("schema_version") != "atlas-artifact-manifest-v1":
        raise PromotionError("unsupported artifact-manifest schema")
    if manifest.get("artifact_kind") != "geometry-render-candidate":
        raise PromotionError("artifact is not a geometry-render-candidate")
    if manifest.get("git_sha") != artifact.get("git_sha"):
        raise PromotionError("artifact Git SHA does not match promotion registry")

    metadata = manifest.get("metadata") or {}
    if metadata.get("land_fabric") != artifact.get("land_fabric_id"):
        raise PromotionError("land fabric ID differs between artifact and promotion registry")
    if metadata.get("land_sha256") != artifact.get("land_sha256"):
        raise PromotionError("land fabric SHA differs between artifact and promotion registry")

    parameters = manifest.get("parameters") or {}
    if parameters != artifact.get("parameters"):
        raise PromotionError(
            f"render parameters differ: manifest={parameters} registry={artifact.get('parameters')}"
        )

    manifest_artifacts = basename_records(manifest, "artifacts")
    manifest_qc = basename_records(manifest, "qc")
    plan_files = artifact.get("files") or {}

    for filename, expected_hash in plan_files.items():
        file_path = artifact_dir / filename
        require_file_hash(file_path, str(expected_hash), filename)
        record = manifest_artifacts.get(filename) or manifest_qc.get(filename)
        if record is None:
            raise PromotionError(f"{filename} is not recorded in artifact manifest")
        if record.get("sha256") != expected_hash:
            raise PromotionError(f"manifest SHA differs from registry for {filename}")

    candidate_cache: dict[str, dict[str, dict[str, Any]]] = {}
    decision_cache: dict[str, dict[str, dict[str, Any]]] = {}
    results: list[dict[str, Any]] = []

    for item in plan.get("features", []):
        geometry_id = str(item.get("geometry_id", ""))
        action = item.get("action")
        candidate_name = str(item.get("artifact_file", ""))
        decision_name = str(item.get("decision_file", ""))

        if not geometry_id or action not in {
            "promote",
            "quarantine",
            "preserve_existing_live",
        }:
            raise PromotionError(f"invalid feature entry: {item}")

        if candidate_name not in candidate_cache:
            candidate_cache[candidate_name] = feature_map(artifact_dir / candidate_name)
        if decision_name not in decision_cache:
            decision_cache[decision_name] = decision_map(artifact_dir / decision_name)

        candidate = candidate_cache[candidate_name].get(geometry_id)
        decision = decision_cache[decision_name].get(geometry_id)
        if candidate is None:
            raise PromotionError(f"{geometry_id}: candidate missing from {candidate_name}")
        if decision is None:
            raise PromotionError(f"{geometry_id}: QC decision missing from {decision_name}")

        actual_qc = decision.get("status")
        if actual_qc != item.get("qc_status"):
            raise PromotionError(
                f"{geometry_id}: registry qc_status={item.get('qc_status')} "
                f"but decision={actual_qc}"
            )

        if action == "promote":
            if actual_qc != "qc_passed":
                raise PromotionError(f"{geometry_id}: non-passing QC cannot be promoted")
            if item.get("visual_status") != "visually_accepted_candidate":
                raise PromotionError(f"{geometry_id}: visual acceptance is required")
            if item.get("semantic_scope_status") not in ALLOWED_PROMOTE_SCOPE:
                raise PromotionError(f"{geometry_id}: semantic scope is not accepted")
        elif action == "quarantine":
            if actual_qc != "quarantined":
                raise PromotionError(
                    f"{geometry_id}: quarantine action requires quarantined QC state"
                )
        elif action == "preserve_existing_live":
            if item.get("semantic_scope_status") != "accepted_existing_live":
                raise PromotionError(
                    f"{geometry_id}: preserve_existing_live requires accepted_existing_live"
                )

        metrics = decision.get("metrics") or {}
        results.append(
            {
                "geometry_id": geometry_id,
                "name": item.get("name"),
                "action": action,
                "artifact_file": candidate_name,
                "artifact_file_sha256": plan_files[candidate_name],
                "decision_file": decision_name,
                "decision_file_sha256": plan_files[decision_name],
                "semantic_scope_status": item.get("semantic_scope_status"),
                "semantic_scope_note": item.get("semantic_scope_note"),
                "geometry": candidate["geometry"],
                "metrics": metrics,
            }
        )

    return plan, manifest, results


def inspect_database(
    conn: Any,
    plan: dict[str, Any],
    manifest: dict[str, Any],
    rows: list[dict[str, Any]],
) -> list[str]:
    problems: list[str] = []
    policy_id = plan["policy_id"]
    artifact = plan["artifact"]

    with conn.cursor() as cur:
        cur.execute(
            """
            select fabric_id, content_sha256
            from cartography.land_fabric
            where active
            order by created_at desc
            limit 1
            """
        )
        fabric = cur.fetchone()
        if not fabric:
            problems.append("no active land fabric")
        else:
            if fabric[0] != artifact["land_fabric_id"]:
                problems.append(
                    f"active fabric ID={fabric[0]} expected={artifact['land_fabric_id']}"
                )
            if fabric[1] != artifact["land_sha256"]:
                problems.append("active land fabric SHA-256 differs from reviewed artifact")

        cur.execute(
            """
            select active, generator_kind
            from cartography.geometry_render_policy
            where policy_id=%s
            """,
            (policy_id,),
        )
        policy = cur.fetchone()
        if not policy:
            problems.append(f"render policy {policy_id} does not exist")
        elif not policy[0] or policy[1] != "external":
            problems.append(
                f"render policy {policy_id} must be active external; "
                f"active={policy[0]} generator_kind={policy[1]}"
            )

        for row in rows:
            geometry_id = row["geometry_id"]
            action = row["action"]

            cur.execute(
                """
                select review_status::text, st_npoints(geom)
                from atlas.geometry
                where geometry_id=%s::uuid
                """,
                (geometry_id,),
            )
            source = cur.fetchone()
            if not source:
                problems.append(f"{geometry_id}: source geometry missing")
                continue
            if source[0] != "reviewed":
                problems.append(
                    f"{geometry_id}: source review_status={source[0]}, expected reviewed"
                )

            source_npoints = row["metrics"].get("source_npoints")
            if source_npoints is not None and int(source[1]) != int(source_npoints):
                problems.append(
                    f"{geometry_id}: source vertex count changed "
                    f"database={source[1]} artifact={source_npoints}"
                )

            cur.execute(
                """
                select source_npoints, render_npoints
                from cartography.render_geometry_cache
                where geometry_id=%s::uuid
                  and fabric_id=%s
                  and policy_id=%s
                """,
                (geometry_id, artifact["land_fabric_id"], policy_id),
            )
            cached = cur.fetchone()

            if action == "promote" and cached:
                problems.append(
                    f"{geometry_id}: target external cache row already exists unexpectedly"
                )
            elif action == "preserve_existing_live" and not cached:
                problems.append(
                    f"{geometry_id}: expected accepted live cache row is missing"
                )
            elif action == "quarantine" and cached:
                problems.append(
                    f"{geometry_id}: quarantined geometry already has external cache row"
                )

    return problems


def apply_promotions(
    conn: Any,
    plan: dict[str, Any],
    manifest: dict[str, Any],
    rows: list[dict[str, Any]],
) -> list[str]:
    inserted: list[str] = []
    artifact = plan["artifact"]
    policy_id = plan["policy_id"]
    smooth_iterations = int(manifest["parameters"]["smooth_iterations"])

    with conn.cursor() as cur:
        for row in rows:
            if row["action"] != "promote":
                continue
            metrics = row["metrics"]
            geometry_json = json.dumps(row["geometry"], separators=(",", ":"))

            cur.execute(
                """
                insert into cartography.render_geometry_cache(
                    geometry_id,
                    fabric_id,
                    policy_id,
                    geom,
                    source_npoints,
                    render_npoints,
                    smoothing_iterations,
                    smoothing_hausdorff_m,
                    smoothing_area_delta_pct,
                    coastal_recovery_m_used,
                    coastal_extra_area_pct,
                    generated_at
                ) values (
                    %s::uuid,
                    %s,
                    %s,
                    st_setsrid(st_geomfromgeojson(%s), 4326),
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    null,
                    null,
                    %s::timestamptz
                )
                """,
                (
                    row["geometry_id"],
                    artifact["land_fabric_id"],
                    policy_id,
                    geometry_json,
                    int(metrics["source_npoints"]),
                    int(metrics["render_npoints"]),
                    smooth_iterations,
                    float(metrics["hausdorff_m"]),
                    float(metrics["area_delta_pct"]),
                    manifest["created_at"],
                ),
            )

            cur.execute(
                """
                select
                    st_isvalid(c.geom),
                    st_srid(c.geom),
                    st_npoints(c.geom),
                    st_equals(
                        c.geom,
                        st_setsrid(st_geomfromgeojson(%s), 4326)
                    )
                from cartography.render_geometry_cache c
                where c.geometry_id=%s::uuid
                  and c.fabric_id=%s
                  and c.policy_id=%s
                """,
                (
                    geometry_json,
                    row["geometry_id"],
                    artifact["land_fabric_id"],
                    policy_id,
                ),
            )
            verified = cur.fetchone()
            if not verified or verified != (
                True,
                4326,
                int(metrics["render_npoints"]),
                True,
            ):
                raise PromotionError(
                    f"{row['geometry_id']}: post-insert geometry verification failed: {verified}"
                )
            inserted.append(row["geometry_id"])

    return inserted


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("promotion_plan", type=Path)
    parser.add_argument("artifact_dir", type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        plan, manifest, rows = validate_artifact(args.promotion_plan, args.artifact_dir)
    except PromotionError as exc:
        raise SystemExit(f"BLOCK: {exc}") from exc

    promotable = [row for row in rows if row["action"] == "promote"]
    quarantined = [row for row in rows if row["action"] == "quarantine"]
    preserved = [row for row in rows if row["action"] == "preserve_existing_live"]

    result: dict[str, Any] = {
        "promotion_id": plan["promotion_id"],
        "mode": "artifact-only dry run",
        "promotion_plan_sha256": sha256(args.promotion_plan),
        "artifact_manifest_sha256": sha256(
            args.artifact_dir / plan["artifact"]["manifest_file"]
        ),
        "artifact_git_sha": manifest["git_sha"],
        "promotable": [row["geometry_id"] for row in promotable],
        "quarantined": [row["geometry_id"] for row in quarantined],
        "preserve_existing_live": [row["geometry_id"] for row in preserved],
    }

    if not args.dsn:
        if args.apply:
            parser.error("--dsn or DATABASE_URL is required with --apply")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required when --dsn/DATABASE_URL is supplied") from exc

    with psycopg.connect(args.dsn, autocommit=False) as conn:
        problems = inspect_database(conn, plan, manifest, rows)
        if problems:
            conn.rollback()
            for problem in problems:
                print(f"BLOCK: {problem}", file=sys.stderr)
            return 2

        result["mode"] = "database-gated dry run"
        if not args.apply:
            conn.rollback()
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0

        try:
            inserted = apply_promotions(conn, plan, manifest, rows)
            conn.commit()
        except Exception:
            conn.rollback()
            raise

        result["mode"] = "applied"
        result["inserted"] = inserted

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
