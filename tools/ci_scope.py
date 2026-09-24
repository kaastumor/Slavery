"""Skip PostGIS only for known documentation/experimental-research-only diffs.

Unknown paths fail closed to full database verification. All PRs still run Python
regressions and sanitation. Input is Git's NUL-separated changed-path list.
"""
from pathlib import Path
import sys


def requires_database(paths):
    safe_roots = ('docs/', 'experiments/', 'programmes/')
    safe_files = {'README.md', 'BACKLOG.md', 'CHANGELOG.md'}
    return not paths or any(
        path not in safe_files and not (path.startswith(safe_roots) and Path(path).suffix in {'.md', '.csv', '.json', '.txt'})
        for path in paths
    )


if __name__ == '__main__':
    paths = Path(sys.argv[1]).read_bytes().decode('utf-8').rstrip('\0').split('\0')
    print('database=' + str(requires_database(paths)).lower())
