#!/usr/bin/env python3
import argparse
import json
import sys
import time
import urllib.error
import urllib.request


def fetch(url: str, timeout: float):
    start = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": "Historical-Slavery-Atlas-Healthcheck/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read()
        elapsed = time.monotonic() - start
        return response.status, elapsed, body


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public Historical Slavery Atlas availability.")
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--site-url", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=15.0)
    parser.add_argument("--max-api-seconds", type=float, default=10.0)
    args = parser.parse_args()

    errors = []
    metrics = {}

    try:
        status, elapsed, body = fetch(args.api_url, args.timeout_seconds)
        metrics["api_status"] = status
        metrics["api_seconds"] = round(elapsed, 3)
        if status != 200:
            errors.append(f"API returned HTTP {status}")
        else:
            try:
                payload = json.loads(body)
            except json.JSONDecodeError as exc:
                errors.append(f"API returned invalid JSON: {exc}")
                payload = {}

            release_version = payload.get("release_version")
            release_channel = payload.get("release_channel")
            if not release_version:
                errors.append("API payload is missing release_version")
            else:
                metrics["release_version"] = release_version
            if release_channel:
                metrics["release_channel"] = release_channel

            places = payload.get("places")
            if not isinstance(places, list) or len(places) < 1:
                errors.append("API payload contains no places")
            else:
                metrics["place_count"] = len(places)
                metrics["claim_count"] = sum(
                    len(place.get("claims") or [])
                    for place in places
                    if isinstance(place, dict)
                )
            cartography = payload.get("cartography") or {}
            if not cartography.get("source_url"):
                errors.append("API payload is missing cartography.source_url")
            if elapsed > args.max_api_seconds:
                errors.append(
                    f"API latency {elapsed:.2f}s exceeds {args.max_api_seconds:.2f}s threshold"
                )
    except Exception as exc:
        errors.append(f"API request failed: {exc}")

    try:
        status, elapsed, body = fetch(args.site_url, args.timeout_seconds)
        metrics["site_status"] = status
        metrics["site_seconds"] = round(elapsed, 3)
        if status != 200:
            errors.append(f"Site returned HTTP {status}")
        elif b"Historical Slavery Atlas" not in body:
            errors.append("Site HTML does not contain expected atlas title")
    except Exception as exc:
        errors.append(f"Site request failed: {exc}")

    print(json.dumps({"ok": not errors, "metrics": metrics, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
