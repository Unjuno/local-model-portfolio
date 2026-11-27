import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(row): return (row["asset_kind"],row["repo_id"])

class TestR184TATR(unittest.TestCase):
    def test_catalog_append(self):
        prior=read("catalog/effective-portfolio-2026-11-28-v87.json")["items"]
        current=read("catalog/effective-portfolio-2026-11-28-v88.json")["items"]
        self.assertEqual(current[:-1],prior)
        self.assertEqual(len(current),282)
        self.assertEqual(len(set(map(key,current))),282)
        self.assertEqual(current[-1],read("catalog/revisions/v88-2026-11-28.json")["additions"][0])
        self.assertEqual(current[-1]["portfolio_decision"],"conditional")
        self.assertFalse(current[-1]["download_approved"])
        self.assertTrue(current[-1]["research_only_nonexecutable"])
    def test_sidecar_joins(self):
        rows=read("catalog/effective-portfolio-2026-11-28-v88.json")["items"]
        active={key(x) for x in rows if x["portfolio_decision"] in ("conditional","select")}
        cond={key(x) for x in rows if x["portfolio_decision"]=="conditional"}
        self.assertEqual(len(active),226)
        self.assertEqual(len(cond),170)
        for path,field in [("queues/proposed-v88-2026-11-28.json","candidates"),("catalog/readiness/v88-2026-11-28-r184-all226-gates.json","records"),("catalog/preparation/2026-11-28-insurance-bundles-v88.json","items")]:
            side=read(path)[field]
            self.assertEqual(len(side),226)
            self.assertEqual(set(map(key,side)),active)
        self.assertEqual(set(map(key,read("catalog/access/2026-11-28-v88-conditional-hub-gates.json")["entries"])),cond)
        self.assertTrue(all(not x["ready_to_acquire"] and not x["download_approved"] for x in read("catalog/readiness/v88-2026-11-28-r184-all226-gates.json")["records"]))
    def test_manifest_not_authority(self):
        m=read("manifests/drafts/r184-2026-11-28-tatr-source-partial.candidate.json")
        self.assertFalse(m["download_enabled"])
        self.assertFalse(m["approved"])
        self.assertEqual(m["source_models"][0]["source_files"][0]["bytes"],115437156)
        self.assertIsNone(m["full_dependency_inclusive_bytes"])
        self.assertIsNone(m["owner_incremental_bytes"])
