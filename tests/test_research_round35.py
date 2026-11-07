"""R35 deterministic public LFS-file evidence audit. Stdlib, offline, no weights."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestR35LTXFileCensus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x = load("catalog/research/2026-11-08-r35-ltx-pinned-file-census.json")
        cls.base = load("catalog/research/2026-11-08-r34-capacity-evidence.json")
        cls.current = load("catalog/CURRENT.json")
        cls.approved = load("queues/approved.json")

    def test_repository_identity_has_exact_revision(self):
        self.assertEqual(len(self.x["repos"]), 3)
        for row in self.x["repos"]:
            self.assertRegex(row["immutable_commit"], r"^[a-f0-9]{40}$")
            self.assertGreater(row["current_tree_bytes"], 0)
            self.assertGreater(row["current_tree_file_count"], 0)

    def test_original_and_mirror_have_same_fifteen_model_files(self):
        o = self.x["chris_original_mirror_binary_identity"]
        self.assertEqual(o["match_count"], 15)
        self.assertEqual(len(o["shared_model_files"]), 15)
        self.assertTrue(o["all_match"])
        self.assertEqual(o["source_only_model_files"], [])
        self.assertEqual(o["mirror_only_model_files"], [])
        self.assertEqual(o["distinct_training_state_count"], 1)
        for row in o["shared_model_files"]:
            self.assertRegex(row["sha256"], r"^[a-f0-9]{64}$")
            self.assertTrue(row["mirror_byte_equal"])
            self.assertTrue(row["mirror_sha_equal"])

    def test_mirror_differs_in_non_weight_files_not_model_identity(self):
        original, mirror = self.x["repos"][:2]
        self.assertGreater(original["current_tree_file_count"], mirror["current_tree_file_count"])
        self.assertNotEqual(original["current_tree_bytes"], mirror["current_tree_bytes"])
        self.assertEqual(original["model_files"], mirror["model_files"])

    def test_chris_partial_core_is_sum_of_exact_selected_weights(self):
        c = self.x["chris_component_alternatives"]
        choices = {z["key"]: z for z in c["chosen_components"]}
        base = ["gemma4_encoder_int8", "audio_vae", "video_vae"]
        fp = choices["transformer_fp8_scaled"]["bytes"] + sum(choices[k]["bytes"] for k in base)
        q6 = choices["transformer_q6_alternative"]["bytes"] + sum(choices[k]["bytes"] for k in base)
        self.assertEqual(fp, 36_468_259_016)
        self.assertEqual(q6, 32_754_581_408)
        self.assertEqual(c["archive_research_core_fp8_scaled_bytes"], fp)
        self.assertEqual(c["archive_research_core_q6_alternative_bytes"], q6)
        self.assertEqual(c["archive_fp8_scaled_plus_two_upscalers_bytes"],
                         fp + choices["spatial_upscaler"]["bytes"] + choices["temporal_upscaler"]["bytes"])
        self.assertEqual(c["observed_actual_q6_gguf_bytes"], 17_759_973_824)
        self.assertTrue(c["these_are_partial_subset_not_full_executable_package"])

    def test_all_chris_chosen_files_have_sources_and_mirror(self):
        for x in self.x["chris_component_alternatives"]["chosen_components"]:
            self.assertGreater(x["bytes"], 0)
            self.assertRegex(x["sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(x["git_blob_sha1"], r"^[0-9a-f]{40}$")
            self.assertTrue(x["exists_in_mirror"])

    def test_stuubs_exact_total_and_7_variants_in_3_states(self):
        s = self.x["stuubs_trained_stages_and_formats"]
        self.assertEqual(len(s["files"]), 7)
        self.assertEqual(len({r["learned_state"] for r in s["files"]}), 3)
        self.assertEqual(sum(r["bytes"] for r in s["files"]), 195_941_911_488)
        self.assertEqual(s["source_tree_all_bytes"], 195_942_118_539)
        self.assertEqual(s["v1_bf16_bytes"], 42_008_732_600)
        self.assertEqual(s["difference_vs_full_repo_if_only_v1_bf16_bytes"],
                         s["source_tree_all_bytes"] - s["v1_bf16_bytes"])
        self.assertAlmostEqual(self.base["stuubs_representation_scenario"]["source_all_weight_variants_displayed_gb_approx"], 195.9)
        for file in s["files"]:
            self.assertRegex(file["sha256"], r"^[a-f0-9]{64}$")

    def test_archival_scope_does_not_imply_rights_or_execution(self):
        x = self.x["status"]
        self.assertTrue(x["existing_catalog_unchanged"])
        self.assertFalse(x["rights_unverified"] is False)
        self.assertTrue(x["source_sha_are_not_local_rehash"])
        self.assertEqual(x["new_approval_entries"], 0)
        self.assertEqual(x["payloads_downloaded"], 0)
        self.assertIsNone(x["physical_archive_free_bytes"])
        self.assertEqual(self.approved["entries"], [])
        self.assertEqual(self.current["expected"]["archive_limit_bytes"], 4_000_000_000_000)

if __name__ == "__main__":
    unittest.main()
