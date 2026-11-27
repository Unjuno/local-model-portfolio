import json, unittest, collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p): return json.loads((R/p).read_text())
def key(x):return x['asset_kind'],x['repo_id']
class V78Specialist(unittest.TestCase):
 def test_previous_rows_and_one_add(self):
  old=read('catalog/effective-portfolio-2026-11-28-v77.json')['items'];new=read('catalog/effective-portfolio-2026-11-28-v78.json')['items'];self.assertEqual(new[:-1],old);self.assertEqual(len(new),270);self.assertEqual(new[-1]['repo_id'],'nvidia/c-fast-foundationstereo');self.assertEqual(new[-1]['portfolio_decision'],'conditional');self.assertIsNone(new[-1]['parameter_gate']['total_parameters']);self.assertFalse(new[-1]['can_enter_approved_queue'])
 def test_manifest_and_alternative_formats(self):
  m=read('manifests/drafts/r175-2026-11-28-five-specialist-publisher-sources-UNAPPROVED.candidate.json');self.assertEqual(len(m['repositories']),5);self.assertEqual(sum(len(s['files']) for s in m['repositories']),106);self.assertFalse(m['download_approved'])
  for s in m['repositories']:
   self.assertRegex(s['revision'],r'^[0-9a-f]{40}$');self.assertEqual(sum(f['bytes'] for f in s['files']),s['full_publisher_bytes'])
   for f in s['files']:
    self.assertRegex(f['git_blob_oid'],r'^[0-9a-f]{40}$')
    if f['publisher_lfs_sha256']:self.assertRegex(f['publisher_lfs_sha256'],r'^[0-9a-f]{64}$')
  s=m['repositories'][0];self.assertEqual(s['full_publisher_bytes'],277572515);self.assertEqual(s['candidate_source_bytes'],71115522);self.assertFalse(any(p.startswith('onnx/') for p in s['candidate_source_paths']));self.assertEqual(sum(f['bytes'] for f in s['files'] if f['path'].startswith('onnx/')),206456993)
 def test_joins_and_fail_closed(self):
  items=read('catalog/effective-portfolio-2026-11-28-v78.json')['items'];active={key(x) for x in items if x['portfolio_decision'] in ('select','conditional')};cond={key(x) for x in items if x['portfolio_decision']=='conditional'}
  self.assertEqual(len(active),214);self.assertEqual(len(cond),158)
  for rows in (read('queues/proposed-v78-2026-11-28.json')['candidates'],read('catalog/preparation/2026-11-28-insurance-bundles-v78.json')['items'],read('catalog/readiness/v78-2026-11-28-r175-all214-gates.json')['records']):
   self.assertEqual(len(rows),214);self.assertEqual({key(x) for x in rows},active);self.assertTrue(all(not x['download_approved'] for x in rows))
  self.assertEqual({key(x) for x in read('catalog/access/2026-11-28-v78-conditional-hub-gates.json')['entries']},cond)
  self.assertTrue(all(not x['ready_to_acquire'] and x['final_selected_file_bytes'] is None for x in read('catalog/readiness/v78-2026-11-28-r175-all214-gates.json')['records']));self.assertEqual(read('queues/approved.json')['entries'],[])
 def test_hold_not_registered(self):
  d=read('catalog/decisions/2026-11-28-r175-new-specialist-adjudication.json');c={x['repo_id'] for x in read('catalog/effective-portfolio-2026-11-28-v78.json')['items']};self.assertEqual(sum(x['decision']=='HOLD' for x in d['decisions']),4);self.assertTrue(all(x['repo_id'] not in c for x in d['decisions'] if x['decision']=='HOLD'));self.assertFalse(read('queues/proposed-v78-r175-specialist-research-UNAPPROVED.json')['download_enabled'])
