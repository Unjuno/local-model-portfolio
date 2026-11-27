import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def key(x):return x["asset_kind"],x["repo_id"]
class OpenThaiResearch(unittest.TestCase):
 def test_append_only(self):
  a=load("catalog/effective-portfolio-2026-11-28-v79.json")["items"];b=load("catalog/effective-portfolio-2026-11-28-v80.json")["items"]
  self.assertEqual(b[:-1],a);self.assertEqual(len(b),273);self.assertEqual(len({key(x) for x in b}),273);self.assertEqual(b[-1],load("catalog/revisions/v80-2026-11-28.json")["additions"][0]);self.assertEqual(b[-1]["repo_id"],"iapp/OpenThai2.2-OCR-Text-20261127");self.assertIsNone(b[-1]["parameter_gate"]["total_parameters"])
 def test_joins_stop(self):
  b=load("catalog/effective-portfolio-2026-11-28-v80.json")["items"];act={key(x) for x in b if x["portfolio_decision"] in ("select","conditional")};con={key(x) for x in b if x["portfolio_decision"]=="conditional"}
  self.assertEqual(len(act),217);self.assertEqual(len(con),161)
  for path,k in [("queues/proposed-v80-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v80.json","items"),("catalog/readiness/v80-2026-11-28-r177-all217-gates.json","records"),("catalog/access/2026-11-28-v80-conditional-hub-gates.json","entries")]:
   z=load(path)[k];self.assertEqual({key(x) for x in z},con if k=="entries" else act);self.assertEqual(len(z),161 if k=="entries" else 217)
  self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in load("catalog/readiness/v80-2026-11-28-r177-all217-gates.json")["records"]));self.assertEqual(load("queues/approved.json")["entries"],[])
 def test_manifest(self):
  m=load("manifests/drafts/r177-2026-11-28-openthai22-cpu-ocr-source.candidate.json");s=m["source_models"][0];f=s["source_files"];g=[x for x in f if x["selected_candidate"]]
  self.assertEqual(len(f),18);self.assertEqual(sum(x["bytes"] for x in f),15436348);self.assertEqual(len(g),16);self.assertEqual(sum(x["bytes"] for x in g),8360306);self.assertEqual({x["path"] for x in f if x["checksum_conflict"]},{"README.md"});self.assertEqual(sum(bool(x["lfs_sha256"]) for x in f),6);self.assertTrue(all(x["lfs_sha256"]==x["publisher_sha256sum"] for x in f if x["lfs_sha256"]));self.assertFalse(m["download_enabled"]);self.assertFalse(m["approved_by_user"]);self.assertIsNone(s["owner_incremental_bytes"]);self.assertIsNone(s["complete_dependency_inclusive_bytes"])
