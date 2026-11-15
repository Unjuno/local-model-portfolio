"""Fail-closed canonical selection checks; supports new immutable revisions without stale hardcoded totals."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ACTIVE={"select","conditional"}
def read(path):
 p=(ROOT/path).resolve()
 if not p.is_relative_to(ROOT.resolve()): raise ValueError("unsafe path")
 return json.loads(p.read_text(encoding="utf-8"))
def identity(x):return x["asset_kind"],x["repo_id"]
class CurrentPortfolioIntegrity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.current=read("catalog/CURRENT.json")
  cls.view=read(cls.current["materialized_catalog_path"])
  cls.queue=read(cls.current["priority_worklist_path"])
  cls.prep=read(cls.current["insurance_preparation_worklist_path"])
  cls.access=read(cls.current["latest_conditional_access_audit"]["path"])
  cls.readiness=read(cls.current["latest_active_readiness_audit"]["summary_path"])
 def test_exact_canonical_counts_and_unique_ids(self):
  c=self.current;v=self.view
  self.assertEqual(v["revision_id"],c["revision_id"])
  self.assertEqual(len(v["items"]),c["expected"]["tracked"])
  self.assertEqual(len({identity(x) for x in v["items"]}),len(v["items"]))
  self.assertEqual(sum(x["asset_kind"]=="model" for x in v["items"]),c["expected"]["models"])
  self.assertEqual(sum(x["asset_kind"]=="dataset" for x in v["items"]),c["expected"]["datasets"])
  for decision,count in c["expected"]["by_decision"].items():
   self.assertEqual(sum(x["portfolio_decision"]==decision for x in v["items"]),count)
  self.assertEqual(v["counts"]["tracked"],c["expected"]["tracked"])
  self.assertEqual(v["counts"]["active"],c["expected"]["active"])
  self.assertEqual(len(c["ordered_overlays"]),len(set(c["ordered_overlays"])))
  self.assertTrue(all(x["download_approved"] is False for x in v["items"]))
 def test_preserve_original_v19_identity(self):
  old=read("catalog/effective-portfolio-2026-11-06-v19.json")
  present={identity(x):x for x in self.view["items"]}
  self.assertEqual(len(old["items"]),150)
  for x in old["items"]:
   self.assertIn(identity(x),present)
   self.assertEqual(x["portfolio_decision"],present[identity(x)]["portfolio_decision"])
 def test_queue_access_readiness_join(self):
  active={identity(x) for x in self.view["items"] if x["portfolio_decision"] in ACTIVE}
  cond={identity(x) for x in self.view["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),self.current["expected"]["active"])
  self.assertEqual(active,{identity(x) for x in self.queue["candidates"]})
  self.assertEqual(active,{identity(x) for x in self.prep["items"]})
  self.assertEqual(active,{identity(x) for x in self.readiness["records"]})
  self.assertEqual(cond,{identity(x) for x in self.access["entries"]})
  self.assertEqual(len(self.access["entries"]),self.current["expected"]["by_decision"]["conditional"])
  self.assertEqual(sum(x["hub_gated"] is True for x in self.access["entries"]),self.access["gated_count"])
  self.assertEqual(self.access["gated_count"],self.current["latest_conditional_access_audit"]["observed_gated"])
  self.assertTrue(self.access["fail_closed_if_missing"])
  self.assertTrue(all(x["owner_access_permission"]=="unknown" and not x["download_authorized"] for x in self.access["entries"]))
  self.assertEqual(self.queue["source_revision"],self.current["revision_id"])
  self.assertEqual(self.prep["source_revision"],self.current["revision_id"])
  self.assertFalse(self.queue["approved"])
  self.assertFalse(self.queue["download_enabled"])
  self.assertFalse(self.prep["download_enabled"])
  self.assertTrue(all(x["not_authorized"] and not x["download_approved"] for x in self.queue["candidates"]))
  self.assertEqual(read("queues/approved.json")["entries"],[])
 def test_parameter_and_owner_capacity_stops(self):
  policy=read("policies/limits.json")
  self.assertEqual(policy["archive_target_bytes"],4_000_000_000_000)
  self.assertEqual(policy["minimum_free_bytes"],200_000_000_000)
  unknown={identity(x) for x in self.view["items"] if x["asset_kind"]=="model" and x["portfolio_decision"] in ACTIVE and x["parameter_gate"]["status"]=="UNVERIFIED_BLOCK_FINAL_LOCK"}
  self.assertEqual(len(unknown),self.current["expected"]["parameter_evidence_review"]["remaining_active_unknown"])
  q={identity(x):x for x in self.queue["candidates"]}
  self.assertTrue(all(q[k]["research_only"] and not q[k]["can_enter_approved_queue"] for k in unknown))
  self.assertEqual(self.readiness["summary"]["active"],len(q))
  self.assertEqual(self.readiness["summary"]["ready_to_approve"],0)
if __name__=="__main__":unittest.main()
