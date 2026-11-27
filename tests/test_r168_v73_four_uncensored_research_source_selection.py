"""Publisher source audit and decision tests (metadata only, no HF tensor imports)."""
import json,re,unittest
from pathlib import Path
from scripts.ledger_history_r168 import historical_116_receipts,current_133_reported_or_more
ROOT=Path(__file__).resolve().parents[1]
def J(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class R168UncensoredTrainedStateStudy(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=J('manifests/drafts/r168-2026-11-27-four-small-uncensored-source-frozen.candidate.json')
  cls.dec=J('catalog/decisions/2026-11-27-r168-v73-small-uncensored-priority-and-false-approval-repair.json')
  cls.q=J('queues/proposed-v73-r168-four-small-uncensored-ranked-UNAPPROVED.json')
  cls.ledger=J('catalog/execution/2026-11-19-acquisition-ledger.json')
  cls.c=J('catalog/CURRENT.json')
  cls.v=J(cls.c['materialized_catalog_path'])
 def test_canonical_old_265_211_133_reported_plus_no_new_approval(self):
  self.assertEqual((self.c['revision_id'],self.c['expected']['tracked'],self.c['expected']['active']),('v73-20261125',265,211))
  self.assertEqual((self.ledger['summary']['models_verified'],self.ledger['summary']['files_verified_total'],self.ledger['summary']['bytes_verified_total']),(133,2095,2451205481822))
  self.assertTrue(current_133_reported_or_more(self.ledger))
  self.assertEqual(len(historical_116_receipts(self.ledger)),116)
  self.assertEqual(J('queues/approved.json')['entries'],[])
  self.assertTrue(self.dec['previous_catalogue_265_assets_unmodified'])
  self.assertFalse(self.src['owner_local_SHA_now_verified'])
  self.assertEqual(self.dec['weight_bytes_transferred'],0)
 def test_exact53_per_file_publisher_git_sha_lfs_sha_and_bytes(self):
  rows=self.src['research_sources']
  spec=[
   ('Peymandc/MiniCPM5-1B-Uncensored-Flawless-Peymandc','f6d05b4391b4a35b3b07a31f3d36e70e34fd5834','apache-2.0',16,2174627424,1080632832),
   ('NuclearDorfus/Luciole-1B-Instruct-1.1-Heretic','b5e8bf34650ec6fc0aed2028758791905cef74cf','apache-2.0',8,2648259206,1319309312),
   ('Peymandc/LFM3-1.7B-Heretic-Uncensored','72c1fa3b225c4663f9de0a682d6909cc14599125','other',19,3476041387,1728801536),
   ('Sussysam/Qwen3-4B-Instruct-2507-heretic','1df0100e297aa073f65e9295054e3ce235800f27','apache-2.0',10,8056453418,4022468096)]
  self.assertEqual(self.src['publisher_file_count'],53)
  self.assertEqual(self.src['publisher_reference_bytes'],16355381435)
  self.assertEqual(len(rows),4)
  for row,(name,sha,license,n,bytes_,params) in zip(rows,spec):
   self.assertEqual((row['repo_id'],row['publisher_revision_sha'],row['license_metadata'],row['publisher_file_count'],row['publisher_full_source_bytes'],row['publisher_stored_safetensors_elements']),(name,sha,license,n,bytes_,params))
   self.assertFalse(row['gated'])
   self.assertEqual(len(row['publisher_files']),n)
   self.assertEqual(sum(z['bytes'] for z in row['publisher_files']),bytes_)
   self.assertEqual(len({z['path'] for z in row['publisher_files']}),n)
   for z in row['publisher_files']:
    self.assertTrue(re.fullmatch(r'[0-9a-f]{40}',z['publisher_git_blob_sha1']))
    if z['publisher_lfs_sha256']:self.assertTrue(re.fullmatch(r'[0-9a-f]{64}',z['publisher_lfs_sha256']))
    self.assertFalse(z['owner_SHA_verified'])
   for flag in ('owner_download_approved','publisher_code_executed','local_disk_SHA_verified','owner_license_acts_reviewed','full_offline_restore_verified','independent_neutral_benchmark_reproduced'):
    self.assertFalse(row[flag])
 def test_MiniCPM_parent_133_verified_exact_replay_rev_and_trained_state_different(self):
  mini=self.src['research_sources'][0]
  parent=self.src['parent_source_references'][0]
  self.assertEqual(mini['parent_repo_id'],'openbmb/MiniCPM5-1B')
  self.assertEqual(mini['parent_training_sha'],'ac83f813ba7da263c51a9f3ec37c2072597e54af')
  self.assertEqual((parent['publisher_revision_sha'],parent['report_revision_sha']),(mini['parent_training_sha'],mini['parent_training_sha']))
  self.assertTrue(parent['report_in_133_receipts'])
  self.assertNotEqual(mini['trained_weight_files'][0]['lfs_sha256'],parent['trained_weight_refs'][0]['sha256'])
  self.assertEqual(mini['reproduce_strategy'],'merge')
  self.assertEqual((mini['trials'],mini['ARA_rank']),(1000,50))
  self.assertEqual((mini['author_refusal_keyword_count_parent'],mini['author_refusal_keyword_count_edited']),(81,3))
  self.assertEqual(mini['author_KL'],0.007)
  self.assertFalse(parent['owner_device_SHA_independently_verified'])
 def test_Luciole_and_LFM_license_abi_quality_hold_no_hidden_promotion(self):
  luc,lmf=self.src['research_sources'][1:3]
  self.assertEqual(luc['parent_repo_id'],'OpenLLM-France/Luciole-1B-Instruct-1.1')
  self.assertFalse(self.src['parent_source_references'][1]['report_in_133_receipts'])
  self.assertEqual(luc['author_KL'],0.4199)
  self.assertEqual((luc['author_refusal_keyword_count_parent'],luc['author_refusal_keyword_count_edited']),(100,0))
  self.assertTrue(luc['no_model_repository_LICENSE_file'])
  self.assertEqual(lmf['license_name'],'lfm1.0')
  self.assertEqual(lmf['license_metadata'],'other')
  self.assertTrue({'modeling_lfm3.py','lfm3_conv.py','configuration_lfm3.py'}.issubset(set(lmf['custom_model_python_files'])))
  self.assertEqual(lmf['author_KL'],0.0732)
  self.assertFalse(self.src['parent_source_references'][2]['report_in_133_receipts'])
 def test_Qwen_4B_high_divergence_and_redundant_full_model_rejected(self):
  q=self.src['research_sources'][3]
  self.assertEqual(q['author_KL'],1.5593)
  self.assertEqual(q['publisher_full_source_bytes'],8056453418)
  self.assertTrue(q['no_model_repository_LICENSE_file'])
  self.assertIn('REJECT',q['research_decision'])
  self.assertNotIn(q['repo_id'],{x['repo_id'] for x in self.v['items']})
  self.assertNotIn(q['repo_id'],{x['repo_id'] for x in self.ledger['models']})
 def test_queue_P0_and_strict_unapproved_governance(self):
  a=self.q
  self.assertEqual(a['P0_source_file_count'],16)
  self.assertEqual(a['P0_full_source_reference_bytes'],2174627424)
  self.assertEqual(a['publisher_full_file_refs'],53)
  self.assertEqual(a['publisher_all_source_reference_bytes'],16355381435)
  self.assertEqual([x['rank'] for x in a['priority_rows']],[0,1,2,3])
  self.assertEqual([x['action'].split('_')[0] for x in a['priority_rows']],['P0','P1','P2','REJECT'])
  self.assertTrue(a['parent_MiniCPM5_1B_reported_acquired_before_this_study'])
  self.assertFalse(a['download_enabled'] or a['approved_by_user'] or a['license_review_done'])
  self.assertFalse(a['owner_live_disk_SHA_verified'] or a['offline_wheelhouse_and_runtime_verified'])
  self.assertEqual(a['explicit_user_authorizations_added'],0)
  self.assertEqual(a['full_model_payload_transferred_bytes_now'],0)
if __name__=='__main__':unittest.main()
