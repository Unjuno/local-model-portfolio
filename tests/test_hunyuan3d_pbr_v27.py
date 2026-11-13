"""v27 read-only Hunyuan3D PBR source dependency and fail-closed rights regression."""
import copy
import unittest
from scripts import audit_hunyuan3d_pbr_v27 as m

class Hunyuan3DPBRTests(unittest.TestCase):
    def synthetic(self):
        txt={
          "hy3dpaint/textureGenPipeline.py":
             'self.dino_ckpt_path = "facebook/dinov2-giant"\n'
             'self.realesrgan_ckpt_path = "ckpt/RealESRGAN_x4plus.pth"\n'
             '# Hunyuan 3D is licensed under the TENCENT HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT',
          "hy3dpaint/utils/multiview_utils.py":
             'allow_patterns=["hunyuan3d-paintpbr-v2-1/*"]\n'
             'self.dino_v2 = Dino_v2(config.dino_ckpt_path)',
          "hy3dpaint/hunyuanpaintpbr/unet/modules.py":
             'self.use_dino = True\n'
             'self.dino_v2 = AutoModel.from_pretrained(dino_v2_path)',
          "hy3dpaint/utils/image_super_utils.py":
             'model_path=config.realesrgan_ckpt_path',
          "hy3dpaint/README.md":m.REAL_RELEASE_URL,
          "README.md":"torch==2.5.1",
          "requirements.txt":"transformers==4.46.0\ndiffusers==0.30.0",
          "LICENSE":"EUROPEAN UNION / UNITED KINGDOM / SOUTH KOREA / Territory",
          "hy3dpaint/LICENSE":"TENCENT HUNYUAN 3D 2.1 COMMUNITY LICENSE AGREEMENT",
        }
        return txt
    def test_publisher_code_original_dependencies_and_legal_restrictions(self):
        x=m.check_pipeline(self.synthetic())
        self.assertTrue(x["DINOv2_giant_required_by_default_pbr_checkpoint"])
        self.assertTrue(x["external_super_resolution_checkpoint_required_for_default_paint_pipeline"])
        self.assertTrue(x["root_community_license_excludes_EU_UK_South_Korea"])
        self.assertFalse(x["environment_candidate"]["tested_on_owner_hardware"])
        wrong=copy.deepcopy(self.synthetic())
        wrong["hy3dpaint/textureGenPipeline.py"]=wrong["hy3dpaint/textureGenPipeline.py"].replace("dinov2-giant","dinov3-vit7b16")
        with self.assertRaises(ValueError):m.check_pipeline(wrong)
        wrong=copy.deepcopy(self.synthetic())
        wrong["hy3dpaint/hunyuanpaintpbr/unet/modules.py"]=wrong["hy3dpaint/hunyuanpaintpbr/unet/modules.py"].replace("True","False")
        with self.assertRaises(ValueError):m.check_pipeline(wrong)
        wrong=copy.deepcopy(self.synthetic())
        wrong["LICENSE"]=wrong["LICENSE"].replace("SOUTH KOREA","")
        with self.assertRaises(ValueError):m.check_pipeline(wrong)
    def test_dinov2_original_only_no_duplicate_pytorch(self):
        rows=[
          {"path":"config.json","bytes":250,"sha256":None,"git_blob_sha1":"a"*40,"identity_kind":"git_blob_sha1"},
          {"path":"preprocessor_config.json","bytes":110,"sha256":None,"git_blob_sha1":"b"*40,"identity_kind":"git_blob_sha1"},
          {"path":"README.md","bytes":900,"sha256":None,"git_blob_sha1":"c"*40,"identity_kind":"git_blob_sha1"},
          {"path":"model.safetensors","bytes":2_400_000_000,"sha256":None,"identity_kind":"unverifiable_payload_hash"},
          {"path":"pytorch_model.bin","bytes":2_400_000_000,"sha256":None,"identity_kind":"unverifiable_payload_hash"},
        ]
        snap={"repo_id":m.DINO,"asset_kind":"model","tree_complete":True,
              "payload_bytes_downloaded":0,"download_authorized":False,"gated":False,
              "license_metadata":"apache-2.0","pinned_revision":"f"*40,
              "source_scope_bytes":4_800_001_260,"files":rows}
        result=m.dino_profile(snap)
        self.assertEqual(result["selected_original_files_bytes"],2_400_001_260)
        self.assertEqual(result["not_chosen_alternative_weight_files"],["pytorch_model.bin"])
        self.assertFalse(result["locally_verified_source_hashes"])
        snap["gated"]="auto"
        with self.assertRaises(ValueError):m.dino_profile(snap)
    def test_immutable_asset_identity_not_a_hash(self):
        self.assertEqual(m.REAL_RELEASE_BYTES,67_040_989)
        self.assertEqual(m.REAL_RELEASE_ASSET_ID,40831506)
        self.assertTrue(m.REAL_RELEASE_URL.endswith("/v0.1.0/RealESRGAN_x4plus.pth"))
        self.assertEqual(len(m.CODE_SHA),40)
    def test_repository_is_still_v27_and_no_approval(self):
        c=m.load("catalog/effective-portfolio-2026-11-07-v27.json")
        self.assertEqual((c["revision_id"],c["counts"]["tracked"],c["counts"]["active"]),
                         ("v27-20261107",173,126))
        self.assertFalse(m.load("queues/approved.json")["entries"])
        s=m.load("catalog/capacity/2026-11-07/v27/capacity-summary.json")
        self.assertEqual(s["known_scope_content_union_bytes"],3_417_685_712_585)
        self.assertEqual(len(s["assets_with_open_dependency_issues"]),35)
if __name__=="__main__":unittest.main()
