"""R39 backend-specific weight candidate audits. Stdlib, offline, no downloads."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class TestR39BackendPackageEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = read("manifests/drafts/r39-backend-specific-large-sources.candidate.json")
        cls.r38 = read("catalog/research/2026-11-08-r38-large-asset-alternative-layouts.json")
        cls.current = read("catalog/CURRENT.json")
        cls.limits = read("policies/limits.json")
        cls.queue = read("queues/approved.json")
        cls.packs = {p["key"]: p for p in cls.d["packages"]}
        cls.source = {p["repo_id"]: p for p in cls.r38["records"]}

    def test_exact_seven_nonexecuting_packages_and_unique_keys(self):
        self.assertEqual(len(self.packs), 7)
        self.assertEqual(len(self.d["packages"]), len(self.packs))
        self.assertIn("NON_EXECUTABLE", self.d["status"])
        self.assertFalse(self.d["do_not_download_any_files"] is False)
        self.assertTrue(all(not p["approved_for_download"] for p in self.packs.values()))
        self.assertTrue(all(not p["complete_runtime_closure"] for p in self.packs.values()))
        self.assertTrue(all(not p["owner_hardware_verified"] for p in self.packs.values()))

    def test_group_selection_copies_exact_source_metadata(self):
        for p in self.packs.values():
            self.assertRegex(p["revision"], r"^[0-9a-f]{40}$")
            self.assertEqual(p["revision"], self.source[p["repo_id"]]["revision"])
            self.assertEqual(p["source_repo_bytes"], self.source[p["repo_id"]]["source_repo_bytes"])
            source_files = {}
            for g in self.source[p["repo_id"]]["grouped_file_components"].values():
                for f in g["files"]:
                    source_files[f["path"]] = f
            self.assertEqual(len(p["selected_files"]), p["selected_file_count"])
            self.assertEqual(len(p["selected_files"]),
                             len({x["path"] for x in p["selected_files"]}))
            self.assertEqual(p["selected_total_bytes"], sum(x["bytes"] for x in p["selected_files"]))
            self.assertEqual(p["weights_bytes"]+p["support_bytes"], p["selected_total_bytes"])
            self.assertEqual(p["weight_file_count"]+p["support_file_count"],p["selected_file_count"])
            for x in p["selected_files"]:
                self.assertIn(x["path"], source_files)
                orig = source_files[x["path"]]
                self.assertEqual(x["bytes"], orig["bytes"])
                self.assertEqual(x["source_sha256"], orig["sha256"])
                self.assertEqual(x["hash_masked"], orig.get("has_redacted_hash", False))
                self.assertFalse(x["body_downloaded"])
                self.assertFalse(x["local_sha_verified"])

    def test_mistral_hf_and_native_one_learned_model_two_format_options(self):
        hf = self.packs["mistral4-hf"]
        native = self.packs["mistral4-native"]
        self.assertEqual((hf["weight_file_count"],native["weight_file_count"]),(3,7))
        self.assertEqual(hf["selected_total_bytes"], 120_956_545_012)
        self.assertEqual(native["selected_total_bytes"],120_947_140_060)
        self.assertIn("config.json", {x["path"] for x in hf["selected_files"]})
        self.assertNotIn("params.json", {x["path"] for x in hf["selected_files"]})
        self.assertIn("params.json", {x["path"] for x in native["selected_files"]})
        self.assertIn("mistral",hf["backend_support"].lower())
        self.assertEqual(hf["repo_id"],native["repo_id"])

    def test_gptoss_three_backend_variants_not_three_model_families(self):
        hf = self.packs["gptoss120-hf"]
        orig = self.packs["gptoss120-original"]
        metal = self.packs["gptoss120-metal"]
        self.assertEqual((hf["weight_file_count"],orig["weight_file_count"],metal["weight_file_count"]),
                         (15,7,1))
        self.assertEqual(hf["selected_total_bytes"],65_276_857_840)
        self.assertEqual(orig["selected_total_bytes"],65_276_818_674)
        self.assertEqual(metal["selected_total_bytes"],65_266_144_611)
        self.assertEqual(len({hf["repo_id"],orig["repo_id"],metal["repo_id"]}),1)
        self.assertIn("original/config.json", {x["path"] for x in orig["selected_files"]})
        self.assertIn("metal/model.bin", {x["path"] for x in metal["selected_files"]})
        self.assertIn("Harmony", hf["backend_support"])

    def test_gated_flux_has_no_downloadable_hash_lock(self):
        diff = self.packs["flux2-diffusers"]
        single = self.packs["flux2-single-file"]
        self.assertEqual((diff["weight_file_count"],single["weight_file_count"]),(18,12))
        self.assertEqual(diff["weights_bytes"],112_805_617_244)
        self.assertEqual(diff["selected_total_bytes"],112_823_043_233)
        self.assertEqual(single["selected_total_bytes"],112_822_993_214)
        for p in (diff,single):
            self.assertTrue(all(x["hash_masked"] and x["source_sha256"] is None
                                for x in p["selected_files"] if x["role"] == "weight"))
            self.assertFalse(p["approved_for_download"])
            self.assertIn("BLOCKED",p["archive_preference"])
        self.assertTrue(self.d["gated_flux_is_comparison_only"])

    def test_one_baseline_hf_pair_does_not_claim_full_archive_approval(self):
        base = self.d["research_baseline_scenario"]
        self.assertEqual(base["choices"],["mistral4-hf","gptoss120-hf"])
        self.assertEqual(base["weights_and_support_files_bytes"],186_233_402_852)
        self.assertEqual(base["weights_and_support_files_bytes"],
                         sum(self.packs[k]["selected_total_bytes"] for k in base["choices"]))
        self.assertFalse(base["not_budget_approved"] is False)
        self.assertTrue(base["missing_runtime_dependencies_not_zero"])

    def test_alternate_formats_not_inferred_bitwise_identical(self):
        self.assertTrue(self.d["does_not_assert_bitwise_format_equivalence"])
        self.assertTrue(self.d["does_not_assert_same_hash_for_differently_named_shards"])
        self.assertTrue(self.d["special_trained_states_not_pruned"])
        self.assertTrue(self.d["all_shards_in_one_model_are_required"])
        self.assertEqual(len(self.d["alternatives"]),4)
        self.assertTrue(any(a.get("hardware_specific_metal") for a in self.d["alternatives"]))

    def test_4tb_budget_free_floor_and_queue_no_changes(self):
        p=self.d["archive_policy"]
        self.assertEqual(p["user_planning_ceiling_bytes"],4_000_000_000_000)
        self.assertEqual(p["minimum_physical_free_bytes"],200_000_000_000)
        self.assertIsNone(p["actual_user_disk_free_bytes"])
        self.assertEqual(self.limits["archive_target_bytes"],p["user_planning_ceiling_bytes"])
        self.assertEqual(self.limits["minimum_free_bytes"],p["minimum_physical_free_bytes"])
        self.assertEqual(self.current["expected"]["tracked"],150)
        self.assertEqual(self.current["expected"]["active"],105)
        self.assertEqual(p["approved_download_queue_changes"],0)
        self.assertEqual(self.queue["entries"],[])
        self.assertTrue(self.d["do_not_download_any_files"])

if __name__=="__main__":
    unittest.main()
