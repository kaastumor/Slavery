"""Deterministic state transitions for AUTOMATION_CONTROL_V2_20261001.

No credentials, network, scheduler or model calls. The caller must publish the returned
state as a SINGLE-parent commit and advance the control ref with force=false.
This checks compliant callers; it is not a sandbox or tool-permission boundary.
"""
import copy
import hashlib
import json
import re
import sys

CONTRACT = 'AUTOMATION_CONTROL_V2_20261001'
REPOS = {'kaastumor/morrow-needle', 'kaastumor/Slavery', 'kaastumor/Boekanalyse'}
LIVE = {'CLAIMED', 'ACTIVE'}
END = {'CHECKPOINTED', 'COMPLETE', 'BLOCKED', 'FAILED_RETRYABLE', 'WAITING_EXTERNAL', 'NEEDS_REVIEW'}
ALLOW = {'branch_edit', 'draft_pr', 'issue_checkpoint', 'read_only'}
SHA = re.compile(r'^[0-9a-f]{40}$')
IDENT = re.compile(r'^[A-Za-z0-9_.:/-]{1,160}$')

class Refused(ValueError):
    pass

def require(ok, reason):
    if not ok:
        raise Refused(reason)

def initial(repo, now):
    require(repo in REPOS, 'UNKNOWN_REPOSITORY')
    return dict(schema=2, contract=CONTRACT, repository=repo, generation=0,
                state='UNCLAIMED', owner_attempt=None, lease_until=None,
                updated_at=now, stage=None, checkpoint=None, operation=None, effects=[],
                receipts=[], archive_ref=None, failure_count=0, failure_key=None)

def validate(s):
    require(isinstance(s, dict), 'MALFORMED_STATE')
    require(s.get('schema') == 2 and s.get('contract') == CONTRACT, 'CONTRACT_MISMATCH')
    require(s.get('repository') in REPOS, 'UNKNOWN_REPOSITORY')
    require(s.get('state') in LIVE | END | {'UNCLAIMED'}, 'INVALID_STATE')
    require(type(s.get('generation')) is int and s['generation'] >= 0, 'BAD_GENERATION')
    require(type(s.get('updated_at')) in (int, float), 'BAD_CLOCK')
    require(isinstance(s.get('receipts'), list) and len(s['receipts']) <= 16, 'INDEX_FULL')
    require(isinstance(s.get('effects'), list) and len(s['effects']) <= 8, 'EFFECT_INDEX_FULL')
    require(type(s.get('failure_count')) is int and s['failure_count'] >= 0, 'BAD_FAILURE_COUNT')
    if s['state'] in LIVE:
        require(isinstance(s.get('owner_attempt'), str) and IDENT.fullmatch(s['owner_attempt']), 'BAD_OWNER')
        require(type(s.get('lease_until')) in (int, float), 'BAD_LEASE')
        require(isinstance(s.get('stage'), dict), 'MISSING_STAGE')
    require(len(json.dumps(s).encode()) <= 8192, 'INDEX_FULL')

def stage_key(repo, task, stage, input_revision):
    require(repo in REPOS and type(task) is int and task > 0, 'BAD_TASK')
    require(isinstance(stage, str) and IDENT.fullmatch(stage), 'BAD_STAGE')
    require(isinstance(input_revision, str) and SHA.fullmatch(input_revision), 'BAD_INPUT')
    return hashlib.sha256(json.dumps([repo, task, stage, input_revision, CONTRACT],
                         separators=(',', ':')).encode()).hexdigest()

