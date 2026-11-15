"""v43 rights evidence correction must be isolated to existing GR00T N1.6, no downloads."""
import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding="utf-8"))
def key(x):return x["asset_kind"],x["repo_id"]
class GR00TLicenseV43(unittest.TestCase):
 def test_exact_one_existing_asset_corrected(self):
  a=read("catalog/effective-portfolio-2026-11-15-v42.json")["items"]
  b=read("catalog/effective-portfolio-2026-11-15-v43.json")["items"]
  self.assertEqual(len(a),195);self.assertEqual(len(b),195)
  self.assertEqual({key(x) for x in a},{key(x) for x in b})
  self.assertEqual([(x["portfolio_decision"]) for x in a],[(x["portfolio_decision"]) for x in b])
  self.assertEqual([x["repo_id"] for x,y in zip(a,b) if x!=y],["nvidia/GR00T-N1.6-3B"])
  x=next(x for x in b if x["repo_id"]=="nvidia/GR00T-N1.6-3B")
  self.assertEqual(x["license_original_reviewed_date"],"2026-11-15")
  self.assertTrue(x["noncommercial_use_scope_publisher_license_confirmed"])
  self.assertIn("non-commercial",x["license_metadata"])
  self.assertFalse(x["license_text_reviewed"]);self.assertFalse(x["license_all_acts_user_signoff"])
  self.assertFalse(x["download_approved"])
  self.assertFalse(any(y["repo_id"]=="nvidia/GR00T-N1.7-3B" for y in b))
 def test_queue_access_readiness_and_hdd_stay_blocked(self):
  c=read("catalog/CURRENT.json")
  self.assertEqual(c["revision_id"],"v43-20261115")
  view=read(c["materialized_catalog_path"])
  q=read(c["priority_worklist_path"])
  p=read(c["insurance_preparation_worklist_path"])
  a=read(c["latest_conditional_access_audit"]["path"])
  r=read(c["latest_active_readiness_audit"]["summary_path"])
  self.assertEqual(len(view["items"]),195)
  self.assertEqual(len(q["candidates"]),len(p["items"]),len(r["records"]))
  self.assertEqual(len(q["candidates"]),148);self.assertEqual(len(a["entries"]),95)
  self.assertEqual(a["gated_count"],20);self.assertEqual(r["summary"]["ready_to_approve"],0)
  self.assertEqual(r["summary"]["downloads_approved"],0)
  self.assertEqual(r["summary"]["blocking_gate_counts"]["GR00T_N16_NONCOMMERCIAL_LICENSE_AND_N17_REPLACEMENT_DEPENDENCY_REVIEW"],1)
  self.assertEqual(read("queues/approved.json")["entries"],[])
  self.assertEqual(read("catalog/readiness/CURRENT.json")["catalog_revision"],c["revision_id"])
  self.assertEqual(read("catalog/estimates/CURRENT.json")["portfolio_revision"],c["revision_id"])
 def test_hold_is_documented_not_download_or_swap(self):
  a=read("catalog/revisions/v43-2026-11-15.json")
  self.assertEqual(a["changes"][0]["expected_old_license_metadata"],"unknown")
  self.assertEqual(a["non_selected_replacement"]["decision"],"RESEARCH_HOLD_NO_ASSET_ADDED")
  self.assertEqual(a["selection_added"],0)
  self.assertFalse(a["download_approved"])
if __name__=="__main__":unittest.main()
