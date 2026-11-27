"""R158: metadata-only original source selection. No network or model loading."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST='manifests/drafts/r158-2026-11-24-minicpm5-kolibri-stage-fixed.candidate.json'
DECISION='catalog/decisions/2026-11-24-r158-v66-mini-final-base-kolibri-selection.json'
QUEUE='queues/proposed-v66-r158-three-new-originals-UNAPPROVED.json'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf8'))

from scripts.ledger_history_r168 import historical_117_ledger

class R158Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=load(MANIFEST)
        cls.d=load(DECISION)
        cls.q=load(QUEUE)
        cls.sources={x['repo_id']:x for x in cls.m['frozen_new_original_source_repos']}

    def test_baseline_and_receipt_reuse_without_new_transfer(self):
        cur=load('catalog/CURRENT.json')
        catalog=load('catalog/effective-portfolio-2026-11-24-v66.json')
        ledger=historical_117_ledger(load('catalog/execution/2026-11-19-acquisition-ledger.json'))
        self.assertGreaterEqual(cur['expected']['tracked'],246)
        self.assertEqual((catalog['counts']['tracked'],catalog['counts']['active']),(246,197))
        self.assertEqual(ledger['summary']['models_verified'],116)
        prev={x['repo_id'] for x in catalog['items']}
        acquired={x['repo_id'] for x in ledger['models'] if x['status']=='VERIFIED'}
        self.assertEqual(len(acquired),116)
        self.assertTrue(acquired.issubset(prev))
        self.assertTrue(self.sources.keys().isdisjoint(prev))
        self.assertTrue(self.sources.keys().isdisjoint(acquired))
        self.assertEqual(self.d['canonical']['tracked'],246)
        self.assertEqual(self.d['latest_acquired_ledger']['models_verified'],116)
        self.assertTrue(self.d['latest_acquired_ledger']['all_reported_repo_IDs_matched_current_catalog'])
        self.assertEqual(load('queues/approved.json')['entries'],[])
        self.assertEqual(self.q['prior_116_receipts_reacquire_count'],0)

    def test_three_fixed_source_tree_shapes_and_digests(self):
        specs={
            'openbmb/MiniCPM5-2B':('42433e90dad95123ab87729fd7011e7110629556',11,5043807977,1,1),
            'openbmb/MiniCPM5-2B-Base':('e09861095569642c3cf632d80e3200ee1d30b547',10,5043780610,1,1),
            'Aleph-Alpha/Kolibri-1.1':('bfc33150d363f55a86cd4f0f7f79711deb9e0361',42,77556017718,32,31)
        }
        self.assertEqual(set(specs),set(self.sources))
        for rid,(rev,n,bytes_,sha_n,weight_n) in specs.items():
            src=self.sources[rid]
            self.assertEqual(src['revision_sha'],rev)
            self.assertEqual((src['published_files_count'],src['published_all_file_bytes'],src['publisher_lfs_sha256_refs'],src['model_weight_file_count']),
                             (n,bytes_,sha_n,weight_n))
            fs=src['files']
            self.assertEqual(len(fs),n)
            self.assertEqual(sum(f['bytes'] for f in fs),bytes_)
            self.assertEqual(len({f['path'].casefold() for f in fs}),n)
            for f in fs:
                self.assertRegex(f['git_blob_sha1'],r'^[0-9a-f]{40}$')
                if f['publisher_lfs_sha256'] is not None:self.assertRegex(f['publisher_lfs_sha256'],r'^[0-9a-f]{64}$')
                self.assertIs(f['local_sha256_verified'],False)
                self.assertIs(f['file_present_on_owner_HDD'],None)
            self.assertFalse(src['user_download_approved'])
            self.assertFalse(src['offline_restore_abi_verified'])
        self.assertEqual((self.q['total_referenced_files'],self.q['total_referenced_bytes'],self.q['total_publisher_lfs_refs']),
                         (63,87643606305,34))
        self.assertEqual(self.m['exact_review_scope']['publisher_reference_bytes'],87643606305)

    def test_four_mini_training_stages_are_different_weight_sha(self):
        stages=self.m['model_stage_relations']['MiniCPM5_2B_trajectory']
        self.assertEqual(len(stages),4)
        alt={x['repo_id']:x for x in self.m['frozen_provenance_alternatives_research_only']}
        d={**self.sources,**alt}
        digests=[d[p]['trained_weight_lfs_sha256_ids'][0] for p in stages]
        self.assertEqual(len(set(digests)),4)
        self.assertTrue(all(re.fullmatch(r'[a-f0-9]{64}',x) for x in digests))
        self.assertFalse(self.m['model_stage_relations']['base_is_proven_uncensored'])
        self.assertFalse(self.d['priority_decisions'][1]['independent_benchmark_complete'])

    def test_kolibri_parameter_discrepancy_and_non_executable_policy(self):
        k=self.m['Kolibri']
        self.assertEqual(k['first_party_card_total_parameters'],75128393984)
        self.assertEqual(k['official_hub_safetensors_stored_elements'],75112665344)
        self.assertEqual(k['unresolved_count_difference'],15728640)
        self.assertTrue(k['first_party_license_file_present'])
        self.assertFalse(k['owner_real_runtime_memory_validated'])
        self.assertTrue(self.m['approval_and_rights']['owner_D_rehash_not_done'])
        self.assertTrue(self.m['approval_and_rights']['all_user_approval_flags_false'])
        self.assertEqual(self.d['real_user_approval_gate']['new_entries_created'],0)
        self.assertFalse(self.d['real_user_approval_gate']['weight_download_enabled'])
        self.assertEqual(self.d['this_turn_models_downloaded'],0)
        self.assertFalse(self.d['third_party_model_code_executed'])
        self.assertEqual(len(self.d['alternatives_held']),6)

if __name__=='__main__':unittest.main()
