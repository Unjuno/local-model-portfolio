"""R36 fixed-source metadata audit. Offline standard library; never retrieves model weights."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class R36SourceClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = read("catalog/research/2026-11-08-r36-22-asset-source-closure.json")
        cls.r34 = read("catalog/research/2026-11-08-r34-capacity-evidence.json")
        cls.current = read("catalog/CURRENT.json")
        cls.view = read(cls.current["materialized_catalog_path"])
        cls.limits = read("policies/limits.json")
        cls.queue = read("queues/approved.json")
        cls.r21 = read("manifests/drafts/round21-pinned-preservation.candidate.json")
        cls.rows = {x["repo_id"]: x for x in cls.e["source_records"]}

    def test_all_22_previously_unknown_active_source_ids_revisited(self):
        source = {x["repo_id"] for x in self.r34["active_missing_source_repo_size"]}
        self.assertEqual(len(source), 22)
        self.assertEqual(len(self.rows), 22)
        self.assertEqual(set(self.rows), source)
        for row in self.rows.values():
            self.assertRegex(row["full_revision_sha"], r"^[a-f0-9]{40}$")
            self.assertIn(row["full_revision_sha"], row["source_api_url"])
            self.assertIn(row["repo_id"], row["source_api_url"])
            self.assertIn(row["decision"], ("select", "conditional"))

    def test_21_model_full_repo_byte_counts_and_one_dataset_subset(self):
        models = [x for x in self.rows.values() if x["asset_kind"] == "model"]
        datasets = [x for x in self.rows.values() if x["asset_kind"] == "dataset"]
        self.assertEqual((len(models), len(datasets)), (21, 1))
        self.assertEqual(self.e["verification_scope"]["model_full_tree_confirmed"], 21)
        self.assertTrue(all(x["full_source_repo_bytes"] > 0 for x in models))
        self.assertTrue(all(x["full_source_repo_bytes"] >= (x["selected_weight_or_subset_bytes"] or 0) for x in models))
        self.assertIsNone(datasets[0]["full_source_repo_bytes"])
        self.assertEqual(self.e["source_total_bytes_across_21_models_not_the_download_need"],
                         sum(x["full_source_repo_bytes"] for x in models))

    def test_selected_file_bodies_pinned_and_not_claimed_as_full_runtime(self):
        self.assertEqual(sum(x["selected_weight_or_subset_bytes"] is not None for x in self.rows.values()), 21)
        for row in self.rows.values():
            self.assertFalse(row["fully_complete_dependency_and_code_manifest"])
            if row["components"] is not None:
                self.assertEqual(sum(x["bytes"] for x in row["components"]),
                                 row["selected_weight_or_subset_bytes"])
                for comp in row["components"]:
                    self.assertGreater(comp["bytes"], 0)
                    if comp["sha256"] is not None:
                        self.assertRegex(comp["sha256"], r"^[a-f0-9]{64}$")

    def test_heretic_gguf_1_645tb_is_not_needed_for_one_q4(self):
        x = self.e["derived"]["heretic"]
        self.assertEqual(x["full_source_bytes"], 1_645_270_647_302)
        self.assertEqual(x["q4_multilingual_plus_projector_bytes"], 17_176_647_232)
        self.assertEqual(x["unused_source_formats_if_only_this_example_bytes"],
                         x["full_source_bytes"] - x["q4_multilingual_plus_projector_bytes"])
        self.assertTrue(x["multiple_quant_and_older_ARA_variants"])
        self.assertTrue(x["does_not_prove_unneeded_different_ARA_stages"])

    def test_fineweb_sample_is_14_files_not_the_full_dataset(self):
        x = self.rows["HuggingFaceFW/fineweb-edu"]
        self.assertEqual(x["pinned_file_count"], 14)
        self.assertEqual(x["selected_weight_or_subset_bytes"], 28_518_193_415)
        self.assertIsNone(x["full_source_repo_bytes"])
        self.assertFalse(x["full_dataset_repo_bytes_known"])
        self.assertEqual(len(x["components"]), 14)
        self.assertTrue(all(c["path"].startswith("sample/10BT/") for c in x["components"]))
        self.assertTrue(all(c["sha256"] is not None for c in x["components"]))
        self.assertIsNone(self.e["derived"]["fineweb"]["full_dataset_total_bytes"])

    def test_official_ltx_is_gated_with_sha_hashes_masked(self):
        x = self.rows["Lightricks/LTX-2.5"]
        self.assertEqual(x["full_source_repo_bytes"], 200_853_702_264)
        self.assertEqual(x["selected_example_kind"], "UNAUTHORIZED_GATED_PIPELINE_EXAMPLE")
        self.assertTrue(all(c["sha256"] is None and c["sha256_redacted"] for c in x["components"]))
        self.assertTrue(self.e["derived"]["official_ltx"]["final_lock_blocked"])

    def test_lilavati_equal_byte_size_is_not_a_duplicate_sha(self):
        gen = self.rows["udgamlabs/Lilavati"]["components"][0]
        chk = self.rows["udgamlabs/Lilavati-Checker"]["components"][0]
        self.assertEqual(gen["bytes"], 189_484_448)
        self.assertEqual(gen["bytes"], chk["bytes"])
        self.assertNotEqual(gen["sha256"], chk["sha256"])
        self.assertTrue(self.e["derived"]["complementary"]["lilavati_same_bytes_but_different_sha"])

    def test_lfm_target_and_draft_and_audio_codec_are_distinct_components(self):
        v = self.e["derived"]["complementary"]
        self.assertEqual(v["liquid_vlm_target_plus_drafter_weight_bytes"], 6_806_008_386)
        self.assertEqual(v["lilavati_generator_plus_checker_weight_bytes"], 378_968_896)
        codec = {x["path"]: x["bytes"] for x in self.rows["Edge0/Audio8-TTS-Realistic-Air"]["components"]}
        self.assertEqual(set(codec), {"model.safetensors", "codec.pth"})
        self.assertGreater(codec["codec.pth"], codec["model.safetensors"])
        self.assertEqual(v["tts_audio8_model_and_codec_bytes"], sum(codec.values()))

    def test_interpretic_q4_lfs_matches_prior_immutable_plan(self):
        recent = {x["path"]: x for x in self.rows[
            "InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF"]["components"]}
        historical = next(x for x in self.r21["repositories"] if x["key"] == "interpretic-gguf")
        prior_weights = [f for f in historical["files"] if f["role"] == "weight"]
        self.assertEqual(len(prior_weights), 2)
        for f in prior_weights:
            self.assertEqual(recent[f["path"]]["bytes"], f["bytes"])
            self.assertEqual(recent[f["path"]]["sha256"], f["source_sha256"])
        self.assertNotEqual(historical["revision"], self.rows[
            "InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF"]["full_revision_sha"])

    def test_multiple_chatterbox_versions_are_not_arbitrarily_discarded(self):
        x = self.rows["ResembleAI/chatterbox"]
        self.assertEqual(x["model_files_in_repo"], 12)
        self.assertIsNone(x["components"])
        self.assertIsNone(x["selected_weight_or_subset_bytes"])
        self.assertEqual(x["selected_example_kind"], "UNDECIDED_MULTI_VERSION_TTS")

    def test_no_approval_or_physical_disk_claim(self):
        self.assertEqual(self.current["expected"]["tracked"], 150)
        self.assertEqual(self.current["expected"]["active"], 105)
        self.assertEqual(self.limits["archive_target_bytes"], 4_000_000_000_000)
        self.assertEqual(self.limits["minimum_free_bytes"], 200_000_000_000)
        self.assertEqual(self.queue["entries"], [])
        self.assertTrue(self.e["research_recommendation"]["no_approved_downloads"])
        self.assertFalse(self.e["source_lock_draft"]["original_owner_disk_checked"])
        self.assertEqual(self.e["verification_scope"]["existing_model_states_changed"], 0)
        self.assertEqual(next(x for x in self.view["items"] if
                              x["repo_id"] == "Nanbeige/Nanbeige4.3-33B")["portfolio_decision"],
                         "select")

if __name__ == "__main__":
    unittest.main()
