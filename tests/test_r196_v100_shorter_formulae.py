import json,pathlib,unittest
R=pathlib.Path(__file__).resolve().parents[1]
def L(p):return json.loads((R/p).read_text(encoding="utf-8"))
def ids(x):return sorted((y["asset_kind"],y["repo_id"]) for y in x)
class Regression(unittest.TestCase):
 def test_append(self):
  a=L("catalog/effective-portfolio-2026-11-28-v99.json");b=L("catalog/effective-portfolio-2026-11-28-v100.json");self.assertEqual(a["items"],b["items"][:-1]);self.assertEqual(b["items"][-1:],L("catalog/revisions/v100-2026-11-28.json")["additions"]);self.assertEqual(len(set(ids(b["items"]))),294);self.assertIsNone(b["items"][-1]["parameter_gate"]["total_parameters"])
 def test_joins(self):
  a=[x for x in L("catalog/effective-portfolio-2026-11-28-v100.json")["items"] if x["portfolio_decision"] in ("select","conditional")];self.assertEqual(len(a),238);self.assertEqual(ids(a),ids(L("queues/proposed-v100-2026-11-28.json")["candidates"]));self.assertEqual(ids(a),ids(L("catalog/preparation/2026-11-28-insurance-bundles-v100.json")["items"]));self.assertEqual(ids([x for x in a if x["portfolio_decision"]=="conditional"]),ids(L("catalog/access/2026-11-28-v100-conditional-hub-gates.json")["entries"]));s=L("catalog/readiness/v100-2026-11-28-r196-all238-gates.json");self.assertEqual(ids(a),ids(s["records"]));self.assertEqual(s["records"][:-1],L("catalog/readiness/v99-2026-11-28-r195-all237-gates.json")["records"]);self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in s["records"]));self.assertEqual(L("queues/approved.json")["entries"],[])
 def test_bytes(self):
  m=L("manifests/drafts/r196-2026-11-28-shorter-formulae-publisher-scope.candidate.json");self.assertEqual(sum(x["bytes"] for x in m["files"]),5485162467);self.assertEqual(sum(x["bytes"] for x in m["files"] if x["selected_source_reference"]),1166430727);self.assertEqual(sum(x["bytes"] for x in m["pinned_code"]["files"]),7088086);self.assertEqual(m["combined_reference_bytes"],1173518813);self.assertIsNone(m["complete_dependency_inclusive_bytes"]);self.assertFalse(m["download_approved"])
 def test_policy(self):
  c=L("catalog/CURRENT.json");self.assertIn("catalog/revisions/v100-2026-11-28.json",c["ordered_overlays"]);self.assertEqual(c["expected"]["archive_limit_bytes"],4000000000000);self.assertEqual(c["expected"]["minimum_free_bytes"],200000000000);self.assertEqual(L("catalog/snapshots/2026-11-28-v99-current-before-v100.json")["revision_id"],"v99-20261128")
if __name__=="__main__":unittest.main()
