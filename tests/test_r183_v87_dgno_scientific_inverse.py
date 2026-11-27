import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
def key(x):return x["asset_kind"],x["repo_id"]
class DGNOFormal(unittest.TestCase):
 def test_append_only(self):
  old=load("catalog/effective-portfolio-2026-11-28-v86.json")["items"];new=load("catalog/effective-portfolio-2026-11-28-v87.json")["items"];self.assertEqual(new[:-1],old);self.assertEqual(len(new),281);self.assertEqual(new[-1],load("catalog/revisions/v87-2026-11-28.json")["additions"][0]);self.assertEqual(len(set(map(key,new))),281);self.assertEqual(new[-1]["parameter_gate"]["status"],"UNVERIFIED_BLOCK_FINAL_LOCK")
 def test_scopes(self):
  m=load("manifests/drafts/r183-2026-11-28-dgno-fluorescence-source.candidate.json");s=m["source_models"][0];self.assertEqual(len(s["source_files"]),10);self.assertEqual(sum(f["bytes"] for f in s["source_files"]),3991019385);self.assertEqual(sum(f["bytes"] for f in s["source_files"] if f["selected_candidate"]),205417842);self.assertEqual(len(m["runtime_source"]["source_files"]),59);self.assertEqual(sum(f["bytes"] for f in m["runtime_source"]["source_files"]),481026);self.assertEqual(m["combined_selected_model_plus_code_reference_bytes"],205898868);self.assertFalse(m["download_enabled"]);self.assertIsNone(m["complete_dependency_inclusive_bytes"]);self.assertTrue(m["formal_catalog_promotion_performed"]);self.assertEqual({f["path"] for f in s["source_files"] if f["selected_candidate"] and f["lfs_sha256"]},{"pretrained/DGNO_BBBC006_w1_Cell.pth","pretrained/DGNO_BBBC006_w2_Face.pth"})
 def test_joins_and_stop(self):
  new=load("catalog/effective-portfolio-2026-11-28-v87.json")["items"];act={key(x) for x in new if x["portfolio_decision"] in ("select","conditional")};con={key(x) for x in new if x["portfolio_decision"]=="conditional"};self.assertEqual(len(act),225);self.assertEqual(len(con),169)
  for p,k in [("queues/proposed-v87-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v87.json","items"),("catalog/readiness/v87-2026-11-28-r183-all225-gates.json","records"),("catalog/access/2026-11-28-v87-conditional-hub-gates.json","entries")]:
   z=load(p)[k];self.assertEqual({key(x) for x in z},con if k=="entries" else act);self.assertEqual(len(z),169 if k=="entries" else 225)
  self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in load("catalog/readiness/v87-2026-11-28-r183-all225-gates.json")["records"]));self.assertEqual(load("queues/approved.json")["entries"],[])
