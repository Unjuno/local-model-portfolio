"""R168: refuse fake machine approvals and verify immutable ledger 116->133 growth."""
import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/path)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class R168ApprovalAndLedger(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.builder=module('scripts/build_v73_candidates.py','build_v73_r168_review_only')
  cls.executor=module('scripts/preserve_execute.py','preserve_r168_synthetic_review')
  cls.audit=read('catalog/audits/2026-11-27-r168-133-receipts-original117-signedness-and-historical-integrity.json')
  cls.ledger=read('catalog/execution/2026-11-19-acquisition-ledger.json')
 def test_historical_117_core_rows_provenance_preserved_inside_133_and_beyond(self):
  a=self.audit
  old=a['prior117_digest_by_repo_id']
  f=a['all_verified_and_one_prior_hold_core_digest_by_repo_id']
  self.assertEqual((len(old),len(f)),(117,134))
  self.assertEqual(a['prior116_verified_ids'],116)
  self.assertEqual(a['new_verified_records_since_prior116'],17)
  self.assertEqual(a['prior_one_held'],'orcarouter/Qwen3.8-27B-Uncensored')
  self.assertEqual(a['prior_immutable_reference_commit'],'6fd190ce077dec748130a69c76fbd26c0fbae190')
  self.assertTrue(a['prior_117_matching_status_repo_revision_file_count_bytes_weight_sha'])
  self.assertTrue(all(old[repo]==f[repo] for repo in old))
  byid={x['repo_id']:x for x in self.ledger['models']}
  self.assertEqual(len(byid),len(self.ledger['models']))
  for repo,h in f.items():
   self.assertIn(repo,byid)
   x=byid[repo]
   y={k:x.get(k) for k in a['core_fields_in_sha256']}
   digest=hashlib.sha256(json.dumps(y,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')).hexdigest()
   self.assertEqual(h,digest,repo)
  self.assertGreaterEqual(self.ledger['summary']['models_verified'],133)
  self.assertGreaterEqual(self.ledger['summary']['files_verified_total'],2095)
  self.assertGreaterEqual(self.ledger['summary']['bytes_verified_total'],2451205481822)
  self.assertEqual(read('queues/approved.json')['entries'],[])
  self.assertFalse(a['owner_live_actual_D_free_bytes_now_verified'])
  self.assertTrue(a['human_approval_evidence_completeness_unknown'])
 def test_publisher_scope_path_bad_or_missing_hash_rejected(self):
  fn=self.builder.immutable_scope
  good=[{'path':'sub/model.safetensors','bytes':100,'sha256':'a'*64,'git_blob_sha1':'b'*40}]
  self.assertEqual(fn(good)[0]['sha256'],'a'*64)
  for bad in (
    [{'path':'../steal','bytes':100,'sha256':'a'*64}],
    [{'path':'/absolute','bytes':100,'sha256':'a'*64}],
    [{'path':'foo\\bar','bytes':100,'sha256':'a'*64}],
    [{'path':'a//b','bytes':100,'sha256':'a'*64}],
    [{'path':'model','bytes':100}],
    [{'path':'model','bytes':0,'sha256':'a'*64}],
    [{'path':'model','bytes':True,'sha256':'a'*64}],
    [{'path':'model','bytes':100,'sha256':'short'}],
    good+good,[]):
   self.assertIsNone(fn(bad))
 def test_v73_builder_outputs_unapproved_review_only_and_never_owner_approved(self):
  b=self.builder
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);eff=root/'eff.json';led=root/'ledger';led.mkdir();out=root/'discovered'
   (led/'ledger.json').write_text(json.dumps({'entries':[{'repo_id':'already/verified','status':'VERIFIED'}]}))
   base={'asset_kind':'model','portfolio_decision':'conditional','repo_id':'sample/valid',
     'upstream_revision_sha_observed':'a'*40,'license_metadata':'Apache-2.0',
     'observed_access':'Public ungated','candidate_selected_source_files':[{'path':'model.safetensors','bytes':100,'sha256':'b'*64,'git_blob_sha1':'c'*40}]}
   data={'revision_id':'v73-20261125','items':[base,{**base,'repo_id':'already/verified'},
      {**base,'repo_id':'sample/held','portfolio_decision':'hold'},
      {**base,'repo_id':'sample/restricted','license_metadata':'CC BY-NC 4.0'},
      {**base,'repo_id':'ngocthien/tihon-tts','license_metadata':'Apache-2.0'}]}
   eff.write_text(json.dumps(data))
   with mock.patch.object(b,'LEDGER_DIR',led),mock.patch.object(b,'EFF',eff),\
       mock.patch.object(b,'DISC',out),mock.patch.object(b,'PLAN',out/'plan-UNAPPROVED.json'),\
       mock.patch.object(b,'REVIEW',out/'review-UNAPPROVED.json'):
    b.main()
   a=json.loads((out/'plan-UNAPPROVED.json').read_text())
   review=json.loads((out/'review-UNAPPROVED.json').read_text())
   self.assertFalse(a['download_enabled'] or a['approved'])
   self.assertEqual([x['repo_id'] for x in a['candidates']],['sample/valid'])
   self.assertEqual(review['authorization_source'],None)
   self.assertEqual(len(review['entries']),1)
   self.assertFalse(review['download_enabled'] or review['approved'])
   self.assertFalse((out/'approved-v73.json').exists())
   for e in review['entries']:
    self.assertIsNone(e['approval_ref'])
    for k in ('approved','download_enabled','approved_by_user','license_text_reviewed','parent_dependency_rights_reviewed','nonstandard_license_permission_verified'):
     self.assertFalse(e[k])
 def test_v73_builder_fails_closed_without_owner_ledger_and_writes_no_state(self):
  b=self.builder
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)
   with mock.patch.object(b,'LEDGER_DIR',d/'MISSING'),mock.patch.object(b,'DISC',d/'OUT'):
    with self.assertRaisesRegex(ValueError,'ledger directory'):b.main()
   self.assertFalse((d/'OUT').exists())
 def test_executor_rejects_old_synthetic_v73_even_when_every_boolean_is_true(self):
  task={'repo_id':'sample/valid','rev':'a'*40,'files':[{'path':'model.safetensors','bytes':100,'sha256':'b'*64}]}
  good={'repo_id':'sample/valid','revision_sha':'a'*40,'files':[{'path':'model.safetensors','bytes':100,'sha256':'b'*64}],
        'approved':True,'download_enabled':True,'approved_by_user':True,
        'license_text_reviewed':True,'parent_dependency_rights_reviewed':True,
        'nonstandard_license_permission_verified':True}
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'testapproval.json'
   for ref,source in [
     ('v73-pinned-candidate-sample-valid',None),
     ('v73-pinned-candidate-sample-valid','v73 effective portfolio pinned candidate sources, exact per-file publisher hashes'),
     ('owner-explicit-individual-reviewed-scope','v73 effective portfolio pinned candidate sources, exact per-file publisher hashes')]:
    p.write_text(json.dumps({'authorization_source':source,'entries':[{**good,'approval_ref':ref}]}))
    self.assertIsNone(self.executor.approval_for(task,approval_path=p))
   # Legitimate explicitly reviewed individual scope remains possible.
   p.write_text(json.dumps({'authorization_source':'human reviewed per-file legal acts','entries':[{**good,'approval_ref':'owner-reviewed-individual-scope-2026-11-27'}]}))
   self.assertIsNotNone(self.executor.approval_for(task,approval_path=p))
if __name__=='__main__':unittest.main()
