"""Fail-closed canonical selection checks across immutable revisions (stdlib)."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):
 p=(ROOT/path).resolve()
 if not p.is_relative_to(ROOT.resolve()):raise ValueError("unsafe path")
 return json.loads(p.read_text(encoding="utf-8"))
def identity(x):return x["asset_kind"],x["repo_id"]
ACTIVE={"select","conditional"}
class CurrentPortfolioIntegrity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.current=read("catalog/CURRENT.json")
  cls.view=read(cls.current["materialized_catalog_path"])
  cls.queue=read(cls.current["priority_worklist_path"])
  cls.prep=read(cls.current["insurance_preparation_worklist_path"])
  cls.access=read(cls.current["latest_conditional_access_audit"]["path"])
 def test_latest_revision_and_exact_counts(self):
  c=self.current;v=self.view
  self.assertEqual(c["revision_id"],"v37-20261115")
  self.assertEqual(v["revision_id"],c["revision_id"])
  self.assertEqual(len(v["items"]),191)
  self.assertEqual(len({identity(x) for x in v["items"]}),191)
  self.assertEqual(v["counts"]["tracked"],c["expected"]["tracked"])
  self.assertEqual(v["counts"]["active"],c["expected"]["active"])
  self.assertEqual(sum(x["asset_kind"]=="model" for x in v["items"]),165)
  self.assertEqual(sum(x["asset_kind"]=="dataset" for x in v["items"]),26)
  self.assertEqual({d:sum(x["portfolio_decision"]==d for x in v["items"]) for d in ("select","conditional","hold","deferred","excluded")},{"select":53,"conditional":91,"hold":28,"deferred":13,"excluded":6})
  self.assertEqual(c["ordered_overlays"][-1],"catalog/revisions/v37-2026-11-15.json")
  self.assertTrue(all(x["download_approved"] is False for x in v["items"]))
 def test_preserve_old_150_assets(self):
  old=read("catalog/effective-portfolio-2026-11-06-v19.json")
  records={identity(x):x for x in self.view["items"]}
  self.assertEqual(len(old["items"]),150)
  for x in old["items"]:
   self.assertIn(identity(x),records)
   self.assertEqual(records[identity(x)]["portfolio_decision"],x["portfolio_decision"])
  self.assertEqual(len(records)-len(old["items"]),41)
 def test_queue_dependency_and_access_id_join(self):
  v=self.view
  active={identity(x) for x in v["items"] if x["portfolio_decision"] in ACTIVE}
  conditional={identity(x) for x in v["items"] if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),144)
  self.assertEqual(active,{identity(x) for x in self.queue["candidates"]})
  self.assertEqual(active,{identity(x) for x in self.prep["items"]})
  self.assertEqual(conditional,{identity(x) for x in self.access["entries"]})
  self.assertEqual(len(self.access["entries"]),91)
  self.assertEqual(sum(x["hub_gated"] for x in self.access["entries"]),19)
  self.assertTrue(self.access["fail_closed_if_missing"])
  self.assertTrue(all(x["owner_access_permission"]=="unknown" and not x["download_authorized"] for x in self.access["entries"]))
  self.assertEqual(self.queue["source_revision"],self.current["revision_id"])
  self.assertEqual(self.prep["source_revision"],self.current["revision_id"])
  self.assertFalse(self.queue["approved"]);self.assertFalse(self.queue["download_enabled"]);self.assertFalse(self.prep["download_enabled"])
  self.assertTrue(all(x["not_authorized"] and not x["download_approved"] for x in self.queue["candidates"]))
  self.assertEqual(read("queues/approved.json")["entries"],[])
 def test_parameter_and_capacity_blocks(self):
  policy=read("policies/limits.json")
  self.assertEqual(policy["archive_target_bytes"],4_000_000_000_000)
  self.assertEqual(policy["minimum_free_bytes"],200_000_000_000)
  unknown={identity(x) for x in self.view["items"] if x["asset_kind"]=="model" and x["portfolio_decision"] in ACTIVE and x["parameter_gate"]["status"]=="UNVERIFIED_BLOCK_FINAL_LOCK"}
  self.assertEqual(len(unknown),9)
  q={identity(x):x for x in self.queue["candidates"]}
  self.assertTrue(all(q[k]["research_only"] and not q[k]["can_enter_approved_queue"] for k in unknown))
  r=read(self.current["latest_active_readiness_audit"]["summary_path"])
  self.assertEqual(len(r["records"]),144)
  self.assertEqual(r["summary"]["ready_to_approve"],0)
if __name__=="__main__":unittest.main()
