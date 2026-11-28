import json,unittest,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def get(p): return json.loads((ROOT/p).read_text())
class TestSeisLM(unittest.TestCase):
 def test_rows(self):
  old=get('catalog/effective-portfolio-2026-11-28-v98.json')['items']; new=get('catalog/effective-portfolio-2026-11-28-v99.json')['items']
  self.assertEqual(new[:-1],old); self.assertEqual(len(new),293); self.assertEqual(len({(x['asset_kind'],x['repo_id']) for x in new}),293); self.assertEqual(get('catalog/revisions/v99-2026-11-28.json')['additions'],new[-1:]); self.assertEqual(new[-1]['repo_id'],'ltlltl2006/seislm-base')
 def test_joins(self):
  a=get('catalog/effective-portfolio-2026-11-28-v99.json'); ids=lambda xs:{(x['asset_kind'],x['repo_id']) for x in xs}
  active=ids(x for x in a['items'] if x['portfolio_decision'] in ('select','conditional')); cond=ids(x for x in a['items'] if x['portfolio_decision']=='conditional')
  self.assertEqual((len(active),len(cond)),(237,181))
  for p,k in [('queues/proposed-v99-2026-11-28.json','candidates'),('catalog/preparation/2026-11-28-insurance-bundles-v99.json','items'),('catalog/readiness/v99-2026-11-28-r195-all237-gates.json','records')]:
   rows=get(p)[k]; self.assertEqual(ids(rows),active); self.assertEqual(len(rows),237); self.assertTrue(all(not x['download_approved'] for x in rows))
  self.assertEqual(ids(get('catalog/access/2026-11-28-v99-conditional-hub-gates.json')['entries']),cond)
 def test_stop(self):
  g=get('catalog/readiness/v99-2026-11-28-r195-all237-gates.json');self.assertTrue(all(not x['ready_to_acquire'] and x['blocking_gates'] for x in g['records']));self.assertEqual(g['summary']['blocking_gate_counts'],dict(collections.Counter(k for x in g['records'] for k in x['blocking_gates'])))
 def test_bytes(self):
  m=get('manifests/drafts/r195-2026-11-28-seislm-source.candidate.json');self.assertEqual(sum(x['bytes'] for x in m['files']),45633248);self.assertEqual(sum(x['bytes'] for x in m['files'] if x['selected']),45546712);self.assertEqual(sum(x['selected'] for x in m['files']),7);self.assertIsNone(m['complete_dependency_inclusive_bytes']);self.assertFalse(m['download_approved'])
 def test_current(self):
  c=get('catalog/CURRENT.json')
  if c['revision_id']=='v99-20261128':
   self.assertEqual(c['expected']['tracked'],293);self.assertEqual(c['expected']['active'],237);self.assertEqual(c['materialized_catalog_path'],'catalog/effective-portfolio-2026-11-28-v99.json');self.assertEqual(get('queues/approved.json')['entries'],[]);self.assertEqual(get('catalog/execution/2026-11-19-acquisition-ledger.json')['summary']['models_verified'],133)
if __name__=='__main__':unittest.main()
