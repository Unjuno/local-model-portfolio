"""R34 capacity evidence checks; static, offline, never downloads model weights."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class TestR34CapacityEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = read_json("catalog/research/2026-11-08-r34-capacity-evidence.json")
        cls.cur = read_json("catalog/CURRENT.json")
        cls.view = read_json(cls.cur["materialized_catalog_path"])
        cls.limits = read_json("policies/limits.json")
        cls.r21 = read_json("manifests/drafts/round21-pinned-preservation.candidate.json")
        cls.approved = read_json("queues/approved.json")
        cls.items = cls.view["items"]
        cls.active = [x for x in cls.items if x["portfolio_decision"] in ("select", "conditional")]

    @staticmethod
    def source_bytes(item):
        return (item.get("resource_screen") or {}).get("source_all_repo_bytes")

    def test_all_150_are_retained_unique_and_current(self):
        s = self.audit["statistics"]
        self.assertEqual(self.view["revision_id"], self.cur["revision_id"])
        self.assertEqual(len(self.items), 150)
        self.assertEqual(len(self.active), 105)
        self.assertEqual(s["tracked"], len(self.items))
        self.assertEqual(s["active"], len(self.active))
        self.assertEqual(len(self.audit["full_research_inventory"]), 150)
        ids = [(x["asset_kind"], x["repo_id"]) for x in self.items]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(self.audit["full_research_inventory"]), len(ids))

    def test_source_repo_coverage_is_not_claimed_as_selected_bytes(self):
        known = [x for x in self.active if isinstance(self.source_bytes(x), int)]
        unknown = [x for x in self.active if not isinstance(self.source_bytes(x), int)]
        s = self.audit["statistics"]
        self.assertEqual(s["known_active_source_repo_bytes_count"], len(known))
        self.assertEqual(s["unknown_active_source_repo_bytes_count"], len(unknown))
        self.assertEqual(s["known_active_source_repo_bytes_sum"], sum(self.source_bytes(x) for x in known))
        self.assertEqual(s["known_active_source_repo_bytes_count"], 83)
        self.assertEqual(s["unknown_active_source_repo_bytes_count"], 22)
        self.assertTrue(self.audit["policy_notes"]["unknown_not_zero"])
        self.assertIsNone(self.audit["estimated_archive_remaining_bytes"])

    def test_high_cost_source_repos_are_not_pinned_approval(self):
        s = self.audit["statistics"]
        large = [x for x in self.active if isinstance(self.source_bytes(x), int)
                 and self.source_bytes(x) >= 100_000_000_000]
        self.assertEqual(s["active_source_repo_ge_100gb_count"], len(large))
        self.assertEqual(s["active_source_repo_ge_100gb_sum"],
                         sum(self.source_bytes(x) for x in large))
        self.assertEqual(len(large), 8)
        self.assertTrue(all(x["selected_file_bytes"] is None
                            for x in self.audit["active_high_source_repo_bytes"]))

    def test_selected_file_evidence_counts_only_two_records(self):
        chosen = [x for x in self.active if isinstance(x.get("selected_file_bytes"), int)]
        s = self.audit["statistics"]
        self.assertEqual(s["known_active_selected_file_bytes_count"], len(chosen))
        self.assertEqual(s["known_active_selected_file_bytes_sum"],
                         sum(x["selected_file_bytes"] for x in chosen))
        self.assertEqual(len(chosen), 2)
        self.assertEqual(s["pinned_active_revision_count"], 2)

    def test_r21_complete_package_includes_separate_support_repos(self):
        p = self.audit["r21_exact_packages"]
        self.assertEqual(len(p), 2)
        repos = {x["key"]: x for x in self.r21["repositories"]}
        packages = {x["key"]: x for x in self.r21["packages"]}
        for row in p:
            self.assertEqual(row["total_bytes"], packages[row["key"]]["selected_model_and_support_bytes"])
            self.assertEqual(row["repo_components_bytes"], sum(repos[k]["selected_bytes"] for k in
                             packages[row["key"]]["repository_keys"]))
        e = self.audit["r21_identity_examples"]
        self.assertEqual(e["interpretic_catalog_record_bytes"] +
                         e["interpretic_extra_provenance_bytes"],
                         e["interpretic_complete_r21_package_bytes"])
        self.assertEqual(e["chatr_catalog_adapter_record_bytes"] +
                         e["chatr_pinned_base_dependencies_bytes"],
                         e["chatr_complete_r21_package_bytes"])
        self.assertFalse(e["shared_base_locally_hash_verified"])

    def test_stuubs_separate_trained_stages_from_quantizations(self):
        x = self.audit["stuubs_representation_scenario"]
        files = x["observed_files"]
        self.assertEqual(len(files), 7)
        self.assertEqual(len(set(f["file"] for f in files)), 7)
        self.assertEqual(len(set(f["learned_state"] for f in files)), 3)
        self.assertEqual(x["quant_variants_same_v1_state"], 4)
        self.assertAlmostEqual(sum(f["displayed_gb"] for f in files), 195.9)
        self.assertAlmostEqual(x["current_v1_bf16_only_displayed_gb_approx"], 42.0)
        self.assertAlmostEqual(x["illustrative_weight_payload_dedup_saving_displayed_gb_approx"], 153.9)
        self.assertFalse(x["actual_disk_savings_verified"])
        self.assertTrue(x["live_repo_sizes_rounded_not_exact"])
        self.assertTrue(any("DIFFERENT" in x for x in [x["conditions"]]))

    def test_user_selected_model_and_capacity_limits_not_weakened(self):
        n = [x for x in self.items if x["repo_id"] == "Nanbeige/Nanbeige4.3-33B"]
        self.assertEqual(len(n), 1)
        self.assertEqual(n[0]["portfolio_decision"], "select")
        self.assertEqual(self.limits["archive_target_bytes"], 4_000_000_000_000)
        self.assertEqual(self.limits["minimum_free_bytes"], 200_000_000_000)
        self.assertEqual(self.cur["expected"]["archive_limit_bytes"],
                         self.limits["archive_target_bytes"])
        self.assertEqual(self.audit["archive_policy"]["actual_free_disk_bytes"], None)

    def test_read_only_no_approval_and_special_state_not_excluded(self):
        self.assertEqual(self.approved["entries"], [])
        self.assertEqual(self.audit["statistics"]["approved_entry_count"], 0)
        self.assertTrue(self.audit["policy_notes"]["multiple_distinct_special_training_states_can_be_kept"])
        self.assertTrue(self.audit["policy_notes"]["same_learned_state_multiple_quants_not_new_models"])
        self.assertEqual(self.audit["formal_catalog_changes"], 0)
        self.assertEqual(self.audit["model_payload_downloads"], 0)
        self.assertFalse(self.audit["final_acquisition_ready"])

if __name__ == "__main__":
    unittest.main()
