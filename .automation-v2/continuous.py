"""Bounded worker self-reports and deterministic continuous health checks.

No network, scheduler, permissions or model routing. Publish every ledger change
as one-parent, non-force control-branch commit and independently read it back.
Prior rolling entries remain in immutable Git commit history. A self-report is
not host launch telemetry, project acceptance, or proof of substantive progress.
"""
import copy
import json
import re
import sys
import controller

TASKS = {
    'kaastumor/morrow-needle': '6abc4ceae8808191b350f310b1363a96',
    'kaastumor/Slavery': '6ab725934774819199a54678f44deae1',
    'kaastumor/Boekanalyse': '6ab725aafd048191ae7a642631f125de',
}
CONTRACT = 'CONTINUOUS_VALIDATION_V1_20261001'
OUTCOMES = {'NO_CHANGE', 'GATED', 'BUSY', 'COMPLETED', 'CHECKPOINTED',
            'BLOCKED', 'FAILED', 'NEEDS_REVIEW'}
CHECKS = {'live_inventory', 'canonical_gate', 'controller_tests',
          'project_tests', 'checkout_hashes', 'target_readback', 'lease_fence'}
FIELDS = {'run_id', 'task_id', 'started_at', 'finished_at', 'outcome',
          'canonical_owner', 'main_head', 'control_ref', 'checks', 'evidence_kind'}

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def initial(repo):
    require(repo in TASKS, 'UNKNOWN_REPOSITORY')
    return dict(schema=1, contract=CONTRACT, repository=repo, runs=[])

def validate_run(repo, run):
    require(isinstance(run, dict) and set(run) == FIELDS, 'UNEXPECTED_RECEIPT_FIELDS')
    require(isinstance(run['run_id'], str) and
            re.fullmatch(r'[A-Za-z0-9_.:-]{1,96}', run['run_id']), 'BAD_RUN_ID')
    require(run['task_id'] == TASKS[repo], 'WRONG_TASK')
    require(type(run['started_at']) is int and type(run['finished_at']) is int and
            0 <= run['started_at'] <= run['finished_at'], 'BAD_CLOCK')
    require(run['outcome'] in OUTCOMES, 'BAD_OUTCOME')
    require(run['evidence_kind'] == 'WORKER_SELF_REPORT', 'BAD_ATTRIBUTION')
    for field in ('main_head', 'control_ref'):
        require(isinstance(run[field], str) and controller.SHA.fullmatch(run[field]), 'BAD_REVISION')
    url = run['canonical_owner']
    require(url is None or (isinstance(url, str) and re.fullmatch(
        r'https://github\.com/' + re.escape(repo) + r'/(?:issues|pull)/[1-9][0-9]*(?:#issuecomment-[0-9]+)?', url)),
        'NONPUBLIC_OWNER')
    require(isinstance(run['checks'], list) and all(isinstance(x, str) for x in run['checks']) and
            len(run['checks']) == len(set(run['checks'])) and set(run['checks']) <= CHECKS, 'BAD_CHECKS')
    require(run['finished_at'] - run['started_at'] <= 1500 or
            run['outcome'] in {'FAILED', 'NEEDS_REVIEW'}, 'OVERRUN_MUST_BE_REPORTED')

def validate(ledger):
    require(isinstance(ledger, dict) and set(ledger) == {'schema', 'contract', 'repository', 'runs'}, 'BAD_LEDGER')
    require(ledger['schema'] == 1 and ledger['contract'] == CONTRACT and ledger['repository'] in TASKS, 'BAD_CONTRACT')
    require(isinstance(ledger['runs'], list) and len(ledger['runs']) <= 24, 'LEDGER_LIMIT')
    ids = set()
    previous_start = -1
    for run in ledger['runs']:
        validate_run(ledger['repository'], run)
        require(run['run_id'] not in ids, 'DUPLICATE_RUN')
        require(run['started_at'] >= previous_start, 'CLOCK_REGRESSION')
        previous_start = run['started_at']
        ids.add(run['run_id'])
    require(len(json.dumps(ledger).encode()) <= 24576, 'LEDGER_LIMIT')

