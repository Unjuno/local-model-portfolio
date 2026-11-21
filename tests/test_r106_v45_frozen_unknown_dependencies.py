"""Validate R106 v45 source and four independent fail-closed dependency reasons."""
import unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def j(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def k(x):return x["asset_kind"],x["repo_id"].lower()
class TestR106(unittest.TestCase):
 def test_current_joins(self):
  c=j("catalog/CURRENT.json")
  self.assertIn("catalog/revisions/v45-2026-11-18.json", c["ordered_overlays"])
  v=j("catalog/effective-portfolio-2026-11-18-v45.json")
  q=j("queues/proposed-v45-2026-11-18.json")
  p=j("catalog/preparation/2026-11-18-insurance-bundles-v45.json")
  a=j("catalog/access/2026-11-18-v45-conditional-hub-gates.json")
  r=j("catalog/readiness/v45-2026-11-18-r106-all151-gates.json")
  active={k(x) for x in v["items"] if x["portfolio_decision"] in ("select","conditional")}
  cond={k(x) for x in v["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(v["revision_id"],"v45-20261118")
  self.assertEqual((len(v["items"]),len(active),len(cond)),(198,151,98))
  self.assertEqual(active,{k(x) for x in q["candidates"]})
  self.assertEqual(active,{k(x) for x in p["items"]})
  self.assertEqual(active,{k(x) for x in r["records"]})
  self.assertEqual(cond,{k(x) for x in a["entries"]})
  self.assertEqual(sum(x["hub_gated"] is True for x in a["entries"]),20)
  self.assertFalse(any(x["download_approved"] for x in v["items"]))
  self.assertEqual(r["summary"]["unknown_total_active"],9)
  self.assertEqual(j("queues/approved.json")["entries"],[])
 def test_source_scopes_and_hard_blocks(self):
  s=j("catalog/research/2026-11-18-r106-four-unknown-model-static-scope.json")
  r=j("catalog/readiness/v45-2026-11-18-r106-all151-gates.json")
  self.assertEqual(len(s["records"]),4)
  self.assertEqual(s["records"][0]["detail"]["stored_elements_from_prior_r66"],49635347496)
  self.assertEqual(s["records"][1]["detail"]["mandatory_codec"]["bytes"],1871099728)
  self.assertEqual(s["records"][2]["detail"]["external_trained_dependencies"],["kyutai/mimi","speechbrain/spkrec-ecapa-voxceleb"])
  self.assertEqual(s["records"][3]["detail"]["anonymous_config_status"],401)
  for x in s["records"]:
   rr=next(a for a in r["records"] if a["repo_id"]==x["repo_id"])
   self.assertIn(x["blocking_gate"],rr["blocking_gates"])
   self.assertEqual(rr["parameter_gate"],"UNVERIFIED_BLOCK_FINAL_LOCK")
   self.assertFalse(rr["ready_to_acquire"])
if __name__=="__main__":unittest.main()
