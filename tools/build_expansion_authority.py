#!/usr/bin/env python3
"""Freeze an explicit minor-release expansion authority bundle.

The expansion contract is predecessor-union, never "all reviewed rows":

    immutable predecessor authority membership
    + exact selected reviewed claim IDs
    + exact selected reviewed geometry IDs
    + deterministic source/spatial dependency closure for those additions

It does not publish claims, mutate release channels, or infer P-levels.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
from typing import Any

from full_state_release_bundle import (
    BUNDLE_SCHEMA,
    MEMBERSHIP_KEYS,
    canonical_bytes,
    object_digests,
    sha256_file,
    sha256_value,
    snapshot_objects,
    validate_bundle,
)


SELECTION_SCHEMAS = {"historical-slavery-atlas-expansion-selection-v1", "historical-slavery-atlas-expansion-selection-v2"}
PURPOSE = "canonical_research_state_proof"


class ExpansionError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ExpansionError(f"{path} must contain a JSON object")
    return data


def sorted_unique(values) -> list[str]:
    return sorted({str(value) for value in values if value is not None})


def load_selection(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if data.get("selection_schema") not in SELECTION_SCHEMAS:
        raise ExpansionError("unsupported expansion selection schema")
    pred = data.get("predecessor")
    additions = data.get("additions")
    if not isinstance(pred, dict) or not isinstance(additions, dict):
        raise ExpansionError("selection predecessor/additions are required")
    required_keys = [
        "direct_recovery_claim_ids",
        "post_m1_claim_ids",
        "approved_geometry_ids",
    ]
    if data.get("selection_schema") == "historical-slavery-atlas-expansion-selection-v2":
        required_keys.append("reviewed_state_claim_ids")
    for key in required_keys:
        values = additions.get(key)
        if not isinstance(values, list) or values != sorted(set(values)):
            raise ExpansionError(f"additions.{key} must be sorted and unique")
    direct = set(additions["direct_recovery_claim_ids"])
    post_m1 = set(additions["post_m1_claim_ids"])
    reviewed_state = set(additions.get("reviewed_state_claim_ids", []))
    if direct & post_m1 or direct & reviewed_state or post_m1 & reviewed_state:
        raise ExpansionError("expansion claim categories overlap")
    if data.get("selection_schema") == "historical-slavery-atlas-expansion-selection-v1":
        excluded = set((data.get("exclusions") or {}).get("disputed_claim_ids", []))
        if excluded & (direct | post_m1):
            raise ExpansionError("explicitly excluded disputed claims are selected")
    return data


def load_predecessor(selection: dict[str, Any], path: Path) -> dict[str, Any]:
    bundle = load_json(path)
    validate_bundle(bundle)
    pred = selection["predecessor"]
    if pred.get("release_version") != "v0.7.0":
        raise ExpansionError("Atlas Expansion 01 must extend v0.7.0")
    if sha256_file(path) != pred.get("authority_bundle_sha256"):
        raise ExpansionError("predecessor authority SHA-256 mismatch")
    if bundle.get("membership_sha256") != pred.get("membership_sha256"):
        raise ExpansionError("predecessor membership SHA-256 mismatch")
    return bundle


def _rows(cur, query: str, params: tuple[Any, ...]) -> list[tuple]:
    cur.execute(query, params)
    return cur.fetchall()


def derive_addition_closure(
    cur,
    selection: dict[str, Any],
) -> tuple[list[str], list[str], list[str]]:
    additions = selection["additions"]
    direct = additions["direct_recovery_claim_ids"]
    post_m1 = additions["post_m1_claim_ids"]
    reviewed_state = additions.get("reviewed_state_claim_ids", [])
    claim_ids = sorted_unique([*direct, *post_m1, *reviewed_state])
    geometry_ids = additions["approved_geometry_ids"]

    rows = _rows(
        cur,
        """
        select c.claim_id::text,c.review_status::text,c.claim_kind_code,
               tp.spatial_entity_id::text,tp.practice_level,
               tp.classification_status,
               exists(
                 select 1 from atlas.claim_source cs
                 where cs.claim_id=c.claim_id
               ) as has_source
        from atlas.claim c
        left join atlas.territorial_practice_claim tp using(claim_id)
        where c.claim_id=any(%s::uuid[])
        order by c.claim_id
        """,
        (claim_ids,),
    )
    if len(rows) != len(claim_ids):
        found = {str(row[0]) for row in rows}
        raise ExpansionError(
            "selected claims missing from database: "
            + ", ".join(sorted(set(claim_ids) - found))
        )

    post_m1_set = set(post_m1)
    reviewed_state_set = set(reviewed_state)
    spatial_ids: set[str] = set()
    for claim_id, review, kind, spatial_id, practice_level, classification, has_source in rows:
        claim_id = str(claim_id)
        if review != "reviewed":
            raise ExpansionError(f"{claim_id}: review_status={review}")
        if kind != "territorial_practice" or spatial_id is None:
            raise ExpansionError(f"{claim_id}: expansion claim is not territorial practice")
        if not has_source:
            raise ExpansionError(f"{claim_id}: no claim-level source")
        if claim_id in post_m1_set and practice_level is not None:
            raise ExpansionError(f"{claim_id}: post-M1 claim assigns practice_level")
        if claim_id in set(direct) and classification != "reviewed":
            raise ExpansionError(
                f"{claim_id}: direct-recovery classification_status={classification!r}"
            )
        if claim_id in reviewed_state_set and classification not in {
            "disputed",
            "reviewed_with_date_dispute",
        }:
            raise ExpansionError(
                f"{claim_id}: reviewed-state classification_status={classification!r}"
            )
        spatial_ids.add(str(spatial_id))

    geometry_rows = _rows(
        cur,
        """
        select g.geometry_id::text,g.spatial_entity_id::text,
               g.review_status::text,g.accuracy_status::text,
               g.geometry_source_version_id::text,
               g.geom is not null as is_resolved
        from atlas.geometry g
        where g.geometry_id=any(%s::uuid[])
        order by g.geometry_id
        """,
        (geometry_ids,),
    )
    if len(geometry_rows) != len(geometry_ids):
        found = {str(row[0]) for row in geometry_rows}
        raise ExpansionError(
            "selected geometries missing from database: "
            + ", ".join(sorted(set(geometry_ids) - found))
        )
    for geometry_id, spatial_id, review, _accuracy, _source_version_id, is_resolved in geometry_rows:
        if review != "reviewed":
            raise ExpansionError(f"{geometry_id}: geometry is not reviewed")
        if not is_resolved:
            raise ExpansionError(f"{geometry_id}: selected geometry is unresolved")
        if str(spatial_id) not in spatial_ids:
            raise ExpansionError(
                f"{geometry_id}: geometry belongs outside selected added entities"
            )

    if selection.get("selection_schema") == "historical-slavery-atlas-expansion-selection-v1":
        uncovered = _rows(
            cur,
            """
            select c.claim_id::text
            from atlas.claim c
            join atlas.territorial_practice_claim tp using(claim_id)
            where c.claim_id=any(%s::uuid[])
              and not exists (
                select 1 from atlas.geometry g
                where g.geometry_id=any(%s::uuid[])
                  and g.spatial_entity_id=tp.spatial_entity_id
                  and g.review_status='reviewed'
                  and (
                    g.valid_years is null
                    or c.valid_years is null
                    or g.valid_years && c.valid_years
                  )
              )
            order by c.claim_id
            """,
            (claim_ids, geometry_ids),
        )
        if uncovered:
            raise ExpansionError(
                "selected claims lack an overlapping selected reviewed geometry: "
                + ", ".join(str(row[0]) for row in uncovered)
            )
    else:
        orphan_geometries = _rows(
            cur,
            """
            select g.geometry_id::text
            from atlas.geometry g
            where g.geometry_id=any(%s::uuid[])
              and not exists (
                select 1
                from atlas.claim c
                join atlas.territorial_practice_claim tp using(claim_id)
                where c.claim_id=any(%s::uuid[])
                  and tp.spatial_entity_id=g.spatial_entity_id
                  and (
                    g.valid_years is null
                    or c.valid_years is null
                    or g.valid_years && c.valid_years
                  )
              )
            order by g.geometry_id
            """,
            (geometry_ids, claim_ids),
        )
        if orphan_geometries:
            raise ExpansionError(
                "selected geometries lack an overlapping selected claim: "
                + ", ".join(str(row[0]) for row in orphan_geometries)
            )

    source_rows = _rows(
        cur,
        """
        select distinct source_version_id::text
        from (
          select cs.source_version_id
          from atlas.claim_source cs
          where cs.claim_id=any(%s::uuid[])
          union
          select g.geometry_source_version_id
          from atlas.geometry g
          where g.geometry_id=any(%s::uuid[])
            and g.geometry_source_version_id is not null
        ) s
        order by source_version_id
        """,
        (claim_ids, geometry_ids),
    )
    source_ids = [str(row[0]) for row in source_rows]
    return claim_ids, sorted(spatial_ids), source_ids


def build_membership(
    predecessor: dict[str, Any],
    claim_ids: list[str],
    spatial_ids: list[str],
    geometry_ids: list[str],
    source_ids: list[str],
) -> dict[str, list[str]]:
    base = predecessor["membership"]
    membership = {
        key: list(base[key])
        for key in MEMBERSHIP_KEYS
    }
    membership["claim_ids"] = sorted_unique([*membership["claim_ids"], *claim_ids])
    membership["spatial_entity_ids"] = sorted_unique(
        [*membership["spatial_entity_ids"], *spatial_ids]
    )
    membership["geometry_ids"] = sorted_unique(
        [*membership["geometry_ids"], *geometry_ids]
    )
    membership["source_version_ids"] = sorted_unique(
        [*membership["source_version_ids"], *source_ids]
    )
    return membership


def verify_predecessor_objects_preserved(
    predecessor: dict[str, Any],
    objects: dict[str, dict[str, Any]],
) -> None:
    for group, old_objects in predecessor["objects"].items():
        for object_id, expected in old_objects.items():
            if objects[group].get(object_id) != expected:
                raise ExpansionError(
                    f"predecessor object drifted: {group}:{object_id}"
                )


def build_authority(
    conn,
    selection: dict[str, Any],
    predecessor: dict[str, Any],
    *,
    selection_sha256: str,
    source_git_sha: str,
) -> dict[str, Any]:
    with conn.cursor() as cur:
        claim_ids, spatial_ids, source_ids = derive_addition_closure(cur, selection)
        geometry_ids = selection["additions"]["approved_geometry_ids"]
        membership = build_membership(
            predecessor, claim_ids, spatial_ids, geometry_ids, source_ids
        )

        expected = selection.get("expected_counts") or {}
        actual_checks = {
            "candidate_claims": len(membership["claim_ids"]),
            "candidate_spatial_entities": len(membership["spatial_entity_ids"]),
            "candidate_geometries": len(membership["geometry_ids"]),
        }
        for key, actual in actual_checks.items():
            if key in expected and int(expected[key]) != actual:
                raise ExpansionError(
                    f"{key} count mismatch: {actual} != {expected[key]}"
                )

        objects, cartography = snapshot_objects(cur, membership)

    verify_predecessor_objects_preserved(predecessor, objects)
    digests = object_digests(objects)
    cartography_sha = sha256_value(cartography)
    release = {
        "release_version": "v0.8.0-expansion-01-authority-v1",
        "schema_version": "0034",
        "canonical": False,
        "purpose": PURPOSE,
        "canonical_predecessor_version": "v0.7.0",
        "reviewed_candidate_id": "atlas-expansion-01",
        "changelog": (
            "Explicit predecessor-union authority candidate for v0.8.0: "
            "v0.7.0 plus reviewed Atlas Expansion 01 recovery/intake additions."
        ),
        "qc_summary": (
            "Explicit selected claims/geometries only; predecessor objects preserved; "
            "post-M1 P-level assignment rejected; claim completeness and geometry "
            "completeness remain independent; selected geometries are reviewed, resolved "
            "and overlap at least one selected claim."
        ),
        "unresolved_issues": (
            "Independent historical review remains 0. Reviewed disputed/date-disputed "
            "states remain explicit rather than being normalized away. Unreconciled "
            "legacy prototype rows remain excluded. Candidate is not yet canonical or public."
        ),
    }
    state = {
        "bundle_schema": BUNDLE_SCHEMA,
        "schema_version": release["schema_version"],
        "membership": membership,
        "object_digests": digests,
        "cartography_sha256": cartography_sha,
    }
    return {
        "bundle_schema": BUNDLE_SCHEMA,
        "candidate_sha256": selection_sha256,
        "source_git_sha": source_git_sha,
        "release": release,
        "membership": membership,
        "membership_sha256": sha256_value(membership),
        "cartography": cartography,
        "cartography_sha256": cartography_sha,
        "objects": objects,
        "object_digests": digests,
        "database_state_sha256": sha256_value(state),
    }


def verify_live(
    conn,
    selection: dict[str, Any],
    predecessor: dict[str, Any],
    bundle: dict[str, Any],
) -> None:
    validate_bundle(bundle)
    with conn.cursor() as cur:
        claim_ids, spatial_ids, source_ids = derive_addition_closure(cur, selection)
        membership = build_membership(
            predecessor,
            claim_ids,
            spatial_ids,
            selection["additions"]["approved_geometry_ids"],
            source_ids,
        )
        objects, cartography = snapshot_objects(cur, membership)
    if membership != bundle["membership"]:
        raise ExpansionError("live explicit membership differs from frozen authority")
    if object_digests(objects) != bundle["object_digests"]:
        raise ExpansionError("live object state differs from frozen authority")
    if sha256_value(cartography) != bundle["cartography_sha256"]:
        raise ExpansionError("live cartography differs from frozen authority")
    verify_predecessor_objects_preserved(predecessor, objects)



def _sql_literal(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        if not value:
            return "ARRAY[]::uuid[]"
        return "ARRAY[" + ",".join(_sql_literal(str(item)) for item in value) + "]"
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def _bind_sql(query: str, params: tuple[Any, ...]) -> str:
    rendered = query
    for value in params:
        if "%s" not in rendered:
            raise ExpansionError("too many SQL parameters for management query")
        rendered = rendered.replace("%s", _sql_literal(value), 1)
    if "%s" in rendered:
        raise ExpansionError("not enough SQL parameters for management query")
    return rendered


def _management_query(project_ref: str, token: str, query: str) -> Any:
    request = urllib.request.Request(
        f"https://api.supabase.com/v1/projects/{project_ref}/database/query",
        data=json.dumps({"query": query}, separators=(",", ":")).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "historical-slavery-atlas-expansion-authority/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ExpansionError(
            f"Supabase Management API query failed HTTP {exc.code}: {body[:3000]}"
        ) from exc
    except urllib.error.URLError as exc:
        raise ExpansionError(f"Supabase Management API query failed: {exc}") from exc


def _management_rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("result", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    raise ExpansionError(f"unexpected management query response: {type(payload)}")


class ManagementCursor:
    def __init__(self, project_ref: str, token: str):
        self.project_ref = project_ref
        self.token = token
        self._rows: list[tuple[Any, ...]] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query: str, params: tuple[Any, ...] | None = None) -> None:
        rendered = _bind_sql(query, params or ())
        rows = _management_rows(
            _management_query(self.project_ref, self.token, rendered)
        )
        # PostgreSQL/Management API JSON preserves SELECT field order.  Convert each
        # row to the tuple contract used by the existing preservation snapshotter.
        self._rows = [tuple(row.values()) for row in rows]

    def fetchall(self) -> list[tuple[Any, ...]]:
        return list(self._rows)

    def fetchone(self) -> tuple[Any, ...] | None:
        return self._rows[0] if self._rows else None


class ManagementConnection:
    def __init__(self, project_ref: str, token: str):
        self.project_ref = project_ref
        self.token = token

    def cursor(self) -> ManagementCursor:
        return ManagementCursor(self.project_ref, self.token)

    def rollback(self) -> None:
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "verify"):
        cmd = sub.add_parser(name)
        cmd.add_argument("selection", type=Path)
        cmd.add_argument("predecessor_authority", type=Path)
        cmd.add_argument("authority_bundle", type=Path)
        cmd.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
        cmd.add_argument("--project-ref")
        cmd.add_argument(
            "--management-token",
            default=os.environ.get("SUPABASE_MANAGEMENT_TOKEN"),
        )
        cmd.add_argument("--source-git-sha", default=os.environ.get("GITHUB_SHA", "unknown"))

    args = parser.parse_args()
    try:
        selection = load_selection(args.selection)
        predecessor = load_predecessor(selection, args.predecessor_authority)
        if args.dsn:
            import psycopg
            connection = psycopg.connect(args.dsn, autocommit=False)
        elif args.project_ref and args.management_token:
            connection = ManagementConnection(args.project_ref, args.management_token)
        else:
            parser.error(
                "provide --dsn/DATABASE_URL or --project-ref plus "
                "--management-token/SUPABASE_MANAGEMENT_TOKEN"
            )

        with connection as conn:
            if args.command == "build":
                bundle = build_authority(
                    conn,
                    selection,
                    predecessor,
                    selection_sha256=sha256_file(args.selection),
                    source_git_sha=args.source_git_sha,
                )
                validate_bundle(bundle)
                args.authority_bundle.parent.mkdir(parents=True, exist_ok=True)
                args.authority_bundle.write_bytes(canonical_bytes(bundle))
                result = {
                    "authority_bundle": str(args.authority_bundle),
                    "authority_bundle_sha256": sha256_file(args.authority_bundle),
                    "membership_sha256": bundle["membership_sha256"],
                    "database_state_sha256": bundle["database_state_sha256"],
                    "counts": {
                        key: len(value)
                        for key, value in bundle["membership"].items()
                    },
                }
            else:
                bundle = load_json(args.authority_bundle)
                if bundle.get("candidate_sha256") != sha256_file(args.selection):
                    raise ExpansionError("selection SHA-256 differs from frozen authority")
                verify_live(conn, selection, predecessor, bundle)
                result = {
                    "verification": "EXACT_EXPANSION_AUTHORITY_MATCH",
                    "membership_sha256": bundle["membership_sha256"],
                    "database_state_sha256": bundle["database_state_sha256"],
                }
            conn.rollback()

        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ExpansionError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
