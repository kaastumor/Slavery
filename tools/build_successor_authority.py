#!/usr/bin/env python3
"""Freeze an explicit successor authority from a reviewed v0.8.2-style selection.

The successor is predecessor-union only:

    immutable predecessor authority membership
    + exact selected reviewed claim additions
    + exact bounded predecessor-object augmentations named by the selection
    + deterministic source/spatial dependency closure for only those additions

The tool does not publish a canonical release, move a serving channel, infer
practice levels, or discover membership from "all reviewed rows".
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

from build_expansion_authority import ManagementConnection
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

SELECTION_SCHEMA = "historical-slavery-atlas-successor-claim-selection-v1"
PURPOSE = "canonical_research_state_proof"


class SuccessorAuthorityError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SuccessorAuthorityError(f"{path} must contain a JSON object")
    return data


def sorted_unique(values) -> list[str]:
    return sorted({str(value) for value in values if value is not None})


def load_selection(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if data.get("selection_schema") != SELECTION_SCHEMA:
        raise SuccessorAuthorityError("unsupported successor selection schema")
    if data.get("status") != "RELEASE_READY_PENDING_AUTHORITY_FREEZE":
        raise SuccessorAuthorityError("selection is not ready for authority freeze")
    if data.get("release_ready") is not True or data.get("release_blockers") != []:
        raise SuccessorAuthorityError("selection still has release blockers")

    predecessor = data.get("canonical_predecessor")
    if not isinstance(predecessor, dict) or predecessor.get("version") != "v0.8.1":
        raise SuccessorAuthorityError("successor must explicitly extend v0.8.1")

    additions = data.get("claim_additions")
    if not isinstance(additions, list) or not additions:
        raise SuccessorAuthorityError("claim_additions are required")
    claim_ids = [str(row.get("claim_id")) for row in additions]
    spatial_ids = [str(row.get("spatial_entity_id")) for row in additions]
    if len(set(claim_ids)) != len(claim_ids):
        raise SuccessorAuthorityError("claim additions must be unique")
    if len(set(spatial_ids)) != len(spatial_ids):
        raise SuccessorAuthorityError("claim target spatial entities must be unique")

    geometry_policy = data.get("geometry_policy")
    if not isinstance(geometry_policy, dict):
        raise SuccessorAuthorityError("geometry_policy is required")
    if geometry_policy.get("new_practice_extent_geometry_ids") != []:
        raise SuccessorAuthorityError(
            "successor must not add practice-extent geometry implicitly"
        )
    if geometry_policy.get("claim_completeness_independent_of_geometry") is not True:
        raise SuccessorAuthorityError(
            "claim completeness must remain independent of geometry"
        )
    if geometry_policy.get("modern_country_proxy_as_practice_extent_forbidden") is not True:
        raise SuccessorAuthorityError("modern country proxy practice extent is not forbidden")
    if geometry_policy.get("inherited_geometry_reuse_status") != (
        "CLEARED_BY_D120_SUCCESSOR_REVIEW"
    ):
        raise SuccessorAuthorityError("D-120 successor geometry review is not cleared")

    correction = data.get("predecessor_object_correction_required")
    if not isinstance(correction, dict):
        raise SuccessorAuthorityError("bounded predecessor-object correction is required")
    if correction.get("disposition") != (
        "INCLUDE_AS_EXPLICIT_BOUNDED_SUCCESSOR_AUGMENTATION"
    ):
        raise SuccessorAuthorityError("predecessor correction has no accepted disposition")
    if correction.get("semantic_scope") != (
        "claim_evidence_locus_only_not_territorial_extent"
    ):
        raise SuccessorAuthorityError("predecessor correction scope is not bounded")
    loci = correction.get("current_evidence_loci")
    if not isinstance(loci, list) or len(loci) != 2:
        raise SuccessorAuthorityError("expected exactly two evidence-locus records")
    if sorted_unique(row.get("spatial_entity_id") for row in loci) != sorted_unique(
        correction.get("add_spatial_entity_ids") or []
    ):
        raise SuccessorAuthorityError("locus spatial IDs differ from correction additions")
    if sorted_unique(row.get("geometry_id") for row in loci) != sorted_unique(
        correction.get("add_geometry_ids") or []
    ):
        raise SuccessorAuthorityError("locus geometry IDs differ from correction additions")
    if any(row.get("role") != "evidence_locus_only" for row in loci):
        raise SuccessorAuthorityError("Mycenaean additions are not evidence-locus-only")

    rules = data.get("rules") or {}
    for key in (
        "explicit_membership_only",
        "reviewed_row_discovery_forbidden",
        "no_new_p_level",
        "unresolved_geometry_not_absence",
        "prior_release_immutable",
        "source_dependency_closure_required_at_authority_freeze",
        "mycenaean_locus_augmentation_explicit",
    ):
        if rules.get(key) is not True:
            raise SuccessorAuthorityError(f"selection rule {key} is not asserted")
    return data


def load_predecessor(selection: dict[str, Any], path: Path) -> dict[str, Any]:
    bundle = load_json(path)
    validate_bundle(bundle)
    predecessor = selection["canonical_predecessor"]
    if bundle["release"].get("release_version") != (
        "v0.8.1-rome-geometry-authority-v1"
    ):
        raise SuccessorAuthorityError("unexpected predecessor authority version")
    if sha256_file(path) != predecessor.get("authority_bundle_sha256"):
        raise SuccessorAuthorityError("predecessor authority SHA-256 mismatch")
    if bundle.get("membership_sha256") != predecessor.get("membership_sha256"):
        raise SuccessorAuthorityError("predecessor membership SHA-256 mismatch")
    if bundle.get("database_state_sha256") != predecessor.get("database_state_sha256"):
        raise SuccessorAuthorityError("predecessor database-state SHA-256 mismatch")
    return bundle


def _rows(cur, query: str, params: tuple[Any, ...]) -> list[tuple]:
    cur.execute(query, params)
    return cur.fetchall()


def derive_successor_membership(
    cur,
    selection: dict[str, Any],
    predecessor: dict[str, Any],
) -> dict[str, list[str]]:
    additions = selection["claim_additions"]
    claim_ids = sorted_unique(row["claim_id"] for row in additions)
    expected_targets = {
        str(row["claim_id"]): str(row["spatial_entity_id"]) for row in additions
    }

    rows = _rows(
        cur,
        """
        select c.claim_id::text,
               c.review_status::text,
               c.claim_kind_code,
               c.publication_status::text,
               tp.spatial_entity_id::text,
               tp.practice_level,
               tp.classification_status,
               exists (
                 select 1 from atlas.claim_source cs where cs.claim_id=c.claim_id
               ) as has_source
        from atlas.claim c
        join atlas.territorial_practice_claim tp using(claim_id)
        where c.claim_id=any(%s::uuid[])
        order by c.claim_id
        """,
        (claim_ids,),
    )
    if len(rows) != len(claim_ids):
        found = {str(row[0]) for row in rows}
        raise SuccessorAuthorityError(
            "selected claims missing from database: "
            + ", ".join(sorted(set(claim_ids) - found))
        )

    selected_spatial_ids: set[str] = set()
    for (
        claim_id,
        review_status,
        claim_kind,
        publication_status,
        spatial_id,
        practice_level,
        classification_status,
        has_source,
    ) in rows:
        claim_id = str(claim_id)
        spatial_id = str(spatial_id)
        if review_status != "reviewed":
            raise SuccessorAuthorityError(f"{claim_id}: not reviewed")
        if claim_kind != "territorial_practice":
            raise SuccessorAuthorityError(f"{claim_id}: wrong claim kind {claim_kind}")
        if publication_status != "unpublished":
            raise SuccessorAuthorityError(
                f"{claim_id}: expected unpublished research state, got {publication_status}"
            )
        if spatial_id != expected_targets[claim_id]:
            raise SuccessorAuthorityError(f"{claim_id}: spatial target drifted {spatial_id}")
        if practice_level is not None:
            raise SuccessorAuthorityError(
                f"{claim_id}: post-M1 successor assigns practice_level"
            )
        if not str(classification_status).startswith("reviewed_"):
            raise SuccessorAuthorityError(
                f"{claim_id}: classification_status={classification_status!r}"
            )
        if not has_source:
            raise SuccessorAuthorityError(f"{claim_id}: no claim-level source")
        selected_spatial_ids.add(spatial_id)

    correction = selection["predecessor_object_correction_required"]
    correction_claim_id = str(correction["claim_id"])
    expected_loci = {
        (str(row["spatial_entity_id"]), str(row["geometry_id"]))
        for row in correction["current_evidence_loci"]
    }
    add_locus_spatial_ids = sorted_unique(
        row["spatial_entity_id"] for row in correction["current_evidence_loci"]
    )
    add_locus_geometry_ids = sorted_unique(
        row["geometry_id"] for row in correction["current_evidence_loci"]
    )
    locus_rows = _rows(
        cur,
        """
        select cel.spatial_entity_id::text,
               cel.role_text,
               g.geometry_id::text,
               g.review_status::text,
               g.accuracy_status::text,
               geometrytype(g.geom),
               g.geometry_source_version_id::text
        from atlas.claim_evidence_locus cel
        join atlas.geometry g
          on g.spatial_entity_id=cel.spatial_entity_id
         and g.geometry_id=any(%s::uuid[])
        where cel.claim_id=%s::uuid
        order by cel.spatial_entity_id,g.geometry_id
        """,
        (add_locus_geometry_ids, correction_claim_id),
    )
    actual_loci = {(str(row[0]), str(row[2])) for row in locus_rows}
    if actual_loci != expected_loci:
        raise SuccessorAuthorityError(
            f"bounded evidence-locus pairs drifted: {sorted(actual_loci)}"
        )
    for spatial_id, role_text, geometry_id, review, accuracy, geom_type, _source in locus_rows:
        if review != "reviewed":
            raise SuccessorAuthorityError(f"{geometry_id}: locus geometry not reviewed")
        if str(geom_type).upper() != "POINT":
            raise SuccessorAuthorityError(f"{geometry_id}: locus geometry is not a point")
        if accuracy != "modern_proxy":
            raise SuccessorAuthorityError(
                f"{geometry_id}: expected explicit modern_proxy evidence locus"
            )
        if "locus" not in str(role_text).lower():
            raise SuccessorAuthorityError(
                f"{correction_claim_id}: locus role is not explicit"
            )

    count_rows = _rows(
        cur,
        """
        select count(*)::int
        from atlas.claim_evidence_locus
        where claim_id=%s::uuid
        """,
        (correction_claim_id,),
    )
    if count_rows[0][0] != len(expected_loci):
        raise SuccessorAuthorityError(
            "Mycenaean claim has unexpected extra evidence loci"
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
        (claim_ids, add_locus_geometry_ids),
    )
    dependency_source_ids = [str(row[0]) for row in source_rows]

    membership = {key: list(predecessor["membership"][key]) for key in MEMBERSHIP_KEYS}
    membership["claim_ids"] = sorted_unique([*membership["claim_ids"], *claim_ids])
    membership["spatial_entity_ids"] = sorted_unique(
        [*membership["spatial_entity_ids"], *selected_spatial_ids, *add_locus_spatial_ids]
    )
    membership["geometry_ids"] = sorted_unique(
        [*membership["geometry_ids"], *add_locus_geometry_ids]
    )
    membership["source_version_ids"] = sorted_unique(
        [*membership["source_version_ids"], *dependency_source_ids]
    )

    expected = selection["expected_claim_state"]
    if len(membership["claim_ids"]) != int(expected["successor_claims"]):
        raise SuccessorAuthorityError("successor claim count mismatch")
    if len(membership["spatial_entity_ids"]) != int(expected["successor_spatial_entities"]):
        raise SuccessorAuthorityError("successor spatial-entity count mismatch")
    expected_geometry = int(
        selection["geometry_policy"]["expected_successor_geometry_membership"]
    )
    if len(membership["geometry_ids"]) != expected_geometry:
        raise SuccessorAuthorityError("successor geometry count mismatch")
    return membership


def verify_predecessor_objects_preserved(
    predecessor: dict[str, Any],
    objects: dict[str, dict[str, Any]],
    selection: dict[str, Any],
) -> None:
    correction = selection["predecessor_object_correction_required"]
    correction_claim_id = str(correction["claim_id"])
    released_loci = int(correction["released_evidence_loci_count"])

    for group, old_objects in predecessor["objects"].items():
        for object_id, expected in old_objects.items():
            current = objects[group].get(object_id)
            if group == "claims" and object_id == correction_claim_id:
                if current is None:
                    raise SuccessorAuthorityError(
                        "bounded predecessor claim disappeared from successor snapshot"
                    )
                if len(expected.get("evidence_loci") or []) != released_loci:
                    raise SuccessorAuthorityError(
                        "predecessor evidence-locus baseline differs from selection"
                    )
                current_without_augmentation = json.loads(json.dumps(current))
                current_without_augmentation["evidence_loci"] = expected.get(
                    "evidence_loci", []
                )
                if current_without_augmentation != expected:
                    raise SuccessorAuthorityError(
                        "predecessor claim drift exceeds bounded evidence-locus augmentation"
                    )
                expected_ids = sorted_unique(correction["add_spatial_entity_ids"])
                current_ids = sorted_unique(
                    row.get("spatial_entity_id")
                    for row in current.get("evidence_loci") or []
                )
                if current_ids != expected_ids:
                    raise SuccessorAuthorityError(
                        "bounded predecessor claim augmentation has wrong locus membership"
                    )
                continue
            if current != expected:
                raise SuccessorAuthorityError(
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
        membership = derive_successor_membership(cur, selection, predecessor)
        objects, cartography = snapshot_objects(cur, membership)

    verify_predecessor_objects_preserved(predecessor, objects, selection)
    if cartography != predecessor["cartography"]:
        raise SuccessorAuthorityError("canonical cartography drifted from v0.8.1")

    digests = object_digests(objects)
    state = {
        "bundle_schema": BUNDLE_SCHEMA,
        "schema_version": "0034",
        "membership": membership,
        "object_digests": digests,
        "cartography_sha256": sha256_value(cartography),
    }
    excluded = selection.get("excluded_pending_reconciliation") or []
    excluded_subjects = ", ".join(
        str(row.get("subject")) for row in excluded if isinstance(row, dict)
    )
    release = {
        "release_version": "v0.8.2-post-overnight-authority-v1",
        "schema_version": "0034",
        "canonical": False,
        "purpose": PURPOSE,
        "canonical_predecessor_version": "v0.8.1",
        "canonical_predecessor_artifact_sha256": selection[
            "canonical_predecessor"
        ]["manifest_sha256"],
        "reviewed_candidate_id": selection["candidate_version"],
        "changelog": (
            "Explicit v0.8.2 successor authority: preserve v0.8.1; add the exact "
            "11 reviewed post-M1 territorial-practice claims frozen by the selection; "
            "add the two reviewed Pylos/Knossos evidence-locus point geometries and "
            "spatial entities as an explicit bounded Mycenaean claim-object "
            "augmentation; keep new-claim practice extent unresolved."
        ),
        "qc_summary": (
            "Explicit membership only; selected claims are reviewed, source-backed, "
            "unpublished research rows with practice_level=NULL; no new practice-extent "
            "geometry is inferred; D-120 successor geometry review is cleared; "
            "predecessor objects are byte/semantic-equal except the explicitly bounded "
            "Mycenaean evidence-locus augmentation; canonical cartography is unchanged."
        ),
        "unresolved_issues": (
            "Independent historical review remains 0. "
            + (
                f"Excluded pending current-method reconciliation: {excluded_subjects}. "
                if excluded_subjects
                else ""
            )
            + "New successor claims with unresolved historical geometry remain unmapped "
            "rather than using modern-country proxy practice extent."
        ),
    }
    return {
        "bundle_schema": BUNDLE_SCHEMA,
        "candidate_sha256": selection_sha256,
        "source_git_sha": source_git_sha,
        "release": release,
        "membership": membership,
        "membership_sha256": sha256_value(membership),
        "cartography": cartography,
        "cartography_sha256": sha256_value(cartography),
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
        membership = derive_successor_membership(cur, selection, predecessor)
        objects, cartography = snapshot_objects(cur, membership)

    if membership != bundle["membership"]:
        raise SuccessorAuthorityError("live explicit membership differs from authority")
    verify_predecessor_objects_preserved(predecessor, objects, selection)
    if object_digests(objects) != bundle["object_digests"]:
        raise SuccessorAuthorityError("live object state differs from authority")
    if sha256_value(cartography) != bundle["cartography_sha256"]:
        raise SuccessorAuthorityError("live cartography differs from authority")


def connect(args):
    if args.dsn:
        try:
            import psycopg
        except ImportError as exc:
            raise SuccessorAuthorityError("psycopg is required for --dsn mode") from exc
        return psycopg.connect(args.dsn, autocommit=False)
    if args.project_ref and args.management_token:
        return ManagementConnection(args.project_ref, args.management_token)
    raise SuccessorAuthorityError(
        "provide --dsn/DATABASE_URL or --project-ref plus --management-token"
    )


def add_connection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--project-ref")
    parser.add_argument(
        "--management-token",
        default=os.environ.get("SUPABASE_MANAGEMENT_TOKEN"),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("build", "verify"):
        cmd = sub.add_parser(name)
        cmd.add_argument("selection", type=Path)
        cmd.add_argument("predecessor_authority", type=Path)
        cmd.add_argument("authority_bundle", type=Path)
        cmd.add_argument(
            "--source-git-sha",
            default=os.environ.get("GITHUB_SHA", "unknown"),
        )
        add_connection_args(cmd)

    lint = sub.add_parser("lint")
    lint.add_argument("authority_bundle", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "lint":
            bundle = load_json(args.authority_bundle)
            validate_bundle(bundle)
            print(
                json.dumps(
                    {
                        "release_version": bundle["release"]["release_version"],
                        "membership_sha256": bundle["membership_sha256"],
                        "database_state_sha256": bundle["database_state_sha256"],
                        "mode": "lint-only",
                    },
                    indent=2,
                )
            )
            return 0

        selection = load_selection(args.selection)
        predecessor = load_predecessor(selection, args.predecessor_authority)
        with connect(args) as conn:
            if args.command == "build":
                bundle = build_authority(
                    conn,
                    selection,
                    predecessor,
                    selection_sha256=sha256_file(args.selection),
                    source_git_sha=args.source_git_sha,
                )
                conn.rollback()
                args.authority_bundle.parent.mkdir(parents=True, exist_ok=True)
                args.authority_bundle.write_bytes(canonical_bytes(bundle))
                print(
                    json.dumps(
                        {
                            "authority_bundle": str(args.authority_bundle),
                            "authority_bundle_sha256": sha256_file(args.authority_bundle),
                            "membership_sha256": bundle["membership_sha256"],
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

            bundle = load_json(args.authority_bundle)
            if bundle.get("candidate_sha256") != sha256_file(args.selection):
                raise SuccessorAuthorityError(
                    "authority candidate_sha256 differs from selection file"
                )
            verify_live(conn, selection, predecessor, bundle)
            conn.rollback()
            print(
                json.dumps(
                    {
                        "release_version": bundle["release"]["release_version"],
                        "authority_bundle_sha256": sha256_file(args.authority_bundle),
                        "database_state_sha256": bundle["database_state_sha256"],
                        "mode": "verified-no-write",
                    },
                    indent=2,
                )
            )
            return 0
    except (OSError, json.JSONDecodeError, SuccessorAuthorityError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
