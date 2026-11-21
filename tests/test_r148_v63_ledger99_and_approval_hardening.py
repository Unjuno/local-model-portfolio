"""R148: catalog completed against the 99-model acquisition report, no implicit approvals.

Never downloads or runs any model. TempDir intercepts builder output.
"""
import importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
def L(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def imp(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/"scripts"/(name+".py"))
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module

class R148Ledger99AndApprovals(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.current=L('catalog/CURRENT.json')
  cls.original=L('catalog/effective-portfolio-2026-11-22-v62.json')
  cls.new=L('catalog/effective-portfolio-2026-11-22-v63.json')
  cls.ov=L('catalog/revisions/v63-2026-11-22.json')
  cls.source=L('manifests/drafts/r148-2026-11-22-ledger99-four-untracked-trained-sources.candidate.json')
  cls.ledger=L('catalog/execution/2026-11-19-acquisition-ledger.json')
  cls.revision=L('catalog/research/2026-11-22-r148-ledger99-immutable-revision-drift.json')
  cls.queue=L('queues/proposed-v63-2026-11-22.json')
  cls.ready=L('catalog/readiness/v63-2026-11-22-r148-all188-gates.json')
  cls.access=L('catalog/access/2026-11-22-v63-conditional-hub-gates.json')
  cls.prep=L('catalog/preparation/2026-11-22-insurance-bundles-v63.json')
 def test_current_integrity_and_immutable_old231(self):
  self.assertEqual(self.current['revision_id'],'v63-20261122')
  self.assertEqual(self.current['ordered_overlays'][-1],'catalog/revisions/v63-2026-11-22.json')
  self.assertEqual(self.current['materialized_catalog_path'],'catalog/effective-portfolio-2026-11-22-v63.json')
  self.assertEqual(self.original['items'],self.new['items'][:231])
  self.assertEqual(len(self.new['items']),235)
  self.assertEqual(len({(x['asset_kind'],x['repo_id']) for x in self.new['items']}),235)
  self.assertEqual((self.new['counts']['tracked'],self.new['counts']['active'],self.new['counts']['models'],self.new['counts']['datasets']),(235,188,209,26))
  self.assertEqual((self.new['counts']['by_decision']['select'],self.new['counts']['by_decision']['conditional']),(55,133))
  self.assertEqual(self.new['counts']['parameter_gate']['UNVERIFIED_BLOCK_FINAL_LOCK'],26)
  self.assertEqual(self.new['counts']['parameter_gate']['PASS_TOTAL_PARAMS_LT_150B'],181)
  for k in ('tracked','active','models','datasets','by_decision','by_tier','by_forecast_wave','parameter_gate','resource_screen'):
   self.assertEqual(self.current['expected'][k],self.new['counts'][k])
  self.assertEqual(self.current['expected']['budget_scenario'],self.new['budget'])
 def test_all99_ledger_ids_represented_without_any_transfer(self):
  reported=[x for x in self.ledger['models'] if x['status']=='VERIFIED']
  self.assertEqual(len(reported),99)
  ids={x['repo_id'] for x in self.new['items']}
  self.assertTrue(all(x['repo_id'] in ids for x in reported))
  self.assertEqual(len(self.source['publisher_sources']),4)
  self.assertEqual((self.source['publisher_selected_files'],self.source['publisher_reference_bytes'],self.source['published_source_digest_refs']),(49,27418360473,12))
  got_reported={x['repo_id']:x for x in reported}
  for model in self.source['publisher_sources']:
   rep=got_reported[model['repo_id']]
   self.assertEqual((model['model_source_file_count'],model['model_source_bytes']),(rep['files_verified'],rep['source_bytes']))
   self.assertEqual(model['model_source_bytes'],sum(x['bytes'] for x in model['files']))
   self.assertEqual(model['frozen_acquired_revision_sha'],rep['revision_sha'])
   self.assertFalse(model['download_approved'])
   for f in model['files']:
    self.assertEqual(len(f['git_blob_sha1']),40)
    if f['publisher_lfs_sha256']:self.assertEqual(len(f['publisher_lfs_sha256']),64)
    self.assertFalse(f['owner_local_sha_rechecked_by_this_audit'])
  ids=[x['repo_id'] for x in self.ov['additions']]
  self.assertEqual(ids,[x['repo_id'] for x in self.source['publisher_sources']])
  self.assertEqual([x['portfolio_decision'] for x in self.ov['additions']],['conditional','conditional','select','select'])
  self.assertTrue(all(x['historical_acquisition_reported_verified'] for x in self.ov['additions']))
  self.assertTrue(all(not x['download_approved'] for x in self.ov['additions']))
  self.assertEqual(self.ov['new_model_payload_downloaded'],0)
 def test_revision_delta_eight_same_weights_one_real_difference(self):
  r=self.revision
  self.assertEqual(r['matched_canonical_repo_IDS'],95)
  self.assertEqual(r['verified_without_catalog_entry_before_reconciliation'],4)
  self.assertEqual(r['verified_repo_revision_sha_conflicts'],9)
  self.assertEqual(r['same_publisher_weights_but_possible_runtime_metadata_drift'],8)
  bad=[x for x in r['revision_comparisons'] if x['status']=='WEIGHT_OR_WEIGHT_SCOPE_DIFFERENT']
  self.assertEqual(len(bad),1)
  self.assertEqual(bad[0]['repo_id'],'nvidia/RFD4-Proteina')
  self.assertIn('transformers/model.safetensors',bad[0]['changed_weight_paths'])
  self.assertIn('adapter/adapter_model.safetensors',bad[0]['extra_weight_paths'])
  for x in r['revision_comparisons']:
   self.assertEqual(len(x['catalog_observed_sha']),40)
   self.assertEqual(len(x['acquired_reported_sha']),40)
   if x not in bad:
    self.assertFalse(x['changed_weight_paths'])
    self.assertFalse(x['extra_weight_paths'])
    self.assertFalse(x['missing_weight_paths'])
 def test_all188_stopped_and_133_conditional_access(self):
  active={(x['asset_kind'],x['repo_id']) for x in self.new['items'] if x['portfolio_decision'] in ('select','conditional')}
  conditional={(x['asset_kind'],x['repo_id']) for x in self.new['items'] if x['portfolio_decision']=='conditional'}
  self.assertEqual(len(active),188)
  for view in (self.queue['candidates'],self.ready['records'],self.prep['items']):
   self.assertEqual({(x['asset_kind'],x['repo_id']) for x in view},active)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in self.access['entries']},conditional)
  self.assertEqual(self.access['gated_count'],21)
  self.assertEqual(self.ready['summary']['blocked_any'],188)
  self.assertEqual(self.ready['summary']['ready_to_approve'],0)
  self.assertFalse(self.queue['approved'])
  self.assertFalse(self.queue['download_enabled'])
  self.assertFalse(self.prep['download_enabled'])
  self.assertEqual(L('queues/approved.json')['entries'],[])
  self.assertEqual(L('catalog/readiness/CURRENT.json')['catalog_revision'],'v63-20261122')
  self.assertEqual(L('catalog/estimates/CURRENT.json')['portfolio_revision'],'v63-20261122')
 def test_synthetic_2026_ref_is_rejected_even_if_flags_true(self):
  p=imp('preserve_execute')
  task={'repo_id':'Example/Model','rev':'a'*40,'files':[{'path':'model.safetensors','bytes':11,'sha256':'b'*64}]}
  approval={'repo_id':task['repo_id'],'revision_sha':task['rev'],
   'approved':True,'download_enabled':True,'approved_by_user':True,
   'license_text_reviewed':True,'parent_dependency_rights_reviewed':True,
   'nonstandard_license_permission_verified':True,
   'approval_ref':'v62 R147 canonical post96 source queue; user directive 2026-11-19 continuous acquisition to D drive',
   'files':[{'path':'model.safetensors','bytes':11,'sha256':'b'*64}]}
  with tempfile.TemporaryDirectory() as td:
   f=Path(td)/'legacy-approved.json';f.write_text(json.dumps({'entries':[approval]}))
   self.assertIsNone(p.approval_for(task,approval_path=f))
   approval['approval_ref']='owner-explicit-individual-license-scope-review-2026-11-22'
   f.write_text(json.dumps({'entries':[approval]}))
   self.assertIsNotNone(p.approval_for(task,approval_path=f))
 def test_v62_builder_produces_no_approved_file_or_user_attestation(self):
  b=imp('build_v62_plan')
  with tempfile.TemporaryDirectory() as td:
   scratch=Path(td)
   with mock.patch.object(b,'QUEUE',ROOT/'queues/proposed-v62-r147-post96-next-research-sources.json'),\
        mock.patch.object(b,'DISC',scratch),\
        mock.patch.object(b,'PLAN',scratch/'plan-v62.json'),\
        mock.patch.object(b,'APPROVAL',scratch/'review-v62-UNAPPROVED.json'):
    b.main()
   plan=json.loads((scratch/'plan-v62.json').read_text())
   data=json.loads((scratch/'review-v62-UNAPPROVED.json').read_text())
   self.assertFalse(plan['download_enabled'])
   self.assertFalse(plan['approved'])
   self.assertGreaterEqual(len(plan['candidates']),8)
   self.assertEqual(len(data['entries']),len(plan['candidates']))
   for x in data['entries']:
    for field in ('approved','download_enabled','approved_by_user','license_text_reviewed','parent_dependency_rights_reviewed','nonstandard_license_permission_verified'):
     self.assertIs(x[field],False)
    self.assertIsNone(x['approval_ref'])
   self.assertFalse((scratch/'approved-v62.json').exists())
 def test_all_other_generators_also_unapproved_by_default(self):
  for path in ('scripts/build_v59_plan.py','scripts/build_repair_plan.py','scripts/prepare_session_approvals.py'):
   s=(ROOT/path).read_text(encoding='utf-8')
   self.assertNotIn('"approved": True',s)
   self.assertNotIn('"approved_by_user": True',s)
   self.assertIn('"license_text_reviewed": False',s)
   self.assertIn('UNAPPROVED',s)
  q=L('queues/proposed-v63-r149-after99-11-research-only.json')
  self.assertEqual(q['reported_acquired']['models_verified'],99)
  self.assertEqual(q['candidate_repo_count'],11)
  self.assertEqual(q['nonhold_publisher_reference_bytes'],68544170933)
  self.assertEqual(q['approval_controls']['entries_approved'],0)
if __name__=='__main__':unittest.main()
