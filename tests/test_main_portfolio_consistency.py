"""Current portfolio is one coherent, non-executable, rights-gated selection; stdlib-only."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):
 t=(ROOT/p).resolve()
 if not t.is_relative_to(ROOT.resolve()): raise ValueError("unsafe path")
 return json.loads(t.read_text(encoding="utf-8"))
def key(x): return x["asset_kind"],x["repo_id"].lower()
class CurrentPortfolioIntegrity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=load("catalog/CURRENT.json")
  cls.v=load(cls.c["materialized_catalog_path"])
  cls.q=load(cls.c["priority_worklist_path"])
  cls.p=load(cls.c["insurance_preparation_worklist_path"])
  cls.a=load(cls.c["latest_conditional_access_audit"]["path"])
  cls.r=load(cls.c["latest_active_readiness_audit"]["summary_path"])
 def test_current_counts_and_parent_preservation(self):
  e=self.c["expected"]
  self.assertEqual(self.v["revision_id"],self.c["revision_id"])
  self.assertEqual(len(self.v["items"]),e["tracked"])
  self.assertEqual(len({key(x) for x in self.v["items"]}),e["tracked"])
  self.assertEqual(sum(x["asset_kind"]=="model" for x in self.v["items"]),e["models"])
  self.assertEqual(sum(x["asset_kind"]=="dataset" for x in self.v["items"]),e["datasets"])
  for status,n in e["by_decision"].items():
   self.assertEqual(sum(x["portfolio_decision"]==status for x in self.v["items"]),n)
  old=load("catalog/effective-portfolio-2026-11-06-v19.json")
  active={key(x):x for x in self.v["items"]}
  self.assertEqual(len(old["items"]),150)
  for x in old["items"]:
   self.assertIn(key(x),active)
   self.assertEqual(x["portfolio_decision"],active[key(x)]["portfolio_decision"])
 def test_all_active_id_joins_and_legal_gates(self):
  active={key(x) for x in self.v["items"] if x["portfolio_decision"] in ("select","conditional")}
  cond={key(x) for x in self.v["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),self.c["expected"]["active"])
  self.assertEqual(active,{key(x) for x in self.q["candidates"]})
  self.assertEqual(active,{key(x) for x in self.p["items"]})
  self.assertEqual(active,{key(x) for x in self.r["records"]})
  self.assertEqual(cond,{key(x) for x in self.a["entries"]})
  self.assertEqual(len(cond),self.c["expected"]["by_decision"]["conditional"])
  self.assertEqual(sum(x["hub_gated"] is True for x in self.a["entries"]),self.a["gated_count"])
  self.assertEqual(self.a["source_revision"],self.c["revision_id"])
  self.assertTrue(all(x["owner_access_permission"]=="unknown" and not x["download_authorized"] for x in self.a["entries"]))
  self.assertEqual(self.q["source_revision"],self.c["revision_id"])
  self.assertEqual(self.p["source_revision"],self.c["revision_id"])
  self.assertFalse(self.q["approved"] or self.q["download_enabled"] or self.p["download_enabled"])
  self.assertTrue(all(x["not_authorized"] and not x["download_approved"] for x in self.q["candidates"]))
  self.assertTrue(all(not x["download_approved"] for x in self.v["items"]))
  self.assertEqual(load("queues/approved.json")["entries"],[])
  self.assertEqual(self.r["summary"]["ready_to_approve"],0)
 def test_critical_parameter_unknown_and_storage_floor(self):
  active=[x for x in self.v["items"] if x["portfolio_decision"] in ("select","conditional")]
  u=[x for x in active if x["asset_kind"]=="model" and x["parameter_gate"]["status"]=="UNVERIFIED_BLOCK_FINAL_LOCK"]
  self.assertEqual(len(u),self.c["expected"]["parameter_evidence_review"]["remaining_active_unknown"])
  qq={key(x):x for x in self.q["candidates"]}
  self.assertTrue(all(qq[key(x)]["research_only"] and not qq[key(x)]["can_enter_approved_queue"] for x in u))
  lim=load("policies/limits.json")
  self.assertEqual(lim["archive_target_bytes"],4_000_000_000_000)
  self.assertEqual(lim["minimum_free_bytes"],200_000_000_000)
if __name__=="__main__":unittest.main()
