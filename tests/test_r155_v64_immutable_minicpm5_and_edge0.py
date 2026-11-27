"""R155 static source only; no network, model loading, license granting or weights."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'manifests/drafts/r155-2026-11-22-minicpm5-edge0-immutable-sources.candidate.json'
DECISION = 'catalog/decisions/2026-11-22-r155-v64-small-and-native-4bit-selection.json'


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


from scripts.ledger_history_r168 import historical_117_ledger

class R155ImmutablePublisherReferences(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = load(SOURCE)
        cls.d = load(DECISION)
        cls.models = {m['repo_id']: m for m in cls.s['model_sources']}

    def test_historical_v64_and_prior_receipts_not_double_selected(self):
        history = load('catalog/effective-portfolio-2026-11-22-v64.json')
        self.assertEqual((history['counts']['tracked'], history['counts']['active']), (236, 189))
        current = load('catalog/CURRENT.json')
        self.assertGreaterEqual(current['expected']['tracked'], 236)
        self.assertEqual(self.d['baseline_catalog_revision'], 'v64-20261122')
        self.assertEqual(load('queues/approved.json')['entries'], [])
        reported = {r['repo_id'] for r in historical_117_ledger(load('catalog/execution/2026-11-19-acquisition-ledger.json'))['models'] if r['status'] == 'VERIFIED'}
        self.assertGreaterEqual(len(reported), 112)
        self.assertFalse(reported.intersection(self.models))
        existing = {m['repo_id'] for m in history['items']}
        self.assertFalse(existing.intersection(self.models))
        self.assertIn('qvac/BotPsy-0.8B', existing)
        self.assertIn('robbyant/lingbot-touch-tiny', existing)
        self.assertIn('qvac/BotPsy-0.8B', reported)
        self.assertIn('robbyant/lingbot-touch-tiny', reported)

    def test_three_full_publisher_immutables_byte_and_digest_identity(self):
        expected = {
            'openbmb/MiniCPM5-2B': (11, 5043807977, 1, '42433e90dad95123ab87729fd7011e7110629556'),
            'Edge0/Edge0-120B-NVFP4': (43, 98531583107, 13, 'b0628ee6f3655c40a1afde343d6e265387eea094'),
            'Edge0/Edge0-145B-NVFP4': (43, 113772093975, 14, 'f7a465395af029f3f59a624caefb0fc273988faa'),
        }
        self.assertEqual(set(self.models), set(expected))
        for rid, (count, bytes_, refs, rev) in expected.items():
            m = self.models[rid]
            self.assertEqual((m['published_file_count'], m['published_total_bytes'],
                              m['publisher_lfs_sha256_references'], m['publisher_revision_sha']),
                             (count, bytes_, refs, rev))
            files = m['selected_files']
            self.assertEqual(len(files), count)
            self.assertEqual(len({f['path'].casefold() for f in files}), count)
            self.assertEqual(sum(f['publisher_bytes'] for f in files), bytes_)
            self.assertEqual(sum(bool(f['publisher_lfs_sha256']) for f in files), refs)
            for file in files:
                self.assertRegex(file['publisher_git_blob_oid_sha1'], r'^[a-f0-9]{40}$')
                if file['publisher_lfs_sha256']:
                    self.assertRegex(file['publisher_lfs_sha256'], r'^[a-f0-9]{64}$')
                self.assertFalse(file['owner_local_sha256_verified'])
            self.assertFalse(m['download_approved'])
            self.assertFalse(m['complete_offline_restore_verified'])
        self.assertEqual(self.models['openbmb/MiniCPM5-2B']['publisher_safetensors_elements'], 2516756480)
        self.assertIsNone(self.models['Edge0/Edge0-145B-NVFP4']['publisher_safetensors_elements'])

    def test_edge0_shared_sha_and_inclusive_default_PLE(self):
        s = self.s['edge0_pair_shared_publisher_hashes']
        self.assertEqual(s['identical_paths_count'], 27)
        self.assertEqual(s['identical_publisher_byte_references'], 60467010496)
        self.assertEqual(s['two_full_publisher_repos_reference_bytes'], 212303677082)
        self.assertEqual(s['two_with_perfect_publisher_hash_dedup_reference_bytes'], 151836666586)
        a = self.models['Edge0/Edge0-120B-NVFP4']
        b = self.models['Edge0/Edge0-145B-NVFP4']
        fs_a = {f['path']: f for f in a['selected_files']}
        fs_b = {f['path']: f for f in b['selected_files']}
        self.assertEqual(fs_a['ple-fp8.gguf']['publisher_bytes'], 51200246112)
        self.assertEqual(fs_b['ple-fp8.gguf']['publisher_lfs_sha256'],
                         fs_a['ple-fp8.gguf']['publisher_lfs_sha256'])
        shared = []
        for path in fs_a.keys() & fs_b.keys():
            a_file, b_file = fs_a[path], fs_b[path]
            same = (a_file['publisher_lfs_sha256'] or a_file['publisher_git_blob_oid_sha1']) == (
                b_file['publisher_lfs_sha256'] or b_file['publisher_git_blob_oid_sha1'])
            if same and a_file['publisher_bytes'] == b_file['publisher_bytes']:
                shared.append(a_file['publisher_bytes'])
        self.assertEqual((len(shared), sum(shared)), (27, 60467010496))
        self.assertFalse(s['owner_HDD_shared_presence_and_sha_verified'])
        self.assertFalse(self.d['edge0_full_source_cross_repo_sha_dedup']['physically_available_or_dedup_saved_on_owner_drive'])

    def test_licenses_and_absent_runtime_gate_do_not_turn_to_approval(self):
        self.assertEqual(self.d['permission_separation']['new_approvals'], 0)
        self.assertEqual(self.d['permission_separation']['model_weight_bytes_downloaded_by_review'], 0)
        self.assertFalse(self.d['permission_separation']['custom_model_code_executed'])
        self.assertFalse(self.s['rights_and_abi_gates']['edge_model_param_count_including_PLE_MTP_verified'])
        self.assertFalse(self.s['rights_and_abi_gates']['edge_upstream_qwen_owner_rights_reviewed'])
        self.assertEqual([d['download_enabled'] for d in self.d['decisions']], [False]*3)
        self.assertEqual(self.d['alternative_risks_and_not_selected'][1]['action'],
                         'GATED_HOLD_NO_ACCESS_BYPASS')
        self.assertEqual(self.s['weight_payloads_transferred_by_this_audit'], 0)


if __name__ == '__main__':
    unittest.main()
