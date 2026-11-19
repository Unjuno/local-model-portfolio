"""R125 archived-model delta: pinned publisher-sidecar inference and executable fail-closed gates.

All tests are local and do not download weights or execute publisher code.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
R122 = ROOT / "queues/proposed-v50-r122-deduplicated-next15-sources.json"
R125 = ROOT / "queues/proposed-v52-r125-ledger61-delta-next15.json"
LEDGER = ROOT / "catalog/execution/2026-11-19-acquisition-ledger.json"
SCRIPT = ROOT / "scripts/download_r115_windows.py"
spec = importlib.util.spec_from_file_location("r125_downloader", SCRIPT)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class DifferentialScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = load(R122)
        cls.delta = load(R125)
        cls.ledger = load(LEDGER)
        cls.previous = {e["source_repo_id"]: e for e in cls.base["entries"]}
        cls.claims = {e["repo_id"]: e for e in cls.ledger["models"]}
        cls.proposed = {e["source_repo_id"]: e for e in cls.delta["entries"]}

    def test_15_entries_287_files_publisher_sha_and_bytes(self):
        entries = app.validate_manifest(self.delta)
        self.assertEqual(len(entries), 15)
        self.assertEqual(len({r["source_repo_id"] for r in entries}), 15)
        self.assertEqual(sum(len(r["files"]) for r in entries), 287)
        self.assertEqual(sum(sum(bool(f.get("sha256")) for f in r["files"]) for r in entries), 118)
        self.assertEqual(sum(r["source_bytes"] for r in entries), 327549073014)

    def test_exact_canonical_source_rename_avoided(self):
        self.assertEqual(set(self.previous), set(self.proposed))
        self.assertEqual(len(self.proposed), 15)
        for rid, proposal in self.proposed.items():
            self.assertEqual(proposal["source_revision"], self.previous[rid]["source_revision"])
            self.assertEqual(proposal["repository_type"], self.previous[rid]["repository_type"])

    def test_twelve_non_delta_scopes_are_unchanged(self):
        supplementary = {"RWKV/RWKV7-7.2B-20260805",
                         "GSAI-ML/iLLaDA-8B-Base",
                         "microsoft/TRELLIS.2-4B"}
        for rid in set(self.proposed) - supplementary:
            self.assertEqual(self.proposed[rid]["files"], self.previous[rid]["files"])
            self.assertEqual(self.proposed[rid]["source_bytes"], self.previous[rid]["source_bytes"])
            self.assertEqual(self.proposed[rid]["prerequisite_weight_files"], [])

    def test_remaining_sidecars_and_matching_ledger_sha(self):
        expected = {
            "RWKV/RWKV7-7.2B-20260805": (7, 337813, 3),
            "GSAI-ML/iLLaDA-8B-Base": (4, 28506, 5),
            "microsoft/TRELLIS.2-4B": (1, 1519, 9),
        }
        for rid, (n, b, weight_count) in expected.items():
            e = self.proposed[rid]
            self.assertEqual((len(e["files"]), e["source_bytes"]), (n, b))
            self.assertEqual(len(e["prerequisite_weight_files"]), weight_count)
            claim = self.claims[rid]
            self.assertEqual(e["source_revision"], claim["revision_sha"])
            pub = {f["path"]: f for f in self.previous[rid]["files"]}
            prereq = {f["path"]: f for f in e["prerequisite_weight_files"]}
            actual = {f["path"]: f["sha256"] for f in claim["weight_files_sha256"]}
            self.assertEqual(set(prereq), set(actual))
            for path, digest in actual.items():
                self.assertEqual(prereq[path]["sha256"], digest)
                self.assertEqual(prereq[path], pub[path])
            self.assertTrue(all(f["path"] in pub for f in e["files"]))
            self.assertEqual(set(f["path"] for f in e["files"]) & set(prereq), set())

    def test_unique_subset_is_inference_not_physical_check(self):
        for rid in ("RWKV/RWKV7-7.2B-20260805",
                    "GSAI-ML/iLLaDA-8B-Base",
                    "microsoft/TRELLIS.2-4B"):
            e = self.proposed[rid]
            obs = self.claims[rid]
            original = self.previous[rid]
            weights = {f["path"] for f in e["prerequisite_weight_files"]}
            others = [f for f in original["files"] if f["path"] not in weights]
            n = original["source_file_count"] - obs["files_total"]
            b = original["source_bytes"] - obs["source_bytes"]
            matches = 0
            for mask in range(1 << len(others)):
                if mask.bit_count() == n and sum(x["bytes"] for i, x in enumerate(others) if mask & (1 << i)) == b:
                    matches += 1
            self.assertEqual(matches, 1)
            self.assertFalse(e["current_owner_disk_rehashed_this_turn"])

    def test_approval_fingerprint_binds_prerequisite_hash(self):
        e = self.proposed["GSAI-ML/iLLaDA-8B-Base"]
        original = app.source_fingerprint(e)
        bad = copy.deepcopy(e)
        bad["prerequisite_weight_files"][0]["sha256"] = "0" * 64
        self.assertNotEqual(original, app.source_fingerprint(bad))

    def test_prerequisite_sha_tamper_fails_closed(self):
        bad = copy.deepcopy(self.delta)
        entry = next(x for x in bad["entries"] if x["source_repo_id"] == "microsoft/TRELLIS.2-4B")
        entry["prerequisite_weight_files"][0]["sha256"] = "bad"
        with self.assertRaisesRegex(ValueError, "prerequisite"):
            app.validate_manifest(bad)
        bad = copy.deepcopy(self.delta)
        entry = next(x for x in bad["entries"] if x["source_repo_id"] == "microsoft/TRELLIS.2-4B")
        entry["prerequisite_weight_files"].clear()
        with self.assertRaises(ValueError):
            app.validate_manifest(bad)

    def test_cannot_inject_missing_weight_into_supplement(self):
        bad = copy.deepcopy(self.delta)
        entry = next(x for x in bad["entries"] if x["source_repo_id"] == "RWKV/RWKV7-7.2B-20260805")
        entry["files"].append(entry["prerequisite_weight_files"][0])
        with self.assertRaises(ValueError):
            app.validate_manifest(bad)

    def test_existing_weights_sha_gate_blocks_missing_corruption(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            destination = root / "models" / "publisher" / "model"
            destination.mkdir(parents=True)
            weight = destination / "original.safetensors"
            expected_bytes = b"verified-in-test"
            expected = {
                "path": "original.safetensors",
                "bytes": len(expected_bytes),
                "sha256": hashlib.sha256(expected_bytes).hexdigest(),
                "git_blob_sha1": None,
            }
            # No file: no transfer may begin.
            self.assertEqual(
                app.inspect_existing_weight_prerequisites(root, destination, [expected]),
                [("original.safetensors", "not_regular_file")])
            weight.write_bytes(expected_bytes)
            self.assertEqual(
                app.inspect_existing_weight_prerequisites(root, destination, [expected]), [])
            weight.write_bytes(b"corrupted-bytes!"[:len(expected_bytes)])
            invalid = app.inspect_existing_weight_prerequisites(root, destination, [expected])
            self.assertEqual(len(invalid), 1)
            self.assertTrue(invalid[0][1] in ("sha256_mismatch", "size_mismatch"))

    def test_weight_gate_refuses_symlink_even_on_matching_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            destination = root / "models" / "author" / "name"
            destination.mkdir(parents=True)
            outside = root / "outside-weight"
            outside.write_bytes(b"abc")
            link = destination / "linked.safetensors"
            link.symlink_to(outside)
            with self.assertRaises(ValueError):
                app.inspect_existing_weight_prerequisites(
                    root, destination,
                    [{"path": "linked.safetensors", "bytes": 3,
                      "sha256": hashlib.sha256(b"abc").hexdigest(),
                      "git_blob_sha1": None}])

    def test_empty_approval_does_not_enable_any_transfer(self):
        with tempfile.TemporaryDirectory() as td:
            empty = Path(td) / "approved.json"
            empty.write_text('{"schema_version":1,"entries":[]}', encoding="utf-8")
            with self.assertRaises(ValueError):
                app.assert_explicit_approved_sources(app.validate_manifest(self.delta)[:1], empty)

    def test_dataset_and_first_small_files_remain_selected(self):
        first = self.delta["entries"][0]
        self.assertEqual(first["source_repo_id"], "elyza/ELYZA-tasks-100")
        self.assertEqual(first["repository_type"], "dataset")
        self.assertTrue(any(x["path"] == "test.csv" for x in first["files"]))
        self.assertEqual(self.delta["entries"][1]["source_repo_id"], "CohereLabs/aya_dataset")
        self.assertEqual(self.delta["entries"][2]["source_repo_id"], "Reson8/Rumble-2-Flash")

    def test_report_count_and_byte_reconciliation(self):
        diff = self.delta["source_difference"]
        self.assertEqual(diff["base_source_bytes"] - diff["new_selected_source_bytes"], 47152036163)
        self.assertEqual(diff["inferred_sidecar_only_source_bytes"], 367838)
        self.assertEqual(diff["other_new_or_precision_specific_source_bytes"], 327548705176)
        self.assertEqual(self.delta["source_acquisition_claim_reported_verified_models"], 61)
        self.assertEqual(self.delta["source_acquisition_claim_reported_bytes"], 409835119252)


if __name__ == "__main__":
    unittest.main()
