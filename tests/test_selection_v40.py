"""GroundingPI v40 exact original source and fail-closed acquisition regression."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
class GroundingPIv40(unittest.TestCase):
 def test_preserves_entire_v39_and_only_one_addition(self):
  a=load("catalog/effective-portfolio-2026-11-15-v39.json")["items"]
  b=load("catalog/effective-portfolio-2026-11-15-v40.json")["items"]
  self.assertEqual(len(a),194); self.assertEqual(len(b),195)
  self.assertEqual(b[:194],a)
  self.assertEqual(b[-1]["repo_id"],"GroundingPI/GroundingPI")
  self.assertEqual(b[-1]["parameter_gate"]["total_parameters"],4843664384)
  self.assertFalse(b[-1]["download_approved"])
  self.assertIsNone(b[-1]["fully_pinned_revision_sha"])
  self.assertIsNone(b[-1]["selected_file_bytes"])
 def test_checksums_source_and_rights_remain_conditional(self):
  m=load("manifests/drafts/v39-groundingpi-source28.candidate.json")
  e=load("catalog/research/2026-11-15-r88-groundingpi-thinker-original-license-comparison.json")
  self.assertEqual(len(m["files"]),28)
  self.assertEqual(sum(x["bytes"] for x in m["files"]),9704102624)
  self.assertEqual(m["original_BF16_shard_bytes"],9687403168)
  self.assertEqual(e["ground"]["weight_metadata"]["index_parameters"],4843664384)
  self.assertEqual(e["ground"]["weight_metadata"]["headers_overhead_bytes"],74400)
  self.assertIn("LICENSE-Kimi-K3",m["license_scopes"])
  self.assertFalse(m["authorized_download"])
 def test_current_all_id_joins_and_owner_gate(self):
  c=load("catalog/CURRENT.json")
  self.assertEqual(load("catalog/effective-portfolio-2026-11-15-v40.json")["revision_id"],"v40-20261115")
  v=load(c["materialized_catalog_path"])
  q=load(c["priority_worklist_path"])
  p=load(c["insurance_preparation_worklist_path"])
  a=load(c["latest_conditional_access_audit"]["path"])
  r=load(c["latest_active_readiness_audit"]["summary_path"])
  key=lambda x:(x["asset_kind"],x["repo_id"])
  ids={key(x) for x in v["items"] if x["portfolio_decision"] in ("select","conditional")}
  self.assertEqual(len(ids),148)
  self.assertEqual(ids,{key(x) for x in q["candidates"]})
  self.assertEqual(ids,{key(x) for x in p["items"]})
  self.assertEqual(ids,{key(x) for x in r["records"]})
  self.assertEqual(len(a["entries"]),95)
  self.assertEqual(a["gated_count"],20)
  self.assertEqual(r["summary"]["unknown_total_active"],9)
  self.assertEqual(r["summary"]["ready_to_approve"],0)
  self.assertEqual(load("queues/approved.json")["entries"],[])
if __name__=="__main__":unittest.main()
