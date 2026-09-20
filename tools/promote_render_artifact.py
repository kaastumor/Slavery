#!/usr/bin/env python3
"""Validate and promote an approved external geometry render artifact.

Dry-run is the default. Promotion is intentionally separate from geometry
generation: this tool consumes an already-built, checksummed candidate artifact
and an explicit visual-approval manifest. It never recomputes geometry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any


APPROVAL_SCHEMA = "geometry-render-approval-v1"


class PromotionError(ValueError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PromotionError(f"could not read {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PromotionError(f"{path}: top-level JSON must be an object")
    return payload


def record_for_basename(records: list[dict[str, Any]], filename: str) -> dict[str, Any]:
    matches = [
        row
        for row in records
        if Path(str(row.get("path", ""))).name == filename
    ]
    if len(matches) != 1:
        raise PromotionError(
            f"manifest must contain exactly one record for {filename}; found {len(matches)}"
        )
    return matches[0]


def feature_id(feature: dict[str, Any]) -> str:
    props = feature.get("properties") or {}
    value = props.get("geometry_id")
    if value in (None, ""):
        raise PromotionError("every candidate feature needs properties.geometry_id")
    return str(value)


def validate_package(
    candidate_path: Path,
    decision_path: Path,
    artifact_manifest_path: Path,
    approval_path: Path,
) -> dict[str, Any]:
    candidate = load_json(candidate_path)
    decision = load_json(decision_path)
    artifact = load_json(artifact_manifest_path)
    approval = load_json(approval_path)

    if candidate.get("type") != "FeatureCollection":
        raise PromotionError("candidate must be a GeoJSON FeatureCollection")
    if approval.get("schema_version") != APPROVAL_SCHEMA:
        raise PromotionError(
            f"approval schema must be {APPROVAL_SCHEMA}"
        )
    if approval.get("visual_review_status") != "accepted":
        raise PromotionError("visual_review_status must be accepted")
    if not approval.get("reviewed_by") or not approval.get("reviewed_at"):
        raise PromotionError("reviewed_by and reviewed_at are required")

    candidate_record = record_for_basename(
        artifact.get("artifacts") or [], candidate_path.name
    )
    decision_record = record_for_basename(
        artifact.get("qc") or [], decision_path.name
    )

    actual_candidate_sha = sha256(candidate_path)
    actual_decision_sha = sha256(decision_path)
    expected_candidate_sha = str(approval.get("candidate_sha256") or "")
    expected_decision_sha = str(approval.get("decision_sha256") or "")

    for label, actual, manifest_value, approval_value in [
        (
            "candidate",
            actual_candidate_sha,
            str(candidate_record.get("sha256") or ""),
            expected_candidate_sha,
        ),
        (
            "decision",
            actual_decision_sha,
            str(decision_record.get("sha256") or ""),
            expected_decision_sha,
        ),
    ]:
        if not approval_value:
            raise PromotionError(f"approval missing {label}_sha256")
        if actual != manifest_value or actual != approval_value:
            raise PromotionError(
                f"{label} checksum mismatch: actual={actual} "
                f"artifact_manifest={manifest_value} approval={approval_value}"
            )

    build_git_sha = str(approval.get("build_git_sha") or "")
    if not build_git_sha or build_git_sha != str(artifact.get("git_sha") or ""):
        raise PromotionError("approval build_git_sha does not match artifact manifest")

    policy_id = str(approval.get("policy_id") or "")
    if not policy_id or policy_id != str(decision.get("policy_id") or ""):
        raise PromotionError("approval policy_id does not match QC decision")

    fabric_id = str(approval.get("fabric_id") or "")
    if not fabric_id or fabric_id != str((artifact.get("metadata") or {}).get("land_fabric") or ""):
        raise PromotionError("approval fabric_id does not match artifact manifest")

    tolerance = int(approval.get("snap_tolerance_m"))
    manifest_tolerance = int((artifact.get("parameters") or {}).get("snap_tolerance_m"))
    if tolerance != manifest_tolerance:
        raise PromotionError("approval snap_tolerance_m does not match artifact manifest")

    selection = decision.get("candidate_selection") or {}
    role = selection.get("selection_role")
    preferred = selection.get("preferred_snap_tolerance_m")
    allow_alternate = bool(approval.get("allow_alternate_tolerance", False))
    if role != "preferred_baseline" and not allow_alternate:
        raise PromotionError(
            f"candidate selection role is {role!r}; explicit alternate approval required"
        )
    if preferred is not None and role == "preferred_baseline" and tolerance != int(preferred):
        raise PromotionError("preferred-baseline decision has inconsistent tolerance")

    features = candidate.get("features") or []
    candidate_by_id: dict[str, dict[str, Any]] = {}
    for feature in features:
        gid = feature_id(feature)
        if gid in candidate_by_id:
            raise PromotionError(f"duplicate geometry_id in candidate: {gid}")
        candidate_by_id[gid] = feature

    decisions = {
        str(row.get("geometry_id")): row
        for row in (decision.get("features") or [])
    }

    approved = [str(v) for v in (approval.get("approved_geometry_ids") or [])]
    quarantined = [str(v) for v in (approval.get("quarantined_geometry_ids") or [])]
    if not approved:
        raise PromotionError("approved_geometry_ids must not be empty")
    if len(approved) != len(set(approved)) or len(quarantined) != len(set(quarantined)):
        raise PromotionError("approval geometry id lists must not contain duplicates")
    overlap = sorted(set(approved) & set(quarantined))
    if overlap:
        raise PromotionError("geometry ids cannot be both approved and quarantined: " + ", ".join(overlap))

    classified = set(approved) | set(quarantined)
    unclassified = sorted(set(candidate_by_id) - classified)
    missing = sorted(classified - set(candidate_by_id))
    if unclassified:
        raise PromotionError(
            "every candidate geometry must be explicitly approved or quarantined: "
            + ", ".join(unclassified)
        )
    if missing:
        raise PromotionError(
            "approval references geometry ids absent from candidate: " + ", ".join(missing)
        )

    for gid in approved:
        row = decisions.get(gid)
        if not row:
            raise PromotionError(f"approved geometry {gid} has no QC decision")
        if row.get("status") != "qc_passed":
            raise PromotionError(
                f"approved geometry {gid} has QC status {row.get('status')!r}"
            )
        if not (candidate_by_id[gid].get("geometry")):
            raise PromotionError(f"approved geometry {gid} has no geometry")

    for gid in quarantined:
        row = decisions.get(gid)
        if not row:
            raise PromotionError(f"quarantined geometry {gid} has no QC decision")
        if row.get("status") != "quarantined":
            raise PromotionError(
                f"approval quarantines {gid}, but QC status is {row.get('status')!r}"
            )

    return {
        "candidate": candidate,
        "candidate_by_id": candidate_by_id,
        "decisions": decisions,
        "approval": approval,
        "artifact": artifact,
        "approved_ids": approved,
        "quarantined_ids": quarantined,
        "policy_id": policy_id,
        "fabric_id": fabric_id,
        "snap_tolerance_m": tolerance,
        "candidate_sha256": actual_candidate_sha,
        "decision_sha256": actual_decision_sha,
        "build_git_sha": build_git_sha,
    }


def inspect_database(cur, package: dict[str, Any], replace_existing: bool) -> list[str]:
    problems: list[str] = []

    cur.execute(
        """
        select active
        from cartography.land_fabric
        where fabric_id=%s
        """,
        (package["fabric_id"],),
    )
    row = cur.fetchone()
    if row is None:
        problems.append(f"unknown land fabric: {package['fabric_id']}")
    elif not row[0]:
        problems.append(f"land fabric is not active: {package['fabric_id']}")

    cur.execute(
        """
        select active, generator_kind
        from cartography.geometry_render_policy
        where policy_id=%s
        """,
        (package["policy_id"],),
    )
    row = cur.fetchone()
    if row is None:
        problems.append(f"unknown render policy: {package['policy_id']}")
    else:
        if not row[0]:
            problems.append(f"render policy is not active: {package['policy_id']}")
        if row[1] != "external":
            problems.append(
                f"render policy generator_kind={row[1]!r}, expected 'external'"
            )

    ids = package["approved_ids"]
    cur.execute(
        """
        select g.geometry_id::text, st_npoints(g.geom)
        from atlas.geometry g
        where g.geometry_id=any(%s::uuid[])
        order by g.geometry_id
        """,
        (ids,),
    )
    source_npoints = {gid: npoints for gid, npoints in cur.fetchall()}
    for gid in ids:
        if gid not in source_npoints:
            problems.append(f"approved geometry not found in atlas.geometry: {gid}")
            continue
        expected = package["decisions"][gid].get("metrics", {}).get("source_npoints")
        if expected is not None and int(expected) != int(source_npoints[gid]):
            problems.append(
                f"{gid}: source_npoints changed since build "
                f"({source_npoints[gid]} live vs {expected} artifact)"
            )

    cur.execute(
        """
        select geometry_id::text
        from cartography.render_geometry_cache
        where fabric_id=%s
          and policy_id=%s
          and geometry_id=any(%s::uuid[])
        order by geometry_id
        """,
        (package["fabric_id"], package["policy_id"], ids),
    )
    existing = [row[0] for row in cur.fetchall()]
    if existing and not replace_existing:
        problems.append(
            "approved render already exists; replacement requires --replace-existing: "
            + ", ".join(existing)
        )

    return problems


def write_rows(cur, package: dict[str, Any], replace_existing: bool) -> None:
    manifest_parameters = package["artifact"].get("parameters") or {}
    smoothing_iterations = int(manifest_parameters.get("smooth_iterations", 0))

    for gid in package["approved_ids"]:
        feature = package["candidate_by_id"][gid]
        metrics = package["decisions"][gid].get("metrics") or {}
        geometry_json = json.dumps(feature["geometry"], separators=(",", ":"))

        sql = """
            insert into cartography.render_geometry_cache(
                geometry_id, fabric_id, policy_id, geom,
                source_npoints, render_npoints, smoothing_iterations,
                smoothing_hausdorff_m, smoothing_area_delta_pct,
                coastal_recovery_m_used, coastal_extra_area_pct, generated_at
            ) values (
                %s::uuid, %s, %s,
                st_setsrid(st_geomfromgeojson(%s), 4326),
                %s, %s, %s, %s, %s, null, null, now()
            )
        """
        params = (
            gid,
            package["fabric_id"],
            package["policy_id"],
            geometry_json,
            int(metrics["source_npoints"]),
            int(metrics["render_npoints"]),
            smoothing_iterations,
            float(metrics["hausdorff_m"]),
            float(metrics["area_delta_pct"]),
        )
        if replace_existing:
            sql += """
                on conflict (geometry_id, fabric_id, policy_id)
                do update set
                    geom=excluded.geom,
                    source_npoints=excluded.source_npoints,
                    render_npoints=excluded.render_npoints,
                    smoothing_iterations=excluded.smoothing_iterations,
                    smoothing_hausdorff_m=excluded.smoothing_hausdorff_m,
                    smoothing_area_delta_pct=excluded.smoothing_area_delta_pct,
                    coastal_recovery_m_used=null,
                    coastal_extra_area_pct=null,
                    generated_at=excluded.generated_at
            """
        cur.execute(sql, params)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("decision", type=Path)
    parser.add_argument("artifact_manifest", type=Path)
    parser.add_argument("approval", type=Path)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--replace-existing", action="store_true")
    args = parser.parse_args()

    try:
        package = validate_package(
            args.candidate,
            args.decision,
            args.artifact_manifest,
            args.approval,
        )
    except PromotionError as exc:
        raise SystemExit(f"invalid geometry promotion package: {exc}") from exc

    summary = {
        "policy_id": package["policy_id"],
        "fabric_id": package["fabric_id"],
        "snap_tolerance_m": package["snap_tolerance_m"],
        "build_git_sha": package["build_git_sha"],
        "candidate_sha256": package["candidate_sha256"],
        "approved_count": len(package["approved_ids"]),
        "quarantined_count": len(package["quarantined_ids"]),
        "mode": "package-only dry run" if not args.dsn else "database dry run",
    }

    if not args.dsn:
        if args.apply:
            parser.error("--dsn or DATABASE_URL is required with --apply")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; install requirements.txt") from exc

    with psycopg.connect(args.dsn, autocommit=False) as conn:
        with conn.cursor() as cur:
            problems = inspect_database(cur, package, args.replace_existing)
        if problems:
            for problem in problems:
                print(f"BLOCK: {problem}", file=sys.stderr)
            conn.rollback()
            return 2

        print(
            f"READY: {len(package['approved_ids'])} render geometries pass the promotion gate"
        )
        if not args.apply:
            conn.rollback()
            print("DRY RUN: no database changes made")
            return 0

        try:
            with conn.transaction():
                with conn.cursor() as cur:
                    write_rows(cur, package, args.replace_existing)
                    problems = inspect_database(cur, package, True)
                    if problems:
                        raise PromotionError("; ".join(problems))
        except Exception:
            conn.rollback()
            raise

    summary["mode"] = "applied"
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
