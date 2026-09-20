#!/usr/bin/env python3
import argparse
import json
import socket
import time
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe atlas API and classify whether a project restart may help.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=12.0)
    parser.add_argument("--slow-seconds", type=float, default=15.0)
    args = parser.parse_args()

    started = time.monotonic()
    req = urllib.request.Request(
        args.url,
        headers={"User-Agent": "Historical-Slavery-Atlas-Self-Heal-Probe/1.0"},
    )

    result = {
        "healthy": False,
        "restart_candidate": False,
        "reason": None,
        "http_status": None,
        "elapsed_seconds": None,
        "release_channel": None,
        "release_version": None,
        "place_count": None,
        "claim_count": None,
    }

    try:
        with urllib.request.urlopen(req, timeout=args.timeout_seconds) as response:
            body = response.read()
            elapsed = time.monotonic() - started
            result["http_status"] = response.status
            result["elapsed_seconds"] = round(elapsed, 3)

            if response.status >= 500:
                result["restart_candidate"] = True
                result["reason"] = f"http_{response.status}"
            elif response.status >= 400:
                result["reason"] = f"http_{response.status}_nonrestartable"
            else:
                try:
                    payload = json.loads(body)
                except json.JSONDecodeError:
                    result["reason"] = "invalid_json_nonrestartable"
                else:
                    places = payload.get("places")
                    result["release_channel"] = payload.get("release_channel")
                    result["release_version"] = payload.get("release_version")
                    if isinstance(places, list):
                        result["place_count"] = len(places)
                        result["claim_count"] = sum(
                            len(place.get("claims") or [])
                            for place in places
                            if isinstance(place, dict)
                        )
                    if not payload.get("release_version") or not isinstance(places, list) or not places:
                        result["reason"] = "invalid_payload_nonrestartable"
                    elif elapsed > args.slow_seconds:
                        result["restart_candidate"] = True
                        result["reason"] = "severely_slow_api"
                    else:
                        result["healthy"] = True
                        result["reason"] = "ok"

    except urllib.error.HTTPError as exc:
        elapsed = time.monotonic() - started
        result["http_status"] = exc.code
        result["elapsed_seconds"] = round(elapsed, 3)
        if exc.code >= 500:
            result["restart_candidate"] = True
            result["reason"] = f"http_{exc.code}"
        else:
            result["reason"] = f"http_{exc.code}_nonrestartable"
    except (TimeoutError, socket.timeout):
        result["elapsed_seconds"] = round(time.monotonic() - started, 3)
        result["restart_candidate"] = True
        result["reason"] = "timeout"
    except urllib.error.URLError as exc:
        result["elapsed_seconds"] = round(time.monotonic() - started, 3)
        reason = getattr(exc, "reason", None)
        if isinstance(reason, (TimeoutError, socket.timeout)):
            result["restart_candidate"] = True
            result["reason"] = "timeout"
        else:
            result["reason"] = f"network_error_nonrestartable:{reason}"
    except Exception as exc:
        result["elapsed_seconds"] = round(time.monotonic() - started, 3)
        result["reason"] = f"unexpected_nonrestartable:{type(exc).__name__}:{exc}"

    print(json.dumps(result, sort_keys=True))
    if result["healthy"]:
        return 0
    if result["restart_candidate"]:
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
