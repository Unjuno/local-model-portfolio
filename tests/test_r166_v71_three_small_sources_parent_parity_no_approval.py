"""R166 immutable publisher metadata and STOP audit; stdlib only, no model code import."""
import json,re,unittest,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8'))
from scripts.ledger_history_r168 import historical_117_ledger

class R166SourceProof(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=load('catalog/snapshots/v73-2026-11-25-current.json')
  cls.cat=load('catalog/effective-portfolio-2026-11-25-v71.json')
  cls.ledger=historical_117_ledger(load('catalog/execution/2026-11-19-acquisition-ledger.json'))
  cls.src=load('manifests/drafts/r166-2026-11-25-tiny-tts-inkling-adapter-complete-publisher-scope.candidate.json')
  cls.parent=load('catalog/research/2026-11-25-r166-inkling-heretic-parent-source-parity-no-redownload.json')
  cls.queue=load('queues/proposed-v71-r166-three-small-complete-source-UNAPPROVED.json')
  cls.dec=load('catalog/decisions/2026-11-25-r166-v71-three-small-source-finalization-and-stop.json')
 def test_current_v71_remains_exact_260_210_and_116_existing_ledger(self):
  self.assertIn((self.c['revision_id'],self.c['expected']['tracked'],self.c['expected']['active']),(('v71-20261125',260,210),('v72-20261125',264,210),('v73-20261125',265,211)))
  self.assertEqual(load(self.c['materialized_catalog_path'])['items'][:260],self.cat['items'])
  self.assertEqual((self.cat['counts']['by_decision']['select'],self.cat['counts']['by_decision']['conditional'],self.cat['counts']['by_decision']['hold']),(56,154,31))
  self.assertEqual((self.ledger['summary']['models_verified'],self.ledger['summary']['files_verified_total'],self.ledger['summary']['bytes_verified_total']),(116,1758,2021784002725))
  base={x['repo_id'] for x in self.cat['items']}
  receipts={x['repo_id'] for x in self.ledger['models'] if x['status']=='VERIFIED'}
  self.assertTrue(receipts.issubset(base))
  self.assertTrue(set(x['repo_id'] for x in self.src['sources']).issubset(base))
  self.assertTrue(set(x['repo_id'] for x in self.src['sources']).isdisjoint(receipts))
  self.assertEqual(load('queues/approved.json')['entries'],[])
 def test_all89_complete_first_party_files_including_paradee_50pagination_correction(self):
  specs=[
   ('sahilmahendrakar/Paradee-8M-v1.3','b569f5efb789af5ba643a44af348427242ceb784',59,87606314,9,74922992,'apache-2.0'),
   ('ngocthien/tihon-tts','bc71174f68651e7ff32a90f1ffd5e7528288d403',20,1862130,13,480266,'cc-by-nc-4.0'),
   ('electroglyph/Inkling-2-Mini-uncensored-LoRA','4d81722b2e939460d5b544e5319b80e9b960236b',10,52406603,10,52406603,'apache-2.0')]
  for x,row in zip(self.src['sources'],specs):
   repo,rev,count,tot,selcnt,selbytes,lic=row
   self.assertEqual(x['repo_id'],repo)
   self.assertEqual(x['publisher_revision_sha'],rev)
   self.assertEqual(x['publisher_card_license_tag'],lic)
   self.assertFalse(x['publisher_gated'])
   self.assertEqual((x['source_file_count'],x['source_repo_bytes'],x['selected_file_count'],x['selected_source_bytes']),(count,tot,selcnt,selbytes))
   files=x['full_publisher_repo_file_hashes']
   self.assertEqual(len(files),count)
   self.assertEqual(len({q['path'] for q in files}),count)
   self.assertEqual(sum(q['bytes'] for q in files),tot)
   sel=[q for q in files if q['selected_for_minimal_source']]
   self.assertEqual((len(sel),sum(q['bytes'] for q in sel)),(selcnt,selbytes))
   for q in files:
    self.assertTrue(re.fullmatch(r'[a-f0-9]{40}',q['publisher_git_blob_sha1']))
    self.assertGreater(q['bytes'],0)
    if q['publisher_lfs_sha256']:self.assertTrue(re.fullmatch(r'[a-f0-9]{64}',q['publisher_lfs_sha256']))
    self.assertFalse(q['owner_actual_sha_verified'])
   for key in ('owner_license_use_act_verified','owner_local_files_SHA_rechecked','complete_runtime_closure_verified','offline_restore_passed','owner_download_approval','model_weight_downloaded_by_research'):
    self.assertFalse(x[key])
  self.assertEqual(self.src['all_publisher_files'],89)
  self.assertEqual(self.src['all_publisher_repo_reference_bytes'],141875047)
  self.assertEqual((self.src['minimally_selected_unique_files'],self.src['minimally_selected_reference_bytes']),(32,127809861))
  self.assertEqual((self.src['excluded_same_training_or_audio_legal_files'],self.src['excluded_reference_bytes']),(57,14065186))
  self.assertEqual(127809861+14065186,141875047)
  paradee=self.src['sources'][0]
  self.assertEqual(sum(x['path'].startswith('samples/') for x in paradee['full_publisher_repo_file_hashes']),49)
  self.assertTrue({'onnx/paradee.onnx','onnx/paradee_int8.onnx','pytorch/text_side.pt','pytorch/decoder.pt','config.json','tokenizer.json','LICENSE'}.issubset({q['path'] for q in paradee['full_publisher_repo_file_hashes'] if q['selected_for_minimal_source']}))
 def test_five_publisher_core_weight_shas_match_historical_r162(self):
  old=load('manifests/drafts/r162-2026-11-25-paradee13-tihon100k-core-weight-pins.candidate.json')
  lora=load('manifests/drafts/r162-2026-11-25-electroglyph-inkling-heretic-v22-adapter-core.candidate.json')
  known={w['path']:w['sha256'] for m in old['model_sources'] for w in m['weights']}
  known['adapter_model.safetensors']=lora['core_weight_files'][0]['sha256']
  seen={}
  for model in self.src['sources']:
   for file in model['full_publisher_repo_file_hashes']:
    if file['path'] in known:
     self.assertEqual(file['publisher_lfs_sha256'],known[file['path']])
     seen[file['path']]=file['publisher_lfs_sha256']
  self.assertEqual(len(seen),5)
  self.assertEqual(sum(w['bytes'] for s in old['model_sources'] for w in s['weights'])+lora['core_weight_files'][0]['bytes'],92138387)
 def test_paradee_external_code_both_g2p_weight_and_training_uv_metadata(self):
  code=self.src['external_publisher_runtime_source_git']
  self.assertEqual(code['pinned_commit'],'2de547e45da92840a636c499eb0782e988be1e47')
  self.assertTrue(code['blob_tree_complete'])
  self.assertEqual((code['blob_count'],code['pinned_code_bytes']),(38,4678996))
  codefiles={x['path'] for x in code['static_code_git_blob_evidence']}
  self.assertTrue({'LICENSE','pyproject.toml','paradee/g2p.py','paradee/tts.py','paradee/data/g2p.onnx','paradee/data/g2p.json.gz','training/uv.lock'}.issubset(codefiles))
  self.assertTrue(all(len(x['publisher_git_blob_sha1'])==40 for x in code['static_code_git_blob_evidence']))
  self.assertFalse(code['full_dependency_wheelhouse_built'])
  self.assertFalse(code['source_code_executed'])
  self.assertTrue(self.src['sources'][0]['pytorch_pt_never_load_without_unpickling_security_review'])
 def test_tihon_gated_rights_custom_code_100125_vs_100118_and_no_tflite(self):
  t=self.src['sources'][1]
  self.assertEqual(t['publisher_card_license_tag'],'cc-by-nc-4.0')
  self.assertEqual(t['publisher_safetensors_element_count_total'],100125)
  self.assertEqual(t['author_architecture_count_claim'],100118)
  self.assertEqual(t['count_mismatch_author_vs_stored_elements'],7)
  self.assertTrue(t['source_has_tflite_runner_but_no_tflite_graphs'])
  self.assertFalse(any(x['path'].endswith('.tflite') for x in t['full_publisher_repo_file_hashes']))
  selected={x['path'] for x in t['full_publisher_repo_file_hashes'] if x['selected_for_minimal_source']}
  self.assertTrue({'NOTICE','config.json','model.safetensors','configuration_tihon.py','modeling_tihon.py','pipeline_tihon.py','tihon_tts/tflite_runner.py'}.issubset(selected))
  self.assertFalse(any(x.startswith('samples/') for x in selected))
  self.assertTrue(t['unsafe_trust_remote_code_disabled'])
 def test_inkling_parent_training_revision_differs_only_by_dtype_config_and_no_20GB_redownload(self):
  p=self.parent
  self.assertEqual((p['matched_path_git_OID_count'],p['same_file_count_each']),(13,14))
  self.assertEqual(p['changed_file_git_oid_paths'],['config.json'])
  self.assertEqual(p['training_config_bytes']-p['acquired_config_bytes'],23)
  self.assertTrue(p['config_change_only_added_key_dtype_bfloat16'])
  self.assertTrue(p['all_model_main_MTP_tokenizer_lfs_sha_same'])
  self.assertTrue(p['model_and_MTP_tokenizer_SHA_matches_acquisition_ledger_receipt_metadata'])
  self.assertEqual(p['owner_acquisition_ledger_reported_parent_revision'],'1fb4134b9a74f9681054f4ef82e4bf1f458a2337')
  self.assertEqual(p['adapter_parent_revision_from_Publisher_reproduce_TOML'],'ed40e7da625f594fc9c4990f5f66be24873c22d7')
  self.assertTrue(p['no_distinct_parent_learned_state_transfer_needed'])
  self.assertFalse(p['owner_real_D_model_hash_or_correct_config_patch_verified'])
  self.assertFalse(p['custom_Peft_InklingLoop_backend_compatibility_verified'])
  self.assertFalse(p['owner_download_approved'])
 def test_review_queue_manifest_exact_and_never_implicit_approval(self):
  q=self.queue
  self.assertEqual(q['catalog_revision'],'v71-20261125')
  self.assertEqual(q['research_source_repos'],3)
  self.assertEqual(q['selected_source_file_count'],32)
  self.assertEqual(q['selected_reference_bytes'],127809861)
  self.assertEqual([r['rank'] for r in q['research_order']],[1,2,3])
  self.assertFalse(q['download_enabled'] or q['approved_by_user'])
  self.assertEqual(q['download_approvals_added'],0)
  self.assertEqual(q['trained_weight_file_transfer_bytes_now'],0)
  for row in q['research_order']:
   self.assertFalse(row['download_enabled'] or row['approved_by_user'] or row['owner_explicit_model_file_scope_approval'])
   self.assertFalse(row['license_text_reviewed'] or row['parent_dependency_rights_reviewed'])
   self.assertEqual(sum(f['bytes'] for f in row['selected_file_metadata']),row['selected_source_reference_bytes'])
   for f in row['selected_file_metadata']:
    self.assertFalse(f['owner_local_SHA_verified'])
  self.assertTrue(self.dec['prior_260_catalog_items_unchanged'])
  self.assertEqual(self.dec['new_weight_downloads'],0)
  self.assertEqual(self.dec['new_approvals'],0)
  self.assertFalse(self.dec['owner_D_modified'])
  self.assertEqual(load('queues/approved.json')['entries'],[])
if __name__=='__main__':unittest.main()
