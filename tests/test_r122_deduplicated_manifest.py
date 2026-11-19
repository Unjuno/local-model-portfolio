"""Offline source-scope and downloader regression tests for R122 (no weight download)."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "queues/proposed-v50-r122-deduplicated-next15-sources.json"
R121 = ROOT / "queues/proposed-v50-r121-master-sources-17.json"
R119 = ROOT / "queues/proposed-v49-r119-next7-public-source-entries.json"
R117 = ROOT / "queues/proposed-v48-r117-next-wave-eight-source-pinned.json"
LEDGER = ROOT / "catalog/execution/2026-11-19-acquisition-ledger.json"
SCRIPT = ROOT / "scripts/download_r115_windows.py"
module_spec = importlib.util.spec_from_file_location("r122_downloader", SCRIPT)
module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(module)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class R122Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = read(D)
        cls.a, cls.b, cls.c = read(R121), read(R119), read(R117)
        cls.ledger = read(LEDGER)

    def test_immutable_queue_15_source_repos(self):
        result = module.validate_manifest(self.d)
        self.assertEqual(len(result), 15)
        self.assertEqual(len({x["source_repo_id"] for x in result}), 15)
        self.assertEqual(len([x for x in result if x["repository_type"] == "dataset"]), 2)
        self.assertEqual(sum(len(x["files"]) for x in result), 333)
        self.assertEqual(sum(sum(f.get("sha256") is not None for f in x["files"]) for x in result), 135)
        self.assertEqual(sum(x["source_bytes"] for x in result), 374701290840)

    def test_four_exact_duplicate_scopes_removed(self):
        removed = self.d["source_deduplication_evidence"]
        self.assertEqual(len(removed), 4)
        self.assertEqual({x["id"] for x in removed},
                         {"Zyphra/ZONOS3-Mini", "InterpreticAI/Qwen3.8-27B-Uncensored-v2",
                          "0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF",
                          "microsoft/Fara1.5-27B"})
        self.assertEqual(sum(x["bytes"] for x in removed), 179484014188)
        self.assertEqual(self.d["source_union"]["gross_pre_dedupe_source_bytes"],
                         self.d["source_union"]["unique_selected_source_bytes"]
                         + self.d["source_union"]["exact_duplicate_scope_bytes"])

    def test_reported_seven_exact_scopes_stay_out(self):
        prior = {x["repo_id"]: x for x in self.ledger["models"] if x["status"] == "VERIFIED"}
        matched = [x for x in self.a["entries"] if
                   x.get("eligible_for_unattended_archive_after_local_preflight")
                   and x["catalog_repo_id"] in prior
                   and prior[x["catalog_repo_id"]]["revision_sha"] == x["source_revision"]
                   and prior[x["catalog_repo_id"]]["source_bytes"] == x["source_bytes"]
                   and prior[x["catalog_repo_id"]]["files_total"] == len(x["files"])]
        self.assertEqual(len(matched), 7)
        out = {x["source_repo_id"] for x in self.d["entries"]}
        self.assertFalse(any(x["source_repo_id"] in out for x in matched))

    def test_verified_old_quantization_is_not_original_upgrade(self):
        for rid in ("InterpreticAI/Qwen3.8-27B-Uncensored-v2-GGUF",
                    "0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF",
                    "Zyphra/ZONOS3-Mini"):
            catalog_scope = next(x for x in self.d["entries"] if x["catalog_repo_id"] == rid)
            prev = next(x for x in self.ledger["models"] if x["repo_id"] == rid)
            self.assertNotEqual(prev["source_bytes"], catalog_scope["source_bytes"])
            self.assertTrue(catalog_scope["prior_ledger"]["previously_acquired_same_repo_different_source_scope"])
            self.assertFalse(catalog_scope["prior_ledger"]["reported_verified_scope_match"])

    def test_dataset_download_calls_dataset_repo_type(self):
        source = next(x for x in self.d["entries"] if x["repository_type"] == "dataset")
        client = Mock(return_value="/fake/local/path")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "datasets" / source["source_repo_id"]
            module.hub_download_selected(client, source, source["files"][0]["path"], path)
            client.assert_called_once_with(repo_id=source["source_repo_id"],
                                          filename=source["files"][0]["path"],
                                          revision=source["source_revision"],
                                          local_dir=str(path), repo_type="dataset")

    def test_distinct_dataset_local_namespace(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            source = next(x for x in self.d["entries"] if x["repository_type"] == "dataset")
            where = module.select_existing_destination(base, source["source_repo_id"],
                                                       source["files"], repository_type="dataset")
            self.assertTrue(where.is_relative_to(base / "datasets"))
            self.assertNotIn("/models/", str(where))

    def test_approval_fingerprint_binds_dataset_type(self):
        d = next(x for x in self.d["entries"] if x["repository_type"] == "dataset")
        old = module.source_fingerprint(d)
        alternate = copy.deepcopy(d)
        alternate["repository_type"] = "model"
        self.assertNotEqual(old, module.source_fingerprint(alternate))

    def test_approval_fails_closed_and_never_calls_network(self):
        with tempfile.TemporaryDirectory() as td:
            approval = Path(td) / "approved.json"
            approval.write_text('{"schema_version":1,"entries":[]}', encoding="utf-8")
            with self.assertRaises(ValueError):
                module.assert_explicit_approved_sources(self.d["entries"][:1], approval)

    def test_tampered_byte_count_and_lfs_sha_rejected(self):
        bad = copy.deepcopy(self.d)
        bad["entries"][0]["files"][0]["bytes"] += 1
        with self.assertRaises(ValueError):
            module.validate_manifest(bad)
        bad = copy.deepcopy(self.d)
        wrong = next(f for f in bad["entries"][2]["files"] if f.get("sha256"))
        wrong["sha256"] = "badhash"
        with self.assertRaises(ValueError):
            module.validate_manifest(bad)

    def test_type_and_licensing_violations_rejected(self):
        wrong = copy.deepcopy(self.d)
        wrong["entries"][0]["repository_type"] = "unsupported"
        with self.assertRaises(ValueError):
            module.validate_manifest(wrong)
        wrong = copy.deepcopy(self.d)
        wrong["entries"][0]["license_metadata"] = "unknown"
        with self.assertRaises(ValueError):
            module.validate_manifest(wrong)

    def test_no_dangerous_acquisition_approval(self):
        self.assertFalse(self.d["authorizations"]["user_exact_manifest_approved"])
        self.assertEqual(self.d["authorizations"]["approved_queue_entries"], 0)
        self.assertTrue(all(x["download_approved"] is False for x in self.d["entries"]))


if __name__ == "__main__":
    unittest.main()
