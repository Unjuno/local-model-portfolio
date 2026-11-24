"""R151 v64: immutable publisher metadata, unique specialist and zero approvals.
Offline unit tests. Do not retrieve or run model weights.
"""
import collections,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def L(path):return json.loads((R/path).read_text(encoding='utf-8'))
class R151BisonOriginalSelection(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=L('catalog/CURRENT.json')
  cls.old=L('catalog/effective-portfolio-2026-11-22-v63.json')
  cls.new=L('catalog/effective-portfolio-2026-11-22-v64.json')
  cls.ov=L('catalog/revisions/v64-2026-11-22.json')
  cls.source=L('manifests/drafts/r151-2026-11-22-baseten-bison-and-groundhog-frozen.candidate.json')
  cls.ready=L('catalog/readiness/v64-2026-11-22-r151-all189-gates.json')
  cls.acc=L('catalog/access/2026-11-22-v64-conditional-hub-gates.json')
  cls.q=L('queues/proposed-v64-2026-11-22.json')
  cls.post=L('queues/proposed-v64-r152-post99-13-plus-bison-research-only.json')
  cls.drift=L('catalog/research/2026-11-22-r151-publisher-revision-drift-after99.json')
 def test_canonical_latest_all_235_unchanged(self):
  self.assertIn('catalog/revisions/v64-2026-11-22.json',self.c['ordered_overlays'])
  self.assertIn(self.c['revision_id'],('v64-20261122','v65-20261122', 'v66-20261124','v67-20261124',"v68-20261125","v69-20261125","v70-20261125", "v71-20261125"))
  self.assertEqual(self.new['revision_id'],'v64-20261122')
  self.assertEqual(self.old['items'],self.new['items'][:235])
  self.assertEqual(len(self.new['items']),236)
  self.assertEqual(len({(x['asset_kind'],x['repo_id']) for x in self.new['items']}),236)
  self.assertEqual((self.new['counts']['tracked'],self.new['counts']['active'],self.new['counts']['models'],self.new['counts']['datasets']),(236,189,210,26))
  self.assertEqual((self.new['counts']['by_decision']['select'],self.new['counts']['by_decision']['conditional']),(55,134))
  for k in ('tracked','active','models','datasets','by_decision','by_tier','by_forecast_wave','parameter_gate','resource_screen'):
   self.assertEqual(self.c['expected'][k],L(self.c['materialized_catalog_path'])['counts'][k])
  self.assertEqual(self.c['expected']['budget_scenario'],L(self.c['materialized_catalog_path'])['budget'])
 def test_full_repo_immutable_16_file_publisher_BF16_and_license(self):
  self.assertEqual(self.source['selected_original'],'baselabs/bison-1')
  self.assertEqual(self.source['selected_all_publisher_source_bytes'],65398108261)
  self.assertEqual(self.source['selected_all_publisher_source_files'],16)
  self.assertEqual(self.source['selected_file_LFS_SHA256_count'],4)
  b,g=self.source['sources']
  self.assertEqual((b['repo_id'],b['revision_sha']),('baselabs/bison-1','bf8350b2c59eb6c36e95d02a2af870aec18724a7'))
  self.assertEqual((g['repo_id'],g['revision_sha']),('baselabs/groundhog-1','f4602c43599114a7af2c158472b59a4ff2d13663'))
  self.assertEqual(g['publisher_source_bytes'],53120939617)
  self.assertEqual(self.source['gated_small_comparator']['gated'],'manual')
  self.assertEqual(self.source['gated_small_comparator']['decision'],'RESEARCH_HOLD_NEEDS_OWNER_ENTITLEMENT_NO_BYPASS')
  for x in (b,g):
   self.assertEqual(len(x['files']),16)
   self.assertEqual(sum(t['bytes'] for t in x['files']),x['publisher_source_bytes'])
   self.assertEqual(len(set(t['path'] for t in x['files'])),16)
   self.assertTrue({'LICENSE','NOTICE','model.safetensors.index.json','model-00001-of-00002.safetensors','model-00002-of-00002.safetensors'}.issubset({t['path'] for t in x['files']}))
   self.assertFalse(x['download_approved'])
   for t in x['files']:
    self.assertEqual(len(t['publisher_git_blob_sha1']),40)
    if t['publisher_lfs_sha256']:self.assertEqual(len(t['publisher_lfs_sha256']),64)
    self.assertFalse(t['owner_local_sha_verified'])
 def test_new_model_selected_but_not_acquisition_ready(self):
  x=self.new['items'][-1];z=self.ov['additions'][0]
  self.assertEqual(x,z)
  self.assertEqual((x['repo_id'],x['portfolio_decision'],x['risk_tier']),('baselabs/bison-1','conditional','R2'))
  self.assertEqual((x['candidate_selected_source_file_count'],x['candidate_selected_source_file_bytes']),(16,65398108261))
  self.assertEqual(x['parameter_gate']['total_parameters'],31273086512)
  self.assertEqual(x['parameter_gate']['BF16_stored_tensor_elements'],32682375020)
  self.assertTrue(x['research_only_nonexecutable'])
  for flag in ('download_approved','download_ready','can_enter_approved_queue','model_payload_fetched','personal_access_verified','license_text_reviewed','dependencies_reviewed'):
   self.assertFalse(x[flag])
  self.assertIsNone(x['selected_file_bytes'])
  self.assertIsNone(x['fully_pinned_revision_sha'])
  self.assertEqual((self.ov['previous_asset_count'],self.ov['previous_active_count'],self.ov['added_assets'],self.ov['removed_assets'],self.ov['changed_prior_decisions']),(235,188,1,0,0))
 def test_189_active_all_blocked_same_IDs_across_ledgers(self):
  ids={(x['asset_kind'],x['repo_id']) for x in self.new['items'] if x['portfolio_decision'] in ('select','conditional')}
  self.assertEqual(len(ids),189)
  self.assertEqual(ids,{(x['asset_kind'],x['repo_id']) for x in self.ready['records']})
  self.assertEqual(ids,{(x['asset_kind'],x['repo_id']) for x in self.q['candidates']})
  prep=L('catalog/preparation/2026-11-22-insurance-bundles-v64.json')
  self.assertEqual(ids,{(x['asset_kind'],x['repo_id']) for x in prep['items']})
  self.assertEqual((self.ready['summary']['tracked'],self.ready['summary']['blocked_any'],self.ready['summary']['conditional']),(236,189,134))
  self.assertEqual(self.ready['summary']['ready_to_approve'],0)
  self.assertEqual(self.ready['summary']['downloads_approved'],0)
  self.assertFalse(self.ready['ready_to_acquire'])
  self.assertFalse(self.q['download_enabled'])
  self.assertFalse(prep['download_enabled'])
  self.assertTrue(all(not x['download_approved'] and not x['ready_to_acquire'] for x in self.ready['records']))
  self.assertEqual(dict(collections.Counter(g for x in self.ready['records'] for g in x['blocking_gates'])),self.ready['summary']['blocking_gate_counts'])
 def test_all_conditional_access_134_no_new_gated(self):
  self.assertEqual(self.acc['source_revision'],'v64-20261122')
  self.assertEqual((self.acc['scope'],self.acc['tracked_conditional'],self.acc['gated_count']),(134,134,21))
  self.assertEqual(len(self.acc['entries']),134)
  self.assertFalse(self.acc['download_authorized'])
  x=next(e for e in self.acc['entries'] if e['repo_id']=='baselabs/bison-1')
  self.assertIs(x['hub_gated'],False)
  self.assertFalse(x['download_authorized'])
  self.assertFalse(x['owner_license_rights_verified'])
 def test_99_ledger_already_acquired_stays_unmodified_and_not_approved(self):
  ledger=L('catalog/execution/2026-11-19-acquisition-ledger.json')
  rep={x['repo_id'] for x in ledger['models'] if x['status']=='VERIFIED'}
  self.assertGreaterEqual(len(rep),99)
  self.assertIn('baselabs/bison-1',rep)
  self.assertTrue({'baselabs/bison-1','Qwen/Qwen3.5-0.8B'}.issubset(rep))
  self.assertEqual(L('queues/approved.json')['entries'],[])
  self.assertFalse(self.source['metadata_only_no_weight_payload_fetched'] is False)
  self.assertFalse(self.ov['approved_downloads_added'])
  self.assertEqual(self.ov['new_weight_payloads_downloaded'],0)
 def test_next_research_source_join_and_phase_totals(self):
  old=L('queues/proposed-v63-r150-after99-13-research-only.json')
  for revised,historic in zip(self.post['candidate_research_only'][:13],old['candidate_research_only']):
   for key,value in historic.items():
    self.assertEqual(revised[key],value, (historic['repo_id'],key))
  self.assertEqual(self.post['candidate_repo_count'],14)
  self.assertEqual(self.post['nonhold_candidate_repos'],13)
  self.assertEqual(self.post['nonhold_publisher_reference_bytes'],75155724960+65398108261)
  self.assertEqual(self.post['phase_summary']['P2_MID_SPECIALIZED_ABI_REVIEW']['source_repos'],3)
  self.assertEqual(sum(x['publisher_reference_bytes'] for x in self.post['candidate_research_only'] if x['phase']!='P3_LARGE_RESEARCH_HOLD'),self.post['nonhold_publisher_reference_bytes'])
  self.assertEqual(self.post['candidate_research_only'][-1]['repo_id'],'baselabs/bison-1')
  self.assertTrue(all(not x['download_approved'] for x in self.post['candidate_research_only']))
 def test_r149_only_LFM3_parent_rev_drift_no_training_weight_mutation(self):
  z=[x for x in self.drift['checks'] if x['revision_changed']]
  self.assertEqual(len(self.drift['checks']),11)
  self.assertEqual(len(z),1)
  self.assertEqual(z[0]['repo_id'],'LiquidAI/LFM3-VL-2B')
  self.assertEqual(z[0]['frozen_revision'],'f83d2b0a2296aaa277f394990a9b8b949ddf9691')
  self.assertEqual(z[0]['current_revision'],'23387beda43c60310348e83e25f78f33c3140d3a')
  self.assertFalse(z[0]['changed_weight_sha256'])
  self.assertNotIn('model.safetensors',{x['path'] for x in z[0]['changes']})
  self.assertTrue(z[0]['silent_repin_forbidden'])
 def test_all_latest_pointers_align_and_never_claim_live_hdd(self):
  self.assertIn(L('catalog/readiness/CURRENT.json')['catalog_revision'],('v64-20261122','v65-20261122', 'v66-20261124','v67-20261124',"v68-20261125","v69-20261125","v70-20261125", "v71-20261125"))
  self.assertIn(L('catalog/estimates/CURRENT.json')['portfolio_revision'],('v64-20261122','v65-20261122', 'v66-20261124','v67-20261124',"v68-20261125","v69-20261125","v70-20261125", "v71-20261125"))
  self.assertEqual(L(self.c['latest_active_readiness_audit']['summary_path'])['summary']['active'],self.c['expected']['active'])
  self.assertFalse(self.new['budget']['physical_capacity_verified'])
  self.assertIsNone(self.new['budget']['owner_actual_free_bytes'])
  self.assertEqual(self.new['budget']['v64_new_download_reservation_approved_bytes'],0)
  self.assertEqual(len(L(self.c['priority_worklist_path'])['candidates']),self.c['expected']['active'])
if __name__=='__main__':unittest.main()
