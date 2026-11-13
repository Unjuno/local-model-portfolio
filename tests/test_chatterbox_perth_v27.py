"""Guards for preserved Chatterbox/Perth source, default-v2 mismatch, no approvals."""
import copy,unittest
from scripts import audit_chatterbox_perth_v27 as a
class ChatterboxPerthSourceTests(unittest.TestCase):
    def test_baseline_is_immutable_and_126(self):
        c=a.read_json("catalog/effective-portfolio-2026-11-07-v27.json")
        self.assertEqual((c["revision_id"],c["counts"]["tracked"],c["counts"]["active"]),
                         ("v27-20261107",173,126))
        self.assertFalse(a.read_json("queues/approved.json")["entries"])
        b=a.read_json("catalog/capacity/2026-11-07/v27/selected-file-capacity.json")
        self.assertEqual(b["known_scope_content_union_bytes"],3_417_685_712_585)
        self.assertEqual(len(b["assets_with_open_dependency_issues"]),35)
        self.assertEqual(b["exact_primary_file_scope_count"],126)
    def test_code_revision_vs_weight_revision_is_not_identical(self):
        self.assertEqual(a.CHAT[1],"ab55923c27757c90cfcc407baa57dc25a7d25217")
        self.assertEqual(a.PERTH[1],"ff1c8ac55a976971245cdd53c18d6131ca00d993")
        self.assertEqual(a.CKPT,"src/perth/perth_net/pretrained/implicit/perth_net_250000.pth.tar")
        self.assertNotEqual(a.CHAT[1],a.PERTH[1])
    def test_hash_aware_source_increment_without_materialization(self):
        b=a.read_json("catalog/capacity/2026-11-07/v27/selected-file-capacity.json")
        before=copy.deepcopy(b)
        x=[{"path":"test_aaa","bytes":12,"git_blob_sha1":"a"*40,"identity_kind":"git_blob_sha1"}]
        y=[{"path":"test_bbb","bytes":8,"git_blob_sha1":"b"*40,"identity_kind":"git_blob_sha1"}]
        r=a.source_only_dedup(b,x,y)
        self.assertEqual(b,before)
        self.assertEqual(r["hash_identity_aware_new_bytes"],20)
        self.assertEqual(r["research_scenario_logical_bytes"],b["known_scope_content_union_bytes"]+20)
        self.assertIsNone(r["physical_owner_disk_free_bytes"])
        self.assertIsNone(r["full_offline_archive_bytes"])
    def test_static_compatibility_checks_fail_closed(self):
        ch={"README.md":"As of August 2026, Chatterbox is retired research",
            "LICENSE":"MIT License",
            "pyproject.toml":"resemble-perth @ git+https://github.com/resemble-ai/Perth.git@master\ntransformers==5.2.0\ntorch==2.6.0\ntorchaudio==2.6.0",
            "src/chatterbox/mtl_tts.py":'DEFAULT_MULTILINGUAL_T3_MODEL = "t3_mtl23ls_v2.safetensors"\n"v3": "t3_mtl23ls_v3.safetensors"\nckpt_dir / "s3gen.pt"\nperth.PerthImplicitWatermarker()\napply_watermark\nrevision="main"'}
        pe={"LICENSE":"MIT License",
            "pyproject.toml":"", "src/perth/config.py":'"perth_net", "pretrained"',
            "src/perth/__init__.py":"except ImportError:\n    PerthImplicitWatermarker = None",
            "src/perth/perth_net/perth_net_implicit/perth_watermarker.py":"PerthNet.load(run_name, models_dir)"}
        r=a.audit_source_strings(ch,pe)
        self.assertTrue(r["explicit_t3_model_v3_required_for_selected_archive"])
        self.assertTrue(r["perth_package_installed_from_MUTABLE_master"])
        self.assertFalse(r["gpu_runtime_tested"])
        bad=copy.deepcopy(ch);bad["pyproject.toml"]=bad["pyproject.toml"].replace("@master","@deadbeef")
        with self.assertRaises(ValueError):a.audit_source_strings(bad,pe)
        bad=copy.deepcopy(ch);bad["src/chatterbox/mtl_tts.py"]=bad["src/chatterbox/mtl_tts.py"].replace('"v3":','"v7":')
        with self.assertRaises(ValueError):a.audit_source_strings(bad,pe)
        bad=copy.deepcopy(pe);bad["src/perth/__init__.py"]=""
        with self.assertRaises(ValueError):a.audit_source_strings(ch,bad)
if __name__=="__main__":
    unittest.main()