def record(ledger, run):
    validate(ledger)
    validate_run(ledger['repository'], run)
    for old in ledger['runs']:
        if old['run_id'] == run['run_id']:
            require(old == run, 'AMBIGUOUS_RUN_REPLAY')
            return copy.deepcopy(ledger)
    require(not ledger['runs'] or run['started_at'] >= ledger['runs'][-1]['started_at'], 'CLOCK_REGRESSION')
    result = copy.deepcopy(ledger)
    result['runs'] = (result['runs'] + [copy.deepcopy(run)])[-24:]
    validate(result)
    return result

def health(state, ledger, now, *, canonical_issue_closed=False, worker_enabled=True, schedule_finite=False):
    require(type(now) is int and all(type(x) is bool for x in
            (canonical_issue_closed, worker_enabled, schedule_finite)), 'BAD_HEALTH_INPUT')
    controller.validate(state)
    validate(ledger)
    require(state['repository'] == ledger['repository'], 'REPOSITORY_MISMATCH')
    require(now >= state['updated_at'], 'FUTURE_STATE')
    alerts = []
    last = ledger['runs'][-1] if ledger['runs'] else None
    continuity = 'UNVERIFIED'
    if last:
        require(now >= last['finished_at'], 'FUTURE_RECEIPT')
        age = now - last['finished_at']
        continuity = 'PASS' if age <= 7200 else 'FAIL'
        if age > 7200:
            alerts.append('NO_VERIFIED_WORKER_RECEIPT_OVER_2H')
        if last['outcome'] in {'FAILED', 'BLOCKED', 'NEEDS_REVIEW'}:
            alerts.append('WORKER_' + last['outcome'])
    else:
        alerts.append('WORKER_RECEIPT_MISSING')
    if not worker_enabled:
        alerts.append('WORKER_DISABLED')
        continuity = 'FAIL'
    if schedule_finite:
        alerts.append('CONTINUOUS_SCHEDULE_HAS_END')
    if state['state'] in controller.LIVE:
        if now >= state['lease_until']:
            alerts.append('EXPIRED_CLAIM_REQUIRES_RECONCILIATION')
        elif now - state['updated_at'] > 1500:
            alerts.append('LIVE_CLAIM_REPORTING_DEADLINE')
    if canonical_issue_closed and state['state'] in {'BLOCKED', 'WAITING_EXTERNAL', 'NEEDS_REVIEW', 'CHECKPOINTED'}:
        alerts.append('STALE_CHECKPOINT_OWNER_CLOSED')
    if state['operation'] and state['operation']['status'] != 'VERIFIED':
        alerts.append('UNRESOLVED_OPERATION')
    if len({x['id'] for x in state['effects']}) != len(state['effects']):
        alerts.append('DUPLICATE_EFFECT_ID')
    if state['failure_count'] >= 2:
        alerts.append('REPEATED_FAILURE_CUTOFF')
    if len(state['receipts']) >= 14:
        alerts.append('CONTROL_INDEX_NEAR_LIMIT')
    return dict(repository=state['repository'], receipt_continuity=continuity,
                last_outcome=last['outcome'] if last else 'UNKNOWN', alerts=alerts,
                host_launch_reliability='UNVERIFIED', model_cost='UNVERIFIED',
                substantive_autonomy='UNVERIFIED', crash_takeover='UNVERIFIED',
                evidence_kind='READBACK_OF_WORKER_SELF_REPORTS')

if __name__ == '__main__':
    request = json.load(open(sys.argv[1]))
    action = request.pop('action')
    require(action in {'record', 'health'}, 'BAD_ACTION')
    print(json.dumps(globals()[action](**request), sort_keys=True, indent=2))
