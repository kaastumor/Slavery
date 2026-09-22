from pathlib import Path

from tools.sanitize_repo import scan


def _write(root: Path, rel: str, text: str = "ok\n") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _baseline(tmp_path: Path) -> list[str]:
    paths = [
        "BACKLOG.md",
        "docs/23_PROJECT_CHARTER.md",
        "docs/24_WAY_OF_WORKING.md",
        "docs/25_PROJECT_HEALTH.md",
        "docs/automation/hourly-worker.md",
        "docs/08_DECISIONS_LOG.md",
        "SECURITY.md",
    ]
    for rel in paths:
        _write(tmp_path, rel)
    return paths


def test_clean_repository_shape_passes(tmp_path: Path) -> None:
    paths = _baseline(tmp_path)
    assert scan(tmp_path, paths) == []


def test_private_release_binary_is_rejected(tmp_path: Path) -> None:
    paths = _baseline(tmp_path) + ["data/releases/v0.6.1/canonical.xlsx"]
    _write(tmp_path, paths[-1])
    assert any("forbidden tracked path" in x for x in scan(tmp_path, paths))


def test_merge_marker_and_secret_are_rejected(tmp_path: Path) -> None:
    paths = _baseline(tmp_path) + ["notes.md"]
    _write(tmp_path, "notes.md", "<<<<<<< ours\nghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456\n")
    failures = scan(tmp_path, paths)
    assert any("merge marker" in x for x in failures)
    assert any("GitHub token" in x for x in failures)
