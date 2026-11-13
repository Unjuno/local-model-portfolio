"""v28 fail-closed catalog consistency checks, Python >=3.10 standard library."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class V28Selection(unittest.TestCase):
 def test_two_additions_and_no_download(self):
  v=load('catalog/effective-portfolio-2026-11-12-v28.json')
  prev=load('catalog/effective-portfolio-2026-11-07-v27.json')
  c=v
  q=load('queues/proposed-v28-2026-11-12.json')
  p=load('catalog/preparation/2026-11-12-insurance-bundles-v28.json')
  self.assertEqual(len(v['items']),175)
  self.assertEqual(v['items'][:173],prev['items'])
  self.assertEqual(len({(x['asset_kind'],x['repo_id'].lower()) for x in v['items']}),175)
  self.assertEqual({x['repo_id'] for x in v['items'][173:]},{'qvac/BotPsy-0.8B','ibm-granite/granite-timeseries-ttm-r3'})
  self.assertEqual(c['revision_id'],'v28-20261112')
  self.assertEqual(c['counts']['active'],128)
  self.assertEqual(c['counts']['parameter_gate'],{'PASS_TOTAL_PARAMS_LT_150B':127,'UNVERIFIED_BLOCK_FINAL_LOCK':20,'OVER_150B_QUANT_REVIEW_REQUIRED':2})
  self.assertEqual(len(q['candidates']),128)
  self.assertEqual(len(p['items']),128)
  self.assertFalse(q['download_enabled'])
  self.assertFalse(p['download_enabled'])
  self.assertTrue(all(x['not_authorized'] and not x['download_approved'] for x in q['candidates']))
  self.assertEqual(load('queues/approved.json')['entries'],[])
  self.assertTrue(all(x['fully_pinned_revision_sha'] is None and x['selected_file_bytes'] is None and not x['download_approved'] for x in v['items'][173:]))
if __name__=='__main__':unittest.main()
