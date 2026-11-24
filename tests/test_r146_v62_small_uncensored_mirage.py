"""Offline v62 source identity, learned-state uniqueness, parent/Heretic, runtime and STOP."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def L(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class V62Portfolio(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=L('catalog/CURRENT.json')
  cls.old=L('catalog/effective-portfolio-2026-11-22-v61.json')
  cls.e=L('catalog/effective-portfolio-2026-11-22-v62.json')
  cls.d=L('catalog/revisions/v62-2026-11-22.json')
  cls.m=L('manifests/drafts/r146-2026-11-22-aurora-mirage-lfm3-paired-source.candidate.json')
  cls.q=L('queues/proposed-v62-2026-11-22.json')
  cls.a=L('catalog/access/2026-11-22-v62-conditional-hub-gates.json')
  cls.p=L('catalog/preparation/2026-11-22-insurance-bundles-v62.json')
  cls.r=L('catalog/readiness/v62-2026-11-22-r146-all184-gates.json')
  cls.triage=L('queues/proposed-v62-r147-post96-next-research-sources.json')
  cls.decision=L('catalog/decisions/2026-11-22-r146-v62-original-and-heretic-selection.json')
 def test_current_and_original227_immutable(self):
  self.assertIn(self.c['revision_id'],('v62-20261122','v63-20261122','v64-20261122','v65-20261122', 'v66-20261124','v67-20261124',"v68-20261125","v69-20261125","v70-20261125"))
  self.assertIn('catalog/revisions/v62-2026-11-22.json',self.c['ordered_overlays'])
  self.assertIn(self.c['materialized_catalog_path'],('catalog/effective-portfolio-2026-11-22-v62.json','catalog/effective-portfolio-2026-11-22-v63.json','catalog/effective-portfolio-2026-11-22-v64.json','catalog/effective-portfolio-2026-11-22-v65.json', 'catalog/effective-portfolio-2026-11-24-v66.json','catalog/effective-portfolio-2026-11-24-v67.json',"catalog/effective-portfolio-2026-11-25-v68.json","catalog/effective-portfolio-2026-11-25-v69.json","catalog/effective-portfolio-2026-11-25-v70.json"))
  self.assertEqual(self.old['items'],self.e['items'][:227])
  self.assertEqual(len(self.e['items']),231)
  self.assertEqual(self.d['previous_asset_count'],227)
  self.assertEqual(self.d['previous_active_count'],180)
  self.assertEqual([x['repo_id'] for x in self.e['items'][-4:]],[x['repo_id'] for x in self.d['additions']])
  self.assertEqual(len({(x['asset_kind'],x['repo_id']) for x in self.e['items']}),231)
  self.assertEqual(self.e['counts']['tracked'],231)
  self.assertEqual(self.e['counts']['active'],184)
  self.assertEqual(self.e['counts']['models'],205)
  self.assertEqual(self.e['counts']['datasets'],26)
  self.assertEqual(self.e['counts']['by_decision']['conditional'],131)
  self.assertEqual(self.e['counts']['by_decision']['select'],53)
  self.assertEqual(self.e['counts']['parameter_gate']['PASS_TOTAL_PARAMS_LT_150B'],178)
  self.assertEqual(self.e['counts']['parameter_gate']['UNVERIFIED_BLOCK_FINAL_LOCK'],25)
  for k in ('tracked','active','models','datasets','by_tier','by_decision','by_forecast_wave','parameter_gate','resource_screen'):
   if self.c['revision_id']=='v62-20261122':
    self.assertEqual(self.c['expected'][k],self.e['counts'][k])
   else:
    self.assertIn('catalog/revisions/v62-2026-11-22.json',self.c['ordered_overlays'])
  if self.c['revision_id']=='v62-20261122':self.assertEqual(self.c['expected']['budget_scenario'],self.e['budget'])
 def test_publisher_58_9_lfs_and_formats(self):
  self.assertEqual(self.m['model_repo_count'],4)
  self.assertEqual(self.m['selected_files_count'],58)
  self.assertEqual(self.m['selected_source_bytes'],11026306599)
  self.assertEqual(self.m['selected_lfs_sha256_count'],9)
  self.assertEqual(self.d['publisher_selected_file_refs'],58)
  self.assertEqual(self.d['publisher_selected_source_bytes'],11026306599)
  count=bytes_=lfs=0
  for source,a in zip(self.m['publisher_sources'],self.d['additions']):
   self.assertEqual(len(source['immutable_revision_sha']),40)
   self.assertFalse(source['repo_gated'])
   self.assertFalse(source['repo_private'])
   self.assertFalse(source['download_approved'])
   self.assertFalse(a['download_approved'])
   self.assertTrue(a['research_only_nonexecutable'])
   self.assertFalse(a['download_ready'])
   self.assertEqual(source['publisher_selected_files_count'],len(source['publisher_selected_files']))
   self.assertEqual(source['publisher_selected_bytes'],sum(x['bytes'] for x in source['publisher_selected_files']))
   self.assertEqual(source['publisher_selected_bytes'],a['candidate_selected_source_file_bytes'])
   count+=len(source['publisher_selected_files'])
   bytes_+=source['publisher_selected_bytes']
   lfs+=source['publisher_selected_lfs_sha256_count']
   for f in source['publisher_selected_files']:
    self.assertEqual(len(f['git_blob_sha1']),40)
    if f['publisher_lfs_sha256']:self.assertEqual(len(f['publisher_lfs_sha256']),64)
    self.assertFalse(f['local_sha256_verified'])
  self.assertEqual((count,bytes_,lfs),(58,11026306599,9))
  aurora=self.m['publisher_sources'][0]
  self.assertEqual(len(aurora['not_selected_duplicate_formats_or_nonessential']),16)
  self.assertIn('model.safetensors',[x['path'] for x in aurora['publisher_selected_files']])
  self.assertFalse(any(x['path'].startswith(('fp16/','bf16/')) for x in aurora['publisher_selected_files']))
  heretic=self.m['publisher_sources'][-1]
  formats=[x['path'] for x in heretic['publisher_selected_files']]
  self.assertIn('model.safetensors',formats)
  self.assertIn('LFM3-VL-2B-heretic-Q4_K_M.gguf',formats)
  self.assertIn('LFM3-VL-2B-heretic-mmproj-F16.gguf',formats)
  self.assertEqual(len(heretic['not_selected_duplicate_formats_or_nonessential']),14)
 def test_training_parent_sha_different_and_cactus_runtime_pinned(self):
  relation=self.m['source_relation_compare']
  self.assertEqual(relation['official_LFM3_VL_parent_training_revision'],'f83d2b0a2296aaa277f394990a9b8b949ddf9691')
  self.assertNotEqual(relation['parent_weight_lfs_sha256'],relation['heretic_weight_lfs_sha256'])
  self.assertTrue(relation['training_parent_official_same_weight_sha_as_latest'])
  self.assertGreater(relation['shared_identical_publisher_reference_bytes'],10000000)
  self.assertFalse(relation['owner_local_shared_files_sha_checked'])
  runtime=self.m['cactus_engine_required_for_mirage']
  self.assertEqual(runtime['runtime_version'],'4.1.4')
  self.assertEqual(runtime['selected_runtime_files_bytes'],4137947)
  self.assertEqual(len(runtime['windows_x86_64_and_linux_x86_64_runtime_file_refs']),5)
  self.assertTrue(any(x['path'].endswith('windows-x86_64/cactus.exe') for x in runtime['windows_x86_64_and_linux_x86_64_runtime_file_refs']))
  self.assertTrue(runtime['owner_Windows_D_runtime_binary_untrusted_not_executed'])
  self.assertIsNone(self.d['additions'][1]['parameter_gate']['total_parameters'])
  self.assertEqual(self.d['additions'][1]['parameter_gate']['status'],'UNVERIFIED_BLOCK_FINAL_LOCK')
 def test_all_184_active_fail_closed_and_131_access(self):
  active={(x['asset_kind'],x['repo_id']) for x in self.e['items'] if x['portfolio_decision'] in ('conditional','select')}
  conditional={(x['asset_kind'],x['repo_id']) for x in self.e['items'] if x['portfolio_decision']=='conditional'}
  self.assertEqual(len(active),184)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in self.q['candidates']},active)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in self.r['records']},active)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in self.p['items']},active)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in self.a['entries']},conditional)
  self.assertEqual(self.a['gated_count'],21)
  self.assertEqual(self.r['summary']['blocked_any'],184)
  self.assertEqual(self.r['summary']['unknown_total_active'],12)
  self.assertEqual(self.r['summary']['ready_to_approve'],0)
  self.assertEqual(self.r['summary']['downloads_approved'],0)
  self.assertFalse(self.q['approved'])
  self.assertFalse(self.q['download_enabled'])
  self.assertFalse(self.p['download_enabled'])
  self.assertFalse(self.r['ready_to_acquire'])
  self.assertEqual(L('queues/approved.json')['entries'],[])
  self.assertEqual(L('catalog/readiness/CURRENT.json')['catalog_revision'],self.c['revision_id'])
  self.assertEqual(L('catalog/estimates/CURRENT.json')['portfolio_revision'],self.c['revision_id'])
 def test_post96_research_priority_no_double_fetch(self):
  ledger=L('catalog/execution/2026-11-19-acquisition-ledger.json')
  self.assertGreaterEqual(ledger['summary']['models_verified'],96)
  self.assertEqual(len(self.triage['future_research_queue']),11)
  self.assertEqual(self.triage['nonhold_source_repos'],10)
  self.assertEqual(self.triage['nonhold_publisher_reference_bytes'],68544170933)
  self.assertEqual(self.triage['large_Ripple_HOLD_bytes'],129572889973)
  self.assertEqual(self.triage['additional_Cactus_4_1_4_runtime_reference_bytes_not_in_10_source_bytes'],4137947)
  self.assertFalse(self.triage['download_controls']['approved'])
  self.assertFalse(self.triage['download_controls']['download_enabled'])
  self.assertEqual(len(self.decision['decisions']),4)
  self.assertEqual(self.decision['execution']['approved_queue_entries'],0)
if __name__=='__main__':unittest.main()
