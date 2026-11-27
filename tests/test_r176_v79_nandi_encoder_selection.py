import collections,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def key(r):return r['asset_kind'],r['repo_id']
class R176NandiResearch(unittest.TestCase):
 def test_delta(self):
  old=load('catalog/effective-portfolio-2026-11-28-v78.json')['items']; new=load('catalog/effective-portfolio-2026-11-28-v79.json')['items']; self.assertEqual(len(old),270); self.assertEqual(len(new),272);self.assertEqual(old,new[:270]);self.assertEqual(load('catalog/revisions/v79-2026-11-28.json')['additions'],new[270:]);self.assertEqual({r['repo_id'] for r in new[270:]},{'FrontiersMind/NandiBERT-150M','FrontiersMind/NandiBERT-450M'})
  self.assertEqual(collections.Counter(r['portfolio_decision'] for r in new),{'conditional':160,'select':56,'hold':37,'deferred':13,'excluded':6})
 def test_source_identity_and_capacity(self):
  m=load('manifests/drafts/r176-2026-11-28-nandibert-and-ocr-four-source-frozen.candidate.json');s=m['source_repos'];self.assertEqual(sum(len(x['files']) for x in s),95);self.assertEqual(sum(x['bytes'] for x in s),4732113070);seen={};weights=[]
  for r in s:
   self.assertRegex(r['revision'],r'^[0-9a-f]{40}$');self.assertEqual(r['bytes'],sum(f['size'] for f in r['files']));self.assertFalse(r['gated'])
   for f in r['files']:
    self.assertRegex(f['oid'],r'^[0-9a-f]{40}$')
    if f['lfs']:self.assertRegex(f['lfs']['oid'],r'^[0-9a-f]{64}$');self.assertEqual(f['lfs']['size'],f['size'])
    if r['repo_id'].startswith('FrontiersMind/'):
     k=('lfs',f['lfs']['oid']) if f['lfs'] else ('git',f['oid']);self.assertEqual(seen.get(k,f['size']),f['size']);seen[k]=f['size']
     if f['path'].endswith('.safetensors'):weights.append(k)
  self.assertEqual(len(set(weights)),2);self.assertEqual(sum(seen.values()),1553775254);self.assertFalse(m['download_approved'])
 def test_stops(self):
  v=load('catalog/effective-portfolio-2026-11-28-v79.json')['items'];a={key(x) for x in v if x['portfolio_decision'] in ('select','conditional')};c={key(x) for x in v if x['portfolio_decision']=='conditional'};r=load('catalog/readiness/v79-2026-11-28-r176-all216-gates.json');self.assertEqual(r['records'][:214],load('catalog/readiness/v78-2026-11-28-r175-all214-gates.json')['records'])
  for rs in (r['records'],load('queues/proposed-v79-2026-11-28.json')['candidates'],load('catalog/preparation/2026-11-28-insurance-bundles-v79.json')['items']):self.assertEqual(len(rs),216);self.assertEqual({key(x) for x in rs},a)
  self.assertEqual({key(x) for x in load('catalog/access/2026-11-28-v79-conditional-hub-gates.json')['entries']},c);self.assertTrue(all(not x['download_approved'] and not x['ready_to_acquire'] and x['final_selected_file_bytes'] is None for x in r['records']));self.assertEqual(load('queues/approved.json')['entries'],[])
  self.assertEqual(r['summary']['blocking_gate_counts'],dict(collections.Counter(g for x in r['records'] for g in x['blocking_gates'])))
