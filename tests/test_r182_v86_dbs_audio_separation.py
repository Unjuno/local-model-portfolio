import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
def key(x):return x["asset_kind"],x["repo_id"]
class DBSFormal(unittest.TestCase):
 def test_append_only(self):
  old=load("catalog/effective-portfolio-2026-11-28-v85.json")["items"];new=load("catalog/effective-portfolio-2026-11-28-v86.json")["items"];self.assertEqual(new[:-1],old);self.assertEqual(len(new),280);self.assertEqual(new[-1],load("catalog/revisions/v86-2026-11-28.json")["additions"][0]);self.assertEqual(len(set(map(key,new))),280)
 def test_scopes(self):
  m=load("manifests/drafts/r182-2026-11-28-dbs-audio-source-frozen.candidate.json");s,h=m["source_models"];self.assertEqual(sum(f["bytes"] for f in s["source_files"]),4116715);self.assertEqual(sum(f["bytes"] for f in h["source_files"]),18891321);self.assertEqual(sum(f["bytes"] for f in m["runtime_source"]["source_files"]),206489);self.assertEqual(m["combined_selected_model_plus_code_reference_bytes"],4323204);self.assertFalse(m["download_enabled"]);self.assertIsNone(m["complete_dependency_inclusive_bytes"]);self.assertTrue(m["formal_catalog_promotion_performed"])
 def test_joins_and_stop(self):
  new=load("catalog/effective-portfolio-2026-11-28-v86.json")["items"];act={key(x) for x in new if x["portfolio_decision"] in ("select","conditional")};con={key(x) for x in new if x["portfolio_decision"]=="conditional"};self.assertEqual(len(act),224);self.assertEqual(len(con),168)
  for p,k in [("queues/proposed-v86-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v86.json","items"),("catalog/readiness/v86-2026-11-28-r182-all224-gates.json","records"),("catalog/access/2026-11-28-v86-conditional-hub-gates.json","entries")]:
   z=load(p)[k];self.assertEqual({key(x) for x in z},con if k=="entries" else act);self.assertEqual(len(z),168 if k=="entries" else 224)
  self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in load("catalog/readiness/v86-2026-11-28-r182-all224-gates.json")["records"]));self.assertEqual(load("queues/approved.json")["entries"],[])
