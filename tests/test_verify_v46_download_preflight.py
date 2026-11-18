"""Regression tests for offline, non-acquiring v46 preflight."""
import copy
from pathlib import Path
import tempfile
import unittest

from scripts import verify_v46_download_preflight as p


class FrozenSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = p.load(p.MANIFEST)
        cls.queue = p.load(p.PROPOSED)
        cls.approved = p.load(p.APPROVED)
        cls.limits = p.load(p.LIMITS)

    def verify(self, *, manifest=None, queue=None, approved=None):
        return p.validate(manifest or self.manifest, queue or self.queue,
                          approved or self.approved, self.limits)

    def test_real_snapshot_has_twelve_models_and_all_source_sha(self):
        errors, rows = self.verify()
        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 12)
        self.assertEqual(sum(r["bytes"] for r in rows), 206683452429)
        self.assertEqual(sum(len(r["files"]) for r in rows), 131)
        self.assertEqual(sum(r["publisher_sha256_files"] for r in rows), 50)

    def test_model_file_metadata_tamper_must_fail(self):
        m = copy.deepcopy(self.manifest)
        m["selected_models"][0]["selected_original_files"][0]["source_bytes"] += 1
        errors, _ = self.verify(manifest=m)
        self.assertTrue(any("mismatch" in e.lower() or "differs" in e.lower() for e in errors))

    def test_path_traversal_must_fail(self):
        m = copy.deepcopy(self.manifest)
        m["selected_models"][0]["selected_original_files"][0]["path"] = "../outside"
        errors, _ = self.verify(manifest=m)
        self.assertTrue(any("Unsafe" in e for e in errors))

    def test_wrong_revision_must_fail(self):
        m = copy.deepcopy(self.manifest)
        m["selected_models"][0]["immutable_revision"] = "0" * 40
        errors, _ = self.verify(manifest=m)
        self.assertTrue(any("revision" in e for e in errors))

    def test_approval_fails_closed(self):
        a = copy.deepcopy(self.approved)
        a["entries"] = [{"repo_id": "bogus"}]
        errors, _ = self.verify(approved=a)
        self.assertTrue(any("Approved queue changed" in e for e in errors))

    def test_hash_function_detects_mismatched_content(self):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "tiny.bin"
            f.write_bytes(b"test")
            self.assertFalse(p.verify_file(f, 4, "a" * 64, None))
            import hashlib
            correct = hashlib.sha256(b"test").hexdigest()
            self.assertTrue(p.verify_file(f, 4, correct, None))
            self.assertFalse(p.verify_file(f, 3, correct, None))

    def test_paths_are_restricted(self):
        for bad in ("", "../steal", "/absolute", "sub/../danger", "sub\\evil", "a//b", "c:d"):
            self.assertFalse(p.safe_path(bad))
        self.assertTrue(p.safe_path("mtp/model.safetensors"))

    def test_symlink_rejected_if_present(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            m = {"repo_id": "owner/model", "revision": "a" * 40}
            target = root / "owner/model" / m["revision"]
            target.mkdir(parents=True)
            outside = root / "outside"
            outside.write_bytes(b"test")
            (target / "model.safetensors").symlink_to(outside)
            with self.assertRaises(ValueError):
                p.get_local(root, m, "model.safetensors")

    def test_selected_one_small_source_prints_no_execution(self):
        class Args:
            manifest = p.MANIFEST
            queue = p.PROPOSED
            approved = p.APPROVED
            limits = p.LIMITS
            repo_id = ["ibm-granite/granite-timeseries-ttm-r3"]
            archive_root = None
            verify_existing = False
            show_dry_run = True
        result = p.run(Args())
        self.assertEqual(result["status"], "PASS_SOURCE_METADATA_ONLY")
        self.assertFalse(result["download_approved"])
        self.assertEqual(result["model_count"], 1)
        self.assertEqual(result["candidate_source_bytes"], 5748963)
        self.assertIn("--dry-run", result["dry_run_commands_NOT_EXECUTED"][0])


if __name__ == "__main__":
    unittest.main()
