"""Verify the exact persisted live-run result, not a recomputed author estimate."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'catalog/research/2026-11-14-pruna-header-census.json'


class PrunaCensusEvidence(unittest.TestCase):
    def setUp(self):
        self.raw = SOURCE.read_bytes()
        self.data = json.loads(self.raw)

    def test_live_artifact_byte_identity(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),
                         'c84574df257007eacd23174df231baa1861186501131a955c71029230e04a809')
        self.assertEqual(self.data['status'], 'HEADER_CENSUS_COMPLETE')
        self.assertEqual(self.data['revision'], '7f98acef503cf2bcfba821a78cb1cf1a9928b2df')
        self.assertEqual(self.data['repo_id'], 'PrunaAI/P-H3-Image')

    def test_all_five_components_and_fifteen_files(self):
        d = self.data
        self.assertEqual(len(d['files']), 15)
        self.assertEqual(len({x['file'] for x in d['files']}), 15)
        expected = {'transformer': (7,33122992896),
                    'text_encoder': (2,4437815808),
                    'prompt_upsampler': (4,9409813744),
                    'text_connector': (1,65576960), 'vae': (1,2599148088)}
        self.assertEqual(set(d['components']), set(expected))
        for name,(n,total) in expected.items():
            rows=[x for x in d['files'] if x['component']==name]
            self.assertEqual(len(rows),n)
            self.assertEqual(sum(x['summary']['stored_elements'] for x in rows),total)
            self.assertEqual(d['components'][name]['stored_elements'],total)
        self.assertEqual(sum(x['summary']['tensor_count'] for x in d['files']),2820)
        self.assertEqual(sum(x['summary']['stored_elements'] for x in d['files']),49635347496)
        self.assertEqual(d['stored_elements_upper_bound'],49635347496)

    def test_byte_accounting_and_actual_metadata_transfer(self):
        d=self.data
        self.assertEqual(sum(x['file_bytes'] for x in d['files']),99797308280)
        self.assertEqual(sum(x['header_metadata_bytes_read'] for x in d['files']),339304)
        self.assertEqual(d['application_metadata_bytes_read'],339304)
        dtype=Counter()
        for row in d['files']:
            summary=row['summary']
            bytes_in_file=row['file_bytes']-row['header_metadata_bytes_read']
            self.assertEqual(bytes_in_file,sum(n*{'BF16':2,'F32':4}[kind]
                             for kind,n in summary['dtype_elements'].items()))
            dtype.update(summary['dtype_elements'])
            self.assertRegex(summary['header_sha256'],r'^[0-9a-f]{64}$')
        self.assertEqual(dtype,{'BF16':49372210504,'F32':263136992})
        self.assertEqual(2*dtype['BF16']+4*dtype['F32'],99796968976)

    def test_no_false_trainable_count_or_acquisition_approval(self):
        d=self.data
        self.assertFalse(d['unique_trainable_parameters_verified'])
        self.assertFalse(d['external_dependency_closure_verified'])
        self.assertFalse(d['full_file_sha256_verified'])
        self.assertFalse(d['catalog_parameter_gate_changed'])
        self.assertFalse(d['download_approved'])
        self.assertTrue(d['stored_elements_include_buffers_and_possible_ties'])
        self.assertEqual(d['tensor_payload_bytes_requested'],0)


if __name__=='__main__':
    unittest.main()