def gate(s, now, key, *, ready, pending_known, interactive_owner, dependency_changed=False, archive_checked=False):
    validate(s)
    require(all(type(v) is bool for v in (ready, pending_known, interactive_owner, dependency_changed, archive_checked)), 'BAD_GATE_FLAGS')
    require(type(now) in (int, float) and now >= s['updated_at'], 'CLOCK_REGRESSION')
    if s['state'] in LIVE:
        return 'BUSY' if now < s['lease_until'] else 'RECONCILE_EXPIRED'
    if not pending_known:
        return 'RECONCILE_PENDING'
    if interactive_owner:
        return 'INTERACTIVE_OWNER'
    if s['operation'] and s['operation']['status'] != 'VERIFIED':
        return 'RECONCILE_OPERATION'
    if len(s['receipts']) >= 16:
        return 'INDEX_FULL'
    if s.get('archive_ref') and not archive_checked:
        return 'CHECK_ARCHIVED_RECEIPTS'
    if any(r['key'] == key and r['state'] == 'COMPLETE' for r in s['receipts']):
        return 'ALREADY_COMPLETE'
    if s['state'] in {'BLOCKED', 'WAITING_EXTERNAL', 'NEEDS_REVIEW'} and not dependency_changed:
        return 'UNCHANGED_GATE'
    if s['failure_count'] >= 2 and s['failure_key'] == key and not dependency_changed:
        return 'RETRY_EXHAUSTED'
    return 'READY' if ready else 'NO_ELIGIBLE_WORK'

def claim(s, now, attempt, task, stage, input_revision, *, ready=True,
          pending_known=True, interactive_owner=False, dependency_changed=False, archive_checked=False):
    key = stage_key(s['repository'], task, stage, input_revision)
    require(gate(s, now, key, ready=ready, pending_known=pending_known,
                 interactive_owner=interactive_owner, dependency_changed=dependency_changed, archive_checked=archive_checked) == 'READY', 'CLAIM_NOT_ELIGIBLE')
    require(isinstance(attempt, str) and IDENT.fullmatch(attempt), 'BAD_ATTEMPT')
    x = copy.deepcopy(s)
    x.update(state='CLAIMED', generation=s['generation']+1, owner_attempt=attempt,
             lease_until=now+1800, updated_at=now, operation=None,
             stage=dict(key=key, task=task, name=stage, input_revision=input_revision),
             checkpoint=None)
    x['effects'] = copy.deepcopy(s['effects']) if s['stage'] and s['stage']['key'] == key else []
    if dependency_changed or s['failure_key'] != key:
        x.update(failure_count=0, failure_key=None)
    validate(x)
    return x

def fence(s, now, attempt, generation):
    validate(s)
    require(now >= s['updated_at'], 'CLOCK_REGRESSION')
    require(s['state'] in LIVE and s['owner_attempt'] == attempt and
            s['generation'] == generation, 'STALE_OWNER')
    require(now < s['lease_until'], 'LEASE_EXPIRED')

def start(s, now, attempt, generation):
    fence(s, now, attempt, generation)
    x = copy.deepcopy(s)
    x.update(state='ACTIVE', updated_at=now)
    return x

def intent(s, now, attempt, generation, operation_id, kind, target_ref, expected_head):
    fence(s, now, attempt, generation)
    require(kind in ALLOW, 'ACTION_NOT_AUTHORIZED')
    require(kind == 'read_only' or s['state'] == 'ACTIVE', 'NOT_ACTIVE')
    require(isinstance(operation_id, str) and IDENT.fullmatch(operation_id), 'BAD_OPERATION_ID')
    require(isinstance(expected_head, str) and SHA.fullmatch(expected_head), 'BAD_EXPECTED_HEAD')
    require(isinstance(target_ref, str) and IDENT.fullmatch(target_ref), 'BAD_TARGET')
    branch = target_ref.removeprefix('refs/heads/').removeprefix('heads/')
    require(branch not in {'main', 'master', 'production'}, 'PROTECTED_TARGET')
    require(all(part not in {'', '.', '..'} for part in branch.split('/')), 'BAD_TARGET')
    require(not any(e['id'] == operation_id for e in s['effects']), 'ALREADY_VERIFIED')
    require(len(s['effects']) < 8, 'EFFECT_INDEX_FULL')
    require(not s['operation'] or s['operation']['status'] == 'VERIFIED', 'RECONCILE_OPERATION')
    x = copy.deepcopy(s)
    x.update(updated_at=now, operation=dict(id=operation_id, kind=kind,
             target_ref=target_ref, expected_head=expected_head, status='INTENDED', output_ref=None))
    validate(x)
    return x

