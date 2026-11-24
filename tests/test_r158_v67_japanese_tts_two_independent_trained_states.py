"""R158 V66: Japanese Drama3 fine-tune and separately trained small KL-distilled
expert-pruned GGUF, publisher original frozen SHA, license and ABI fail-closed.
No internet, model code or model weights are executed.
"""
import json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def L(p):return json.loads((ROOT/p).read_text(encoding="utf8"))

class R158JapaneseTTS(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.current=L("catalog/CURRENT.json")
  cls.old=L("catalog/effective-portfolio-2026-11-24-v66.json")
  cls.new=L("catalog/effective-portfolio-2026-11-24-v67.json")
  cls.overlay=L("catalog/revisions/v67-2026-11-24.json")
  cls.man=L("manifests/drafts/r158-2026-11-24-aratako-trained-and-studio-distilled-publisher-originals.candidate.json")
  cls.queue=L("queues/proposed-v67-2026-11-24.json")
  cls.access=L("catalog/access/2026-11-24-v67-conditional-hub-gates.json")
  cls.prep=L("catalog/preparation/2026-11-24-insurance-bundles-v67.json")
  cls.ready=L("catalog/readiness/v67-2026-11-24-r158-all199-gates.json")
  cls.plan=L("queues/proposed-v67-r159-japanese-tts-originals-UNAPPROVED.json")
  cls.ledger=L("catalog/execution/2026-11-19-acquisition-ledger.json")
 def test_exact_old240_immutable_new242_counts_and_current(self):
  self.assertIn(self.current["revision_id"],("v67-20261124","v68-20261125","v69-20261125","v70-20261125", "v71-20261125"))
  self.assertIn(self.current["ordered_overlays"][-1],("catalog/revisions/v67-2026-11-24.json","catalog/revisions/v68-2026-11-25.json","catalog/revisions/v69-2026-11-25.json","catalog/revisions/v70-2026-11-25.json","catalog/revisions/v71-2026-11-25.json"))
  self.assertIn(self.current["materialized_catalog_path"],("catalog/effective-portfolio-2026-11-24-v67.json","catalog/effective-portfolio-2026-11-25-v68.json","catalog/effective-portfolio-2026-11-25-v69.json","catalog/effective-portfolio-2026-11-25-v70.json", "catalog/effective-portfolio-2026-11-25-v71.json"))
  self.assertEqual(self.old["items"],self.new["items"][:246])
  self.assertEqual(self.new["items"][-2:],self.overlay["additions"])
  self.assertEqual((len(self.new["items"]),self.new["counts"]["active"],self.new["counts"]["models"],self.new["counts"]["datasets"]),(248,199,222,26))
  self.assertEqual((self.new["counts"]["by_decision"]["select"],self.new["counts"]["by_decision"]["conditional"],self.new["counts"]["by_decision"]["hold"]),(56,143,30))
  self.assertEqual((self.new["counts"]["parameter_gate"]["PASS_TOTAL_PARAMS_LT_150B"],self.new["counts"]["parameter_gate"]["UNVERIFIED_BLOCK_FINAL_LOCK"]),(189,30))
  self.assertEqual(len({(x["asset_kind"],x["repo_id"]) for x in self.new["items"]}),248)
  current_catalog=L(self.current["materialized_catalog_path"])
  self.assertEqual(self.new["items"],current_catalog["items"][:248])
  for k in ("tracked","active","models","datasets","by_tier","by_decision","by_forecast_wave","parameter_gate","resource_screen"):
   self.assertEqual(current_catalog["counts"][k],self.current["expected"][k])
  self.assertEqual(current_catalog["budget"],self.current["expected"]["budget_scenario"])
 def test_publisher_32_files_51gb_and_all_hashes(self):
  a,b=self.man["model_sources"]
  self.assertEqual([x["repo_id"] for x in (a,b)],
   ["Aratako/Drama-3-Japanese","StudioYebisu-ship-it/Drama-3-Japanese-speech-cpp-gguf"])
  self.assertEqual((self.man["selected_source_file_count"],self.man["selected_source_bytes"],self.man["selected_LFS_SHA256_refs"]),(32,51_265_149_668,11))
  self.assertEqual((a["selected_file_count"],a["selected_source_bytes"]),(20,41_502_599_201))
  self.assertEqual((b["selected_file_count"],b["selected_source_bytes"]),(12,9_762_550_467))
  for obj in self.man["model_sources"]:
   self.assertTrue(obj["observed_public_ungated"])
   self.assertEqual(len(obj["immutable_revision_sha"]),40)
   self.assertEqual(obj["selected_source_bytes"],sum(z["bytes"] for z in obj["selected_files"]))
   self.assertFalse(obj["download_approved"])
   self.assertEqual(len(obj["selected_files"]),obj["selected_file_count"])
   for f in obj["selected_files"]:
    self.assertEqual(len(f["publisher_git_blob_sha1"]),40)
    if f["publisher_lfs_sha256"]:self.assertEqual(len(f["publisher_lfs_sha256"]),64)
    self.assertFalse(f["owner_local_sha_verified"])
 def test_parent_Japanese_finetuning_35p9b_not_claimed_all_bf16(self):
  x=self.man["Japanese_parent_training"]
  self.assertEqual(x["parent_repo"],"fishaudio/drama-3")
  self.assertTrue(x["not_fishaudio_s2_pro_as_immediate_parent"])
  self.assertEqual(x["publisher_original_safetensors_parameters"],35_899_643_008)
  self.assertEqual(x["publisher_dtype_elements"]["BF16"]+x["publisher_dtype_elements"]["F8_E4M3"],35_899_643_008)
  self.assertGreater(x["Japanese_JKYB_kanji_yomi_reading_accuracy_finetune_pct"],
                     x["Japanese_JKYB_kanji_yomi_reading_accuracy_base_pct"])
  self.assertLess(x["JVS_one_ref_CAM_similarity_finetune"],x["JVS_one_ref_CAM_similarity_base"])
  self.assertLess(x["JVS_three_ref_CAM_similarity_finetune"],x["JVS_three_ref_CAM_similarity_base"])
  orig=self.man["model_sources"][0]
  self.assertEqual(sum(f["path"].endswith(".safetensors") for f in orig["selected_files"]),8)
  self.assertEqual(orig["selected_file_count"],20)
  self.assertFalse(any(f["path"].startswith("samples/") for f in orig["selected_files"]))
  self.assertEqual(x["same_codec_as_fishaudio_s2_pro_lfs_SHA256"],"74fc41c5a7151c6f350af8bd7e5d6e3accfcc7f3dfbfac23afd35af07052bb2f")
 def test_studio_small_is_independently_KL_distilled_not_just_format(self):
  s=self.man["Studio_small_new_learned_state"]
  self.assertTrue(s["not_only_simple_gguf_format_conversion"])
  self.assertEqual((s["full_expert_slots"],s["small_pruned_expert_slots"]),(10240,4624))
  self.assertEqual(s["four_layers_retain_256_routed_experts"],[0,1,2,36])
  self.assertTrue(s["Japanese_KL_distillation_claimed"])
  self.assertEqual(s["selected_model_bytes"],9762406560)
  self.assertEqual(s["full_Q4K_gguf_bytes_not_selected"],22359473504)
  self.assertEqual(s["full_Q5K_gguf_bytes_not_selected"],26386005344)
  self.assertEqual(s["audiocpp_alternate_gguf_bytes_not_selected"],9962579296)
  studio=self.man["model_sources"][1]
  self.assertFalse(any(x["path"].endswith("-Q4_K.gguf") or x["path"].endswith("-Q5_K.gguf")
                       for x in studio["selected_files"]))
  self.assertEqual(len(self.man["StudioYebisu_signed_checksum_manifest_small_file_refs"]),6)
  self.assertEqual(self.man["StudioYebisu_signed_checksum_manifest_small_file_refs"][s["selected_model"]],
     "98edad9311a64ea07524f54f24d6d6db77055a3fe7233f24d3bd4351626d9338")
 def test_speedup_vs_realtime_and_vram_physical_constraint(self):
  v=self.man["published_benchmark"]
  self.assertEqual(v["gpu"],"NVIDIA GeForce RTX 4090")
  self.assertEqual(v["cuda"],"12.8")
  self.assertEqual(v["patched_RTFx_aggregate"],3.88)
  self.assertEqual(v["patch_speedup_aggregate"],2.96)
  self.assertEqual(v["single_case_max_RTFx"],4.18)
  self.assertTrue(v["full_Q4K_23p21GiB_full_GPU_not_fit_on_24GB_VRAM"])
  self.assertTrue(v["benchmark_outputs_differ_between_seed42_runs"])
  self.assertTrue(v["benchmark_run_not_reproduced_by_owner"])
  self.assertEqual(v["gpu_clock"],"not reported")
 def test_fish_license_Japanese_corpus_and_speech_patch_still_stop(self):
  r=self.man["rights"]
  self.assertTrue(r["limited_commercial_annual_revenue_below_USD500k_subject_to_terms"])
  self.assertTrue(r["hosted_service_requires_separate_written_license"])
  self.assertTrue(r["JSUT_no_commercial_training_corpus_claim_may_limit_deployment"])
  self.assertTrue(r["JVNV_CC_BY_SA_training_annotation_provenance_requires_review"])
  self.assertTrue(r["owner_individual_usage_rights_unverified"])
  self.assertTrue(self.man["no_untrusted_weight_codec_pth_deserialized"])
  self.assertFalse(self.plan["approved"])
  self.assertFalse(self.plan["download_enabled"])
 def test_all194_readiness_exact_and_reported116_not_redownloaded(self):
  active={(z["asset_kind"],z["repo_id"]) for z in self.new["items"] if z["portfolio_decision"] in ("select","conditional")}
  cond={(z["asset_kind"],z["repo_id"]) for z in self.new["items"] if z["portfolio_decision"]=="conditional"}
  self.assertEqual(len(active),199)
  self.assertEqual({(z["asset_kind"],z["repo_id"]) for z in self.queue["candidates"]},active)
  self.assertEqual({(z["asset_kind"],z["repo_id"]) for z in self.ready["records"]},active)
  self.assertEqual({(z["asset_kind"],z["repo_id"]) for z in self.prep["items"]},active)
  self.assertEqual({(z["asset_kind"],z["repo_id"]) for z in self.access["entries"]},cond)
  self.assertEqual(len(self.access["entries"]),143)
  self.assertEqual(self.access["gated_count"],21)
  self.assertEqual(self.ready["summary"]["blocked_any"],199)
  self.assertEqual(self.ready["summary"]["unknown_total_active"],16)
  self.assertEqual(self.ready["summary"]["ready_to_approve"],0)
  self.assertEqual(len([z for z in self.ledger["models"] if z["status"]=="VERIFIED"]),116)
  self.assertEqual(self.man["no_weights_downloaded"],True)
  self.assertEqual(L("queues/approved.json")["entries"],[])
  self.assertIn(L("catalog/readiness/CURRENT.json")["catalog_revision"],("v67-20261124","v68-20261125","v69-20261125","v70-20261125", "v71-20261125"))
  self.assertIn(L("catalog/estimates/CURRENT.json")["portfolio_revision"],("v67-20261124","v68-20261125","v69-20261125","v70-20261125", "v71-20261125"))
if __name__=="__main__":unittest.main()
