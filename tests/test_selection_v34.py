"""V34 full adoption: old 185 v33 items untouched, 3 distinct learned science checkpoints."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rd(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
class V34(unittest.TestCase):
 def test_append_only_and_research_only(self):
  old=rd("catalog/effective-portfolio-2026-11-15-v33.json")
  new=rd("catalog/effective-portfolio-2026-11-15-v34.json")
  ov=rd("catalog/revisions/v34-2026-11-15.json")
  current=rd("catalog/CURRENT.json")
  self.assertEqual(new["items"][:185],old["items"])
  self.assertEqual(len(new["items"]),188)
  self.assertEqual(len({(x["asset_kind"],x["repo_id"]) for x in new["items"]}),188)
  self.assertEqual(new["counts"]["active"],141)
  self.assertEqual(current["revision_id"],"v34-20261115")
  self.assertEqual({x["repo_id"] for x in ov["additions"]},{"nvidia/Kumo-Anomaly","nvidia/Ising-Decoder-ColorCode-1-Fast","nvidia/Ising-Decoder-SurfaceCode-1-Fast"})
  self.assertEqual(ov["selected_publisher_source_candidate_bytes"],37372669)
  self.assertTrue(all(x["portfolio_decision"]=="conditional" and x["selected_file_bytes"] is None
      and x["fully_pinned_revision_sha"] is None and x["download_approved"] is False
      for x in ov["additions"]))
 def test_141_queue_88_gates_and_true_user_stop(self):
  c=rd("catalog/effective-portfolio-2026-11-15-v34.json")
  q=rd("queues/proposed-v34-2026-11-15.json")
  p=rd("catalog/preparation/2026-11-15-insurance-bundles-v34.json")
  a=rd("catalog/access/2026-11-15-v34-conditional-hub-gates.json")
  r=rd("catalog/readiness/v34-2026-11-15-r81-all141-gates.json")
  keys=lambda xs:{(x["asset_kind"],x["repo_id"]) for x in xs}
  active=[x for x in c["items"] if x["portfolio_decision"] in ("select","conditional")]
  self.assertEqual(keys(active),keys(q["candidates"]))
  self.assertEqual(keys(active),keys(p["items"]))
  self.assertEqual(len(active),141)
  self.assertEqual(len(a["entries"]),88)
  self.assertEqual(sum(x["hub_gated"] for x in a["entries"]),19)
  self.assertEqual(r["summary"]["active"],141)
  self.assertEqual(sum(r["summary"]["first_blocker_counts"].values()),141)
  self.assertEqual(rd("queues/approved.json")["entries"],[])
  self.assertFalse(q["approved"])
  self.assertFalse(q["download_enabled"])
 def test_true_model_construction_not_quant_duplicates(self):
  items={x["repo_id"]:x for x in rd("catalog/effective-portfolio-2026-11-15-v34.json")["items"]}
  self.assertEqual(items["nvidia/Ising-Decoder-SurfaceCode-1-Fast"]["parameter_gate"]["total_parameters"],912772)
  self.assertEqual(items["nvidia/Ising-Decoder-ColorCode-1-Fast"]["parameter_gate"]["total_parameters"],2936580)
  self.assertEqual(items["nvidia/Kumo-Anomaly"]["parameter_gate"]["status"],"UNVERIFIED_BLOCK_FINAL_LOCK")
  self.assertFalse(items["nvidia/Kumo-Anomaly"]["execution_safety"]["execution_approved"])
  self.assertNotIn("nvidia/Nemotron-3.5-Parse",items)
  self.assertEqual(items["nvidia/Ising-Decoder-SurfaceCode-1-Fast"]["upstream_model_file"]["bytes_exact"],1826360)
if __name__=="__main__":unittest.main()
