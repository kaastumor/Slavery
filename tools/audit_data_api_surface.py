#!/usr/bin/env python3
"""Read-only audit of the Supabase Data API boundary.

The atlas public browser is intended to use the atlas-data Edge Function, not
direct PostgREST access to internal atlas/cartography/publish/audit schemas.

This tool:
- reads the project's PostgREST exposed-schema configuration through the
  Supabase Management API;
- obtains a public client key without printing it;
- proves anonymous direct reads to representative internal tables are rejected;
- proves an anonymous DELETE against a guaranteed-nonexistent geometry UUID is
  rejected before any mutation can occur.

It performs no database writes and never prints API keys or management tokens.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any


INTERNAL_SCHEMAS = {"atlas", "cartography", "publish", "audit"}
ZERO_UUID = "00000000-0000-0000-0000-000000000000"


class AuditError(RuntimeError):
    pass


def request_json(
    url: str,
    *,
    headers: dict[str, str],
    method: str = "GET",
    data: bytes | None = None,
    timeout: int = 20,
) -> tuple[int, Any]:
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            try:
                payload: Any = json.loads(body) if body else None
            except json.JSONDecodeError:
                payload = body
            return response.status, payload
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body) if body else None
        except json.JSONDecodeError:
            payload = body
        return exc.code, payload
    except urllib.error.URLError as exc:
        raise AuditError(f"request failed for {url}: {exc}") from exc


def management_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "historical-slavery-atlas-data-api-audit/1",
    }


def exposed_schemas(config: dict[str, Any]) -> list[str]:
    raw = config.get("db_schema")
    if raw is None:
        raw = config.get("db_schemas")
    if isinstance(raw, list):
        return sorted({str(item).strip() for item in raw if str(item).strip()})
    if isinstance(raw, str):
        return sorted({item.strip() for item in raw.split(",") if item.strip()})
    raise AuditError(f"Management API PostgREST config lacks db_schema: keys={sorted(config)}")


def pick_public_key(payload: Any) -> str:
    if not isinstance(payload, list):
        raise AuditError("unexpected API-key response shape")

    preferred = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        key = item.get("api_key") or item.get("key")
        if not key or item.get("disabled") is True:
            continue
        key_type = str(item.get("type") or "")
        name = str(item.get("name") or "")
        rank = 0 if key_type == "publishable" else 1 if name == "anon" else 2
        preferred.append((rank, str(key)))

    if not preferred:
        raise AuditError("no enabled public/publishable API key returned")
    preferred.sort(key=lambda pair: pair[0])
    return preferred[0][1]


def postgrest_probe(
    project_ref: str,
    api_key: str,
    *,
    schema: str,
    table: str,
    method: str,
    query: str,
) -> dict[str, Any]:
    url = f"https://{project_ref}.supabase.co/rest/v1/{table}?{query}"
    profile_header = "Accept-Profile" if method in {"GET", "HEAD"} else "Content-Profile"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        profile_header: schema,
        "Accept": "application/json",
        "User-Agent": "historical-slavery-atlas-data-api-audit/1",
    }
    status, body = request_json(url, headers=headers, method=method)
    code = body.get("code") if isinstance(body, dict) else None
    message = body.get("message") if isinstance(body, dict) else None
    return {
        "schema": schema,
        "table": table,
        "method": method,
        "http_status": status,
        "error_code": code,
        "message": message,
        "accessible": 200 <= status < 300,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-ref", required=True)
    parser.add_argument("--token-env", default="SUPABASE_MANAGEMENT_TOKEN")
    parser.add_argument("--output")
    args = parser.parse_args()

    token = os.environ.get(args.token_env)
    if not token:
        parser.error(f"missing {args.token_env}")

    management_base = f"https://api.supabase.com/v1/projects/{args.project_ref}"
    headers = management_headers(token)

    # The scoped CI token may intentionally lack data_api_config_read. That is
    # not a reason to broaden it: the anonymous PostgREST probes below test the
    # effective public boundary directly.
    config_status, config_payload = request_json(
        management_base + "/postgrest",
        headers=headers,
    )
    if config_status == 200 and isinstance(config_payload, dict):
        schemas = exposed_schemas(config_payload)
        config_source = "management_api"
    else:
        schemas = []
        config_source = "unavailable_to_scoped_token"

    internal_exposed = sorted(INTERNAL_SCHEMAS.intersection(schemas))

    status, keys_payload = request_json(
        management_base + "/api-keys?reveal=true",
        headers=headers,
    )
    if status != 200:
        raise AuditError(f"cannot read project API keys for anonymous probe: HTTP {status}")
    public_key = pick_public_key(keys_payload)

    probes = [
        postgrest_probe(
            args.project_ref,
            public_key,
            schema="atlas",
            table="geometry",
            method="GET",
            query="select=geometry_id&limit=1",
        ),
        postgrest_probe(
            args.project_ref,
            public_key,
            schema="cartography",
            table="land_fabric",
            method="GET",
            query="select=fabric_id&limit=1",
        ),
        postgrest_probe(
            args.project_ref,
            public_key,
            schema="publish",
            table="map_geometry",
            method="GET",
            query="select=geometry_id&limit=1",
        ),
        postgrest_probe(
            args.project_ref,
            public_key,
            schema="audit",
            table="release_manifest",
            method="GET",
            query="select=release_version&limit=1",
        ),
        # A DELETE on a guaranteed-nonexistent UUID is side-effect free even if
        # it unexpectedly reaches SQL. A 2xx response would still prove that
        # anonymous mutation privilege exists and therefore fails the audit.
        postgrest_probe(
            args.project_ref,
            public_key,
            schema="atlas",
            table="geometry",
            method="DELETE",
            query=f"geometry_id=eq.{ZERO_UUID}",
        ),
    ]

    accessible = [probe for probe in probes if probe["accessible"]]

    # PGRST106 exposes the server's accepted profile list in its error message,
    # so when config_read is intentionally unavailable we can still infer the
    # effective exposed schemas from the public endpoint itself.
    inferred = set()
    for probe in probes:
        if probe.get("error_code") == "PGRST106":
            message = str(probe.get("message") or "")
            marker = "The schema must be one of the following: "
            if marker in message:
                tail = message.split(marker, 1)[1]
                for item in tail.replace('"', "").replace("'", "").split(","):
                    item = item.strip().strip(".")
                    if item:
                        inferred.add(item)

    effective_schemas = schemas or sorted(inferred)
    effective_internal_exposed = sorted(INTERNAL_SCHEMAS.intersection(effective_schemas))

    result = {
        "schema_version": "atlas-data-api-security-audit-v1",
        "project_ref": args.project_ref,
        "postgrest_config_status": config_status,
        "postgrest_config_source": config_source,
        "postgrest_exposed_schemas": effective_schemas,
        "internal_schemas_exposed": effective_internal_exposed,
        "anonymous_probes": probes,
        "result": "pass" if not effective_internal_exposed and not accessible else "fail",
    }

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")

    if effective_internal_exposed:
        print(
            "BLOCK: internal schemas are exposed through PostgREST: "
            + ", ".join(effective_internal_exposed),
            file=sys.stderr,
        )
        return 2
    if accessible:
        print(
            "BLOCK: anonymous direct Data API access unexpectedly succeeded: "
            + json.dumps(accessible, sort_keys=True),
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditError as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        raise SystemExit(2)
