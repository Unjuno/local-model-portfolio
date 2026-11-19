# Offline R128 static source and selection integrity; no model code execution.
import unittest,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class R128(unittest.TestCase):
 def test_selection(self):
  c=load("catalog/CURRENT.json");e=load("catalog/effective-portfolio-2026-11-20-v55.json");m=load("manifests/drafts/r128-2026-11-20-olala-mini-final-and-base-originals.candidate.json")
  self.assertEqual(c["revision_id"],"v55-20261120")
  self.assertEqual(c["materialized_catalog_path"],"catalog/effective-portfolio-2026-11-20-v55.json")
  self.assertEqual(len(e["items"]),209)
  self.assertEqual(len({(a["asset_kind"],a["repo_id"]) for a in e["items"]}),209)
  self.assertEqual(e["counts"]["parameter_gate"]["PASS_TOTAL_PARAMS_LT_150B"],159)
  self.assertEqual(c["expected"]["parameter_gate"]["PASS_TOTAL_PARAMS_LT_150B"],159)
  self.assertEqual(sum(x["portfolio_decision"] in ("select","conditional") for x in e["items"]),162)
  self.assertEqual(m["source_files"],33)
  self.assertEqual(m["publisher_source_bytes"],27186930780)
  self.assertNotEqual(m["sources"][0]["original_weight_sha256"],m["sources"][1]["original_weight_sha256"])
 def test_gates(self):
  self.assertEqual(len(load("queues/proposed-v55-2026-11-20.json")["candidates"]),162)
  self.assertEqual(len(load("catalog/readiness/v55-2026-11-20-r128-all162-gates.json")["records"]),162)
  self.assertEqual(len(load("catalog/access/2026-11-20-v55-conditional-hub-gates.json")["entries"]),109)
  self.assertEqual(len(load("catalog/preparation/2026-11-20-insurance-bundles-v55.json")["items"]),162)
  self.assertEqual(load("queues/approved.json")["entries"],[])
if __name__=="__main__":unittest.main()
