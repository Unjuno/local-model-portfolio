import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(x): return x["asset_kind"],x["repo_id"]
class R173(unittest.TestCase):
    def test_append_only(self):
        old=load("catalog/effective-portfolio-2026-11-28-v75.json")["items"]
        new=load("catalog/effective-portfolio-2026-11-28-v76.json")["items"]
        self.assertEqual(new[:-1],old)
        self.assertEqual(len({key(x) for x in new}),267)
        self.assertEqual(new[-1]["repo_id"],"cisco-ai/cisco-time-series-model-1.5")
        self.assertEqual(new[-1]["portfolio_decision"],"conditional")
    def test_source(self):
        m=load("manifests/drafts/r173-2026-11-28-ctsm15-immutable-source.candidate.json")["source_models"][0]
        self.assertEqual(sum(x["bytes"] for x in m["source_files"]),1017721228)
        self.assertEqual(sum(x["bytes"] for x in m["source_files"] if x["selected_candidate"]),1017312524)
        self.assertEqual(sum(x["bytes"] for x in m["runtime_source"]["selected_code_reference_files"]),108265)
        self.assertIsNone(m["complete_dependency_inclusive_bytes"])
        self.assertFalse(m["download_approved"])
    def test_stops(self):
        rows=load("catalog/effective-portfolio-2026-11-28-v76.json")["items"]
        active={key(x) for x in rows if x["portfolio_decision"] in ("select","conditional")}
        cond={key(x) for x in rows if x["portfolio_decision"]=="conditional"}
        self.assertEqual(len(active),211)
        self.assertEqual(len(cond),155)
        gates=load("catalog/readiness/v76-2026-11-28-r173-all211-gates.json")["records"]
        self.assertEqual(active,{key(x) for x in gates})
        self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in gates))
        self.assertEqual(active,{key(x) for x in load("queues/proposed-v76-2026-11-28.json")["candidates"]})
        self.assertEqual(active,{key(x) for x in load("catalog/preparation/2026-11-28-insurance-bundles-v76.json")["items"]})
        self.assertEqual(cond,{key(x) for x in load("catalog/access/2026-11-28-v76-conditional-hub-gates.json")["entries"]})
if __name__=="__main__": unittest.main()
