import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class TestR181SpecialistReconciliation(unittest.TestCase):
    def test_catalog_and_preservation(self):
        prior = load("catalog/effective-portfolio-2026-11-28-v83.json")["items"]
        now = load("catalog/effective-portfolio-2026-11-28-v84.json")["items"]
        self.assertEqual(prior, now[:277])
        self.assertEqual(278, len({x["repo_id"] for x in now}))
        self.assertEqual(["MBZUAI/TerraFM"], [x["repo_id"] for x in now[277:]])
        self.assertEqual(1, sum(x["repo_id"] == "ai-sage/GigaEdge-Enhance" for x in now))
        self.assertEqual(222, sum(x["portfolio_decision"] in ("select","conditional") for x in now))
    def test_sources(self):
        ev = load("catalog/research/2026-11-28-r181-independent-gigaedge-terrafm-crosscheck.json")
        cats = {x["repo_id"]: x for x in load("catalog/effective-portfolio-2026-11-28-v84.json")["items"]}
        for src in ev["independent_source_inventory"]:
            self.assertEqual(src["revision_sha"], cats[src["repo_id"]]["upstream_revision_sha_observed"])
            self.assertEqual(src["full_repo_bytes"], sum(f["bytes"] for f in src["source_files"]))
            self.assertFalse(cats[src["repo_id"]]["download_approved"])
        self.assertEqual(462953535, ev["capacity"]["formal_combined_candidate_bytes"])
        self.assertEqual(0, ev["capacity"]["additional_selected_bytes_from_this_reconciliation"])
    def test_gates(self):
        active = {x["repo_id"] for x in load("catalog/effective-portfolio-2026-11-28-v84.json")["items"] if x["portfolio_decision"] in ("select","conditional")}
        conditional = {x["repo_id"] for x in load("catalog/effective-portfolio-2026-11-28-v84.json")["items"] if x["portfolio_decision"] == "conditional"}
        self.assertEqual(active, {x["repo_id"] for x in load("queues/proposed-v84-2026-11-28.json")["candidates"]})
        self.assertEqual(active, {x["repo_id"] for x in load("catalog/preparation/2026-11-28-insurance-bundles-v84.json")["items"]})
        self.assertEqual(conditional, {x["repo_id"] for x in load("catalog/access/2026-11-28-v84-conditional-hub-gates.json")["entries"]})
        records = load("catalog/readiness/v84-2026-11-28-r180-all222-gates.json")["records"]
        self.assertEqual(active, {x["repo_id"] for x in records})
        self.assertTrue(all(not x["ready_to_acquire"] and not x["download_approved"] for x in records))
        self.assertEqual([], load("queues/approved.json")["entries"])
    def test_research_only(self):
        q = load("queues/research-r181-specialist-alternatives-HOLD.json")
        self.assertFalse(q["download_enabled"])
        self.assertTrue(all(not x["download_approved"] and not x["can_enter_approved_queue"] for x in q["entries"]))

if __name__ == "__main__":
    unittest.main()
