"""Unit and negative tests for static Xiaomi UNIS4B source allowlist."""
import copy
import json
import unittest
from pathlib import Path

from scripts.verify_v39_unis_source_draft import (
    RESEARCH_PATH, DRAFT_PATH, _valid_path, validate,
)

class TestUnisSourceDraft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=json.loads(RESEARCH_PATH.read_text(encoding="utf-8"))
        cls.draft=json.loads(DRAFT_PATH.read_text(encoding="utf-8"))

    def test_current_real_publisher_source_metadata_matches_draft(self):
        result=validate(self.src,self.draft)
        self.assertEqual(result["source_repos"],2)
        self.assertEqual(result["files"],18)
        self.assertEqual(result["source_bytes"],11_991_440_188)
        self.assertEqual(result["safetensors_checkpoints"],3)
        self.assertFalse(result["download_approved"])

    def test_revision_drift_fails(self):
        d=copy.deepcopy(self.draft)
        d["repos"][0]["immutable_revision_sha"]="main"
        with self.assertRaisesRegex(ValueError,"revision"):
            validate(self.src,d)

    def test_bogus_weight_sha256_fails(self):
        d=copy.deepcopy(self.draft)
        rec=next(x for x in d["repos"][0]["files"] if x["path"].endswith(".safetensors"))
        rec["publisher_lfs_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"LFS hash"):
            validate(self.src,d)

    def test_wrong_bytes_fails(self):
        d=copy.deepcopy(self.draft)
        d["repos"][1]["files"][0]["bytes"]+=1
        with self.assertRaisesRegex(ValueError,"bytes"):
            validate(self.src,d)

    def test_pickle_and_path_traversal_fail(self):
        for s in ("model.ckpt","weights.pt","../private.safetensors","/absolute.safetensors",
                  "C:/external.safetensors","foo\\bar.safetensors"):
            with self.subTest(path=s):
                with self.assertRaises(ValueError):
                    _valid_path(s)

    def test_unsafe_state_cannot_pass(self):
        for field in ("approved","download_enabled","download_authorized","auto_download_allowed",
                      "materialize_local_files","offline_restore_verified"):
            d=copy.deepcopy(self.draft)
            d[field]=True
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    validate(self.src,d)

    def test_unreviewed_code_execution_fails(self):
        for field in ("deserialization_from_untrusted_source_permitted",
                      "trust_remote_code_execution_permitted","run_model_to_validate_manifest"):
            d=copy.deepcopy(self.draft)
            d["execution_risk"][field]=True
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    validate(self.src,d)

if __name__=="__main__":
    unittest.main()
