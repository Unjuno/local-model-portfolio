import json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class TestOpenMidnight(unittest.TestCase):
    def test_append_only(self):
        old=load("catalog/effective-portfolio-2026-11-28-v89.json")["items"]
        new=load("catalog/effective-portfolio-2026-11-28-v90.json")["items"]
        self.assertEqual(new[:-1],old)
        self.assertEqual(len(new),284)
        self.assertEqual(new[-1]["repo_id"],"medarc/OpenMidnight-1.1")
        self.assertEqual(new[-1]["portfolio_decision"],"conditional")
    def test_gates(self):
        rows=load("catalog/effective-portfolio-2026-11-28-v90.json")["items"]
        key=lambda x:(x["asset_kind"],x["repo_id"])
        active={key(x) for x in rows if x["portfolio_decision"] in ("select","conditional")}
        cond={key(x) for x in rows if x["portfolio_decision"]=="conditional"}
        for path,field,expected in [("queues/proposed-v90-2026-11-28.json","candidates",active),("catalog/preparation/2026-11-28-insurance-bundles-v90.json","items",active),("catalog/readiness/v90-2026-11-28-r186-all228-gates.json","records",active),("catalog/access/2026-11-28-v90-conditional-hub-gates.json","entries",cond)]:
            rr=load(path)[field]
            self.assertEqual(len(rr),len(expected))
            self.assertEqual({key(x) for x in rr},expected)
            self.assertTrue(all(not x.get("download_approved",False) and not x.get("download_authorized",False) and not x.get("ready_to_acquire",False) for x in rr))
        self.assertEqual(len(active),228)
        self.assertEqual(len(cond),172)
    def test_source(self):
        m=load("manifests/drafts/r186-2026-11-28-openmidnight-source-frozen.candidate.json")
        self.assertEqual(sum(x["size_bytes"] for x in m["files"]),4539168331)
        self.assertEqual(len(m["files"]),7)
        self.assertEqual(sum(x["git_blob_content_independently_checked"] for x in m["files"]),6)
        self.assertIsNone(m["actual_owner_incremental_bytes"])
        self.assertFalse(m["download_approved"])
        self.assertEqual(load("catalog/revisions/v90-2026-11-28.json")["additions"][0],load("catalog/effective-portfolio-2026-11-28-v90.json")["items"][-1])