def public_ref(repo, value):
    prefix = 'https://github.com/'+repo+'/'
    if not isinstance(value, str) or not value.startswith(prefix) or len(value) > 500:
        return False
    tail = value[len(prefix):]
    return all(part not in {'.', '..', ''} for part in tail.split('/')) and bool(re.fullmatch(r'(?:issues/[1-9][0-9]*(?:#issuecomment-[0-9]+)?|pull/[1-9][0-9]*(?:#[A-Za-z0-9_-]+)?|commit/[0-9a-f]{40}|blob/[0-9a-f]{40}/[A-Za-z0-9_./-]+)', tail))

def verified(s, now, attempt, generation, operation_id, output_ref):
    fence(s, now, attempt, generation)
    require(s['operation'] and s['operation']['id'] == operation_id, 'WRONG_OPERATION')
    require(s['operation']['status'] == 'INTENDED', 'ALREADY_VERIFIED')
    require(public_ref(s['repository'], output_ref), 'NONPUBLIC_OUTPUT_REF')
    x = copy.deepcopy(s)
    x['operation'].update(status='VERIFIED', output_ref=output_ref)
    x['effects'].append(dict(id=operation_id, output_ref=output_ref))
    x['updated_at'] = now
    validate(x)
    return x

def finish(s, now, attempt, generation, state, receipt_ref, verification, next_action):
    fence(s, now, attempt, generation)
    require(state in END, 'INVALID_TERMINAL_STATE')
    require(public_ref(s['repository'], receipt_ref), 'NONPUBLIC_RECEIPT')
    require(isinstance(verification, str) and 0 < len(verification) <= 160, 'MISSING_VERIFICATION')
    require(isinstance(next_action, str) and 0 < len(next_action) <= 240, 'MISSING_NEXT_ACTION')
    require(not s['operation'] or s['operation']['status'] == 'VERIFIED', 'RECONCILE_OPERATION')
    require(len(s['receipts']) < 16, 'INDEX_FULL')
    x = copy.deepcopy(s)
    key = s['stage']['key']
    x['receipts'].append(dict(key=key, state=state, receipt_ref=receipt_ref,
                              attempt=attempt, at=now))
    x.update(state=state, owner_attempt=None, lease_until=None, updated_at=now,
             checkpoint=dict(receipt_ref=receipt_ref, verification=verification,
                             next_action=next_action, disposition='SEE_CANONICAL_OWNER'))
    if state == 'FAILED_RETRYABLE':
        x['failure_count'] = s['failure_count'] + 1 if s['failure_key'] == key else 1
        x['failure_key'] = key
    else:
        x.update(failure_count=0, failure_key=None)
    validate(x)
    return x

def compact(s, now, archive_ref):
    validate(s)
    require(s['state'] not in LIVE, 'BUSY')
    require(now >= s['updated_at'], 'CLOCK_REGRESSION')
    prefix = 'https://github.com/'+s['repository']+'/blob/'
    require(isinstance(archive_ref, str) and archive_ref.startswith(prefix) and
            re.fullmatch(r'[0-9a-f]{40}/.automation-v2/state.json', archive_ref[len(prefix):]), 'UNPINNED_ARCHIVE')
    x = copy.deepcopy(s)
    # The pin MUST be independently read back as the exact current pre-compaction
    # state. It includes earlier archive_ref, so older receipts remain recoverable.
    current_key = s['stage']['key'] if s['stage'] else None
    x['receipts'] = [r for r in s['receipts'] if r['state'] != 'COMPLETE' or r['key'] == current_key]
    require(len(x['receipts']) < len(s['receipts']), 'NO_RESOLVED_RECEIPTS_TO_COMPACT')
    x.update(archive_ref=archive_ref, updated_at=now)
    validate(x)
    return x

def main():
    # Usage: python controller.py STATE.json REQUEST.json > candidate-state.json
    # request={"action":"claim", "now":1790856000, ...}; gate returns a decision.
    require(len(sys.argv) == 3, 'USAGE: controller.py STATE.json REQUEST.json')
    with open(sys.argv[1]) as f:
        s = json.load(f)
    with open(sys.argv[2]) as f:
        req = json.load(f)
    action = req.pop('action')
    require(action in {'gate', 'claim', 'start', 'intent', 'verified', 'finish', 'compact'}, 'UNKNOWN_ACTION')
    result = globals()[action](s, **req)
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        sys.exit(2)
