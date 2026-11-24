"""R162 source-only offline regression. Never downloads or executes published model code."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class R162PublisherWeightGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = read("manifests/drafts/r162-2026-11-25-new-uncensored-and-decision-partial-publisher-sha-RESEARCH.candidate.json")
        cls.queue = read("queues/proposed-v68-r162-post116-uncensored-specialists-UNAPPROVED.json")
        cls.decisions = read("catalog/decisions/2026-11-25-r162-small-uncensored-decision-model-selection.json")
        cls.catalog = read("catalog/CURRENT.json")
        cls.ledger = read("catalog/execution/2026-11-19-acquisition-ledger.json")
        cls.approved = read("queues/approved.json")

    def test_source_reference_statistics_and_weight_sha(self):
        records = self.src["publisher_model_source_meta"]
        self.assertEqual(len(records), 5)
        self.assertEqual(self.src["decision_summary"]["source_repos_with_trained_payload"], 4)
        self.assertEqual(self.src["decision_summary"]["source_repos_with_no_weights"], 1)
        expected = {
            "2Beyes/Aurum-2B-Uncensored": (23, 4572557909, 1),
            "AnkitNayak-dev/QJev-1.5B-Abliterated": (15, 3102137211, 2),
            "OpenIntelligenceNet/Aion-1.0-Instruct-2.3B-Abliterated": (11, 4593269888, 1),
            "MC7ever/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16-heretic": (16, 7968035453, 2),
            "electroglyph/Spark-X2.6-4B-uncensored-experimental-LoRA": (1, 1519, 0),
        }
        self.assertEqual({x["repo_id"] for x in records}, set(expected))
        for rec in records:
            model_id = rec["repo_id"]
            count, bytes_total, n_weights = expected[model_id]
            self.assertEqual(rec["publisher_file_count"], count)
            self.assertEqual(len(rec["paths"]), count)
            self.assertEqual(len(rec["trained"]), n_weights)
            self.assertEqual(len(set(rec["paths"])), count)
            self.assertEqual(rec["publisher_source_bytes"], bytes_total)
            self.assertRegex(rec["publisher_revision_sha"], r"^[0-9a-f]{40}$")
            self.assertEqual(rec["selected_weight_bytes"] + rec["unresolved_auxiliary_bytes"], bytes_total)
            self.assertFalse(rec["publisher_file_size_map_complete"])
            self.assertFalse(rec["publisher_all_nonweight_git_blob_sha_and_LFS_verified"])
            self.assertFalse(rec["owner_local_sha_verified"])
            self.assertFalse(rec["owner_licensed_act_reviewed"])
            self.assertFalse(rec["download_approved"])
            self.assertFalse(rec["download_enabled"])
            for w in rec["trained"]:
                self.assertIn(w["path"], rec["paths"])
                self.assertRegex(w["publisher_lfs_sha256"], r"^[0-9a-f]{64}$")
                self.assertGreater(w["bytes"], 0)

    def test_aurum_and_qjev_are_priorities_not_formal_catalog_additions(self):
        sel = self.queue["priority_research_no_download"]
        self.assertEqual([x["repo_id"] for x in sel],
                         ["2Beyes/Aurum-2B-Uncensored", "AnkitNayak-dev/QJev-1.5B-Abliterated"])
        self.assertEqual(sum(x["publisher_full_repo_aggregate_bytes"] for x in sel), 7674695120)
        self.assertEqual(sum(x["publisher_repo_file_count"] for x in sel), 38)
        self.assertEqual(sum(len(x["trained_weight_files"]) for x in sel), 3)
        self.assertEqual(self.queue["summary"]["formally_added_models"], 0)
        self.assertEqual(self.decisions["formal_selection_changes"], 0)
        self.assertTrue(self.decisions["full_source_sha_gate_missing"])
        for x in sel:
            self.assertFalse(x["download_enabled"])
            self.assertFalse(x["download_approved"])
            self.assertFalse(x["full_nonweight_path_metadata_verified"])
            self.assertTrue(x["source_file_size_oid_sha_completion_required"])

    def test_sha_differences_do_not_prove_calibration_or_quality(self):
        by = {x["repo_id"]: x for x in self.src["publisher_model_source_meta"]}
        q = by["AnkitNayak-dev/QJev-1.5B-Abliterated"]
        backbone = next(x for x in q["trained"] if x["path"] == "model.safetensors")
        head = next(x for x in q["trained"] if x["path"] == "decision_head.safetensors")
        self.assertNotEqual(backbone["publisher_lfs_sha256"], q["parent_publisher_weight_sha256"])
        self.assertEqual(head["publisher_lfs_sha256"], q["same_head_as_aligned_parent_sha256"])
        aion = by["OpenIntelligenceNet/Aion-1.0-Instruct-2.3B-Abliterated"]
        self.assertNotEqual(aion["trained"][0]["publisher_lfs_sha256"], aion["parent_publisher_weight_sha256"])
        self.assertTrue(aion["parent_reported_locally_acquired"])
        self.assertTrue(aion["status"].startswith("HOLD"))
        self.assertEqual(len(self.queue["held_comparison_sources"]), 2)

    def test_empty_spark_lora_cannot_enter_selection(self):
        spark = next(x for x in self.src["publisher_model_source_meta"]
                     if x["repo_id"].startswith("electroglyph/"))
        self.assertEqual(spark["paths"], [".gitattributes"])
        self.assertEqual(spark["trained"], [])
        self.assertEqual(spark["selected_weight_bytes"], 0)
        self.assertTrue(spark["status"].startswith("REJECT"))
        self.assertEqual(self.queue["excluded_empty_source_repos"][0]["trained_weight_file_count"], 0)

    def test_current_portfolio_and_owner_authorization_fail_closed(self):
        self.assertEqual(self.approved["entries"], [])
        self.assertFalse(self.queue["authorization_gates"]["download_enabled"])
        self.assertFalse(self.queue["authorization_gates"]["owner_windows_D_independent_SHA_verified"])
        self.assertFalse(self.queue["authorization_gates"]["whole_publisher_original_files_per_path_git_oid_sha_pinned"])
        self.assertFalse(self.queue["authorization_gates"]["complete_offline_restore_tested"])
        self.assertEqual(self.decisions["weights_downloaded"], 0)
        self.assertEqual(self.src["actual_models_downloaded_now"], 0)
        self.assertEqual(self.decisions["approved_downloads"], 0)
        if self.catalog["revision_id"] == "v68-20261125":
            self.assertEqual(self.catalog["expected"]["tracked"], 252)
            self.assertEqual(self.catalog["expected"]["active"], 203)
            self.assertFalse(self.catalog["statuses"]["download_approved"])
        verified = {x["repo_id"] for x in self.ledger["models"] if x["status"] == "VERIFIED"}
        if self.ledger["summary"]["models_verified"] == 116:
            self.assertTrue(verified.isdisjoint(
                {x["repo_id"] for x in self.queue["priority_research_no_download"]}))
            self.assertIn("microsoft/Aion-1.0-Instruct-2.3B", verified)


if __name__ == "__main__":
    unittest.main()
