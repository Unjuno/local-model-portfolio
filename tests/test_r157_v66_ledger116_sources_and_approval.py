"""R157/v66 invariant checks: stdlib only, no model network/download."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def key(x):return x['asset_kind'],x['repo_id']
class R157V66(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=J('catalog/CURRENT.json');cls.e=J(cls.c['materialized_catalog_path'])
  cls.prior=J('catalog/effective-portfolio-2026-11-22-v65.json')
  cls.ledger=J('catalog/execution/2026-11-19-acquisition-ledger.json');cls.src=J('manifests/drafts/r157-2026-11-24-post116-five-originals-medical-moe.candidate.json')
  cls.queue=J(cls.c['priority_worklist_path']);cls.access=J(cls.c['latest_conditional_access_audit']['path'])
  cls.ready=J(cls.c['latest_active_readiness_audit']['summary_path']);cls.prep=J(cls.c['insurance_preparation_worklist_path'])
 def test_snapshot_count_and_retain_old(self):
  self.assertEqual(self.c['revision_id'],'v66-20261124')
  self.assertEqual(self.e['items'][:240],self.prior['items'])
  self.assertEqual(len(self.e['items']),246)
  self.assertEqual(len({key(x) for x in self.e['items']}),246)
  self.assertEqual((self.e['counts']['active'],self.e['counts']['models'],self.e['counts']['datasets']),(197,220,26))
  self.assertEqual((self.e['counts']['by_decision']['select'],self.e['counts']['by_decision']['conditional'],self.e['counts']['by_decision']['hold']),(56,141,30))
 def test_ledger116_and_exact_sources(self):
  got=[x for x in self.ledger['models'] if x['status']=='VERIFIED']
  self.assertEqual(len(got),116)
  ids={x['repo_id'] for x in self.e['items']}
  self.assertTrue(all(x['repo_id'] in ids for x in got))
  self.assertEqual(len(self.src['publisher_sources']),5)
  self.assertEqual(self.src['exact_source_files'],134)
  self.assertEqual(self.src['exact_source_bytes'],306537688378)
  self.assertEqual(sum(x['reported_verified_in_116_ledger'] for x in self.src['publisher_sources']),3)
  for x in self.src['publisher_sources']:
   self.assertEqual(x['model_file_count'],len(x['model_files']))
   self.assertEqual(x['publisher_source_bytes'],sum(f['bytes'] for f in x['model_files']))
   self.assertEqual(len(x['immutable_revision_sha']),40)
   self.assertFalse(x['download_approved'])
   self.assertTrue(all(not f['owner_local_sha256_verified'] for f in x['model_files']))
  self.assertEqual(self.src['over_150b_research_hold']['repo_id'],'inclusionAI/LingSante-3.1-flash-MXFP4')
  self.assertFalse(self.src['over_150b_research_hold']['exact_all_file_scope_frozen'])
 def test_derived_join_and_no_approval(self):
  selected={key(x) for x in self.e['items'] if x['portfolio_decision'] in ('select','conditional')}
  cond={key(x) for x in self.e['items'] if x['portfolio_decision']=='conditional'}
  for arr in [self.queue['candidates'],self.ready['records'],self.prep['items']]:
   self.assertEqual({key(x) for x in arr},selected)
  self.assertEqual({key(x) for x in self.access['entries']},cond)
  self.assertEqual(self.access['gated_count'],21)
  self.assertEqual(self.ready['summary']['ready_to_approve'],0)
  self.assertEqual(self.ready['summary']['blocked_any'],197)
  self.assertEqual(J('queues/approved.json')['entries'],[])
  self.assertFalse(self.queue['approved'] or self.queue['download_enabled'])
  self.assertTrue(all(not x['download_approved'] for x in self.e['items']))
  self.assertEqual(J('catalog/readiness/CURRENT.json')['catalog_revision'],self.c['revision_id'])
  self.assertEqual(J('catalog/estimates/CURRENT.json')['portfolio_revision'],self.c['revision_id'])
if __name__=='__main__':unittest.main()
