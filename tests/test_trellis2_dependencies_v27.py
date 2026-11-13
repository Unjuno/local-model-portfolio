"""TRELLIS.2 v27 source manifest contract and fail-closed unknown gating tests."""
import copy
import unittest
from scripts import audit_trellis2_dependencies_v27 as a

class TrellisDependencies(unittest.TestCase):
    def config(self):
        return {"args":{"models":{"sparse_structure_decoder":
                                  "microsoft/TRELLIS-image-large/ckpts/ss_dec_conv3d_16l8_fp16"},
           "image_cond_model":{"name":"DinoV3FeatureExtractor","args":{"model_name":a.DINO}},
           "rembg_model":{"name":"BiRefNet","args":{"model_name":a.RMBG}}}}
    def txt(self):
        return {"trellis2/pipelines/trellis2_image_to_3d.py":
                "pipeline.rembg_model = getattr(rembg, key)\n"
                "pipeline.image_cond_model = getattr(image_feature_extractor, key)\n"
                "if has_alpha:\n",
                "trellis2/modules/image_feature_extractor.py":
                "DINOv3ViTModel.from_pretrained(model_name)",
                "trellis2/pipelines/rembg/BiRefNet.py":
                "AutoModelForImageSegmentation.from_pretrained",
                "trellis2/pipelines/base.py":
                "models.from_pretrained(v)"}
    def test_parent_selected_and_no_dino_vitl_in_existing_catalog(self):
        c=a.load("catalog/CURRENT.json")
        self.assertEqual(c["revision_id"],"v27-20261107")
        self.assertEqual((c["expected"]["tracked"],c["expected"]["active"]),(173,126))
        q=a.load("queues/approved.json")
        self.assertFalse(q["entries"])
        v=a.load(c["materialized_catalog_path"])
        names={x["repo_id"] for x in v["items"]}
        self.assertIn(a.PARENT,names)
        self.assertNotIn(a.DINO,names)
        self.assertNotIn(a.RMBG,names)
        self.assertNotIn(a.DECODER,names)
        self.assertIn("facebook/dinov3-vit7b16-pretrain-lvd1689m",names)
        self.assertIn("facebook/dinov3-vith16plus-pretrain-lvd1689m",names)
    def test_exact_expected_code_requirements_and_alternatives(self):
        x=a.verify_identifiers(self.config(),self.txt())
        self.assertEqual(x["required_vision_model"],a.DINO)
        self.assertEqual(x["default_loader_rembg_model"],a.RMBG)
        self.assertTrue(x["DINOv3_is_always_constructed_by_default_loader"])
        self.assertTrue(x["RMBG_is_functionally_replaceable_with_different_background_preprocessor"])
        self.assertFalse(x["offlinedemo_executed"])
        conf=self.config()
        conf["args"]["image_cond_model"]["args"]["model_name"]="facebook/dinov3-vit7b16-pretrain-lvd1689m"
        with self.assertRaises(ValueError):a.verify_identifiers(conf,self.txt())
        conf=self.config()
        conf["args"]["models"]["sparse_structure_decoder"]="ckpts/other"
        with self.assertRaises(ValueError):a.verify_identifiers(conf,self.txt())
    def test_decoder_subset_not_whole_repo_and_access_unknown_not_zero(self):
        files=[{"path":a.DECODER_STEM+".json","bytes":500,
                "sha256":None,"identity_kind":"git_blob_sha1"},
               {"path":a.DECODER_STEM+".safetensors","bytes":12000,
                "sha256":"a"*64,"identity_kind":"lfs_payload_sha256"},
               {"path":"ckpts/some-other-model.safetensors","bytes":1000000,
                "sha256":"b"*64,"identity_kind":"lfs_payload_sha256"}]
        src={"repo_id":a.DECODER,"asset_kind":"model","tree_complete":True,
             "files":files,"source_scope_bytes":1_012_500,
             "pinned_revision":"f"*40,"gated":False,"license_metadata":"mit",
             "payload_bytes_downloaded":0,"download_authorized":False}
        row=a.source_select(a.DECODER,src)
        self.assertEqual(row["selected_file_bytes"],12500)
        self.assertEqual(len(row["selected_files"]),2)
        self.assertFalse(row["personal_access_verified"])
        blocked=copy.deepcopy(src);blocked["repo_id"]=a.DINO
        blocked["tree_complete"]=False;blocked["source_scope_bytes"]=None
        blocked["files"]=[];blocked["gated"]="auto";blocked["error"]="HTTPError: 401"
        d=a.source_select(a.DINO,blocked)
        self.assertIsNone(d["selected_file_bytes"])
        self.assertIsNone(d["selected_files"])
        self.assertTrue(d["gated"])
    def test_gated_dependent_source_profile_masks_strong_identity(self):
        files=[{"path":"config.json","bytes":120,"sha256":None,
                "identity_kind":"git_blob_sha1","payload_hash_masked":False},
               {"path":"model.safetensors","bytes":50000,"sha256":None,
                "identity_kind":"unverifiable_payload_hash","payload_hash_masked":True},
               {"path":"pytorch_model.bin","bytes":50000,"sha256":None,
                "identity_kind":"unverifiable_payload_hash","payload_hash_masked":True}]
        src={"repo_id":a.DINO,"asset_kind":"model","tree_complete":True,
             "files":files,"source_scope_bytes":100120,"pinned_revision":"e"*40,
             "gated":"auto","license_metadata":"other",
             "download_authorized":False,"payload_bytes_downloaded":0}
        row=a.source_select(a.DINO,src)
        self.assertEqual(row["selected_file_bytes"],50120)
        self.assertEqual(row["masked_lfs_payload_files"],1)
        self.assertEqual(row["selected_files_missing_sha256"],1)
        self.assertEqual(len(row["selected_files"]),2)
        self.assertFalse(row["license_body_cleared"])
        bad=copy.deepcopy(src);bad["files"]=[f for f in files if f["path"]!="model.safetensors" and f["path"]!="pytorch_model.bin"]
        bad["source_scope_bytes"]=120
        self.assertIsNone(a.source_select(a.DINO,bad)["selected_file_bytes"])
if __name__=="__main__":unittest.main()
