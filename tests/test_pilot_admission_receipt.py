import copy
import json
import unittest
from tools import verify_pilot_admission_receipt as verifier


class PilotAdmissionReceiptTests(unittest.TestCase):
    def test_independent_readback_and_dependency_tamper(self):
        receipt = json.loads(verifier.RECEIPT.read_text(encoding='utf-8'))
        self.assertEqual(verifier.verify(receipt), 494)
        bad = copy.deepcopy(receipt)
        evidence = bad['independent_readback']['cases'][0]['evidence'][0]
        evidence['locator'] = 'unsupported replacement locator'
        with self.assertRaisesRegex(ValueError, 'source/locator binding'):
            verifier.verify(bad)

    def test_wrong_dimension_is_rejected(self):
        receipt = json.loads(verifier.RECEIPT.read_text(encoding='utf-8'))
        external = next(row for row in receipt['independent_readback']['cases']
                        if row['claim']['claim_kind_code'] == 'external_participation')
        external['territorial'] = {'practice_level_code': 'P4'}
        with self.assertRaisesRegex(ValueError, 'dimension separation'):
            verifier.verify(receipt)
