$ErrorActionPreference = "Stop"
$file = "data/releases/v0.6.1/Historical_Slavery_Atlas_v0.6.1_Controlled_Atlantic_Ingestion.xlsx"
$expected = "0a38e4eb6f63c3bb4ce9543be379605d24dd9ff1c1cea1e0a49c0c3db7ba17d4"
if (-not (Test-Path $file)) { throw "Canonical workbook missing: $file" }
$actual = (Get-FileHash -Algorithm SHA256 $file).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "Canonical v0.6.1 checksum mismatch. Expected $expected, found $actual" }
Write-Host "Canonical v0.6.1 checksum OK: $actual"
