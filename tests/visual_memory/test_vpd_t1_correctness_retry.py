"""Scope checks are not aesthetic or glyph-recognition oracles."""
import json
import unittest
from pathlib import Path
from visual_memory.vpd_p6_composition_state import validate_t1_retry_record

ROOT = Path(__file__).resolve().parents[2]


class T1RetryTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / 'evidence/vpd/p1_typography_repair_v1/T1_TECHNICAL_RETRY_RECEIPT_20260914.json').read_text(encoding='utf-8'))

    def test_scope_valid_does_not_mean_human_pass(self):
        validate_t1_retry_record(self.record)
        self.assertIsNone(self.record['post_retry_human_verdict'])

    def test_budget_cannot_expand(self):
        self.record['technical_retries_used']['豆坊'] = 2
        with self.assertRaises(Exception):
            validate_t1_retry_record(self.record)

    def test_failure_cannot_become_pass(self):
        self.record['original_title_gate'] = 'PASS'
        with self.assertRaises(Exception):
            validate_t1_retry_record(self.record)

    def test_t2_stays_closed(self):
        self.record['T2_allowed'] = True
        with self.assertRaises(Exception):
            validate_t1_retry_record(self.record)

    def test_candidate1_cannot_be_modified(self):
        self.record['mutated_glyphs'].append('53:6')
        with self.assertRaises(Exception):
            validate_t1_retry_record(self.record)

    def test_unverified_export_rejected(self):
        self.record['exports'][0]['metadata_readback_verified'] = False
        with self.assertRaises(Exception):
            validate_t1_retry_record(self.record)

    def test_stop_rule_required(self):
        self.record['on_repeat_glyph_failure'] = 'RETRY'
        with self.assertRaises(Exception):
            validate_t1_retry_record(self.record)


if __name__ == '__main__':
    unittest.main()
