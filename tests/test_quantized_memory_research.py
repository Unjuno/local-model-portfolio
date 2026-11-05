"""Read-only consistency tests for >=150B quantized candidate research."""
import json
import unittest
from pathlib import Path
from scripts.check_parameter_cutoff import BASELINE, PEAK_LIMIT

ROOT=Path(__file__).resolve().parents[1]
def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))

class EquivalentMemoryResearchTests(unittest.TestCase):
    def test_policy_requires_matched_peak_not_file_size(self):
        p=load("policies/limits.json")
        t=p["total_parameter_policy"]
        self.assertFalse(t["hard_exclusion_by_parameter_count_alone"])
        self.assertEqual(t["baseline_model_total_parameters"],BASELINE)
        self.assertEqual(t["hard_peak_ram_bytes_exclusive"],PEAK_LIMIT)
        self.assertEqual(t["memory_equivalence"]["required_trials_per_candidate_and_reference"],30)
        self.assertTrue(t["memory_equivalence"]["candidate_measured_complete_peak_must_be_at_or_below_reference"])
    def test_research_is_unapproved_and_catalog_unchanged(self):
        r=load("catalog/research/2026-11-06-over150b-memory-equivalence.json")
        c=load("catalog/CURRENT.json")
        v=load(c["materialized_catalog_path"])
        q=load(c["priority_worklist_path"])
        self.assertEqual(c["revision_id"],"v20-20261106")
        self.assertEqual(len(v["items"]),154)
        self.assertEqual(c["expected"]["active"],108)
        self.assertEqual(len(q["candidates"]),108)
        self.assertFalse(q["approved"])
        self.assertFalse(q["download_enabled"])
        self.assertEqual(load("queues/approved.json")["entries"],[])
        self.assertEqual(len(r["candidates"]),4)
        self.assertEqual(len({x["quantized_repo_id"].lower() for x in r["candidates"]}),4)
        for x in r["candidates"]:
            self.assertGreaterEqual(x["publisher_total_parameters_approx"],BASELINE)
            self.assertIsNone(x["chosen_quantized_commit_sha"])
            self.assertIsNone(x["candidate_measured_complete_peak_bytes"])
            self.assertIsNone(x["reference_measured_complete_peak_bytes"])
            self.assertFalse(x["selected_file_sha256_verified"])
            self.assertFalse(x["user_authorized_download"])
        self.assertEqual(r["current_approval_count"],0)
    def test_original_over150_parents_stay_hold(self):
        a=load("catalog/effective-portfolio-2026-11-06-v20.json")["items"]
        m={x["repo_id"]:x for x in a}
        for key in ("mistralai/Mistral-Large-4-1T-A52B","orcarouter/Qwen3.8-Flash-Next-Uncensored"):
            self.assertEqual(m[key]["portfolio_decision"],"hold")
            self.assertEqual(m[key]["parameter_gate"]["status"],"OVER_150B_QUANT_REVIEW_REQUIRED")
            self.assertFalse(m[key]["download_approved"])

if __name__=="__main__": unittest.main()
