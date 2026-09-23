import tempfile
import unittest
from pathlib import Path

from tools.sanitize_repo import scan


def _write(root: Path, rel: str, text: str = "ok\n") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _baseline(root: Path) -> list[str]:
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
        _write(root, rel)
    return paths


class SanitationTests(unittest.TestCase):
    def test_clean_repository_shape_passes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = _baseline(root)
            self.assertEqual(scan(root, paths), [])

    def test_private_release_binary_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = _baseline(root) + ["data/releases/v0.6.1/canonical.xlsx"]
            _write(root, paths[-1])
            self.assertTrue(any("forbidden tracked path" in x for x in scan(root, paths)))

    def test_merge_marker_and_secret_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = _baseline(root) + ["notes.md"]
            _write(root, "notes.md", "<<<<<<< ours\\n " + "ghp_" + ("A" * 26) + "\\n")
            failures = scan(root, paths)
            self.assertTrue(any("merge marker" in x for x in failures))
            self.assertTrue(any("GitHub token" in x for x in failures))

    def test_rejects_private_key_container_extensions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = _baseline(root) + ["certs/private.pfx"]
            _write(root, paths[-1], "not-a-real-key")
            self.assertTrue(any("forbidden tracked path" in x for x in scan(root, paths)))

    def test_rejects_machine_local_user_path(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = _baseline(root) + ["notes.md"]
            _write(root, "notes.md", "workspace: C:\\\\Users\\\\alice\\\\project\\\\data.json\n")
            self.assertTrue(any("machine-local user path" in x for x in scan(root, paths)))

    def test_rejects_unexpected_large_tracked_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = _baseline(root) + ["generated.bin"]
            path = root / "generated.bin"
            path.write_bytes(b"0" * 5_000_001)
            self.assertTrue(any("larger than 5 MB" in x for x in scan(root, paths)))


if __name__ == "__main__":
    unittest.main()
