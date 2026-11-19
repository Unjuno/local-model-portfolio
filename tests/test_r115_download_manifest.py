"""Offline, network-free tests for the R115 Windows archive downloader."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "download_r115_windows.py"
MANIFEST = ROOT / "queues" / "proposed-v48-r115-master-sources-16.json"

spec = importlib.util.spec_from_file_location("r115_download", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class R115ArchiveTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_count_and_scope(self):
        valid = module.validate_manifest(self.data)
        self.assertEqual(len(self.data["entries"]), 16)
        self.assertEqual(len(valid), 10)
        self.assertEqual(sum(item["source_bytes"] for item in valid), 132430668414)
        self.assertEqual(self.data["hold_count"], 6)
        self.assertTrue(self.data["all_go_files_have_publisher_hash"])
        self.assertEqual(self.data["reported_prior_ledger"]["matching_go_scope_models"], 7)
        self.assertEqual(self.data["reported_prior_ledger"]["unreported_changed_go_scope_bytes"], 124740199959)

    def test_no_gated_or_unlicensed_in_download_first_wave(self):
        for model in module.validate_manifest(self.data):
            self.assertEqual(model["license_metadata"], "apache-2.0")
            self.assertFalse(model["gated"])
            self.assertEqual(len(model["source_revision"]), 40)
            self.assertTrue(all(f["sha256"] or f["git_blob_sha1"] for f in model["files"]))

    def test_known_originals_replace_quantized_only(self):
        valid = module.validate_manifest(self.data)
        original = next(x for x in valid if x["source_repo_id"] ==
                        "InterpreticAI/Qwen3.8-27B-Uncensored-v2")
        self.assertEqual(original["source_bytes"], 55586056799)
        self.assertEqual(sum(x["path"].endswith(".safetensors") for x in original["files"]), 18)
        rvn = next(x for x in valid if x["source_repo_id"] ==
                   "0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF")
        weights = [x for x in rvn["files"] if x["path"].endswith(".gguf")]
        self.assertEqual(len(weights), 1)
        self.assertEqual(weights[0]["path"], "RVN-F16.gguf")
        self.assertEqual(weights[0]["sha256"], "f20c72c23a6564211c5e44af35ea1277d697c009ce8a25ab28d100447e0f155a")

    def test_git_blob_sha1_verification(self):
        payload = b"immutable source example\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_bytes(payload)
            expected = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()
            spec = {"path": "config.json", "bytes": len(payload),
                    "sha256": None, "git_blob_sha1": expected}
            ok, how, local_sha = module.verify_file(path, spec)
            self.assertTrue(ok)
            self.assertEqual(how, "verified_publisher_git_blob_sha1")
            self.assertEqual(local_sha, hashlib.sha256(payload).hexdigest())
            path.write_bytes(b"corrupted")
            self.assertFalse(module.verify_file(path, spec)[0])

    def test_lfs_sha256_has_priority_over_lfs_pointer_blob_sha1(self):
        payload = b"fake LFS contents; bytes not executable"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "model.safetensors"
            path.write_bytes(payload)
            spec = {"path": "model.safetensors", "bytes": len(payload),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "git_blob_sha1": "0" * 40}
            self.assertTrue(module.verify_file(path, spec)[0])
            spec["sha256"] = "f" * 64
            self.assertFalse(module.verify_file(path, spec)[0])

    def test_path_validation(self):
        for value in ["../secret", "dir/../secret", r"dir\other", "/absolute", "C:/data", "dir//name"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    module.validate_relpath(value)
        self.assertEqual(module.validate_relpath("phonemizer/g2p.npz"),
                         ("phonemizer", "g2p.npz"))

    def test_source_fingerprint_order_insensitive(self):
        model = module.validate_manifest(self.data)[0]
        reversed_model = {**model, "files": list(reversed(model["files"]))}
        self.assertEqual(module.source_fingerprint(model),
                         module.source_fingerprint(reversed_model))


    def test_execute_without_exact_approval_stops_before_network_or_disk(self):
        # Verify the policy gate is reached before any D-drive or Hub access.
        from unittest.mock import patch
        with patch.object(module.sys, "argv", [
                "r115_download", "--manifest", str(MANIFEST), "--execute"
        ]):
            with self.assertRaises(SystemExit) as caught:
                module.main()
            self.assertEqual(caught.exception.code, 2)

    def test_exact_source_approval_is_required_and_scope_pinned(self):
        valid = module.validate_manifest(self.data)
        model = valid[0]
        approved = {
            "schema_version": 1,
            "entries": [{
                "source_repo_id": model["source_repo_id"],
                "source_revision": model["source_revision"],
                "source_scope_sha256": module.source_fingerprint(model),
                "approved": True,
                "user_explicit_manifest_consent": True,
                "license_and_parent_rights_reviewed": True,
                "owner_archive_volume_verified": True,
            }],
        }
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "owner-approved.json"
            src.write_text(json.dumps(approved), encoding="utf-8")
            module.assert_explicit_approved_sources([model], src)
            # A single changed file size or revision changes the scope fingerprint.
            altered = {**model, "files": [
                {**model["files"][0], "bytes": model["files"][0]["bytes"] + 1},
                *model["files"][1:],
            ]}
            with self.assertRaises(ValueError):
                module.assert_explicit_approved_sources([altered], src)
            # Explicit consent and legal review are separate required booleans.
            approved["entries"][0]["license_and_parent_rights_reviewed"] = False
            src.write_text(json.dumps(approved), encoding="utf-8")
            with self.assertRaises(ValueError):
                module.assert_explicit_approved_sources([model], src)

    def test_staging_reserves_full_weight_copies_not_quarter_file(self):
        self.assertEqual(module.conservative_staging_bytes(1_000_000), 2_000_000_000)
        self.assertEqual(module.conservative_staging_bytes(53_808_281_888), 107_616_563_776)
        with self.assertRaises(ValueError):
            module.conservative_staging_bytes(-1)


if __name__ == "__main__":
    unittest.main()
