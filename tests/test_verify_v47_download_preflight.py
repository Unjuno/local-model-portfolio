"""v47 R111 fixed source metadata and archive fail-closed checks."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from scripts import verify_v47_download_preflight as p


class V47SourceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q, cls.d, cls.approved, cls.limits, cls.current = [
            p.read_json(path) for path in (p.QUEUE, p.DECISIONS, p.APPROVED, p.LIMITS, p.CANDIDATES)
        ]

    def validate(self, **kw):
        return p.validate(kw.get("q", self.q), kw.get("d", self.d),
                          kw.get("approved", self.approved), kw.get("limits", self.limits),
                          kw.get("current", self.current))

    def test_all_14_models_173_files_72_sha(self):
        errors, rows = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 14)
        self.assertEqual(sum(len(x["files"]) for x in rows), 173)
        self.assertEqual(sum(x["bytes"] for x in rows), 211999468264)

    def test_r110_sha_normalization_for_two_new_models(self):
        entries = {x["repo_id"]: x for x in self.q["entries"]}
        self.assertEqual(sum(1 for x in entries["KittenML/kitten-tts-2-mini"]["files"]
                             if p.source_sha(x) is not None), 19)
        self.assertEqual(sum(1 for x in entries["osunlp/ARLoop-1.2B"]["files"]
                             if p.source_sha(x) is not None), 3)

    def test_byte_tampering_rejected(self):
        q = copy.deepcopy(self.q)
        q["entries"][0]["files"][0]["bytes"] += 1
        e, _ = self.validate(q=q)
        self.assertTrue(e)

    def test_invalid_relative_path_rejected(self):
        q = copy.deepcopy(self.q)
        q["entries"][0]["files"][0]["path"] = "../escape"
        e, _ = self.validate(q=q)
        self.assertTrue(any("Unsafe" in x for x in e))

    def test_wrong_revision_rejected(self):
        q = copy.deepcopy(self.q)
        q["entries"][0]["source_revision"] = "not-a-sha"
        e, _ = self.validate(q=q)
        self.assertTrue(any("Invalid commit" in x for x in e))

    def test_wrong_sha_rejected(self):
        q = copy.deepcopy(self.q)
        q["entries"][-1]["files"][8]["publisher_lfs_sha256"] = "not-a-sha"
        e, _ = self.validate(q=q)
        self.assertTrue(e)

    def test_no_approval_shortcut(self):
        approved = copy.deepcopy(self.approved)
        approved["entries"] = [{"repo_id": "unsafe"}]
        e, _ = self.validate(approved=approved)
        self.assertTrue(any("approved queue" in x.lower() for x in e))

    def test_bad_current_version_rejected(self):
        cur = copy.deepcopy(self.current)
        cur["revision_id"] = "v46-20261118"
        e, _ = self.validate(current=cur)
        self.assertTrue(any("Not v47" in x for x in e))

    def test_sha_file_verification(self):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "small"
            f.write_bytes(b"model")
            sha = hashlib.sha256(b"model").hexdigest()
            self.assertTrue(p.fingerprint(f, 5, {"sha256": sha}))
            self.assertFalse(p.fingerprint(f, 5, {"sha256": "1" * 64}))

    def test_path_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            item = {"repo_id": "owner/model", "revision": "a" * 40}
            inside = root / "owner/model" / item["revision"]
            inside.mkdir(parents=True)
            outside = root / "outside"
            outside.write_bytes(b"file")
            (inside / "weight.safetensors").symlink_to(outside)
            with self.assertRaises(ValueError):
                p.local_file(root, item, "weight.safetensors")

    def test_test_one_model_no_download(self):
        class Args:
            queue = p.QUEUE
            decisions = p.DECISIONS
            current = p.CANDIDATES
            approved = p.APPROVED
            limits = p.LIMITS
            lane = None
            repo_id = ["ibm-granite/granite-timeseries-ttm-r3"]
            archive_root = None
            verify_existing = False
            show_dry_run = True
        result = p.run(Args())
        self.assertEqual(result["status"], "PASS_PUBLISHER_METADATA_ONLY")
        self.assertFalse(result["download_approved"])
        self.assertEqual(result["requested_models"], 1)
        self.assertEqual(result["historical_selected_source_bytes"], 5748963)
        self.assertIn("--dry-run", result["commands_not_executed"][0])


if __name__ == "__main__":
    unittest.main()
