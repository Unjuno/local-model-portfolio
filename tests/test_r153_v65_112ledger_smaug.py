"""R153 v65 selected asset consistency. Stdlib only, no weights download."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
class R153(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=read('catalog/CURRENT.json');cls.v=read(cls.c['materialized_catalog_path'])
  cls.old=read('catalog/effective-portfolio-2026-11-22-v64.json')
  cls.l=read('catalog/execution/2026-11-19-acquisition-ledger.json');cls.s=read('manifests/drafts/r153-2026-11-22-smaug-qwen-hash-reuse-and-atomic-lora.candidate.json')
  cls.q=read(cls.c['priority_worklist_path']);cls.p=read(cls.c['insurance_preparation_worklist_path'])
  cls.g=read(cls.c['latest_active_readiness_audit']['summary_path']);cls.a=read(cls.c['latest_conditional_access_audit']['path'])
 def test_canonical(self):
  self.assertEqual(self.c['revision_id'],'v65-20261122')
  self.assertEqual(self.old['items'],self.v['items'][:236])
  self.assertEqual((len(self.v['items']),self.v['counts']['active'],self.v['counts']['models'],self.v['counts']['datasets']),(240,192,214,26))
  self.assertEqual(self.v['counts']['by_decision']['conditional'],136)
  self.assertEqual(len({(x['asset_kind'],x['repo_id']) for x in self.v['items']}),240)
  ids={x['repo_id'] for x in self.v['items']}
  self.assertEqual(sum(x['status']=='VERIFIED' for x in self.l['models']),112)
  self.assertTrue(all(x['repo_id'] in ids for x in self.l['models'] if x['status']=='VERIFIED'))
 def test_unapproved_joins(self):
  act={(x['asset_kind'],x['repo_id']) for x in self.v['items'] if x['portfolio_decision'] in ('select','conditional')}
  cond={(x['asset_kind'],x['repo_id']) for x in self.v['items'] if x['portfolio_decision']=='conditional'}
  for y in (self.q['candidates'],self.p['items'],self.g['records']):
   self.assertEqual({(x['asset_kind'],x['repo_id']) for x in y},act)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in self.a['entries']},cond)
  self.assertEqual(self.a['gated_count'],21)
  self.assertFalse(self.q['approved'] or self.q['download_enabled'])
  self.assertEqual(self.g['summary']['ready_to_approve'],0)
  self.assertEqual(read('queues/approved.json')['entries'],[])
  self.assertEqual(read('catalog/readiness/CURRENT.json')['catalog_revision'],self.c['revision_id'])
  self.assertEqual(read('catalog/estimates/CURRENT.json')['portfolio_revision'],self.c['revision_id'])
 def test_smaug_shards(self):
  x=next(x for x in self.s['full_sources'] if x['repo_id']=='abacusai/Smaug-Uncensored')
  self.assertEqual((x['identical_shard_count'],x['different_shard_count']),(2,16))
  self.assertEqual(x['identical_shard_bytes'],5934994296)
  self.assertEqual(x['different_shard_bytes'],49628012480)
if __name__=='__main__':unittest.main()
