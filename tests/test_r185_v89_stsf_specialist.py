import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(x): return x["asset_kind"],x["repo_id"]
class STSFResearch(unittest.TestCase):
    def test_append_only(self):
        old=load("catalog/effective-portfolio-2026-11-28-v88.json")["items"]
        new=load("catalog/effective-portfolio-2026-11-28-v89.json")["items"]
        self.assertEqual(new[:-1],old)
        self.assertEqual(len(new),283)
        self.assertEqual(len(set(map(key,new))),283)
        self.assertEqual(new[-1],load("catalog/revisions/v89-2026-11-28.json")["additions"][0])
        self.assertIn(("model","Duane245/DGNO"),set(map(key,new)))
        self.assertIn(("model","microsoft/table-transformer-structure-recognition-v1.1-all"),set(map(key,new)))
    def test_scope(self):
        m=load("manifests/drafts/r184-2026-11-28-stsf-tpls-source.candidate.json");s=m["source_models"][0]
        self.assertEqual(len(s["source_files"]),14)
        self.assertEqual(sum(f["bytes"] for f in s["source_files"]),1475910946)
        self.assertEqual(len(s["selected_source_files"]),6)
        self.assertEqual(sum(f["bytes"] for f in s["selected_source_files"]),295193202)
        self.assertEqual(len(m["runtime_source"]["source_files"]),173)
        self.assertEqual(sum(f["bytes"] for f in m["runtime_source"]["source_files"]),569589)
        self.assertEqual(m["combined_selected_model_plus_code_reference_bytes"],295762791)
        self.assertFalse(m["download_enabled"])
        self.assertIsNone(m["complete_dependency_inclusive_bytes"])
    def test_join_and_stop(self):
        rows=load("catalog/effective-portfolio-2026-11-28-v89.json")["items"];act={key(x) for x in rows if x["portfolio_decision"] in ("select","conditional")};co={key(x) for x in rows if x["portfolio_decision"]=="conditional"}
        self.assertEqual((len(act),len(co)),(227,171))
        for path,field in [("queues/proposed-v89-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v89.json","items"),("catalog/readiness/v89-2026-11-28-r185-all227-gates.json","records"),("catalog/access/2026-11-28-v89-conditional-hub-gates.json","entries")]:
            x=load(path)[field];self.assertEqual(set(map(key,x)),co if field=="entries" else act);self.assertEqual(len(x),171 if field=="entries" else 227)
        self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in load("catalog/readiness/v89-2026-11-28-r185-all227-gates.json")["records"]))
        self.assertEqual(load("queues/approved.json")["entries"],[])
        self.assertEqual(rows[-1]["parameter_gate"]["status"],"UNVERIFIED_BLOCK_FINAL_LOCK")
if __name__=="__main__": unittest.main()
