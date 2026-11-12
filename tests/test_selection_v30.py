"""v30 Alpamayo2 Edge original VLA safe, non-executable selection audit."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def ld(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
class V30(unittest.TestCase):
 def test_single_conditional_vla_and_formal_count(self):
  prev=ld('catalog/effective-portfolio-2026-11-12-v29.json')
  cur=ld('catalog/effective-portfolio-2026-11-12-v30.json')
  cat=ld('catalog/CURRENT.json');q=ld('queues/proposed-v30-2026-11-12.json')
  p=ld('catalog/preparation/2026-11-12-insurance-bundles-v30.json')
  self.assertEqual(cur['items'][:177],prev['items'])
  self.assertEqual(len(cur['items']),178)
  self.assertEqual(len({(x['asset_kind'],x['repo_id'].lower()) for x in cur['items']}),178)
  self.assertEqual(cur['items'][-1]['repo_id'],'nvidia/Alpamayo2-Edge')
  self.assertEqual(cur['items'][-1]['portfolio_decision'],'conditional')
  self.assertEqual(cur['items'][-1]['parameter_gate']['total_parameters'],2651163378)
  self.assertTrue(cur['items'][-1]['license_text_reviewed'])
  self.assertFalse(cur['items'][-1]['download_approved'])
  self.assertIsNone(cur['items'][-1]['fully_pinned_revision_sha'])
  self.assertIsNone(cur['items'][-1]['selected_file_bytes'])
  self.assertEqual(cat['expected']['tracked'],178);self.assertEqual(cat['expected']['active'],131)
  self.assertEqual(cat['expected']['parameter_gate'],{'PASS_TOTAL_PARAMS_LT_150B':130,'UNVERIFIED_BLOCK_FINAL_LOCK':20,'OVER_150B_QUANT_REVIEW_REQUIRED':2})
  self.assertEqual(len(q['candidates']),131);self.assertEqual(len(p['items']),131)
  self.assertFalse(q['approved']);self.assertFalse(q['download_enabled']);self.assertFalse(p['download_enabled'])
  self.assertTrue(all(x['not_authorized'] and not x['download_approved'] for x in q['candidates']))
  self.assertEqual(ld('queues/approved.json')['entries'],[])
 def test_fixed_publisher_lfs_identity(self):
  r=ld('catalog/research/2026-11-12-r50-alpamayo-edge-immutable.json')
  self.assertEqual(len(r['repo_current_files']),12)
  self.assertEqual(r['repo_current_full_bytes'],5320375887)
  self.assertEqual(r['model_shard_bytes'],5302442268)
  self.assertTrue(r['old_vs_new']['weight_shard_sha_same'])
  self.assertEqual(r['old_vs_new']['delta_bytes_total'],6110)
  self.assertTrue(r['validation']['no_runtime_execution'])
if __name__=='__main__':unittest.main()
