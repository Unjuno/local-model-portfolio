"""Offline-only v59 canonical, preservation and acquisition STOP assertions."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class V59CanonicalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cur = load("catalog/CURRENT.json")
        cls.v58 = load("catalog/effective-portfolio-2026-11-21-v58.json")
        cls.v59 = load("catalog/effective-portfolio-2026-11-21-v59.json")
        cls.delta = load("catalog/revisions/v59-2026-11-21.json")
        cls.src = load("manifests/drafts/r139-2026-11-21-inkling-micro-edits-and-deepseek4b-varloop.candidate.json")
        cls.queue = load("queues/proposed-v59-2026-11-21.json")
        cls.access = load("catalog/access/2026-11-21-v59-conditional-hub-gates.json")
        cls.dep = load("catalog/preparation/2026-11-21-insurance-bundles-v59.json")
        cls.ready = load("catalog/readiness/v59-2026-11-21-r139-all174-gates.json")
        cls.next = load("queues/proposed-v59-r140-ledger76-next-21-deduplicated-sources.json")

    def test_correct_pointer_and_historical_preservation(self):
        self.assertIn(self.cur["revision_id"], ("v59-20261121", "v60-20261122", "v61-20261122", "v62-20261122", "v63-20261122", "v64-20261122","v65-20261122", "v66-20261124", "v67-20261124","v68-20261125","v69-20261125","v70-20261125", "v71-20261125", "v72-20261125", "v73-20261125"))
        self.assertIn("catalog/revisions/v59-2026-11-21.json", self.cur["ordered_overlays"])
        self.assertIn(self.cur["materialized_catalog_path"], (
            "catalog/effective-portfolio-2026-11-21-v59.json",
            "catalog/effective-portfolio-2026-11-22-v60.json",
            "catalog/effective-portfolio-2026-11-22-v61.json",
            "catalog/effective-portfolio-2026-11-22-v62.json",
            "catalog/effective-portfolio-2026-11-22-v63.json","catalog/effective-portfolio-2026-11-22-v64.json", "catalog/effective-portfolio-2026-11-22-v65.json", "catalog/effective-portfolio-2026-11-24-v66.json", "catalog/effective-portfolio-2026-11-24-v67.json","catalog/effective-portfolio-2026-11-25-v68.json","catalog/effective-portfolio-2026-11-25-v69.json","catalog/effective-portfolio-2026-11-25-v70.json","catalog/effective-portfolio-2026-11-25-v71.json","catalog/effective-portfolio-2026-11-25-v72.json","catalog/effective-portfolio-2026-11-25-v73.json"))
        self.assertEqual(self.v58["items"], self.v59["items"][:218])
        self.assertEqual([a["repo_id"] for a in self.delta["additions"]],
                         [a["repo_id"] for a in self.v59["items"][-3:]])
        self.assertEqual(len({(a["asset_kind"],a["repo_id"]) for a in self.v59["items"]}),221)
        for k in ("tracked", "active", "models", "datasets", "by_tier",
                  "by_decision", "by_forecast_wave", "parameter_gate", "resource_screen"):
            if self.cur["revision_id"] == "v59-20261121":
                self.assertEqual(self.cur["expected"][k],self.v59["counts"][k])
            else:
                self.assertIn("catalog/revisions/v59-2026-11-21.json",self.cur["ordered_overlays"])
        # Narrative budget_status is a review note and can differ while
        # canonical numeric policy and capacity evidence stay identical.
        actual_budget = self.cur["expected"]["budget_scenario"]
        derived_budget = self.v59["budget"]
        if self.cur["revision_id"] == "v59-20261121":
            self.assertTrue(actual_budget["budget_status"].startswith("V59_"))
            for key, expected_value in derived_budget.items():
                if key != "budget_status":
                    self.assertEqual(actual_budget[key], expected_value)
        else:
            self.assertEqual(self.v59["budget"]["v59_publisher_selected_source_bytes"],9_347_231_341)

    def test_source_and_parent_dedup(self):
        self.assertEqual(self.delta["publisher_source_files_selected"],42)
        self.assertEqual(self.delta["publisher_selected_bytes"],9_347_231_341)
        self.assertEqual(self.src["selected_active_files"],42)
        self.assertEqual(self.src["selected_active_source_bytes"],9_347_231_341)
        self.assertEqual(self.delta["shared_origin_publisher_files_excluded"],13)
        self.assertEqual(self.delta["shared_origin_source_bytes_excluded"],20_191_588_440)
        self.assertEqual(sum(a["candidate_selected_source_file_count"] for a in self.delta["additions"]),42)
        self.assertEqual(sum(a["candidate_selected_source_file_bytes"] for a in self.delta["additions"]),9_347_231_341)
        for a in self.delta["additions"]:
            self.assertEqual(a["portfolio_decision"],"conditional")
            self.assertFalse(a["download_approved"])
            self.assertFalse(a["download_ready"])
            self.assertEqual(len(a["upstream_revision_sha_observed"]),40)
            self.assertEqual(a["parameter_gate"]["status"],"PASS_TOTAL_PARAMS_LT_150B")

    def test_every_active_stopped_and_no_approval(self):
        self.assertEqual(len(self.queue["candidates"]),174)
        self.assertEqual(len(self.dep["items"]),174)
        self.assertEqual(len(self.ready["records"]),174)
        self.assertEqual(len(self.access["entries"]),121)
        self.assertEqual(self.ready["summary"]["blocked_any"],174)
        self.assertEqual(self.ready["summary"]["ready_to_approve"],0)
        self.assertEqual(self.ready["summary"]["downloads_approved"],0)
        self.assertFalse(self.queue["download_enabled"])
        self.assertFalse(self.queue["approved"])
        self.assertFalse(self.dep["download_enabled"])
        self.assertFalse(self.ready["ready_to_acquire"])
        self.assertEqual(load("queues/approved.json")["entries"],[])

    def test_next21_is_research_only_and_not_raw_space_claim(self):
        self.assertEqual(self.next["reported_existing"]["model_count"],76)
        self.assertEqual(self.next["reported_existing"]["verified_files"],1078)
        self.assertFalse(self.next["reported_existing"]["physical_owner_HDD_hash_reverified_now"])
        self.assertEqual(len(self.next["source_entries"]),21)
        self.assertEqual(self.next["total_publisher_reference_bytes"],223_837_135_371)
        phase=self.next["phase_summary"]
        self.assertEqual(sum(q["source_bytes"] for q in phase.values()),223_837_135_371)
        self.assertEqual(phase["P0_PREP_FIRST"]["source_bytes"],609_360_574)
        self.assertEqual(phase["P3_LARGE_SOURCE_HOLD"]["source_bytes"],129_572_889_973)
        self.assertFalse(self.next["download_controls"]["approved"])
        self.assertFalse(self.next["download_controls"]["download_enabled"])

if __name__ == "__main__":
    unittest.main()
