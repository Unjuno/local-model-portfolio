"""Read-only consistency tests for oversized research and evolving selection."""
import json
import unittest
from pathlib import Path
from scripts.check_parameter_cutoff import BASELINE, PEAK_LIMIT

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class EquivalentMemoryResearchTests(unittest.TestCase):
    def test_policy_requires_matched_peak_not_file_size(self):
        policy = load("policies/limits.json")
        rule = policy["total_parameter_policy"]
        self.assertFalse(rule["hard_exclusion_by_parameter_count_alone"])
        self.assertEqual(rule["baseline_model_total_parameters"], BASELINE)
        self.assertEqual(rule["hard_peak_ram_bytes_exclusive"], PEAK_LIMIT)
        self.assertEqual(rule["memory_equivalence"]["required_trials_per_candidate_and_reference"], 30)
        self.assertTrue(rule["memory_equivalence"]["candidate_measured_complete_peak_must_be_at_or_below_reference"])

    def test_research_is_unapproved_and_historical_catalog_unchanged(self):
        research = load("catalog/research/2026-11-06-over150b-memory-equivalence.json")
        historical = load("catalog/effective-portfolio-2026-11-06-v20.json")
        historical_queue = load("queues/proposed-v20-2026-11-06.json")
        self.assertEqual(historical["revision_id"], "v20-20261106")
        self.assertEqual(historical_queue["source_revision"], "v20-20261106")
        self.assertEqual(len(historical["items"]), 154)
        active = {(x["asset_kind"], x["repo_id"]) for x in historical["items"]
                  if x["portfolio_decision"] in ("select", "conditional")}
        self.assertEqual(len(active), 108)
        self.assertEqual(len(historical_queue["candidates"]), 108)
        self.assertEqual(active, {(x["asset_kind"], x["repo_id"])
                                 for x in historical_queue["candidates"]})
        self.assertFalse(historical_queue["approved"])
        self.assertFalse(historical_queue["download_enabled"])
        self.assertEqual(len(research["candidates"]), 4)
        self.assertEqual(len({x["quantized_repo_id"].lower() for x in research["candidates"]}), 4)
        for row in research["candidates"]:
            self.assertGreaterEqual(row["publisher_total_parameters_approx"], BASELINE)
            self.assertIsNone(row["chosen_quantized_commit_sha"])
            self.assertIsNone(row["candidate_measured_complete_peak_bytes"])
            self.assertIsNone(row["reference_measured_complete_peak_bytes"])
            self.assertFalse(row["selected_file_sha256_verified"])
            self.assertFalse(row["user_authorized_download"])
        self.assertEqual(research["current_approval_count"], 0)

    def test_current_catalog_and_queue_are_consistent_without_freezing_revision(self):
        current = load("catalog/CURRENT.json")
        view = load(current["materialized_catalog_path"])
        queue = load(current["priority_worklist_path"])
        self.assertEqual(view["revision_id"], current["revision_id"])
        self.assertEqual(queue["source_revision"], current["revision_id"])
        items = view["items"]
        self.assertEqual(len(items), current["expected"]["tracked"])
        self.assertEqual(len({(x["asset_kind"].lower(), x["repo_id"].lower()) for x in items}), len(items))
        active = {(x["asset_kind"], x["repo_id"]) for x in items
                  if x["portfolio_decision"] in ("select", "conditional")}
        self.assertEqual(len(active), current["expected"]["active"])
        self.assertEqual(len(queue["candidates"]), len(active))
        self.assertEqual(active, {(x["asset_kind"], x["repo_id"]) for x in queue["candidates"]})
        self.assertFalse(queue["approved"])
        self.assertFalse(queue["download_enabled"])
        self.assertTrue(all(x["not_authorized"] is True and x["download_approved"] is False
                            for x in queue["candidates"]))
        self.assertEqual(load("queues/approved.json")["entries"], [])

    def test_original_over150_parents_stay_hold_in_historical_view(self):
        rows = load("catalog/effective-portfolio-2026-11-06-v20.json")["items"]
        models = {x["repo_id"]: x for x in rows}
        for repo_id in ("mistralai/Mistral-Large-4-1T-A52B", "orcarouter/Qwen3.8-Flash-Next-Uncensored"):
            self.assertEqual(models[repo_id]["portfolio_decision"], "hold")
            self.assertEqual(models[repo_id]["parameter_gate"]["status"], "OVER_150B_QUANT_REVIEW_REQUIRED")
            self.assertFalse(models[repo_id]["download_approved"])

if __name__ == "__main__":
    unittest.main()
