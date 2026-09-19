#!/usr/bin/env bash
set -euo pipefail
file="data/releases/v0.6.1/Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx"
expected="0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4"
[[ -f "$file" ]] || { echo "Canonical workbook missing: $file" >&2; exit 1; }
actual="$(sha256sum "$file" | awk '{print $1}')"
[[ "$actual" == "$expected" ]] || { echo "Checksum mismatch: expected $expected, found $actual" >&2; exit 1; }
echo "Canonical v0.6.1 checksum OK: $actual"
