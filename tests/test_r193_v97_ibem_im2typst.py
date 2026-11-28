import json, unittest
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def key(x):return x["asset_kind"],x["repo_id"]
class IBEMFormal(unittest.TestCase):
    def test_overlay(self):
        old=load("catalog/effective-portfolio-2026-11-28-v96.json")["items"]
        new=load("catalog/effective-portfolio-2026-11-28-v97.json")["items"]
        self.assertEqual(new[:-1],old)
        self.assertEqual(len(set(map(key,new))),291)
        self.assertEqual(new[-1],load("catalog/revisions/v97-2026-11-28.json")["additions"][0])
        self.assertEqual(new[-1]["parameter_gate"]["total_parameters"],14157152)
        self.assertIsNone(new[-1]["selected_file_bytes"])
    def test_joins_and_stop(self):
        items=load("catalog/effective-portfolio-2026-11-28-v97.json")["items"]
        active={key(x) for x in items if x["portfolio_decision"] in ("select","conditional")}
        cond={key(x) for x in items if x["portfolio_decision"]=="conditional"}
        self.assertEqual(len(active),235)
        self.assertEqual(len(cond),179)
        for f,k,e in [("queues/proposed-v97-2026-11-28.json","candidates",active),("catalog/preparation/2026-11-28-insurance-bundles-v97.json","items",active),("catalog/readiness/v97-2026-11-28-r193-all235-gates.json","records",active),("catalog/access/2026-11-28-v97-conditional-hub-gates.json","entries",cond)]:
            rows=load(f)[k]
            self.assertEqual(set(map(key,rows)),e)
            self.assertEqual(len(rows),len(e))
        r=load("catalog/readiness/v97-2026-11-28-r193-all235-gates.json")
        self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in r["records"]))
        self.assertEqual(r["summary"]["blocking_gate_counts"],dict(Counter(g for x in r["records"] for g in x["blocking_gates"])))
    def test_source(self):
        m=load("manifests/drafts/r190-2026-11-28-ibem-im2typst-original.candidate.json")
        self.assertEqual(len(m["runtime_source"]["source_files"]),182)
        self.assertEqual(sum(x["bytes"] for x in m["runtime_source"]["source_files"]),2417253)
        self.assertEqual(m["known_partial_source_bytes"],59110340)
        self.assertIsNone(m["complete_dependency_inclusive_bytes"])
        self.assertFalse(m["download_enabled"])
        self.assertFalse(m["download_approved"])
if __name__=="__main__":unittest.main()
