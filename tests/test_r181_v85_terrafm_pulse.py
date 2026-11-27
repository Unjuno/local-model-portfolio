import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class TestSpecialists(unittest.TestCase):
    def test_catalog(self):
        old=load("catalog/effective-portfolio-2026-11-28-v84.json")["items"]
        new=load("catalog/effective-portfolio-2026-11-28-v85.json")["items"]
        self.assertEqual(new[:278],old)
        self.assertEqual(len(new),279)
        key=lambda xs:{(x["asset_kind"],x["repo_id"]) for x in xs}
        self.assertEqual(len(key(new)),279)
        active=[x for x in new if x["portfolio_decision"] in ("select","conditional")]
        cond=[x for x in new if x["portfolio_decision"]=="conditional"]
        for path, field, expected in [("queues/proposed-v85-2026-11-28.json","candidates",active),("catalog/readiness/v85-2026-11-28-r181-all223-gates.json","records",active),("catalog/preparation/2026-11-28-insurance-bundles-v85.json","items",active),("catalog/access/2026-11-28-v85-conditional-hub-gates.json","entries",cond)]:
            self.assertEqual(key(load(path)[field]),key(expected))
        self.assertTrue(all(not x["ready_to_acquire"] and not x["download_approved"] for x in load("catalog/readiness/v85-2026-11-28-r181-all223-gates.json")["records"]))
        self.assertEqual(new[-1:],load("catalog/revisions/v85-2026-11-28.json")["additions"])
    def test_source_scope(self):
        m=load("manifests/drafts/r181-2026-11-28-terrafm-pulse-source.candidate.json")
        self.assertFalse(m["download_approved"])
        self.assertIsNone(m["owner_incremental_bytes"])
        self.assertEqual(sum(f["bytes"] for s in m["source_models"] for f in s["source_files"]),685559)
        self.assertFalse(any(f["path"].startswith("onnx/") for s in m["source_models"] for f in s["source_files"]))
if __name__=="__main__": unittest.main()
