"""v29 static catalog and queue integrity tests (Python 3.10+, stdlib)."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class V29Test(unittest.TestCase):
 def test_two_exact_trained_outcomes(self):
  old=read('catalog/effective-portfolio-2026-11-12-v28.json')
  new=read('catalog/effective-portfolio-2026-11-12-v29.json')
  current=new
  queue=read('queues/proposed-v29-2026-11-12.json')
  plan=read('catalog/preparation/2026-11-12-insurance-bundles-v29.json')
  overlay=read('catalog/revisions/v29-2026-11-12.json')
  self.assertEqual(len(new['items']),177)
  self.assertEqual(new['items'][:175],old['items'])
  self.assertEqual({x['repo_id'] for x in new['items'][175:]},{'Zyphra/ZONOS3-Mini','robbyant/lingbot-touch-tiny'})
  self.assertEqual(len({(x['asset_kind'],x['repo_id'].lower()) for x in new['items']}),177)
  self.assertEqual(current['revision_id'],'v29-20261112')
  self.assertEqual(current['counts']['active'],130)
  self.assertEqual(current['counts']['parameter_gate'],{'PASS_TOTAL_PARAMS_LT_150B':129,'UNVERIFIED_BLOCK_FINAL_LOCK':20,'OVER_150B_QUANT_REVIEW_REQUIRED':2})
  self.assertEqual(len(queue['candidates']),130)
  self.assertEqual(len(plan['items']),130)
  self.assertFalse(queue['approved']);self.assertFalse(queue['download_enabled']);self.assertFalse(plan['download_enabled'])
  self.assertEqual(read('queues/approved.json')['entries'],[])
  self.assertEqual(sum(x['selection_budget_cap_bytes'] for x in overlay['additions']),16300000000)
  self.assertTrue(all(x['not_authorized'] and not x['download_approved'] for x in queue['candidates']))
  self.assertTrue(all(x['fully_pinned_revision_sha'] is None and x['selected_file_bytes'] is None and not x['download_approved'] for x in new['items'][175:]))
  self.assertEqual(new['items'][-2]['parameter_gate']['total_parameters'],886000000)
  self.assertEqual(new['items'][-1]['parameter_gate']['total_parameters'],5460000)
if __name__=='__main__':unittest.main()
