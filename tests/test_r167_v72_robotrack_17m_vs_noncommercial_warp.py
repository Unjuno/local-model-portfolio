"""R167 publisher provenance: no network, no checkpoint load, no privileged execution."""
import json,re,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(p):return json.loads((R/p).read_text(encoding='utf-8'))
class R167RoboTrackStudy(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=J('catalog/CURRENT.json')
  cls.v=J(cls.c['materialized_catalog_path'])
  cls.m=J('manifests/drafts/r167-2026-11-25-robotracker17m-vs-warp-nc-publisher-source-frozen.candidate.json')
  cls.d=J('catalog/decisions/2026-11-25-r167-v72-robotracker-small-vs-warp-source-adjudication.json')
  cls.q=J('queues/proposed-v72-r167-robotrack-two-independent-specialists-UNAPPROVED.json')
  cls.l=J('catalog/execution/2026-11-19-acquisition-ledger.json')
 def test_canonical_v72_and_owner_authorizations_unchanged(self):
  self.assertEqual((self.c['revision_id'],self.c['expected']['tracked'],self.c['expected']['active']),('v72-20261125',264,210))
  self.assertEqual((self.c['expected']['by_decision']['select'],self.c['expected']['by_decision']['conditional'],self.c['expected']['by_decision']['hold']),(56,154,35))
  self.assertEqual(len(self.v['items']),264)
  self.assertEqual((self.l['summary']['models_verified'],self.l['summary']['files_verified_total'],self.l['summary']['bytes_verified_total']),(116,1758,2021784002725))
  self.assertEqual(J('queues/approved.json')['entries'],[])
  self.assertEqual(self.d['new_owner_signed_approvals'],0)
  self.assertEqual(self.d['weights_downloaded_now'],0)
  self.assertFalse(self.q['download_enabled'] or self.q['approved_by_user'])
  self.assertFalse(self.m['download_enabled'] or self.m['approved_by_user'])
  self.assertTrue(self.d['existing_264_assets_preserved'] and self.d['existing_210_active_assets_preserved'])
 def test_both_frozen_first_party_checkpoint_bytes_git_blob_and_lfs_sha(self):
  s=self.m['source_models']
  self.assertEqual(len(s),2)
  specs=[
   ('allenai/RoboTracker','3bda363815dca4395b855ba0e7737517300f937f','apache-2.0',66011293,66004399,
    'robotracker.pth','d846b841b698a772bff681b7c1d5446f11ff5e9c4e0371bfa171190b1c7805b8'),
   ('allenai/RoboTracker-Warp','6cf4ddd90571b5e5bb269cf6cfb6112b91e66ec8','cc-by-nc-4.0',3898587949,3898580646,
    'robotracker_warp.pth','6a45fc269a227dbb87f9aab8cc8efc43eba77113ac891f6156db9834b1b3830c')]
  for row,(name,revision,lic,tot,wsize,wname,sha) in zip(s,specs):
   self.assertEqual((row['repo_id'],row['revision_sha'],row['publisher_license_tag'],row['source_total_bytes'],row['publisher_weight_file_bytes'],row['weight_file_path'],row['publisher_weight_sha256']),(name,revision,lic,tot,wsize,wname,sha))
   self.assertEqual(len(row['source_files']),3)
   self.assertEqual(sum(f['bytes'] for f in row['source_files']),tot)
   self.assertEqual({x['path'] for x in row['source_files']},{'.gitattributes','README.md',wname})
   self.assertTrue(row['publisher_repo_has_no_LICENSE_file'])
   self.assertTrue(re.fullmatch(r'[0-9a-f]{40}',revision))
   self.assertTrue(re.fullmatch(r'[0-9a-f]{64}',sha))
   for f in row['source_files']:
    self.assertTrue(re.fullmatch(r'[0-9a-f]{40}',f['publisher_git_blob_sha1']))
    if f['publisher_lfs_sha256']:self.assertTrue(re.fullmatch(r'[0-9a-f]{64}',f['publisher_lfs_sha256']))
    self.assertFalse(f['owner_actual_sha_verified'])
   for k in ('weight_downloaded_by_this_research','download_approved','owner_local_sha_verified','full_offline_runtime_verified','owner_license_use_acts_verified','untrusted_pth_code_executed'):
    self.assertFalse(row[k])
  self.assertEqual(self.m['publisher_all_source_files_total'],6)
  self.assertEqual(self.m['publisher_all_model_repo_bytes_total'],3964599242)
 def test_training_parent_original_sha_different_small_is_not_GGUF_conversion(self):
  x=self.m['source_models'][0]
  p=self.m['parent_original_AllTracker']
  self.assertEqual(p['repo_id'],'aharley/alltracker')
  self.assertEqual(p['revision_sha'],'c8ba31225828cab9ec512d0627f0f826e641a877')
  self.assertEqual(p['license'],'mit')
  self.assertEqual(p['publisher_alltracker_pth_weight_sha256'],'ffd9ebcfb6d206d594b646999a150540f92c049cf9b2bf940facf7123f62aa1d')
  self.assertNotEqual(x['publisher_weight_sha256'],p['publisher_alltracker_pth_weight_sha256'])
  self.assertTrue(x['edited_weight_distinct_from_parent'])
  self.assertFalse(x['alltracker_training_parent_weights_required_for_full_finetune_inference'])
  self.assertFalse(p['owner_original_parent_download_performed'])
 def test_git_code_all56_and_selected19_license_boundary(self):
  s=self.m['publisher_runtime_source']
  self.assertEqual(s['revision_sha'],'fc5cd87f60fad57c7cbc48c3d09e9aa7b45061a3')
  self.assertEqual(s['git_tree_sha'],'4d44877a3a9c127ce0089a1d2acd0022d8184bed')
  self.assertEqual((s['tracked_blobs_all_count'],s['tracked_blobs_all_bytes']),(56,1907536))
  self.assertEqual((s['selected_deploy_code_file_count'],s['selected_deploy_code_bytes']),(19,164989))
  self.assertEqual(sum(x['bytes'] for x in s['tracked_blobs_all']),1907536)
  self.assertEqual(sum(x['bytes'] for x in s['selected_deploy_code_files']),164989)
  allp={x['path'] for x in s['tracked_blobs_all']}
  smallp={x['path'] for x in s['selected_deploy_code_files']}
  self.assertTrue(smallp.issubset(allp))
  self.assertTrue({'LICENSE','pyproject.toml','robotrack/alltracker/LICENSE','robotrack/alltracker/net.py','robotrack/eval_alltracker.py','robotrack/hub.py','robotrack/evaluate.py','robotrack/metrics.py'}.issubset(smallp))
  self.assertFalse(any(p.startswith('robotrack/cowtracker/') for p in smallp))
  self.assertTrue(s['pyproject_project_combined_licenses_must_act_review'])
  self.assertTrue(s['publisher_small_code_torch_load_weights_only'])
  self.assertEqual(s['python_min'],'3.10')
  self.assertEqual(s['pytorch_min'],'2.1')
  self.assertEqual((s['warp_torch'],s['warp_torchvision'],s['warp_xformers']),('2.10.0','0.25.0','0.0.34'))
  for f in s['tracked_blobs_all']:
   self.assertTrue(re.fullmatch(r'[0-9a-f]{40}',f['git_blob_sha1']))
   self.assertGreaterEqual(f['bytes'],0)
  self.assertFalse(s['owner_code_runtime_executed'])
  self.assertFalse(s['wheelhouse_offline_closed'])
 def test_quality_disclaimer_resolution_and_nc_Warp_hardware_hold(self):
  x,y=self.m['source_models']
  self.assertEqual((x['publisher_RoboTrack_Bench_AJ'],x['publisher_original_AllTracker_Bench_AJ']),(63.40,62.56))
  self.assertEqual((x['publisher_RoboTAP_AJ'],x['publisher_original_AllTracker_RoboTAP_AJ']),(68.41,68.48))
  self.assertIn('384x512',x['benchmark_protocol'])
  self.assertEqual((y['publisher_RoboTrack_Bench_AJ'],y['publisher_original_CoWTracker_Bench_AJ']),(65.98,63.87))
  self.assertIn('336x560',y['benchmark_protocol'])
  self.assertTrue(y['requires_FAIR_Noncommercial_Research_License_code'])
  self.assertEqual(y['noncommercial_weight_license'],'CC-BY-NC 4.0')
  self.assertTrue(y['CUDA_xformers_torch_exact_abi_needed'])
  self.assertEqual(self.d['decisions'][0]['recommended_next_formal_decision'],'CONDITIONAL_FIRST_BEFORE_WARP')
  self.assertEqual(self.d['decisions'][1]['recommended_next_formal_decision'],'HOLD_NONCOMMERCIAL_PARENT_ABI_GPU')
 def test_dataset_source_is_metadata_only_and_licenses_do_not_propagate(self):
  d=self.m['benchmark_reproducibility_dataset_references']
  self.assertEqual(len(d),2)
  self.assertEqual([(x['repo_id'],x['license_tag'],x['publisher_reported_video_clips']) for x in d],
                   [('allenai/RoboTrack-Bench','other',307),('allenai/RoboTrack-15M','odc-by',3000)])
  self.assertEqual([x['revision_sha'] for x in d],['bb275295d5f616260df87dda32f0362108736340','157e5aebfc0eda97da6046dbd668fdfeeca2bc06'])
  self.assertTrue(all(not x['full_dataset_video_hash_scopes_pinned'] and not x['individual_video_rights_and_person_privacy_verified'] and not x['download_approved'] for x in d))
  self.assertTrue(self.q['benchmark_dataset_307_videos_rights_other_do_not_download'])
  self.assertTrue(self.q['training_dataset_3000_videos_odc_by_separate_legal_review'])
 def test_review_queue_source_scope_cost_and_full_stop(self):
  q=self.q
  self.assertEqual(q['current_canonical_revision_unchanged'],'v72-20261125')
  self.assertEqual(q['source_repos_count'],2)
  self.assertEqual(q['publisher_model_source_files'],6)
  self.assertEqual(q['tiny_prioritized_publisher_repo_bytes'],66011293)
  self.assertEqual(q['tiny_model_plus_lean_runtime_publisher_reference_bytes'],66176282)
  self.assertEqual(q['all_repo_code_git_blobs_sha_frozen'],56)
  self.assertEqual([x['priority'] for x in q['priority_research_rows']],[0,2])
  self.assertTrue(all(not item['new_download_approved'] for item in q['priority_research_rows']))
  self.assertEqual(q['approved_queue_entries_added'],0)
  self.assertEqual(q['weight_bytes_downloaded_in_this_research'],0)
  self.assertFalse(q['owner_Windows_D_actual_SHA_rehashed'])
  self.assertFalse(q['Python_checkpoint_and_model_code_executed'])
  self.assertTrue(q['parent_AllTracker_full_weights_must_not_be_duplicated_for_running_full_checkpoint'])
  self.assertFalse(self.m['formal_catalog_promotion_performed'])
if __name__=='__main__':unittest.main()
