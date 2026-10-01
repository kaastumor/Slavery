import copy
import unittest
import controller
import continuous as c

REPO = 'kaastumor/morrow-needle'

class ContinuousTests(unittest.TestCase):
    def setUp(self):
        self.ledger = c.initial(REPO)
        self.state = controller.initial(REPO, 100)
        self.run = dict(run_id='native-test-1', task_id=c.TASKS[REPO], started_at=100,
                        finished_at=110, outcome='GATED', canonical_owner=f'https://github.com/{REPO}/issues/511',
                        main_head='a'*40, control_ref='b'*40, checks=['live_inventory', 'canonical_gate'],
                        evidence_kind='WORKER_SELF_REPORT')
    def populated(self):
        return c.record(self.ledger, self.run)
    def health(self, **kw):
        return c.health(self.state, self.populated(), 120, **kw)
    def test_gated_run_is_observable_without_claiming_progress(self):
        h = self.health()
        self.assertEqual(h['receipt_continuity'], 'PASS')
        self.assertEqual(h['substantive_autonomy'], 'UNVERIFIED')
        self.assertEqual(h['alerts'], [])
    def test_no_change_is_not_missed_run(self):
        self.run['outcome'] = 'NO_CHANGE'
        self.assertEqual(self.health()['last_outcome'], 'NO_CHANGE')
    def test_missing_receipt_is_unknown(self):
        h = c.health(self.state, self.ledger, 120)
        self.assertEqual(h['receipt_continuity'], 'UNVERIFIED')
        self.assertIn('WORKER_RECEIPT_MISSING', h['alerts'])
    def test_two_hour_gap_fails(self):
        self.assertEqual(c.health(self.state, self.populated(), 7311)['receipt_continuity'], 'FAIL')
    def test_exact_two_hour_boundary(self):
        self.assertEqual(c.health(self.state, self.populated(), 7310)['receipt_continuity'], 'PASS')
    def test_exact_replay_is_idempotent(self):
        x = self.populated()
        self.assertEqual(c.record(x, self.run), x)
    def test_changed_replay_is_refused(self):
        x = self.populated()
        self.run['outcome'] = 'COMPLETED'
        with self.assertRaisesRegex(ValueError, 'AMBIGUOUS_RUN_REPLAY'): c.record(x, self.run)
    def test_rolling_limit_retains_latest_24(self):
        x = self.ledger
        for i in range(30):
            r = dict(self.run, run_id=f'run-{i}', started_at=100+i, finished_at=110+i)
            x = c.record(x, r)
        self.assertEqual(len(x['runs']), 24)
        self.assertEqual(x['runs'][0]['run_id'], 'run-6')
    def test_clock_regression_rejected(self):
        x = self.populated()
        r = dict(self.run, run_id='run-2', started_at=99)
        with self.assertRaisesRegex(ValueError, 'CLOCK_REGRESSION'): c.record(x, r)
    def test_negative_duration_rejected(self):
        self.run['finished_at'] = 99
        with self.assertRaisesRegex(ValueError, 'BAD_CLOCK'): self.populated()
    def test_overrun_cannot_be_pass(self):
        self.run['finished_at'] = 1700
        with self.assertRaisesRegex(ValueError, 'OVERRUN'): self.populated()
        self.run['outcome'] = 'NEEDS_REVIEW'
        self.assertEqual(len(self.populated()['runs']), 1)
    def test_private_or_cross_repository_owner_rejected(self):
        for url in ['file:///private/manuscript', 'https://github.com/other/repo/issues/1']:
            self.run['canonical_owner'] = url
            with self.assertRaisesRegex(ValueError, 'NONPUBLIC_OWNER'): self.populated()
    def test_extra_content_field_rejected(self):
        self.run['source_text'] = 'must never enter ledger'
        with self.assertRaisesRegex(ValueError, 'UNEXPECTED_RECEIPT_FIELDS'): self.populated()
    def test_synthetic_receipt_cannot_claim_host_telemetry(self):
        self.run['evidence_kind'] = 'HOST_VERIFIED'
        with self.assertRaisesRegex(ValueError, 'BAD_ATTRIBUTION'): self.populated()
    def test_wrong_task_rejected(self):
        self.run['task_id'] = c.TASKS['kaastumor/Slavery']
        with self.assertRaisesRegex(ValueError, 'WRONG_TASK'): self.populated()
    def test_future_receipt_rejected(self):
        with self.assertRaisesRegex(ValueError, 'FUTURE_RECEIPT'): c.health(self.state, self.populated(), 105)
    def test_stale_closed_blocker_detected(self):
        self.state['state'] = 'BLOCKED'
        self.assertIn('STALE_CHECKPOINT_OWNER_CLOSED', self.health(canonical_issue_closed=True)['alerts'])
    def test_completed_closed_stage_is_not_stale(self):
        self.state['state'] = 'COMPLETE'
        self.assertNotIn('STALE_CHECKPOINT_OWNER_CLOSED', self.health(canonical_issue_closed=True)['alerts'])
    def test_expired_claim_never_changes_owner(self):
        self.state = controller.claim(self.state, 100, 'attempt-1', 511, 'bounded-stage', 'a'*40)
        before = copy.deepcopy(self.state)
        h = c.health(self.state, self.populated(), 1900)
        self.assertIn('EXPIRED_CLAIM_REQUIRES_RECONCILIATION', h['alerts'])
        self.assertEqual(self.state, before)
    def test_duplicate_effect_id_detected(self):
        self.state['effects'] = [{'id':'effect-1'}, {'id':'effect-1'}]
        self.assertIn('DUPLICATE_EFFECT_ID', self.health()['alerts'])
    def test_unresolved_effect_detected(self):
        self.state['operation'] = {'status':'INTENDED'}
        self.assertIn('UNRESOLVED_OPERATION', self.health()['alerts'])
    def test_disabled_or_finite_schedule_detected(self):
        h = self.health(worker_enabled=False, schedule_finite=True)
        self.assertEqual(h['receipt_continuity'], 'FAIL')
        self.assertIn('CONTINUOUS_SCHEDULE_HAS_END', h['alerts'])
    def test_failure_report_alerts(self):
        self.run['outcome'] = 'FAILED'
        self.assertIn('WORKER_FAILED', self.health()['alerts'])
    def test_telemetry_remains_unknown(self):
        h = self.health()
        for key in ('host_launch_reliability','model_cost','crash_takeover'):
            self.assertEqual(h[key], 'UNVERIFIED')

if __name__ == '__main__': unittest.main()
