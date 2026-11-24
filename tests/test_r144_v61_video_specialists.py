"""Offline v61 publisher identity, trained-state differentiation, shared parents, and acquisition STOP."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def L(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class V61VisualAudit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=L('catalog/CURRENT.json');cls.old=L('catalog/effective-portfolio-2026-11-22-v60.json')
  cls.e=L('catalog/effective-portfolio-2026-11-22-v61.json')
  cls.ov=L('catalog/revisions/v61-2026-11-22.json')
  cls.m=L('manifests/drafts/r144-2026-11-22-video-world-and-streaming-publisher-sources.candidate.json')
  cls.q=L('queues/proposed-v61-2026-11-22.json')
  cls.a=L('catalog/access/2026-11-22-v61-conditional-hub-gates.json')
  cls.p=L('catalog/preparation/2026-11-22-insurance-bundles-v61.json')
  cls.r=L('catalog/readiness/v61-2026-11-22-r144-all180-gates.json')
  cls.next=L('queues/proposed-v61-r145-post96-next-research-sources.json')
  cls.decision=L('catalog/decisions/2026-11-22-r144-v61-new-visual-capabilities.json')
 def test_canonical_and_prior224_unchanged(self):
  self.assertIn(self.c['revision_id'],('v61-20261122','v62-20261122','v63-20261122','v64-20261122','v65-20261122', 'v66-20261124','v67-20261124',"v68-20261125","v69-20261125","v70-20261125", "v71-20261125", "v72-20261125", "v73-20261125"))
  self.assertIn('catalog/revisions/v61-2026-11-22.json',self.c['ordered_overlays'])
  self.assertIn(self.c['materialized_catalog_path'],('catalog/effective-portfolio-2026-11-22-v61.json','catalog/effective-portfolio-2026-11-22-v62.json','catalog/effective-portfolio-2026-11-22-v63.json','catalog/effective-portfolio-2026-11-22-v64.json','catalog/effective-portfolio-2026-11-22-v65.json', 'catalog/effective-portfolio-2026-11-24-v66.json','catalog/effective-portfolio-2026-11-24-v67.json',"catalog/effective-portfolio-2026-11-25-v68.json","catalog/effective-portfolio-2026-11-25-v69.json","catalog/effective-portfolio-2026-11-25-v70.json", "catalog/effective-portfolio-2026-11-25-v71.json","catalog/effective-portfolio-2026-11-25-v72.json","catalog/effective-portfolio-2026-11-25-v73.json"))
  self.assertEqual(self.old['items'],self.e['items'][:224])
  self.assertEqual(len(self.e['items']),227)
  self.assertEqual(self.ov['previous_asset_count'],224)
  self.assertEqual(self.ov['previous_active_count'],177)
  self.assertEqual([x['repo_id'] for x in self.ov['additions']],[x['repo_id'] for x in self.e['items'][-3:]])
  self.assertEqual(len({(x['asset_kind'],x['repo_id']) for x in self.e['items']}),227)
  self.assertEqual(self.e['counts']['tracked'],227)
  self.assertEqual(self.e['counts']['active'],180)
  self.assertEqual(self.e['counts']['models'],201)
  self.assertEqual(self.e['counts']['datasets'],26)
  self.assertEqual(self.e['counts']['by_decision']['conditional'],127)
  self.assertEqual(self.e['counts']['by_decision']['select'],53)
  self.assertEqual(self.e['counts']['parameter_gate']['UNVERIFIED_BLOCK_FINAL_LOCK'],24)
  self.assertEqual(self.e['counts']['parameter_gate']['PASS_TOTAL_PARAMS_LT_150B'],175)
  for k in ('tracked','active','models','datasets','by_tier','by_decision','by_forecast_wave','parameter_gate','resource_screen'):
   if self.c['revision_id']=='v61-20261122':
    self.assertEqual(self.e['counts'][k],self.c['expected'][k])
   else:
    self.assertIn('catalog/revisions/v61-2026-11-22.json',self.c['ordered_overlays'])
  if self.c['revision_id']=='v61-20261122':self.assertEqual(self.c['expected']['budget_scenario'],self.e['budget'])
 def test_exact_publisher70_selected_and_dependency_hash(self):
  self.assertEqual((self.m['source_repos'],self.m['full_publisher_file_refs'],self.m['full_publisher_repo_bytes']),(3,93,56364757204))
  self.assertEqual((self.m['selected_file_refs'],self.m['selected_source_bytes'],self.m['selected_lfs_sha256_refs']),(70,55385946049,16))
  self.assertEqual((self.ov['publisher_source_files_selected'],self.ov['publisher_selected_bytes']),(70,55385946049))
  self.assertEqual([a['repo_id'] for a in self.ov['additions']],['apple/FastFrames-S','OpenMOSS-Team/MOSS-VL-Realtime','nvidia/Cosmos3-Nano-Sim-Transfer'])
  counts=bytes_=hashes=0
  for obj,add in zip(self.m['publisher_model_sources'],self.ov['additions']):
   self.assertEqual(len(obj['immutable_revision_sha']),40)
   self.assertFalse(obj['publisher_access']['gated'])
   self.assertFalse(obj['publisher_access']['private'])
   self.assertEqual(sum(x['bytes'] for x in obj['selected_files']),obj['selected_file_bytes'])
   self.assertEqual(len(obj['selected_files']),obj['selected_file_count'])
   self.assertEqual(add['candidate_selected_source_file_bytes'],obj['selected_file_bytes'])
   self.assertFalse(obj['owner_local_sha_verified'])
   counts+=len(obj['selected_files']);bytes_+=obj['selected_file_bytes']
   hashes+=sum(bool(x['publisher_lfs_sha256']) for x in obj['selected_files'])
   for f in obj['selected_files']:
    self.assertEqual(len(f['git_blob_sha1']),40)
    if f['publisher_lfs_sha256']:self.assertEqual(len(f['publisher_lfs_sha256']),64)
    self.assertFalse(f['local_sha256_verified'])
  self.assertEqual((counts,bytes_,hashes),(70,55385946049,16))
  f=self.m['parent_dependencies']['apple_FastFrames_S']
  self.assertEqual(f['frozen_two_step_generator']['file']['bytes'],5676220819)
  self.assertEqual(f['frozen_two_step_generator']['file']['publisher_lfs_sha256'],'8f899a016dffb9539788fac82c6200e43ef6e23b6e61ec6b885bb507a760ce42')
  self.assertEqual(f['wan_text_encoder_tokenizer_vae']['required_selected_bytes'],11891015130)
  self.assertEqual(f['parent_source_reference_bytes_not_verified_on_owner_HDD'],17567235949)
  vae=self.m['parent_dependencies']['nvidia_Cosmos3_Nano_Sim_Transfer']
  self.assertEqual(vae['publisher_VAE_bytes_potential_reuse'],1409400600)
  self.assertFalse(vae['owner_VAE_local_presence_and_SHA_verified'])
  self.assertEqual(len(vae['identical_to_two_selected_models']),2)
  self.assertEqual(vae['identical_publisher_VAE_source']['publisher_lfs_sha256'],'230496cb59ff85bc9c040487737c4062480cb61c71e697b197b4c30142f2a0da')
 def test_nonexecutable_180_sidecars(self):
  active={(x['asset_kind'],x['repo_id']) for x in self.e['items'] if x['portfolio_decision'] in ('conditional','select')}
  cond={(x['asset_kind'],x['repo_id']) for x in self.e['items'] if x['portfolio_decision']=='conditional'}
  self.assertEqual(len(active),180)
  self.assertEqual(active,{(x['asset_kind'],x['repo_id']) for x in self.q['candidates']})
  self.assertEqual(active,{(x['asset_kind'],x['repo_id']) for x in self.p['items']})
  self.assertEqual(active,{(x['asset_kind'],x['repo_id']) for x in self.r['records']})
  self.assertEqual(cond,{(x['asset_kind'],x['repo_id']) for x in self.a['entries']})
  self.assertEqual(self.a['gated_count'],21)
  self.assertEqual(self.r['summary']['active'],180)
  self.assertEqual(self.r['summary']['blocked_any'],180)
  self.assertEqual(self.r['summary']['unknown_total_active'],11)
  self.assertEqual(self.r['summary']['ready_to_approve'],0)
  self.assertEqual(self.r['summary']['downloads_approved'],0)
  self.assertFalse(self.q['approved']);self.assertFalse(self.q['download_enabled'])
  self.assertFalse(self.p['download_enabled']);self.assertFalse(self.r['ready_to_acquire'])
  self.assertTrue(all(not x['download_approved'] and not x['ready_to_acquire'] for x in self.r['records']))
  self.assertEqual(L('queues/approved.json')['entries'],[])
  self.assertEqual(L('catalog/readiness/CURRENT.json')['catalog_revision'],self.c['revision_id'])
  self.assertEqual(L('catalog/estimates/CURRENT.json')['portfolio_revision'],self.c['revision_id'])
 def test_ledger96_seven_source_refilter_and_hold(self):
  ledger=L('catalog/execution/2026-11-19-acquisition-ledger.json')
  self.assertGreaterEqual(ledger['summary']['models_verified'],96)
  self.assertEqual(len(self.next['next_research_sources']),7)
  self.assertEqual(self.next['old_R140_reconciliation']['now_reported_verified'],20)
  self.assertEqual(self.next['old_R140_reconciliation']['remaining_research_only'],['ricursiveAI/Ripple-65B-Preview'])
  self.assertEqual(self.next['six_new_source_bytes_without_ripple'],57517864334)
  self.assertEqual(self.next['fastframes_mandatory_parent_bytes_not_counted_as_six_source_bytes'],17567235949)
  self.assertEqual(self.next['nvidia_shared_vae_potential_hash_reuse_bytes_not_owner_verified'],1409400600)
  self.assertFalse(self.next['download_controls']['approved'])
  self.assertFalse(self.next['download_controls']['download_enabled'])
  self.assertEqual(self.decision['execution']['approved_queue_entries_added'],0)
  self.assertEqual(self.ov['download_authorizations_added'],0)
if __name__=='__main__':unittest.main()
