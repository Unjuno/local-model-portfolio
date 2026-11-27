"""R167 source-only Unbound v2.1 trained-stage selection. Offline stdlib, never execute untrusted code."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
M='manifests/drafts/r167-2026-11-25-inkling2-mini-unbound-v21-compact-3stage-replay-scope.candidate.json'
V='catalog/revisions/v73-2026-11-25.json'
E='catalog/effective-portfolio-2026-11-25-v73.json'
Q='queues/proposed-v73-2026-11-25.json'
R='catalog/readiness/v73-2026-11-25-r167-all211-gates.json'
A='catalog/access/2026-11-25-v73-conditional-hub-gates.json'
P='catalog/preparation/2026-11-25-insurance-bundles-v73.json'

from scripts.ledger_history_r168 import historical_117_ledger

class R167V73(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=read(M);cls.v=read(V);cls.e=read(E);cls.c=read('catalog/snapshots/v73-2026-11-25-current.json')
  cls.q=read(Q);cls.r=read(R);cls.a=read(A);cls.p=read(P)
  cls.old=read('catalog/effective-portfolio-2026-11-25-v72.json')

 def test_98_files_three_pages_and_16_fixed_replay_files(self):
  meta=self.m['all_publisher_source_metadata'];src=self.m['selected_replay_scope']
  self.assertEqual((meta['pages_fetched'],meta['file_count'],meta['repo_bytes'],meta['publisher_lfs_sha_refs']),(3,98,20696238628,39))
  self.assertEqual(len(meta['files']),98)
  self.assertEqual(len({x['path'] for x in meta['files']}),98)
  self.assertEqual(sum(x['bytes'] for x in meta['files']),20696238628)
  self.assertEqual((src['files_count'],src['publisher_reference_bytes']),(16,141452942))
  self.assertEqual(sum(x['bytes'] for x in src['files']),141452942)
  self.assertEqual(sum(x['bytes'] for x in src['files'] if x['path'].endswith('.safetensors')),140060248)
  paths={x['path'] for x in src['files']}
  self.assertTrue({'abliteration/edit.pt','abliteration/apply_edit.py','finetune/lora_v2.safetensors','finetune_v2.1/lora_v2.1.safetensors', 'finetune_v2.1/MANIFEST.json','README.md'} <= paths)
  self.assertNotIn('model-00001-of-00001.safetensors',paths)
  self.assertNotIn('mtp.safetensors',paths)
  self.assertNotIn('lora_v2.1/peft-r64/adapter_model.safetensors',paths)
  for f in meta['files']:
   self.assertRegex(f['git_blob_sha1'],r'^[a-f0-9]{40}$')
   sha=f['publisher_lfs_sha256'];self.assertTrue(sha is None or re.fullmatch(r'^[a-f0-9]{64}$',sha))
  self.assertFalse(src['estimated_reconstruction_deterministic_or_bit_exact_verified'])

 def test_parent_116_reported_compatible_sha_not_owner_local(self):
  ledger=historical_117_ledger(read('catalog/execution/2026-11-19-acquisition-ledger.json'))
  receipts={x['repo_id']:x for x in ledger['models'] if x['status']=='VERIFIED'}
  self.assertEqual(len(receipts),116)
  self.assertIn('thinkingmachines/Inkling-2-Mini',receipts)
  self.assertNotIn(self.m['source_original_repo'],receipts)
  p=self.m['upstream_parent_conformance']
  self.assertEqual(p['author_training_parent_revision'],'ed40e7da625f594fc9c4990f5f66be24873c22d7')
  self.assertEqual(receipts['thinkingmachines/Inkling-2-Mini']['revision_sha'],p['historical_verified_parent_receipt_revision'])
  self.assertEqual(p['same_file_git_oid_count'],13)
  self.assertTrue(p['same_model_and_MTP_tokenizer_LFS_SHA'])
  self.assertTrue(p['publisher_comparison_not_owner_disk_actual_SHA'])

 def test_old264_unchanged_and_new_only_one_trained_state(self):
  self.assertEqual(self.c['revision_id'],'v73-20261125')
  self.assertEqual(self.e['items'][:264],self.old['items'])
  self.assertEqual(self.e['items'][264:],self.v['additions'])
  self.assertEqual((len(self.e['items']),self.e['counts']['tracked'],self.e['counts']['active'],self.e['counts']['models']),(265,265,211,239))
  self.assertEqual(self.e['counts']['by_decision']['conditional'],155)
  self.assertEqual(self.e['counts']['by_decision']['hold'],35)
  self.assertEqual(self.e['counts']['by_decision']['select'],56)
  self.assertEqual(self.c['ordered_overlays'][-1],V)
  self.assertEqual(self.v['added_assets'],['nokeepai/Inkling-2-Mini-Unbound'])
  self.assertEqual(self.e['items'][-1]['candidate_selected_source_file_bytes'],141452942)
  self.assertFalse(self.e['items'][-1]['download_ready'])
  self.assertFalse(self.e['items'][-1]['download_approved'])
  self.assertFalse(self.e['items'][-1]['dependencies_reviewed'])
  self.assertFalse(self.e['items'][-1]['license_text_reviewed'])

 def test_211_eligible_status_all_stop_access_preparation_join(self):
  sel={x['repo_id'] for x in self.e['items'] if x['portfolio_decision'] in ('select','conditional')}
  conditional={x['repo_id'] for x in self.e['items'] if x['portfolio_decision']=='conditional'}
  self.assertEqual(len(sel),211);self.assertEqual(len(conditional),155)
  self.assertEqual({x['repo_id'] for x in self.q['candidates']},sel)
  self.assertEqual({x['repo_id'] for x in self.r['records']},sel)
  self.assertEqual({x['repo_id'] for x in self.p['items']},sel)
  self.assertEqual({x['repo_id'] for x in self.a['entries']},conditional)
  self.assertEqual(self.r['summary']['blocked_any'],211)
  self.assertEqual(self.r['summary']['ready_to_approve'],0)
  self.assertEqual(self.r['summary']['downloads_approved'],0)
  self.assertTrue(all(not x['ready_to_acquire'] and not x['download_approved'] for x in self.r['records']))
  self.assertFalse(self.q['download_enabled']);self.assertFalse(self.a['download_authorized']);self.assertFalse(self.p['download_enabled'])
  self.assertEqual(self.a['gated_count'],21)
  self.assertEqual(read('queues/approved.json')['entries'],[])
  self.assertEqual(read('catalog/snapshots/v73-2026-11-25-readiness-current.json')['catalog_revision'],'v73-20261125')
  self.assertEqual(read('catalog/snapshots/v73-2026-11-25-estimates-current.json')['portfolio_revision'],'v73-20261125')

 def test_approx_peft_is_not_executable_exact_checkpoint(self):
  a=self.m['nonselected_alternatives']
  self.assertEqual(a[0]['kind'],'full_merged_native_source')
  self.assertFalse(a[0]['download_selected'])
  self.assertEqual(a[1]['kind'],'PEFT_r64_SVD_approximation')
  self.assertEqual(a[1]['publisher_reference_bytes'],140030976)
  self.assertFalse(a[1]['bit_exact_full_edited_state'])
  self.assertFalse(self.m['upstream_publisher_code']['full_software_dependency_wheelhouse_abi_verified'])
  self.assertFalse(self.m['license_and_AUP_review']['owner_specific_acts_license_and_AUP_signoff'])
  self.assertFalse(self.m['current_action']['download_approved'])
  self.assertFalse(self.m['current_action']['weight_payload_downloaded'])

if __name__=='__main__':unittest.main()
