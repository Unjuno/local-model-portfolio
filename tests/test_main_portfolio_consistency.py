"""Fail-closed integrity checks for the main branch's active model configuration."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    target = (ROOT / path).resolve()
    if not target.is_relative_to(ROOT.resolve()):
        raise ValueError("path escapes repository")
    return json.loads(target.read_text(encoding="utf-8"))


def identity(item):
    return item["asset_kind"], item["repo_id"]


class CurrentPortfolioIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = read("catalog/CURRENT.json")
        cls.catalog = read(cls.current["materialized_catalog_path"])
        cls.queue = read(cls.current["priority_worklist_path"])
        cls.prep = read(cls.current["insurance_preparation_worklist_path"])
        cls.access = read(cls.current["latest_conditional_access_audit"]["path"])

    def test_materialized_v31_matches_current(self):
        items = self.catalog["items"]
        self.assertEqual(self.current["revision_id"], "v31-20261113")
        self.assertEqual(self.catalog["revision_id"], self.current["revision_id"])
        self.assertEqual(len(items), 179)
        self.assertEqual(len({identity(item) for item in items}), 179)
        self.assertEqual(sum(item["asset_kind"] == "model" for item in items), 153)
        self.assertEqual(sum(item["asset_kind"] == "dataset" for item in items), 26)
        for decision, count in {"select": 53, "conditional": 79,
                                "hold": 28, "deferred": 13, "excluded": 6}.items():
            self.assertEqual(sum(item["portfolio_decision"] == decision
                                 for item in items), count)
        self.assertTrue(all(not item["download_approved"] for item in items))

    def test_preserve_all_v19_models_and_record_additions(self):
        before = read("catalog/effective-portfolio-2026-11-06-v19.json")
        present = {identity(item): item for item in self.catalog["items"]}
        self.assertEqual(len(before["items"]), 150)
        for item in before["items"]:
            self.assertIn(identity(item), present)
            self.assertEqual(item["portfolio_decision"],
                             present[identity(item)]["portfolio_decision"])
        self.assertEqual(len(present) - len(before["items"]), 29)

    def test_candidate_queue_and_dependencies_are_same_132(self):
        active = {identity(item) for item in self.catalog["items"]
                  if item["portfolio_decision"] in ("select", "conditional")}
        proposed = [identity(item) for item in self.queue["candidates"]]
        prepared = [identity(item) for item in self.prep["items"]]
        self.assertEqual(len(active), 132)
        self.assertEqual(len(proposed), 132)
        self.assertEqual(len(prepared), 132)
        self.assertEqual(set(proposed), active)
        self.assertEqual(set(prepared), active)
        self.assertEqual(self.queue["source_revision"], self.current["revision_id"])
        self.assertEqual(self.prep["source_revision"], self.current["revision_id"])
        self.assertFalse(self.queue["approved"])
        self.assertFalse(self.queue["download_enabled"])
        self.assertFalse(self.prep["download_enabled"])
        self.assertTrue(all(item["not_authorized"] and not item["download_approved"]
                            for item in self.queue["candidates"]))
        self.assertEqual(read("queues/approved.json")["entries"], [])

    def test_gated_conditional_metadata_does_not_grant_access(self):
        cond = {identity(item) for item in self.catalog["items"]
                if item["portfolio_decision"] == "conditional"}
        entries = self.access["entries"]
        self.assertEqual(self.access["source_revision"], self.current["revision_id"])
        self.assertTrue(self.access["fail_closed_if_missing"])
        self.assertEqual(len(entries), 79)
        self.assertEqual({identity(row) for row in entries}, cond)
        self.assertEqual(sum(row["hub_gated"] for row in entries), 17)
        self.assertTrue(next(row["hub_gated"] for row in entries
                             if row["repo_id"] == "gradium/phonon-40m-multilingual"))
        self.assertTrue(all(row["owner_access_permission"] == "unknown"
                            and row["download_authorized"] is False for row in entries))

    def test_storage_and_unknown_parameter_gates(self):
        policy = read("policies/limits.json")
        self.assertEqual(policy["archive_target_bytes"], 4_000_000_000_000)
        self.assertEqual(policy["minimum_free_bytes"], 200_000_000_000)
        unknown = {identity(item) for item in self.catalog["items"]
                   if item["portfolio_decision"] in ("select", "conditional")
                   and item["asset_kind"] == "model"
                   and item["parameter_gate"]["status"] == "UNVERIFIED_BLOCK_FINAL_LOCK"}
        self.assertEqual(len(unknown), 7)
        candidates = {identity(row): row for row in self.queue["candidates"]}
        self.assertTrue(all(candidates[key]["research_only"]
                            and not candidates[key]["can_enter_approved_queue"]
                            for key in unknown))


if __name__ == "__main__":
    unittest.main()
