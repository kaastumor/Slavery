"""Materialize an isolated, exact-tree Git snapshot from authorized connector reads.

Usage: checkout.py manifest.json blobs-directory NEW-destination
manifest contains repository, revision, tree_sha, truncated=false and recursive tree.
Each blobs-directory/<sha>.json has sha, encoding, content and expected size.
Use fetch_file(encoding=base64, ref=exact revision). For empty large-file responses,
fetch the Git blob URL's exact UTF-8 content and use encoding=utf-8. Never parse and
reserialize a JSON source file; every recovered byte is checked against its Git SHA.
No network/credentials; no shell interpolation; no source execution. Full Git history
is NOT reconstructed. The local baseline commit has the canonical tree, not its SHA.
"""
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

SHA = re.compile(r'^[0-9a-f]{40}$')

def check(ok, reason):
    if not ok:
        raise ValueError(reason)

def run(root, *args, data=None):
    r = subprocess.run(['git', '-C', str(root), *args], input=data, capture_output=True)
    check(r.returncode == 0, 'Git failed: '+r.stderr.decode(errors='replace')[:300])
    return r.stdout.decode().strip()

def materialize(manifest, cache, destination):
    check(manifest.get('truncated') is False, 'TRUNCATED_TREE')
    check(SHA.fullmatch(manifest.get('revision', '')) and SHA.fullmatch(manifest.get('tree_sha', '')), 'INVALID_REVISION')
    check(manifest.get('repository') in {'kaastumor/morrow-needle','kaastumor/Slavery','kaastumor/Boekanalyse'}, 'WRONG_REPOSITORY')
    root, cache = Path(destination), Path(cache)
    check(not root.exists(), 'DESTINATION_EXISTS')
    entries, seen, prepared = manifest['tree'], set(), []
    # Verify every byte and path BEFORE creating the destination.
    for e in entries:
        path = e['path']
        pp = PurePosixPath(path)
        check(isinstance(path, str) and path and not pp.is_absolute() and
              all(x not in {'', '.', '..', '.git'} for x in path.split('/')) and
              '\\' not in path and '\x00' not in path, 'UNSAFE_PATH')
        check(path not in seen, 'DUPLICATE_PATH')
        seen.add(path)
        check(SHA.fullmatch(e['sha']), 'INVALID_OBJECT_SHA')
        if e['type'] == 'tree':
            check(e['mode'] == '040000', 'BAD_TREE_MODE')
            continue
        check(e['type'] == 'blob' and e['mode'] in {'100644','100755'}, 'UNSUPPORTED_MODE_OR_SUBMODULE')
        b = json.loads((cache/(e['sha']+'.json')).read_text())
        check(b.get('sha') == e['sha'] and b.get('encoding') in {'base64','utf-8'}, 'BLOB_IDENTITY_MISMATCH')
        raw = base64.b64decode(''.join(b['content'].split()), validate=True) if b['encoding']=='base64' else b['content'].encode('utf-8')
        check(b.get('size') == len(raw) and e.get('size') == len(raw), 'BLOB_SIZE_MISMATCH')
        actual = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        check(actual == e['sha'], 'BLOB_HASH_MISMATCH')
        prepared.append((e, raw))
    root.mkdir(parents=True)
    try:
        run(root, 'init', '--quiet')
        run(root, 'config', 'core.autocrlf', 'false')
        run(root, 'config', 'core.filemode', 'true')
        for e, raw in prepared:
            p = root/e['path']
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
            p.chmod(0o755 if e['mode'] == '100755' else 0o644)
            obj = run(root, 'hash-object', '-w', '--stdin', data=raw)
            check(obj == e['sha'], 'LOCAL_BLOB_MISMATCH')
            # Bypass .gitignore and clean/smudge filters: exact index bytes only.
            run(root, 'update-index', '--add', '--cacheinfo', e['mode'], obj, e['path'])
        actual_tree = run(root, 'write-tree')
        check(actual_tree == manifest['tree_sha'], 'TREE_HASH_MISMATCH')
        run(root, '-c', 'user.name=Automation Snapshot', '-c', 'user.email=snapshot@invalid',
            '-c', 'commit.gpgsign=false', 'commit', '--quiet', '-m',
            'Verified snapshot of '+manifest['repository']+'@'+manifest['revision']+'; tree identical; history not reconstructed')
        local_head = run(root, 'rev-parse', 'HEAD')
        check(not run(root, 'status', '--porcelain'), 'WORKTREE_NOT_CLEAN')
        return dict(repository=manifest['repository'], canonical_revision=manifest['revision'],
                    canonical_tree=manifest['tree_sha'], verified_tree=actual_tree,
                    local_baseline_commit=local_head, files=len(prepared),
                    bytes=sum(len(raw) for _,raw in prepared), clean=True,
                    history='NOT_RECONSTRUCTED', authentication='AUTHORIZED_CONNECTOR_READS',
                    destination=str(root.resolve()))
    except Exception:
        # Preserve the failed destination for diagnosis. Never silently reuse it.
        raise

if __name__ == '__main__':
    try:
        check(len(sys.argv) == 4, 'USAGE: checkout.py MANIFEST CACHE NEW_DESTINATION')
        result = materialize(json.loads(Path(sys.argv[1]).read_text()), sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, OSError) as e:
        print(json.dumps({'error':str(e)}), file=sys.stderr)
        sys.exit(2)
