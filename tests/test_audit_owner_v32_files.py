"""Read-only v32 local archive verification tests (no model files downloaded)."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from scripts import audit_owner_v32_files as audit


class OwnerSourceTests(unittest.TestCase):
    def test_source_inventory_one_to_one_for_all_135(self):
        # Real 21MB legacy metadata; never touches external checkpoint payloads.
        root = audit.ROOT
        c = audit.load(root, "catalog/effective-portfolio-2026-11-14-v32.json")
        old = audit.load(root, "catalog/capacity/2026-11-07/v27/selected-file-capacity.json")
        r64 = audit.load(root, "manifests/drafts/r64-eight-source-scopes.candidate.json")
        r48 = audit.load(root, "catalog/research/2026-11-12-r48-pinned-scopes.json")
        idx = audit.build_index(c, old, r64, r48)
        self.assertEqual(len(idx), 135)
        self.assertEqual(sum(x["evidence"] == "V27_PUBLISHER_SOURCE_HISTORY" for x in idx.values()), 126)
        self.assertEqual(sum(x["evidence"] == "R64_FIXED_SOURCE_SUBSET" for x in idx.values()), 8)
        self.assertEqual(sum(x["evidence"] == "R48_REFERENCE_NOT_COMPLETE_RUNTIME" for x in idx.values()), 1)
        self.assertEqual(sum(len(x["files"]) for x in idx.values()), 60020)
        self.assertNotIn("ACE-Step/Ace-Step1.5", idx)

    def test_hash_size_missing_and_unknown_mask_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "actual.bin").write_bytes(b"five!")
            m = audit.normalized("actual.bin", 5, hashlib.sha256(b"five!").hexdigest(),
                                 None, kind="publisher_payload_sha256")
            self.assertEqual(audit.check_file(root, m), "MATCHED")
            self.assertEqual(audit.check_file(root, dict(m, sha256="f" * 64)), "BAD_HASH")
            self.assertEqual(audit.check_file(root, dict(m, bytes=7)), "BAD_SIZE")
            self.assertEqual(audit.check_file(root, dict(m, sha256=None)), "PUBLISHER_HASH_UNKNOWN")
            self.assertEqual(audit.check_file(root, dict(m, path="not-here.bin")), "MISSING")

    def test_git_blob_sha1_content_not_lfs_pointer(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = b"LICENSE\n"
            (root / "LICENSE").write_bytes(data)
            digest = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
            f = audit.normalized("LICENSE", len(data), None, digest, kind="git_blob_sha1")
            self.assertEqual(audit.check_file(root, f), "MATCHED")
            pointer = audit.normalized("model.bin", len(data), None, digest,
                                       kind="unverifiable_payload_hash")
            self.assertIsNone(pointer["git_blob_sha1"])
            self.assertEqual(audit.check_file(root, dict(pointer, path="LICENSE")),
                             "PUBLISHER_HASH_UNKNOWN")

    def test_symlink_even_within_root_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = b"hello"
            (root / "original.bin").write_bytes(data)
            try:
                (root / "alias.bin").symlink_to(root / "original.bin")
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            f = audit.normalized("alias.bin", len(data), hashlib.sha256(data).hexdigest(), None)
            self.assertEqual(audit.check_file(root, f), "UNSAFE_PATH")

    def test_traversal_or_duplicate_file_identity_rejected(self):
        for path in ("../secret", "/etc/passwd", "root//child", "root\\other", "a:b"):
            with self.assertRaises(ValueError):
                audit.normalized(path, 1, None, None)
        with self.assertRaises(ValueError):
            audit.normalized("file", -1, None, None)
        with self.assertRaises(ValueError):
            audit.normalized("file", 1, "bad", None)

    def test_inert_verified_source_does_not_approve_restore(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp)
            repo_id, revision = "example/tiny", "a"*40
            root = archive/"store"/"huggingface"/"model"/"example"/"tiny"/revision
            root.mkdir(parents=True)
            (root/"w.safetensors").write_bytes(b"okay")
            entry = {"kind":"model","repo_id":repo_id,"revision":revision,
                     "evidence":"SYNTHETIC_TEST_ONLY","files":[audit.normalized(
                         "w.safetensors",4,hashlib.sha256(b"okay").hexdigest(),None)]}
            result = audit.inspect_asset(archive, entry)
            self.assertTrue(result["all_selected_file_hashes_match"])
            self.assertFalse(result["legal_acquisition_rights_passed"])
            self.assertFalse(result["offline_reconstruction_test_passed"])


if __name__ == "__main__":
    unittest.main()
