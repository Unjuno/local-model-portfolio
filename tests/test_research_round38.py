"""R38 source-representation audit for eight high-capacity active assets, offline."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(x):
    return json.loads((ROOT/x).read_text(encoding="utf-8"))

class R38LargeArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load("catalog/research/2026-11-08-r38-large-asset-alternative-layouts.json")
        cls.current=load("catalog/CURRENT.json")
        cls.view=load(cls.current["materialized_catalog_path"])
        cls.approved=load("queues/approved.json")
        cls.rows={x["repo_id"]:x for x in cls.r["records"]}
        cls.c=cls.r["comparison"]

    def test_exactly_eight_high_source_active_assets_revisited(self):
        high={x["repo_id"] for x in self.view["items"]
              if x["portfolio_decision"] in ("select","conditional")
              and isinstance((x.get("resource_screen") or {}).get("source_all_repo_bytes"),int)
              and x["resource_screen"]["source_all_repo_bytes"]>=100_000_000_000}
        self.assertEqual(len(high),8)
        self.assertEqual(set(self.rows),high)
        self.assertEqual(sum(x["source_repo_bytes"] for x in self.rows.values()),1_403_226_367_788)

    def test_each_file_group_has_exact_bytes_and_full_git_sha(self):
        for x in self.rows.values():
            self.assertRegex(x["revision"], r"^[0-9a-f]{40}$")
            self.assertEqual(sum(z["bytes"] for z in x["grouped_file_components"].values()),
                             x["source_repo_bytes"])
            self.assertEqual(sum(len(z["files"]) for z in x["grouped_file_components"].values()),
                             x["total_file_count"])
            for g in x["grouped_file_components"].values():
                self.assertEqual(g["bytes"],sum(z["bytes"] for z in g["files"]))
                for f in g["files"]:
                    if f["sha256"] is not None:
                        self.assertRegex(f["sha256"],r"^[0-9a-f]{64}$")

    def test_qwen_coder_40_shards_are_one_model(self):
        x=self.c["qwen_coder_next"]
        self.assertEqual(x["num_shards"],40)
        self.assertGreater(x["weights_bytes"],159_000_000_000)
        self.assertTrue(x["one_80b_weight_state"])

    def test_mistral_small4_native_vs_hf_are_alternate_layouts(self):
        x=self.c["mistral_small4"]
        self.assertEqual(x["native_7_shards"],7)
        self.assertEqual(x["hf_3_shards"],3)
        self.assertEqual(x["native_bytes"],120_927_211_096)
        self.assertEqual(x["hf_bytes"],120_922_973_936)
        self.assertNotEqual(x["native_bytes"],x["hf_bytes"])
        self.assertIn("not bitwise",x["note"])
        self.assertIn("sgl-project",x["sglang_bugfix_primary"])

    def test_gpt_oss_root_original_and_metal_are_backend_representations(self):
        x=self.c["gpt_oss_120b"]
        self.assertEqual((x["hf_15_shards"],x["original_7_shards"],x["metal_file_count"]),(15,7,1))
        self.assertEqual(x["hf_bytes"],65_248_893_184)
        self.assertEqual(x["metal_bytes"],65_238_253_568)
        self.assertIn("not three post-trained",x["note"])

    def test_flux_root_and_diffusers_transformer_are_alternatives_with_dependencies(self):
        x=self.c["flux2_dev"]
        self.assertEqual(x["diffusers_transformer_shard_count"],7)
        self.assertEqual(x["text_encoder_shard_count"],10)
        self.assertEqual(x["selected_diffusers_three_component_groups_bytes"],112_805_617_244)
        self.assertGreater(x["root_single_transformer_bytes"],64_000_000_000)
        self.assertTrue(x["source_weight_shas_masked"])
        self.assertTrue(x["gated"])
        self.assertFalse(self.rows["black-forest-labs/FLUX.2-dev"]["model_weight_sha_complete"])

    def test_gated_specialized_scout_meditron_are_not_excluded(self):
        self.assertEqual(self.rows["meta-llama/Llama-4-Scout-17B-16E"]["gated"],"manual")
        self.assertEqual(self.rows["EPFLiGHT/Meditron3-70B"]["gated"],"auto")
        self.assertEqual(self.c["llama4_scout"]["shards"],50)
        self.assertEqual(self.c["meditron3"]["shards"],30)
        self.assertTrue(self.c["meditron3"]["distinct_medical_finetune"])

    def test_training_data_phases_not_counted_as_quantization(self):
        x=self.c["ifm_sft_data"]
        self.assertEqual(x["pretraining_bytes"],115_169_801_862)
        self.assertEqual(x["instruction_following_bytes"],43_393_764_554)
        self.assertTrue(x["distinct_tasks_not_file_quant_repack"])

    def test_granary_language_partition_and_rights_screen(self):
        x=self.c["granary_v2"]
        self.assertEqual(x["english_bytes"],74_381_590_133)
        self.assertEqual(x["japanese_bytes"],6_182_173)
        self.assertGreater(x["other_languages_plus_support_bytes"],35_000_000_000)
        self.assertTrue(x["individual_corpus_rights_require_review"])

    def test_4tb_user_budget_no_downloads_or_formal_promotion(self):
        self.assertEqual(self.current["expected"]["archive_limit_bytes"],4_000_000_000_000)
        self.assertEqual(self.current["expected"]["tracked"],150)
        self.assertEqual(self.current["expected"]["active"],105)
        self.assertEqual(self.approved["entries"],[])
        self.assertEqual(self.r["selection_rules"]["acquisition_authorizations_added"],0)
        self.assertTrue(self.r["selection_rules"]["current_catalog_unchanged"])
        self.assertTrue(self.r["selection_rules"]["no_files_downloaded"])

if __name__=="__main__":
    unittest.main()
