"""Offline, no-model-load tests of Maya2 publisher file verification."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.verify_maya2_local_bundle import verify_bundle, VerificationError

REPOS = ("maya-research/maya2-native", "kyutai/mimi", "speechbrain/spkrec-ecapa-voxceleb")
REVISIONS = (
    "87a83efdd6551e038246b6b37836a6264713eec3",
    "89091b3e466eb6a9d11e537bf26b144f194978f7",
    "0f99f2d0ebe89ac095bcc5903c4dd8f72b367286",
)

def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class BundleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.locations = {}
        self.scopes = []
        for i, repo_id in enumerate(REPOS):
            base = self.root / ("repo" + str(i))
            base.mkdir()
            self.locations[repo_id] = base
            body = ("test-" + str(i)).encode()
            file_name = "model.safetensors" if i != 2 else "embedding_model.ckpt"
            (base / file_name).write_bytes(body)
            cfg = b'{"ok":true}\n'
            (base / "config.json").write_bytes(cfg)
            self.scopes.append({
                "repo_id": repo_id, "immutable_revision_sha": REVISIONS[i],
                "selected_path_count": 2, "selected_bytes": len(body) + len(cfg),
                "files": [
                    {"path": file_name, "size_bytes": len(body),
                     "publisher_lfs_sha256": hashlib.sha256(body).hexdigest(),
                     "publisher_git_blob_sha1": blob_sha(b"git-lfs placeholder")},
                    {"path": "config.json", "size_bytes": len(cfg),
                     "publisher_lfs_sha256": None, "publisher_git_blob_sha1": blob_sha(cfg)}
                ]
            })
        self.manifest = {"formal_portfolio_revision": "v32-20261114", "source_scopes": self.scopes}

    def test_exact_three_source_packages_pass_without_authorization(self):
        report = verify_bundle(self.manifest, self.locations)
        self.assertEqual(report["status"], "SOURCE_FILES_MATCH_UPSTREAM_METADATA")
        self.assertEqual(report["file_count"], 6)
        self.assertEqual(report["repository_count"], 3)
        self.assertEqual(report["download_authorized"], False)
        self.assertEqual(report["safe_to_execute_model_code"], False)
        self.assertEqual(report["tensor_payloads_loaded"], False)
        self.assertEqual(report["source_total_bytes"], sum(s["selected_bytes"] for s in self.scopes))
        self.assertEqual({r["repo_id"] for r in report["repositories"]}, set(REPOS))

    def test_modified_lfs_weight_fails(self):
        p = self.locations[REPOS[1]] / "model.safetensors"
        p.write_bytes(b"WRONG-")
        with self.assertRaisesRegex(VerificationError, "SHA256"):
            verify_bundle(self.manifest, self.locations)

    def test_modified_regular_git_blob_fails(self):
        p = self.locations[REPOS[0]] / "config.json"
        p.write_bytes(b'{"ok":null}')
        with self.assertRaisesRegex(VerificationError, "size"):
            verify_bundle(self.manifest, self.locations)
        p.write_bytes(b'{"ok":1rue}\n')
        with self.assertRaisesRegex(VerificationError, "Git blob"):
            verify_bundle(self.manifest, self.locations)

    def test_missing_external_model_file_fails(self):
        (self.locations[REPOS[2]] / "embedding_model.ckpt").unlink()
        with self.assertRaises(VerificationError):
            verify_bundle(self.manifest, self.locations)

    def test_symlink_redirect_is_rejected(self):
        body = self.locations[REPOS[1]] / "model.safetensors"
        body.rename(self.locations[REPOS[1]] / "real.safetensors")
        body.symlink_to("real.safetensors")
        with self.assertRaisesRegex(VerificationError, "symlink"):
            verify_bundle(self.manifest, self.locations)

    def test_repo_path_traversal_rejected(self):
        self.scopes[0]["files"][0]["path"] = "../outside.safetensors"
        with self.assertRaises(VerificationError):
            verify_bundle(self.manifest, self.locations)

    def test_missing_commit_sha_fails_closed(self):
        self.scopes[1]["immutable_revision_sha"] = None
        with self.assertRaises(VerificationError):
            verify_bundle(self.manifest, self.locations)

    def test_duplicate_selected_files_fail(self):
        self.scopes[2]["files"][1]["path"] = self.scopes[2]["files"][0]["path"]
        with self.assertRaises(VerificationError):
            verify_bundle(self.manifest, self.locations)

    def test_report_is_not_download_permission_even_with_all_verified_files(self):
        r = verify_bundle(self.manifest, self.locations)
        self.assertFalse(r["download_authorized"])
        self.assertFalse(r["license_cleared_for_user"])
        self.assertFalse(r["full_offline_runtime_verified"])

if __name__ == "__main__":
    unittest.main()
