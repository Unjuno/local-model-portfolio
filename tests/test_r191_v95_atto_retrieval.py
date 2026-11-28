import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(x): return (x["asset_kind"],x["repo_id"])
class TestAttoResearch(unittest.TestCase):
    def test_selection(self):
        old=load("catalog/effective-portfolio-2026-11-28-v94.json")["items"]
        new=load("catalog/effective-portfolio-2026-11-28-v95.json")["items"]
        self.assertEqual(new[:-1],old)
        self.assertEqual(len(set(map(key,new))),289)
        active={key(x) for x in new if x["portfolio_decision"] in ("select","conditional")}
        cond={key(x) for x in new if x["portfolio_decision"]=="conditional"}
        self.assertEqual(len(active),233)
        self.assertEqual(len(cond),177)
        for p,k in [("queues/proposed-v95-2026-11-28.json","candidates"),("catalog/preparation/2026-11-28-insurance-bundles-v95.json","items"),("catalog/readiness/v95-2026-11-28-r191-all233-gates.json","records")]:
            rows=load(p)[k]
            self.assertEqual({key(x) for x in rows},active)
            self.assertTrue(all(not x["download_approved"] for x in rows))
        self.assertEqual({key(x) for x in load("catalog/access/2026-11-28-v95-conditional-hub-gates.json")["entries"]},cond)
        self.assertTrue(all(not x["ready_to_acquire"] for x in load("catalog/readiness/v95-2026-11-28-r191-all233-gates.json")["records"]))
        m=load("manifests/drafts/r191-2026-11-28-atto-source-partial.candidate.json")
        self.assertEqual(m["selected_files"][0]["bytes"],362720)
        self.assertIsNone(m["selected_file_bytes"])
        self.assertFalse(m["download_approved"])
