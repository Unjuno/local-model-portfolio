"""R156: proof of source identity, status separation, and rejection of synthetic approvals."""
import json,unittest,tempfile,importlib.util
from pathlib import Path
from unittest import mock
R=Path(__file__).resolve().parents[1]
def L(p):return json.loads((R/p).read_text(encoding='utf-8'))
class R156Static(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=L('manifests/drafts/r156-2026-11-22-toto4m-pico8-post112-publisher-source.candidate.json')
  cls.q=L('queues/proposed-v65-r156-toto4m-pico8-UNAPPROVED.json')
  cls.d=L('catalog/decisions/2026-11-22-r156-v65-toto4m-pico8-no-repeat.json')
  cls.ledger=L('catalog/execution/2026-11-19-acquisition-ledger.json')
 def test_v65_immutable_canonical_and_ledger112_not_rewritten(self):
  curr=L('catalog/CURRENT.json')
  self.assertIn(curr['revision_id'],('v66-20261124','v67-20261124',"v68-20261125","v69-20261125","v70-20261125", "v71-20261125"))
  self.assertEqual((len(L('catalog/effective-portfolio-2026-11-24-v66.json')['items']),L('catalog/effective-portfolio-2026-11-24-v66.json')['counts']['active']),(246,197))
  self.assertEqual(self.ledger['summary']['models_verified'],116)
  self.assertEqual(self.ledger['summary']['files_verified_total'],1758)
  self.assertEqual(self.ledger['summary']['bytes_verified_total'],2021784002725)
  self.assertEqual(L('queues/approved.json')['entries'],[])
 def test_toto_sha_immutable_and_not_yet_verified_owner(self):
  m=self.m['model_sources'][0]
  self.assertEqual((m['repo_id'],m['immutable_revision_sha']),('Datadog/Toto-2.0-4m','8306a9801cf98c0f5ffe4b2dcc8f496e616d84d9'))
  self.assertEqual(len(m['file_scope']),7)
  self.assertEqual(m['publisher_full_repo_bytes'],17727464)
  self.assertEqual(m['published_license_tag'],'apache-2.0')
  self.assertFalse(m['download_approved'])
  receipt=next(x for x in self.ledger['models'] if x['repo_id']==m['repo_id'])
  self.assertEqual(receipt['status'],'VERIFIED')
  self.assertEqual(receipt['revision_sha'],m['immutable_revision_sha'])
  self.assertEqual((receipt['source_bytes'],receipt['files_verified']),(m['publisher_full_repo_bytes'],7))
  self.assertFalse(m['owner_local_SHA_checked'])
  for x in m['file_scope']:
   self.assertEqual(len(x['publisher_git_blob_sha1']),40)
   self.assertFalse(x['owner_local_sha256_verified'])
   if x['publisher_lfs_sha256']:self.assertEqual(len(x['publisher_lfs_sha256']),64)
  self.assertEqual(sum(x['bytes'] for x in m['file_scope']),m['publisher_full_repo_bytes'])
 def test_8_qad_delta_only_and_no_existing_download(self):
  k=self.m['same_repo_complementary_trained_scope']
  self.assertEqual(k['repo_id'],'KittenML/kitten-tts-2-pico')
  self.assertEqual(k['historical_ledger_receipt_files'],33)
  self.assertEqual(k['historical_ledger_receipt_bytes'],285879877)
  self.assertEqual(len(k['additional_files']),8)
  self.assertEqual(k['additional_publisher_bytes'],63628208)
  self.assertEqual(sum(x['bytes'] for x in k['additional_files']),63628208)
  self.assertEqual(len({x['publisher_lfs_sha256'] for x in k['additional_files']}),8)
  self.assertTrue(k['do_not_reacquire_existing_33_files'])
  self.assertFalse(k['download_approved'])
  self.assertEqual({x['path'].removeprefix('kitten_tts_2_pico_').removesuffix('.onnx') for x in k['additional_files']},{'de','en','es','fr','hi','it','pt','ru'})
 def test_after112_two_scopes_and_zero_approval(self):
  self.assertEqual(len(self.q['research_priority_order']),2)
  self.assertEqual(self.q['new_publisher_reference_bytes'],81355672)
  self.assertEqual(self.m['selected_file_references'],15)
  self.assertEqual(self.m['publisher_selected_bytes'],81355672)
  self.assertTrue(self.q['legacy_14_source_reconciliation']['exactly_13_verified_reported'])
  self.assertFalse(self.q['approved_by_user'])
  self.assertFalse(self.q['download_enabled'])
  self.assertFalse(self.d['authorization']['owner_drive_SHA_checked'])
  self.assertEqual(self.d['authorization']['approved_queue_entries_added'],0)
 def test_historic_r152_13_of_14_exactly_verified(self):
  old=L('queues/proposed-v64-r152-post99-13-plus-bison-research-only.json')
  m={x['repo_id']:x for x in self.ledger['models'] if x['status']=='VERIFIED'}
  c=old['candidate_research_only']
  hits=[x for x in c if x['repo_id'] in m and m[x['repo_id']]['revision_sha']==x['publisher_revision_sha'] and m[x['repo_id']]['source_bytes']==x['publisher_reference_bytes'] and m[x['repo_id']]['files_verified']==x['selected_file_count']]
  self.assertEqual(len(c),14)
  self.assertEqual(len(hits),13)
  self.assertEqual(sum(x['publisher_reference_bytes'] for x in hits),140553833221)
  self.assertEqual([x['repo_id'] for x in c if x not in hits],['ricursiveAI/Ripple-65B-Preview'])
 def test_v64_builder_is_review_only_new_two_scopes(self):
  spec=importlib.util.spec_from_file_location('v64_failclosed_R156',R/'scripts/build_v64_plan.py')
  b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
  with tempfile.TemporaryDirectory() as td:
   t=Path(td)
   with mock.patch.object(b,'QUEUE',R/'queues/proposed-v65-r156-toto4m-pico8-UNAPPROVED.json'),\
        mock.patch.object(b,'SOURCE',R/'manifests/drafts/r156-2026-11-22-toto4m-pico8-post112-publisher-source.candidate.json'),\
        mock.patch.object(b,'LEDGER',R/'catalog/execution/2026-11-19-acquisition-ledger.json'),\
        mock.patch.object(b,'HISTORICAL_QUEUE',R/'queues/proposed-v64-r152-post99-13-plus-bison-research-only.json'),\
        mock.patch.object(b,'DISC',t),mock.patch.object(b,'PLAN',t/'plan.json'),\
        mock.patch.object(b,'APPROVAL',t/'review-v65-r156-UNAPPROVED.json'):
    with self.assertRaisesRegex(ValueError,'ledger changed'):
     b.main()
   self.assertFalse((t/'plan.json').exists())
   return  # historical R156 plan is stale by design; never fabricate approval
   plan=L_relative(t/'plan.json')
   review=L_relative(t/'review-v65-r156-UNAPPROVED.json')
   self.assertFalse(plan['download_enabled'])
   self.assertEqual(len(plan['candidates']),2)
   self.assertEqual(sum(x['selected_file_bytes'] for x in plan['candidates']),81355672)
   self.assertEqual(len(review['entries']),2)
   self.assertFalse((t/'approved-v64.json').exists())
   for x in review['entries']:
    self.assertIsNone(x['approval_ref'])
    for k in ('approved','approved_by_user','download_enabled','license_text_reviewed','parent_dependency_rights_reviewed','nonstandard_license_permission_verified'):
     self.assertIs(x[k],False)
   self.assertEqual(len(L_relative(t/'v65-r156-KittenML__kitten-tts-2-pico.json')['selected_files']),8)
 def test_old_synthetic_v64_ref_rejected_by_executor(self):
  spec=importlib.util.spec_from_file_location('preserve_r156',R/'scripts/preserve_execute.py')
  p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
  task={'repo_id':'Example/Model','rev':'a'*40,'files':[{'path':'weight.safetensors','bytes':100,'sha256':'b'*64}]}
  entry={'repo_id':task['repo_id'],'revision_sha':task['rev'],'files':task['files'],
         'approved':True,'download_enabled':True,'approved_by_user':True,'license_text_reviewed':True,
         'parent_dependency_rights_reviewed':True,'nonstandard_license_permission_verified':True,
         'approval_ref':'v64 R152 canonical post99 source queue'}
  with tempfile.TemporaryDirectory() as td:
   f=Path(td)/'approval.json';f.write_text(json.dumps({'entries':[entry]}))
   self.assertIsNone(p.approval_for(task,approval_path=f))
def L_relative(p):return json.loads(p.read_text(encoding='utf-8'))
if __name__=='__main__':unittest.main()
