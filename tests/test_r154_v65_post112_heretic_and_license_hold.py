"""R154/v65 static research regression: no network and no external model code.
Checks two already-reported 112 ledger sources, tiny LoRA hashes, Cartwheel HOLD,
8 optional Kitten SHA checks, and 0 executable/download approvals.
"""
import json,unittest,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
from scripts.ledger_history_r168 import historical_117_ledger

class R154V65Selection(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.current=read('catalog/CURRENT.json')
  cls.old=read('catalog/effective-portfolio-2026-11-22-v64.json')
  cls.new=read('catalog/effective-portfolio-2026-11-22-v65.json')
  cls.ov=read('catalog/revisions/v65-2026-11-22.json')
  cls.source=read('manifests/drafts/r154-2026-11-22-four-primary-sources-after112.candidate.json')
  cls.audit=read('catalog/audits/2026-11-22-r154-all112-ledger-and-new-source-delta.json')
  cls.ledger=historical_117_ledger(read('catalog/execution/2026-11-19-acquisition-ledger.json'))
  cls.ready=read('catalog/readiness/v65-2026-11-22-r154-all192-gates.json')
  cls.access=read('catalog/access/2026-11-22-v65-conditional-hub-gates.json')
  cls.pico=read('catalog/research/2026-11-22-r154-pico-eight-int8-extra-publisher-sha.json')
  cls.q=read('queues/proposed-v65-2026-11-22.json')
  cls.post=read('queues/proposed-v65-r155-after112-unapproved-source-scopes.json')
 def test_current_and_old236_immutable(self):
  self.assertIn(self.current['revision_id'],('v66-20261124','v67-20261124',"v68-20261125","v69-20261125","v70-20261125", "v71-20261125", "v72-20261125", "v73-20261125"))
  self.assertIn('catalog/revisions/v65-2026-11-22.json',self.current['ordered_overlays'])
  self.assertIn(self.current['materialized_catalog_path'],('catalog/effective-portfolio-2026-11-24-v66.json','catalog/effective-portfolio-2026-11-24-v67.json',"catalog/effective-portfolio-2026-11-25-v68.json","catalog/effective-portfolio-2026-11-25-v69.json","catalog/effective-portfolio-2026-11-25-v70.json", "catalog/effective-portfolio-2026-11-25-v71.json","catalog/effective-portfolio-2026-11-25-v72.json","catalog/effective-portfolio-2026-11-25-v73.json"))
  self.assertEqual(self.old['items'],self.new['items'][:236])
  self.assertEqual(len(self.new['items']),240)
  self.assertEqual(len({(x['asset_kind'],x['repo_id']) for x in self.new['items']}),240)
  self.assertEqual((self.new['counts']['tracked'],self.new['counts']['active'],self.new['counts']['models'],self.new['counts']['datasets']),(240,192,214,26))
  self.assertEqual((self.new['counts']['by_decision']['select'],self.new['counts']['by_decision']['conditional'],self.new['counts']['by_decision']['hold']),(56,136,29))
  latest=read(self.current['materialized_catalog_path'])
  self.assertEqual(self.new['items'],latest['items'][:240])
  for k in ('tracked','active','models','datasets','by_decision','by_tier','by_forecast_wave','parameter_gate','resource_screen'):
   self.assertEqual(self.current['expected'][k],latest['counts'][k])
  self.assertEqual(self.current['expected']['budget_scenario'],latest['budget'])
 def test_all_112_receipt_IDs_registered_and_prior2_missing(self):
  latest=[x for x in self.ledger['models'] if x['status']=='VERIFIED']
  self.assertEqual(len(latest),116)
  self.assertEqual(self.ledger['summary']['files_verified_total'],1758)
  self.assertEqual(self.ledger['summary']['bytes_verified_total'],2021784002725)
  historic=[x for x in latest if x['repo_id'] not in {'nchapman/Qwen3.5-0.8B-Heretic-LoRA','Datadog/Toto-2.0-4m','inclusionAI/LingSante-Pulse-1.0','ostris/primal_vae'}]
  self.assertEqual(len(historic),112)
  verified={x['repo_id']:x for x in historic}  # original R154 112 receipt set, not ledger ordering
  before={x['repo_id'] for x in self.old['items']}
  after={x['repo_id'] for x in self.new['items']}
  self.assertEqual(sorted(set(verified)-before),['mistralai/Timestral-5M','tencent/WeMM-Video-2B'])
  self.assertEqual(set(verified)-after,set())
  self.assertEqual(self.audit['source_ids_missing_after'],[])
  self.assertEqual(sorted(self.audit['source_ids_missing_before']),['mistralai/Timestral-5M','tencent/WeMM-Video-2B'])
  self.assertEqual(self.source['already_receipted_two_bytes'],6611554027)
 def test_all_four_sources_exact_203_files_SHA_and_immutable_revision(self):
  self.assertEqual(len(self.source['publisher_sources']),4)
  self.assertEqual(self.source['total_publisher_file_references'],203)
  self.assertEqual(self.source['total_publisher_bytes_with_two_already_acquired'],6921777220)
  names={'mistralai/Timestral-5M':(6,20854471,'bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f'),
         'tencent/WeMM-Video-2B':(27,6590699556,'821690998399cac0f55bb7f7f805ebafa650c3a4'),
         'nchapman/Qwen3.5-0.8B-Heretic-LoRA':(16,6165749,'92e2ae29c379d7378c696511ec9c70ace8be1434'),
         'GetCartwheelInc/cartwheel-control':(154,304057444,'24fc279af8f70097f503767b81db5384d779aae5')}
  for src in self.source['publisher_sources']:
   n,total,commit=names[src['repo_id']]
   self.assertEqual((src['full_publisher_file_count'],src['full_publisher_file_bytes'],src['model_source_commit']),(n,total,commit))
   self.assertEqual(len(src['files']),n)
   self.assertEqual(sum(z['bytes'] for z in src['files']),total)
   self.assertEqual(len({z['path'] for z in src['files']}),n)
   self.assertFalse(src['download_approved'])
   for z in src['files']:
    self.assertEqual(len(z['git_blob_sha1']),40)
    if z['sha256']:self.assertEqual(len(z['sha256']),64)
    self.assertFalse(z['owner_local_SHA_verified'])
 def test_three_active_and_one_hold_exact(self):
  self.assertEqual(len(self.ov['additions']),4)
  self.assertEqual([x['repo_id'] for x in self.ov['additions']],
   ['mistralai/Timestral-5M','tencent/WeMM-Video-2B',
    'nchapman/Qwen3.5-0.8B-Heretic-LoRA','GetCartwheelInc/cartwheel-control'])
  self.assertEqual(self.new['items'][236:],self.ov['additions'])
  self.assertEqual([x['portfolio_decision'] for x in self.ov['additions']],
                   ['select','conditional','conditional','hold'])
  self.assertEqual(self.ov['added_active'],3)
  self.assertEqual(self.ov['removed_assets'],0)
  self.assertEqual(self.ov['changed_prior_decisions'],0)
  for x in self.ov['additions']:
   self.assertFalse(x['download_approved'])
   self.assertFalse(x['download_ready'])
   self.assertFalse(x['license_text_reviewed'])
   self.assertFalse(x['personal_access_verified'])
  self.assertEqual(self.new['items'][-1]['parameter_gate']['status'],'UNVERIFIED_BLOCK_FINAL_LOCK')
 def test_heretic_exact_two_unique_lora_weights_and_parent_gap(self):
  src=next(x for x in self.source['publisher_sources'] if x['repo_id'].startswith('nchapman/'))
  fs={x['path']:x for x in src['files']}
  self.assertEqual(src['independent_trained_adapter_total_bytes'],2006488)
  self.assertEqual(fs['adapter_model.safetensors']['sha256'],fs['pareto/trial_002_ref4_kl0.0714/adapter_model.safetensors']['sha256'])
  self.assertEqual(fs['adapter_model.safetensors']['sha256'],'269cee632d7b2dc1cb5163d6f1b2a378df3b2130e51c8b08c686709997c28679')
  self.assertEqual(fs['pareto/trial_004_ref6_kl0.0275/adapter_model.safetensors']['sha256'],'26836a1374eb43aef39f04970b558f347a62558ebce8c0e00388ff217146ba6e')
  self.assertTrue(src['adapter_config_revision_is_null'])
  self.assertTrue(src['exact_trained_parent_revision_not_disclosed'])
  self.assertEqual(src['historical_parent_verified_revision'],'2fc06364715b967f1860aea9cf38778875588b17')
  self.assertFalse(src['historical_acquisition_receipt_112'])
  self.assertEqual(self.new['items'][238]['parameter_gate']['status'],'UNVERIFIED_BLOCK_FINAL_LOCK')
 def test_cartwheel_legal_hOLD_and_three_policy_weights_not_active(self):
  x=self.new['items'][-1]
  self.assertEqual(x['repo_id'],'GetCartwheelInc/cartwheel-control')
  self.assertEqual(x['portfolio_decision'],'hold')
  self.assertTrue(x['preservation_bundle']['RP1_third_party_upstream_license_missing'])
  paths=x['preservation_bundle']['distinct_policy_files']
  self.assertEqual(len(paths),3)
  self.assertTrue(all(p.endswith('policy.safetensors') for p in paths))
  self.assertEqual(len(x['preservation_bundle']['must_preserve']),154)
  self.assertNotIn(x['repo_id'],{z['repo_id'] for z in self.q['candidates']})
 def test_KITTEN_8_optional_ONNX_SHA_fixed_no_new_model(self):
  self.assertEqual(self.pico['repo_id'],'KittenML/kitten-tts-2-pico')
  self.assertEqual(self.pico['missing_file_count'],8)
  self.assertEqual(self.pico['missing_file_bytes'],63628208)
  self.assertEqual(self.pico['already_reported_receipt_file_count'],33)
  self.assertEqual(self.pico['live_publisher_full_repo_file_count'],41)
  self.assertEqual(len(self.pico['files']),8)
  self.assertEqual(sum(x['bytes'] for x in self.pico['files']),63628208)
  self.assertTrue(self.pico['independently_trained_vs_quantized_from_existing_weights_unproven'])
  self.assertTrue(all(x['path'].endswith('.onnx') and len(x['sha256'])==64 for x in self.pico['files']))
  self.assertEqual(len({x['sha256'] for x in self.pico['files']}),8)
  self.assertEqual(sum(x['repo_id']=='KittenML/kitten-tts-2-pico' for x in self.new['items']),1)
 def test_all_192_active_readiness_access_and_queue_fail_closed(self):
  active={(x['asset_kind'],x['repo_id']) for x in self.new['items'] if x['portfolio_decision'] in ('select','conditional')}
  self.assertEqual(len(active),192)
  self.assertEqual(active,{(x['asset_kind'],x['repo_id']) for x in self.ready['records']})
  self.assertEqual(active,{(x['asset_kind'],x['repo_id']) for x in self.q['candidates']})
  prep=read('catalog/preparation/2026-11-22-insurance-bundles-v65.json')
  self.assertEqual(active,{(x['asset_kind'],x['repo_id']) for x in prep['items']})
  self.assertEqual((self.ready['summary']['tracked'],self.ready['summary']['active'],self.ready['summary']['blocked_any']),(240,192,192))
  self.assertEqual((self.ready['summary']['select'],self.ready['summary']['conditional'],self.ready['summary']['unknown_total_active']),(56,136,14))
  self.assertEqual((self.ready['summary']['ready_to_approve'],self.ready['summary']['downloads_approved']),(0,0))
  self.assertEqual(dict(collections.Counter(g for x in self.ready['records'] for g in x['blocking_gates'])),self.ready['summary']['blocking_gate_counts'])
  self.assertEqual(dict(collections.Counter(x['first_blocker'] for x in self.ready['records'])),self.ready['summary']['first_blocker_counts'])
  self.assertTrue(all(not x['download_approved'] and not x['ready_to_acquire'] for x in self.ready['records']))
  self.assertEqual((self.access['scope'],self.access['tracked_conditional'],self.access['gated_count'],len(self.access['entries'])),(136,136,21,136))
  self.assertFalse(self.q['approved'])
  self.assertFalse(self.q['download_enabled'])
  self.assertFalse(self.access['download_authorized'])
  self.assertFalse(prep['download_enabled'])
 def test_post112_scope_counts_and_no_approval(self):
  prior=read('queues/proposed-v64-r152-post99-13-plus-bison-research-only.json')
  self.assertEqual(len(prior['candidate_research_only']),14)
  self.assertEqual((self.post['old_post99_queue_14_candidates'],self.post['old_post99_queue_now_reported_verified'],self.post['old_post99_remaining_unverified_held']),(14,13,1))
  self.assertEqual(self.post['nonhold_new_source_research_bytes_NOT_USER_ACQUISITION'],6165749)
  self.assertEqual(self.post['same_model_Kitten_optional_UNPROVEN_conversion_bytes'],63628208)
  self.assertEqual(len(self.post['candidate_research_only']),4)
  self.assertTrue(all(not x['download_enabled'] and not x['owner_specific_license_act_and_download_approval'] for x in self.post['candidate_research_only']))
  self.assertEqual(read('queues/approved.json')['entries'],[])
  self.assertFalse(self.source['real_weight_transfers_performed_by_this_research'])
  self.assertEqual(self.ov['new_weight_payload_downloaded'],0)
  self.assertEqual(self.ov['new_approved_downloads_added'],0)
 def test_current_sidecar_links_and_no_owner_hdd_claims(self):
  self.assertEqual(read('catalog/readiness/CURRENT.json')['catalog_revision'],self.current['revision_id'])
  self.assertEqual(read('catalog/estimates/CURRENT.json')['portfolio_revision'],self.current['revision_id'])
  self.assertEqual(read(self.current['latest_active_readiness_audit']['summary_path'])['catalog_revision'],self.current['revision_id'])
  self.assertEqual(read(self.current['latest_conditional_access_audit']['path'])['source_revision'],self.current['revision_id'])
  self.assertEqual(read(self.current['insurance_preparation_worklist_path'])['source_revision'],self.current['revision_id'])
  self.assertEqual(self.current['latest_reported_ledger_summary']['reported_VERIFIED_models'],116)
  self.assertFalse(self.current['expected']['budget_scenario']['physical_capacity_verified'])
  self.assertEqual(self.current['expected']['budget_scenario']['v65_new_download_reservation_approved_bytes'],0)
if __name__=='__main__':unittest.main()
