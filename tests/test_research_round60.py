"""R60 public-source SHA and distinct image license audit; standard library."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class R60(unittest.TestCase):
 def setUp(self):self.r=read("catalog/research/2026-11-14-r60-pruna-minimax-h3-licensing-format.json")
 def test_formats(self):
  x=self.r
  self.assertEqual(x["Pruna_full"]["learned_weight_file_count"],15)
  self.assertEqual(x["Pruna_full"]["weight_bytes"],99797308280)
  self.assertEqual(x["MiniMax_H3_Image"]["all_weight_files"],41)
  self.assertEqual(x["MiniMax_H3_Image"]["all_weight_bytes"],203969758064)
  self.assertEqual(x["MiniMax_H3_Image"]["standard_one_format"]["weight_bytes"],135343354088)
  self.assertEqual(x["MiniMax_H3_Image"]["diffusers_one_format"]["weight_bytes"],135353705656)
  self.assertEqual(x["Pruna_comfy"]["chosen_bf16_example"]["weight_bytes"],74471781216)
  self.assertEqual(x["Pruna_comfy"]["chosen_w4a8_example"]["weight_bytes"],26808697441)
 def test_encoder_shared_and_hash_limitations(self):
  s=self.r["cross_source_sha256"]
  self.assertEqual(s["shared_shard_count"],14)
  self.assertEqual(s["shared_bytes"],66714912872)
  self.assertEqual(s["current_actual_reduction_bytes"],0)
  self.assertEqual(s["Pruna_full_vs_MiniMax_H3_Image_matching_LFS_sha256_count"],0)
  self.assertTrue(s["nonmatching_file_sha_does_not_prove_distinct_trained_state"])
 def test_lora_and_legal_product_distinction(self):
  x=self.r
  self.assertEqual(x["Pruna_comfy"]["lora"]["file"]["bytes"],1956195360)
  self.assertGreater(x["Pruna_comfy"]["lora"]["lower_bound_lora_plus_parent_weight_bytes"],x["Pruna_comfy"]["lora"]["file"]["bytes"])
  self.assertFalse(x["Pruna_comfy"]["lora"]["standalone_model"])
  self.assertEqual(x["rights"]["pruna"]["annual_revenue_prior_written_authorization_threshold_usd"],20000000)
  self.assertEqual(x["rights"]["minimax_image"]["annualized_revenue_prior_written_authorization_threshold_usd"],1000000)
  self.assertTrue(x["rights"]["minimax_image"]["any_hosted_service_to_third_parties_requires_prior_written_authorization"])
  self.assertTrue(x["rights"]["two_different_model_products_not_evidence_of_retroactive_license_change"])
 def test_main_unchanged(self):
  c=read("catalog/CURRENT.json")
  self.assertEqual((c["revision_id"],c["expected"]["tracked"],c["expected"]["active"]),("v32-20261114",182,135))
  self.assertEqual(c["latest_image_license_overlap_audit"]["path"],"catalog/research/2026-11-14-r60-pruna-minimax-h3-licensing-format.json")
  self.assertEqual(read("queues/approved.json")["entries"],[])
  self.assertFalse(self.r["no_actions"]["download_approved"])
if __name__=="__main__":unittest.main()
