"""R160 v68 three-source precursor regression reconciled with the four-original canonical v68; no model payload fetch or arbitrary code execution.

Run from repository root with: python -m unittest tests.test_r160_v68_three_small_originals
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class R160V68ThreeCompactOriginals(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.before = load("catalog/effective-portfolio-2026-11-24-v67.json")
        cls.after = load("catalog/effective-portfolio-2026-11-25-v68.json")
        cls.overlay = load("catalog/revisions/v68-2026-11-25.json")
        cls.freeze = load("manifests/drafts/r160-2026-11-25-three-edge-trained-originals-source-freeze.candidate.json")
        cls.merged = load("manifests/drafts/r160-2026-11-25-four-small-trained-states-75file-publisher-frozen.candidate.json")
        cls.queue_before = load("queues/proposed-v67-2026-11-24.json")
        cls.queue_after = load("queues/proposed-v68-2026-11-25.json")
        cls.access_before = load("catalog/access/2026-11-24-v67-conditional-hub-gates.json")
        cls.access_after = load("catalog/access/2026-11-25-v68-conditional-hub-gates.json")
        cls.prep_before = load("catalog/preparation/2026-11-24-insurance-bundles-v67.json")
        cls.prep_after = load("catalog/preparation/2026-11-25-insurance-bundles-v68.json")
        cls.readiness_before = load("catalog/readiness/v67-2026-11-24-r158-all199-gates.json")
        cls.readiness_after = load("catalog/readiness/v68-2026-11-25-r160-all203-gates.json")
        cls.current = load("catalog/CURRENT.json")
        cls.approved = load("queues/approved.json")
        cls.ledger = load("catalog/execution/2026-11-19-acquisition-ledger.json")

    def test_v67_248_asset_records_not_changed(self):
        self.assertEqual(self.before["revision_id"], "v67-20261124")
        self.assertEqual(self.after["revision_id"], "v68-20261125")
        self.assertEqual(len(self.before["items"]), 248)
        self.assertEqual(len(self.after["items"]), 252)
        self.assertEqual(self.after["items"][:248], self.before["items"])
        self.assertEqual(self.after["items"][-4:], self.overlay["additions"])
        self.assertEqual(self.overlay["previous_asset_count"], 248)
        self.assertEqual(self.overlay["added_assets"],
                         ["openbmb/MiniCPM5-2B", "illuin/Ivonnet-0.8B",
                          "illuin/IVE-4B", "tencent/WeMM-Ecom-0.8B"])
        self.assertEqual(self.overlay["removed_assets"], [])
        self.assertEqual(self.overlay["changed_prior_decisions"], [])
        keys = [(x["asset_kind"], x["repo_id"]) for x in self.after["items"]]
        self.assertEqual(len(keys), len(set(keys)))

    def test_counts_and_owner_nonapproval(self):
        expected = self.after["counts"]
        self.assertEqual(expected["tracked"], 252)
        self.assertEqual(expected["active"], 203)
        self.assertEqual(expected["models"], 226)
        self.assertEqual(expected["datasets"], 26)
        self.assertEqual(expected["by_decision"]["conditional"], 147)
        self.assertEqual(expected["by_decision"]["select"], 56)
        self.assertEqual(expected["by_tier"]["R1"], 142)
        self.assertEqual(expected["by_tier"]["R2"], 42)
        self.assertEqual(expected["parameter_gate"]["PASS_TOTAL_PARAMS_LT_150B"], 193)
        self.assertIn(self.current["revision_id"], ("v68-20261125", "v69-20261125","v70-20261125"))
        self.assertGreaterEqual(self.current["expected"]["tracked"], 252)
        self.assertGreaterEqual(self.current["expected"]["active"], 203)
        self.assertFalse(self.current["statuses"]["download_approved"])
        self.assertEqual(self.approved["entries"], [])
        self.assertFalse(any(x.get("download_approved", False) for x in self.after["items"]))
        self.assertFalse(self.overlay["owner_D_actual_files_rehashed_now"])
        self.assertEqual(self.overlay["weights_payload_downloaded_now"], 0)

    def test_frozen_publisher_source_and_trained_weights(self):
        f = self.freeze
        self.assertEqual(f["totals"]["source_repos"], 3)
        self.assertEqual(f["totals"]["full_files"], 52)
        self.assertEqual(f["totals"]["full_bytes"], 8505348758)
        self.assertEqual(f["totals"]["LFS_sha256_refs"], 13)
        self.assertEqual(f["totals"]["trained_weight_files"], 4)
        expected_repo = {
            "tencent/WeMM-Ecom-0.8B": (20, 1733044450, 8),
            "openbmb/MiniCPM5-2B": (11, 5043807977, 1),
            "illuin/Ivonnet-0.8B": (21, 1728496331, 4),
        }
        actual = {}
        weight_sha = []
        for s in f["originals"]:
            self.assertRegex(s["publisher_revision_sha"], r"^[a-f0-9]{40}$")
            self.assertEqual(s["publisher_full_file_count"], len(s["publisher_files"]))
            self.assertEqual(s["publisher_full_bytes"], sum(x["bytes"] for x in s["publisher_files"]))
            self.assertEqual(s["publisher_lfs_sha256_refs"],
                             sum(bool(x["publisher_lfs_sha256"]) for x in s["publisher_files"]))
            paths = [x["path"] for x in s["publisher_files"]]
            self.assertEqual(len(paths), len(set(paths)))
            self.assertTrue(set(s["trained_weight_paths"]) <= set(paths))
            for x in s["publisher_files"]:
                self.assertRegex(x["publisher_git_blob_sha1"], r"^[a-f0-9]{40}$")
                self.assertGreaterEqual(x["bytes"], 0)
                if x["publisher_lfs_sha256"] is not None:
                    self.assertRegex(x["publisher_lfs_sha256"], r"^[a-f0-9]{64}$")
                self.assertFalse(x["owner_sha256_verified"])
            weight_sha.extend(s["trained_weight_SHA256"])
            self.assertFalse(s["owner_rights_per_act_approved"])
            self.assertFalse(s["owner_local_SHA_verified"])
            self.assertFalse(s["download_approved"])
            self.assertFalse(s["manifest_individually_approved"])
            actual[s["repo_id"]] = (len(paths), s["publisher_full_bytes"], s["publisher_lfs_sha256_refs"])
        self.assertEqual(actual, expected_repo)
        self.assertEqual(len(weight_sha), 4)
        self.assertEqual(len(set(weight_sha)), 4)
        i = next(x for x in f["originals"] if x["repo_id"] == "illuin/Ivonnet-0.8B")
        self.assertEqual(set(i["trained_weight_paths"]), {"model.safetensors", "readout.safetensors"})
        self.assertFalse(f["source_selected_bytes_are_owner_incremental_bytes"])
        # This three-repo frozen source is a documented precursor and subset of the
        # independently merged four-model v68 source; IVE-4B is not deleted.
        merged = self.merged["publisher_source_aggregates"]
        self.assertEqual(merged["source_repos"], 4)
        self.assertEqual(merged["file_count"], 75)
        self.assertEqual(merged["source_bytes_without_dedup"], 17608061719)
        self.assertEqual(merged["publisher_hash_unique_bytes"], 17587985632)
        self.assertEqual({x["repo_id"] for x in self.merged["model_sources"]},
                         {"tencent/WeMM-Ecom-0.8B", "openbmb/MiniCPM5-2B",
                          "illuin/Ivonnet-0.8B", "illuin/IVE-4B"})

    def test_all_203_active_research_and_approval_stops(self):
        pairs = [
            (self.queue_before["candidates"], self.queue_after["candidates"], 203),
            (self.prep_before["items"], self.prep_after["items"], 203),
            (self.readiness_before["records"], self.readiness_after["records"], 203),
            (self.access_before["entries"], self.access_after["entries"], 147),
        ]
        for prior, after, count in pairs:
            self.assertEqual(after[:len(prior)], prior)
            self.assertEqual(len(after), count)
        ids = {x["repo_id"] for x in self.readiness_after["records"]}
        expected_active = {x["repo_id"] for x in self.after["items"]
                           if x["portfolio_decision"] in ("select", "conditional")}
        self.assertEqual(ids, expected_active)
        self.assertEqual(self.readiness_after["summary"]["blocked_any"], 203)
        self.assertEqual(self.readiness_after["summary"]["ready_to_approve"], 0)
        self.assertFalse(any(r["ready_to_acquire"] or r["download_approved"]
                             for r in self.readiness_after["records"]))
        self.assertFalse(any(r["download_authorized"] for r in self.access_after["entries"]))
        self.assertFalse(any(r["download_approved"] for r in self.queue_after["candidates"]))
        self.assertFalse(any(r["download_approved"] for r in self.prep_after["items"]))
        for new in self.readiness_after["records"][-4:]:
            self.assertIn("EXPLICIT_ACQUISITION_AUTHORIZATION", new["blocking_gates"])
            self.assertIn("OWNER_LOCAL_HASH_AND_OFFLINE_RESTORE", new["blocking_gates"])
            self.assertFalse(new["offline_restore_verified"])

    def test_ledger116_not_duplicated_and_no_authority_fabrication(self):
        self.assertEqual(self.ledger["summary"]["models_verified"], 116)
        self.assertEqual(self.ledger["summary"]["files_verified_total"], 1758)
        self.assertEqual(self.ledger["summary"]["bytes_verified_total"], 2021784002725)
        existing = {x["repo_id"] for x in self.ledger["models"] if x["status"] == "VERIFIED"}
        added = set(self.overlay["added_assets"])
        self.assertFalse(existing & added)
        self.assertEqual(self.current["expected"]["budget_scenario"]["v68_new_download_approval_bytes"], 0)
        self.assertFalse(self.current["latest_v68_small_decision_and_ecommerce"]["owner_D_SHA_rechecked"])
        self.assertEqual(self.current["latest_v68_small_decision_and_ecommerce"]["explicit_approvals_added"], 0)


if __name__ == "__main__":
    unittest.main()
