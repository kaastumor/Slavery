import copy
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Lock
import controller as c

REPO = 'kaastumor/morrow-needle'
HEAD = 'a'*40
REF = 'https://github.com/'+REPO+'/issues/490#issuecomment-123'

class Tests(unittest.TestCase):
    def setUp(self):
        self.s = c.initial(REPO, 1000)
        self.key = c.stage_key(REPO, 490, 'test-stage', HEAD)
    def claim(self, s=None, now=1001, attempt='attempt-a', **kw):
        return c.claim(s or self.s, now, attempt, 490, 'test-stage', HEAD, **kw)
    def active(self):
        return c.start(self.claim(), 1002, 'attempt-a', 1)
    def finish(self, s=None, state='COMPLETE', now=1003):
        return c.finish(s or self.active(), now, 'attempt-a', 1, state,
                        REF, 'Readback PASS; host usage UNKNOWN', 'Resume next accepted dependency')
    def decision(self, s=None, **kw):
        args = dict(ready=True, pending_known=True, interactive_owner=False)
        args.update(kw)
        state = s or self.s
        return c.gate(state, max(1004, state['updated_at']+1), self.key, **args)
    def test_roundtrip_claim_active_checkpoint_resume_complete(self):
        saved = json.loads(json.dumps(self.finish(state='CHECKPOINTED')))
        resumed = self.claim(saved, now=1010, attempt='attempt-b')
        self.assertEqual(resumed['generation'], 2)
        self.assertEqual(resumed['stage']['key'], self.key)
        end = c.finish(resumed, 1011, 'attempt-b', 2, 'COMPLETE', REF, 'PASS', 'Next stage')
        self.assertEqual(self.decision(end), 'ALREADY_COMPLETE')
    def test_complete_does_not_grant_acceptance(self):
        self.assertEqual(self.finish()['checkpoint']['disposition'], 'SEE_CANONICAL_OWNER')
    def test_duplicate_attempt_does_not_duplicate_stage(self):
        self.assertEqual(self.decision(self.finish()), 'ALREADY_COMPLETE')
        with self.assertRaises(c.Refused):
            self.claim(self.finish(), now=1005, attempt='new-attempt')
    def test_busy_predecessor(self):
        self.assertEqual(self.decision(self.active()), 'BUSY')
    def test_crash_expired_lease_cannot_auto_takeover(self):
        s = self.active()
        self.assertEqual(c.gate(s, 2801, self.key, ready=True, pending_known=True,
                               interactive_owner=False), 'RECONCILE_EXPIRED')
        with self.assertRaises(c.Refused): self.claim(s, now=2801, attempt='attempt-b')
    def test_stale_generation_is_fenced(self):
        with self.assertRaisesRegex(c.Refused, 'STALE_OWNER'):
            c.start(self.claim(), 1002, 'attempt-a', 0)
    def test_foreign_owner_is_fenced(self):
        with self.assertRaisesRegex(c.Refused, 'STALE_OWNER'):
            c.start(self.claim(), 1002, 'attempt-b', 1)
    def test_late_owner_cannot_mutate(self):
        with self.assertRaisesRegex(c.Refused, 'LEASE_EXPIRED'):
            c.start(self.claim(), 2801, 'attempt-a', 1)
    def test_unknown_pending_inventory_stops_intake(self):
        self.assertEqual(self.decision(pending_known=False), 'RECONCILE_PENDING')
    def test_interactive_owner_prevents_claim(self):
        self.assertEqual(self.decision(interactive_owner=True), 'INTERACTIVE_OWNER')
    def test_no_work_does_not_make_claim_or_receipt(self):
        before = copy.deepcopy(self.s)
        self.assertEqual(self.decision(ready=False), 'NO_ELIGIBLE_WORK')
        self.assertEqual(self.s, before)
    def test_actual_author_gate_remains_quiet_until_changed(self):
        s = self.finish(state='WAITING_EXTERNAL')
        self.assertEqual(self.decision(s), 'UNCHANGED_GATE')
        self.assertEqual(self.decision(s, dependency_changed=True), 'READY')
    def test_blocked_unchanged_cannot_retry(self):
        self.assertEqual(self.decision(self.finish(state='BLOCKED')), 'UNCHANGED_GATE')
    def test_two_failures_stop_until_prerequisite_changes(self):
        first = self.finish(state='FAILED_RETRYABLE')
        second = self.claim(first, now=1005)
        second = c.finish(second, 1006, 'attempt-a', 2, 'FAILED_RETRYABLE', REF, 'Timeout', 'Retry only after prerequisite changes')
        self.assertEqual(c.gate(second, 1007, self.key, ready=True, pending_known=True, interactive_owner=False), 'RETRY_EXHAUSTED')
        self.assertEqual(c.gate(second, 1007, self.key, ready=True, pending_known=True, interactive_owner=False, dependency_changed=True), 'READY')
    def test_ambiguous_effect_requires_readback_not_replay(self):
        s = c.intent(self.active(), 1003, 'attempt-a', 1, 'op-1', 'branch_edit', 'auto/test', HEAD)
        with self.assertRaisesRegex(c.Refused, 'RECONCILE_OPERATION'):
            self.finish(s, now=1004)
        with self.assertRaisesRegex(c.Refused, 'RECONCILE_OPERATION'):
            c.intent(s, 1004, 'attempt-a', 1, 'op-2', 'draft_pr', 'auto/test', HEAD)
        s = c.verified(s, 1004, 'attempt-a', 1, 'op-1', 'https://github.com/'+REPO+'/commit/'+HEAD)
        self.assertEqual(self.finish(s, now=1005)['state'], 'COMPLETE')
    def test_merge_db_deploy_purchase_are_denied(self):
        for kind in ['merge', 'production_db', 'deploy', 'purchase', 'contact', 'delete']:
            with self.subTest(kind=kind), self.assertRaisesRegex(c.Refused, 'ACTION_NOT_AUTHORIZED'):
                c.intent(self.active(), 1003, 'attempt-a', 1, 'op-1', kind, 'auto/test', HEAD)
    def test_main_targets_denied_all_spellings(self):
        for target in ['main', 'master', 'production', 'heads/main', 'refs/heads/main']:
            with self.subTest(target=target), self.assertRaisesRegex(c.Refused, 'PROTECTED_TARGET'):
                c.intent(self.active(), 1003, 'attempt-a', 1, 'op-1', 'branch_edit', target, HEAD)
    def test_arbitrary_private_output_refs_rejected(self):
        s = c.intent(self.active(), 1003, 'attempt-a', 1, 'op-1', 'issue_checkpoint', 'issue/490', HEAD)
        for output in ['file:///private/manuscript', 'https://evil.test/private', 'https://github.com/'+REPO+'/../../evil', 'source-id-secret']:
            with self.subTest(output=output), self.assertRaisesRegex(c.Refused, 'NONPUBLIC_OUTPUT_REF'):
                c.verified(s, 1004, 'attempt-a', 1, 'op-1', output)
    def test_malformed_state_fails_closed(self):
        for change in [dict(schema=99), dict(repository='other/repo'), dict(state='APPROVED'), dict(generation=-1)]:
            s = dict(self.s, **change)
            with self.subTest(change=change), self.assertRaises(c.Refused): self.decision(s)
    def test_clock_regression_fails_closed(self):
        with self.assertRaisesRegex(c.Refused, 'CLOCK_REGRESSION'):
            c.start(self.claim(), 999, 'attempt-a', 1)
    def test_changed_input_has_distinct_identity(self):
        self.assertNotEqual(self.key, c.stage_key(REPO, 490, 'test-stage', 'b'*40))
    def test_repository_and_contract_identity_isolated(self):
        self.assertNotEqual(self.key, c.stage_key('kaastumor/Slavery', 490, 'test-stage', HEAD))
    def test_index_limit_does_not_discard_unresolved_evidence(self):
        s = self.active()
        s['receipts'] = [dict(key='b'*64, state='BLOCKED', receipt_ref=REF) for _ in range(16)]
        before = copy.deepcopy(s)
        with self.assertRaisesRegex(c.Refused, 'INDEX_FULL'): self.finish(s)
        self.assertEqual(s, before)
    def test_cli_saved_state_resume_and_malformed_request(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)
            (p/'state.json').write_text(json.dumps(self.s))
            req = dict(action='claim', now=1001, attempt='attempt-a', task=490, stage='test-stage', input_revision=HEAD)
            (p/'request.json').write_text(json.dumps(req))
            cmd = [sys.executable, str(pathlib.Path(c.__file__)), str(p/'state.json'), str(p/'request.json')]
            r = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(r.stdout)['state'], 'CLAIMED')
            (p/'request.json').write_text('{"action":"merge"}')
            r = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)
            self.assertEqual(json.loads((p/'state.json').read_text()), self.s)
    def test_simultaneous_claims_one_cas_winner(self):
        # Same-state requests race. State computation is NOT the lock; the CAS is.
        barrier, lock, remote = Barrier(2), Lock(), {'revision': 0, 'state': self.s}
        def contender(attempt):
            expected = remote['revision']
            candidate = self.claim(attempt=attempt)
            barrier.wait()
            with lock:
                if remote['revision'] != expected: return False
                remote.update(revision=expected+1, state=candidate)
                return True
        with ThreadPoolExecutor(2) as pool:
            results = list(pool.map(contender, ['attempt-a', 'attempt-b']))
        self.assertEqual(sum(results), 1)
        self.assertEqual(remote['state']['generation'], 1)

    def test_classifier_strings_cannot_bypass_gate(self):
        with self.assertRaisesRegex(c.Refused, 'BAD_GATE_FLAGS'):
            self.decision(ready='false')
    def test_verified_effect_cannot_replay_after_checkpoint_resume(self):
        s = c.intent(self.active(), 1003, 'attempt-a', 1, 'stable-op-1', 'branch_edit', 'auto/test', HEAD)
        s = c.verified(s, 1004, 'attempt-a', 1, 'stable-op-1', 'https://github.com/'+REPO+'/commit/'+HEAD)
        s = self.finish(s, state='CHECKPOINTED', now=1005)
        s = c.start(self.claim(s, now=1006), 1007, 'attempt-a', 2)
        with self.assertRaisesRegex(c.Refused, 'ALREADY_VERIFIED'):
            c.intent(s, 1008, 'attempt-a', 2, 'stable-op-1', 'branch_edit', 'auto/test', HEAD)
    def test_ref_path_traversal_rejected(self):
        with self.assertRaisesRegex(c.Refused, 'BAD_TARGET'):
            c.intent(self.active(), 1003, 'attempt-a', 1, 'op-1', 'branch_edit', 'auto/../main', HEAD)
    def test_full_index_blocks_before_acquiring_lease(self):
        s = copy.deepcopy(self.s)
        s['receipts'] = [dict(key='b'*64, state='BLOCKED', receipt_ref=REF) for _ in range(16)]
        self.assertEqual(self.decision(s), 'INDEX_FULL')
        with self.assertRaises(c.Refused): self.claim(s)
        self.assertIsNone(s['owner_attempt'])
    def test_compaction_preserves_unresolved_and_current_receipts(self):
        s = self.finish()
        s['receipts'].extend([dict(key='b'*64, state='COMPLETE', receipt_ref=REF), dict(key='c'*64, state='BLOCKED', receipt_ref=REF)])
        x = c.compact(s, 1004, 'https://github.com/'+REPO+'/blob/'+HEAD+'/.automation-v2/state.json')
        self.assertEqual([r['state'] for r in x['receipts']], ['COMPLETE', 'BLOCKED'])
        self.assertEqual(self.decision(x), 'CHECK_ARCHIVED_RECEIPTS')
        self.assertEqual(self.decision(x, archive_checked=True), 'ALREADY_COMPLETE')
    def test_unpinned_compaction_is_refused(self):
        with self.assertRaisesRegex(c.Refused, 'UNPINNED_ARCHIVE'):
            c.compact(self.finish(), 1004, 'https://github.com/'+REPO+'/blob/main/.automation-v2/state.json')
    def test_compaction_cannot_change_active_worker(self):
        with self.assertRaisesRegex(c.Refused, 'BUSY'):
            c.compact(self.active(), 1004, 'https://github.com/'+REPO+'/blob/'+HEAD+'/.automation-v2/state.json')

if __name__ == '__main__':
    unittest.main(verbosity=2)
