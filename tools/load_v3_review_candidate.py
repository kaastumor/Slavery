#!/usr/bin/env python3
"""Idempotently load the frozen v3 review candidate into the Gate-2 research layer.

This loader intentionally preserves reviewed research target/result/source semantics
without inventing P-levels, historical geometry, or positive claim rows. It is a
Gate-2 reconciliation tool, not a publication or canonical-release tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PAYLOAD = ROOT / "reviews" / "db-canonicalization" / "gate2-v3-ingest-payload.json"
CANDIDATE_ID = "post-r1-cumulative-review-v3-cross-frame"
NAMESPACE = uuid.UUID("6b8201e8-3e31-4fa3-9c71-aaf87f374b2c")
VALID_DIRECTIONS = {"supports", "challenges", "qualifies", "context"}


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_uuid(kind: str, *parts: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, "|".join([kind, *parts]))


def target_content_sha(target: dict) -> str:
    material = {"data": target["data"], "lineage": target["lineage"]}
    return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def parse_anchor_year(label: str) -> int | None:
    text = label.strip().upper()
    if not text:
        return None
    bits = text.replace(",", "").split()
    try:
        n = int(bits[0])
    except (ValueError, IndexError):
        return None
    if "BCE" in bits or "BC" in bits:
        return -abs(n)
    if "CE" in bits or "AD" in bits:
        return abs(n)
    return n


def parse_bool(value: str) -> bool | None:
    v = (value or "").strip().lower()
    if v in {"true", "1", "yes"}:
        return True
    if v in {"false", "0", "no"}:
        return False
    return None


def null_if_blank(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def load_payload(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "gate2-v3-ingest-payload-v1":
        raise RuntimeError("unsupported Gate-2 v3 ingest payload schema")
    if data.get("candidate_id") != CANDIDATE_ID:
        raise RuntimeError("unexpected candidate_id")
    if data.get("counts") != {
        "targets": 26,
        "admitted": 21,
        "holds": 5,
        "source_relations": 166,
    }:
        raise RuntimeError(f"unexpected payload counts: {data.get('counts')!r}")
    target_ids = [t["data"]["target_id"] for t in data["targets"]]
    if len(target_ids) != len(set(target_ids)):
        raise RuntimeError("duplicate target_id in payload")
    if set(target_ids) != {r["target_id"] for r in (t["review"] for t in data["targets"])}:
        raise RuntimeError("target/review membership mismatch")
    source_targets = {r["data"]["target_id"] for r in data["source_relations"]}
    missing = sorted(set(target_ids) - source_targets)
    if missing:
        raise RuntimeError(f"targets without source relations: {missing}")
    for rel in data["source_relations"]:
        row = rel["data"]
        for field in ("source_version_ref", "independence_group", "claim_fitness"):
            if not row.get(field):
                raise RuntimeError(f"missing {field} for {row.get('target_id')}")
    return data


def ensure_source(cur, rel: dict) -> uuid.UUID:
    row = rel["data"]
    ref = row["source_version_ref"]
    source_id = stable_uuid("v3-source", ref)
    version_id = stable_uuid("v3-source-version", ref)

    cur.execute(
        """
        INSERT INTO atlas.source(
            source_id, title, source_classification, notes
        ) VALUES (%s,%s,%s,%s)
        ON CONFLICT (source_id) DO NOTHING
        """,
        (
            source_id,
            row["title"],
            null_if_blank(row.get("source_classification")),
            "Gate-2 v3 migration source identity; exact packet source_id is preserved on audit.research_target_source.",
        ),
    )
    cur.execute(
        "SELECT title, source_classification FROM atlas.source WHERE source_id=%s",
        (source_id,),
    )
    existing = cur.fetchone()
    if existing is None or existing[0] != row["title"]:
        raise RuntimeError(f"source identity collision for {ref}")

    cur.execute(
        """
        INSERT INTO atlas.source_version(
            source_version_id, source_id, version_label, url_or_identifier, notes
        ) VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (source_version_id) DO NOTHING
        """,
        (
            version_id,
            source_id,
            ref,
            null_if_blank(row.get("url")),
            "Exact source_version_ref_raw is preserved in the Gate-2 research-target relation.",
        ),
    )
    cur.execute(
        "SELECT source_id, version_label FROM atlas.source_version WHERE source_version_id=%s",
        (version_id,),
    )
    existing_v = cur.fetchone()
    if existing_v is None or existing_v[0] != source_id or existing_v[1] != ref:
        raise RuntimeError(f"source-version identity collision for {ref}")
    return version_id


def upsert_target(cur, target: dict) -> uuid.UUID:
    d = target["data"]
    review = target["review"]
    content_sha = target_content_sha(target)
    result_id = stable_uuid("v3-target-result", d["target_id"], content_sha)

    cur.execute(
        """
        INSERT INTO audit.research_target(
            target_key, target_label, anchor_label, anchor_year, frame_class,
            spatial_entity_id, origin, review_status
        ) VALUES (%s,%s,%s,%s,%s,NULL,%s,'reviewed')
        ON CONFLICT (target_key) DO UPDATE SET
            target_label=EXCLUDED.target_label,
            anchor_label=EXCLUDED.anchor_label,
            anchor_year=EXCLUDED.anchor_year,
            frame_class=EXCLUDED.frame_class,
            origin=EXCLUDED.origin
        """,
        (
            d["target_id"], d["target_label"], d["anchor"], parse_anchor_year(d["anchor"]),
            d["effective_frame_class"], review.get("origin"),
        ),
    )

    cur.execute(
        """
        INSERT INTO audit.research_target_result(
            research_target_result_id, target_key, research_stage, research_outcome,
            bounded_proposition, required_abstention, evidence_locus_summary,
            inference_extent_summary, temporal_state, law_practice_note,
            network_territorial_note, historical_terms, category_mapping_status,
            category_mapping_note, language_access_limitations, coverage_confidence,
            geometry_resolved_form, geometry_claim_role, geometry_unresolved_note,
            source_path, source_blob_ref, content_sha256, review_status
        ) VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'reviewed'
        )
        ON CONFLICT (target_key, content_sha256) DO NOTHING
        """,
        (
            result_id, d["target_id"], d["research_stage"], d["research_outcome"],
            null_if_blank(d.get("bounded_proposition")),
            null_if_blank(d.get("required_abstention")),
            null_if_blank(d.get("evidence_locus")),
            null_if_blank(d.get("inference_extent")),
            null_if_blank(d.get("temporal_state")),
            null_if_blank(d.get("law_practice_note")),
            null_if_blank(d.get("network_territorial_note")),
            null_if_blank(d.get("historical_terms")),
            null_if_blank(d.get("category_mapping_status")),
            null_if_blank(d.get("category_mapping_note")),
            null_if_blank(d.get("language_access_limitations")),
            null_if_blank(d.get("coverage_confidence")),
            null_if_blank(d.get("geometry_resolved_form")),
            null_if_blank(d.get("geometry_claim_role")),
            null_if_blank(d.get("geometry_unresolved_note")),
            target["lineage"]["path"],
            target["lineage"]["blob_sha"],
            content_sha,
        ),
    )

    cur.execute(
        """
        INSERT INTO audit.research_target_review(
            research_target_review_id, research_target_result_id, candidate_id,
            review_level, review_disposition, admitted, review_reason, failure_guards,
            dependency_or_scope_note, notes
        ) VALUES (%s,%s,%s,'internal',%s,%s,%s,%s,%s,%s)
        ON CONFLICT (research_target_result_id, candidate_id, review_level) DO NOTHING
        """,
        (
            stable_uuid("v3-target-review", str(result_id), CANDIDATE_ID, "internal"),
            result_id,
            CANDIDATE_ID,
            review["review_disposition"],
            parse_bool(review["admitted"]),
            null_if_blank(review.get("review_reason")),
            [x for x in review.get("failure_guards", "").split(";") if x],
            null_if_blank(review.get("dependency_or_scope_note")),
            "Gate-2 import preserves internal review only; independent historical review remains zero.",
        ),
    )
    return result_id


def upsert_relation(cur, result_id: uuid.UUID, rel: dict) -> None:
    row = rel["data"]
    version_id = ensure_source(cur, rel)
    lineage_note = canonical_json(rel["lineage"])
    relation_id = stable_uuid(
        "v3-target-source",
        str(result_id),
        row["source_version_ref"],
        row["source_id"],
        row.get("locator", ""),
        rel["lineage"]["path"],
    )
    direction = row.get("direction", "").strip()
    normalized = direction if direction in VALID_DIRECTIONS else None

    cur.execute(
        """
        INSERT INTO audit.research_target_source(
            research_target_source_id, research_target_result_id, source_version_id,
            source_relation_key, source_version_ref_raw, evidence_role,
            independence_group, claim_fitness, direction_raw, normalized_direction,
            locator, notes, source_id_raw, decisive, access_limitation,
            accessed_at_text, asset_sha256, dependency_note
        ) VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        ON CONFLICT (research_target_source_id) DO NOTHING
        """,
        (
            relation_id, result_id, version_id,
            null_if_blank(row.get("source_id")),
            row["source_version_ref"],
            null_if_blank(row.get("evidence_role")),
            row["independence_group"],
            row["claim_fitness"],
            null_if_blank(direction),
            normalized,
            null_if_blank(row.get("locator")),
            lineage_note,
            null_if_blank(row.get("source_id")),
            parse_bool(row.get("decisive", "")),
            null_if_blank(row.get("access_limitation")),
            null_if_blank(row.get("accessed_at")),
            null_if_blank(row.get("asset_sha256")),
            null_if_blank(row.get("dependency_note")),
        ),
    )


def verify(cur) -> dict:
    cur.execute(
        """
        SELECT
          count(*) FILTER (WHERE r.admitted) AS admitted,
          count(*) FILTER (WHERE NOT r.admitted) AS holds,
          count(*) AS reviews
        FROM audit.research_target_review r
        WHERE r.candidate_id=%s AND r.review_level='internal'
        """,
        (CANDIDATE_ID,),
    )
    admitted, holds, reviews = cur.fetchone()

    cur.execute(
        """
        SELECT count(*)
        FROM audit.research_target_source s
        JOIN audit.research_target_review r
          ON r.research_target_result_id=s.research_target_result_id
        WHERE r.candidate_id=%s AND r.review_level='internal'
        """,
        (CANDIDATE_ID,),
    )
    source_relations = cur.fetchone()[0]

    cur.execute(
        """
        SELECT count(*)
        FROM audit.research_target_claim c
        JOIN audit.research_target_review r
          ON r.research_target_result_id=c.research_target_result_id
        WHERE r.candidate_id=%s AND r.review_level='internal'
        """,
        (CANDIDATE_ID,),
    )
    claim_bridges = cur.fetchone()[0]

    result = {
        "targets": reviews,
        "admitted": admitted,
        "holds": holds,
        "source_relations": source_relations,
        "claim_bridges": claim_bridges,
    }
    expected = {"targets": 26, "admitted": 21, "holds": 5, "source_relations": 166}
    for key, value in expected.items():
        if result[key] != value:
            raise RuntimeError(f"Gate-2 verification failed: {key}={result[key]} expected {value}")
    return result


def apply(conn, payload: dict) -> dict:
    source_by_target: dict[str, list[dict]] = {}
    for rel in payload["source_relations"]:
        source_by_target.setdefault(rel["data"]["target_id"], []).append(rel)

    with conn.transaction():
        with conn.cursor() as cur:
            for target in payload["targets"]:
                target_id = target["data"]["target_id"]
                result_id = upsert_target(cur, target)
                for rel in source_by_target[target_id]:
                    upsert_relation(cur, result_id, rel)
            return verify(cur)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", type=Path, default=DEFAULT_PAYLOAD)
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    payload = load_payload(args.payload)
    if args.validate_only:
        print(json.dumps({"payload": "valid", "counts": payload["counts"]}, sort_keys=True))
        return 0
    if not args.dsn:
        parser.error("--dsn or DATABASE_URL is required")

    try:
        import psycopg
    except ImportError as exc:
        raise SystemExit("psycopg is required; run through the tooling container") from exc

    with psycopg.connect(args.dsn, autocommit=False) as conn:
        result = apply(conn, payload)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
