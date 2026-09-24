"""Skip PostGIS for changes that cannot affect the database foundation.

Unknown paths fail closed to full database verification. All PRs still run Python
regressions and sanitation. Frontend-only changes are verified by the dedicated Web
MVP workflow instead of paying for an unrelated PostGIS stack.

Input is Git's NUL-separated changed-path list.
"""
from pathlib import Path
import sys


SAFE_TEXT_ROOTS = ('docs/', 'experiments/', 'programmes/')
SAFE_TEXT_SUFFIXES = {'.md', '.csv', '.json', '.txt'}
SAFE_PREFIXES = ('web/',)
SAFE_FILES = {
    'README.md',
    'BACKLOG.md',
    'CHANGELOG.md',
    '.github/workflows/web-mvp.yml',
    '.github/workflows/deploy-pages.yml',
    'tools/build_exp04_research_preview.py',
    'tools/ci_scope.py',
    'tests/test_ci_scope.py',
    '.github/workflows/exp05-value-browser.yml',
    'experiments/exp05-thin-view-value/run_lane_c_browser.mjs',
}


def is_non_database_path(path):
    if path in SAFE_FILES:
        return True
    if path.startswith(SAFE_PREFIXES):
        return True
    if path.startswith(SAFE_TEXT_ROOTS) and Path(path).suffix in SAFE_TEXT_SUFFIXES:
        return True
    return False


def requires_database(paths):
    return not paths or any(not is_non_database_path(path) for path in paths)


if __name__ == '__main__':
    paths = Path(sys.argv[1]).read_bytes().decode('utf-8').rstrip('\0').split('\0')
    print('database=' + str(requires_database(paths)).lower())
