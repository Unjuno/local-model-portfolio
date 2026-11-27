import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(x): return x["asset_kind"],x["repo_id"]
class R178Audio(unittest.TestCase):
    def test_joins(self):
        old=load("catalog/effective-portfolio-2026-11-28-v80.json")["items"]
        rows=load("catalog/effective-portfolio-2026-11-28-v81.json")["items"]
        self.assertEqual(rows[:273],old)
        self.assertEqual(rows[273:],load("catalog/revisions/v81-2026-11-28.json")["additions"])
        self.assertEqual(len(set(map(key,rows))),275)
        active={key(x) for x in rows if x["portfolio_decision"] in ("select","conditional")}
        conditional={key(x) for x in rows if x["portfolio_decision"]=="conditional"}
        self.assertEqual((len(active),len(conditional)),(219,163))
        for path,field,wanted in [("queues/proposed-v81-2026-11-28.json","candidates",active),("catalog/preparation/2026-11-28-insurance-bundles-v81.json","items",active),("catalog/readiness/v81-2026-11-28-r178-all219-gates.json","records",active),("catalog/access/2026-11-28-v81-conditional-hub-gates.json","entries",conditional)]:
            rr=load(path)[field]
            self.assertEqual(set(map(key,rr)),wanted)
            self.assertEqual(len(rr),len(wanted))
        self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in load("catalog/readiness/v81-2026-11-28-r178-all219-gates.json")["records"]))
        self.assertEqual(load("queues/approved.json")["entries"],[])
    def test_source(self):
        m=load("manifests/drafts/r178-2026-11-28-inworld-audio-originals.candidate.json")
        f=[x for s in m["source_models"] for x in s["source_files"]]
        self.assertEqual(len(f),3)
        self.assertEqual(sum(x["bytes"] for x in f),540092596)
        self.assertEqual(len({x["lfs_sha256"] for x in f}),3)
        self.assertFalse(m["download_enabled"])
        self.assertFalse(m["approved_by_user"])
        self.assertIsNone(m["final_selected_file_bytes"])
