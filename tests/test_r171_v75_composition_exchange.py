import json, unittest, collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8'))
def key(x):return x['asset_kind'],x['repo_id']
class V75Composition(unittest.TestCase):
 def test_delta(self):
  o={key(x):x for x in read('catalog/effective-portfolio-2026-11-27-v74.json')['items']};n={key(x):x for x in read('catalog/effective-portfolio-2026-11-28-v75.json')['items']}
  self.assertEqual(len(o),265);self.assertEqual(len(n),266);self.assertEqual(set(n)-set(o),{('model','allenai/RoboTracker')});self.assertFalse(set(o)-set(n));self.assertEqual([k for k in o if o[k]!=n[k]],[('model','Qwen/Qwen3-Omni-30B-A3B-Instruct')]);self.assertEqual(n['model','Qwen/Qwen3-Omni-30B-A3B-Instruct']['portfolio_decision'],'hold');self.assertTrue(n['model','allenai/RoboTracker']['research_only_nonexecutable']);self.assertIsNone(n['model','allenai/RoboTracker']['parameter_gate']['total_parameters']);self.assertFalse(n['model','allenai/RoboTracker']['can_enter_approved_queue']);self.assertEqual(collections.Counter(x['portfolio_decision'] for x in n.values()),{'select':56,'conditional':154,'hold':37,'deferred':13,'excluded':6})
 def test_joins(self):
  m=read('catalog/effective-portfolio-2026-11-28-v75.json')['items'];a={key(x) for x in m if x['portfolio_decision'] in ('select','conditional')};c={key(x) for x in m if x['portfolio_decision']=='conditional'};r=read('catalog/readiness/v75-2026-11-28-r171-all210-gates.json')['records'];q=read('queues/proposed-v75-2026-11-28.json')['candidates'];p=read('catalog/preparation/2026-11-28-insurance-bundles-v75.json')['items'];e=read('catalog/access/2026-11-28-v75-conditional-hub-gates.json')['entries'];self.assertEqual(len(a),210);self.assertEqual(len(c),154)
  for rows in (r,q,p):self.assertEqual(len(rows),210);self.assertEqual(a,{key(x) for x in rows})
  self.assertEqual(c,{key(x) for x in e});self.assertTrue(all(not x['download_approved'] and not x['ready_to_acquire'] and x['final_selected_file_bytes'] is None for x in r));self.assertEqual(read('queues/approved.json')['entries'],[])
 def test_cost(self):
  a=read('catalog/audits/2026-11-28-r171-v75-dependency-aware-composition.json');self.assertEqual(a['source_proxy_delta_bytes'],66011293-70530595574);self.assertTrue(a['source_proxy_delta_is_not_physical_savings']);self.assertFalse(a['physical_capacity_verified']);self.assertEqual(a['physical_deletions'],0)
