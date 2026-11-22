"""R153 offline metadata regressions; never downloads models or executes publisher code."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class R153Post112SelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = load("catalog/execution/2026-11-19-acquisition-ledger.json")
        cls.queue = load("queues/proposed-v64-r153-after112-next-originals-UNAPPROVED.json")
        cls.source = load("manifests/drafts/r153-2026-11-22-post112-five-distinct-origins-source-frozen.candidate.json")
        cls.current = load("catalog/CURRENT.json")
        cls.approved = load("queues/approved.json")

    def test_post99_acquisition_13_all_match_exact_scope(self):
        q = self.queue["reconciliation_99_to_112"]
        self.assertEqual(q["matched_new_models"], 13)
        self.assertEqual(q["matched_new_files"], 236)
        self.assertEqual(q["matched_new_bytes"], 140553833221)
        ledger_map = {r["repo_id"]: r for r in self.ledger["models"]}
        self.assertEqual(len(q["exclude_from_new_download"]), 13)
        seen = set()
        for r in q["exclude_from_new_download"]:
            self.assertNotIn(r["repo_id"], seen)
            seen.add(r["repo_id"])
            observed = ledger_map[r["repo_id"]]
            self.assertEqual(observed["status"], "VERIFIED")
            self.assertEqual(observed["revision_sha"], r["immutable_revision_sha"])
            self.assertEqual(observed["files_verified"], r["files_verified"])
            self.assertEqual(observed["source_bytes"], r["bytes_reported_verified"])
            self.assertFalse(r["owner_D_sha_independently_verified"])
        self.assertEqual(sum(x["files_verified"] for x in q["exclude_from_new_download"]), 236)
        self.assertEqual(sum(x["bytes_reported_verified"] for x in q["exclude_from_new_download"]), 140553833221)
        self.assertEqual(q["previous_bytes_verified"] + q["matched_new_bytes"], 2020548143087)

    def test_new_source_five_unique_publisher_trees(self):
        repos = self.source["source_repos"]
        self.assertEqual(len(repos), 5)
        self.assertEqual(sum(x["publisher_file_count"] for x in repos), 225)
        self.assertEqual(sum(x["publisher_bytes_full"] for x in repos), 3502502625)
        self.assertEqual(sum(x["publisher_LFS_refs_full"] for x in repos), 162)
        ids = set()
        for source in repos:
            self.assertNotIn(source["id"], ids)
            ids.add(source["id"])
            self.assertRegex(source["sha"], r"^[0-9a-f]{40}$")
            self.assertTrue(source["observed_ungated"])
            paths = {}
            for f in source["files"]:
                self.assertNotIn(f["path"], paths)
                paths[f["path"]] = f
                self.assertRegex(f["git_blob_sha1"], r"^[0-9a-f]{40}$")
                self.assertIsInstance(f["bytes"], int)
                self.assertGreaterEqual(f["bytes"], 0)
                if f["publisher_lfs_sha256"]:
                    self.assertRegex(f["publisher_lfs_sha256"], r"^[0-9a-f]{64}$")
                self.assertFalse(f["owner_local_sha_verified"])
            selected = source["selected_paths"]
            self.assertEqual(len(set(selected)), len(selected))
            self.assertTrue(set(selected) <= set(paths))
            self.assertEqual(source["selected_file_count"], len(selected))
            self.assertEqual(source["selected_bytes"], sum(paths[p]["bytes"] for p in selected))
            self.assertFalse(source["download_approved"])
            self.assertFalse(source["download_enabled"])
            self.assertFalse(source["owner_license_act_approved"])
            self.assertFalse(source["owner_local_SHA_verified"])

    def test_priority_de_dup_weights_and_native_components(self):
        src = {s["id"]: s for s in self.source["source_repos"]}
        n = src["nchapman/Qwen3.5-0.8B-Heretic-LoRA"]
        allfiles = {f["path"]: f for f in n["files"]}
        self.assertEqual(n["selected_file_count"], 12)
        self.assertEqual(n["selected_bytes"], 2031005)
        base = allfiles["adapter_model.safetensors"]["publisher_lfs_sha256"]
        self.assertEqual(base, allfiles["pareto/trial_002_ref4_kl0.0714/adapter_model.safetensors"]["publisher_lfs_sha256"])
        self.assertNotEqual(base, allfiles["pareto/trial_004_ref6_kl0.0275/adapter_model.safetensors"]["publisher_lfs_sha256"])
        self.assertNotIn("pareto/trial_002_ref4_kl0.0714/adapter_model.safetensors", n["selected_paths"])
        self.assertFalse(any(p.endswith(".gguf") for p in n["selected_paths"]))
        cart = src["GetCartwheelInc/cartwheel-control"]
        self.assertEqual(sorted(p for p in cart["selected_paths"] if p.endswith("policy.safetensors")),
                         ["asimov-1/policy.safetensors", "g1/policy.safetensors", "rp1/policy.safetensors"])
        primal = src["ostris/primal_vae"]
        self.assertEqual(len([p for p in primal["selected_paths"] if p.endswith(".safetensors")]), 3)
        self.assertIn("modeling_primal_vae.py", primal["selected_paths"])
        self.assertFalse(any(p.startswith("assets/") for p in primal["selected_paths"]))
        ling = src["inclusionAI/LingSante-Pulse-1.0"]
        self.assertIn("channels.npz", ling["selected_paths"])
        self.assertIn("model.safetensors", ling["selected_paths"])
        octen = src["Octen/Octen-WebGR-0.6B"]
        self.assertEqual(len([p for p in octen["selected_paths"] if p.startswith("sid_table/") and p.endswith(".parquet")]), 16)
        self.assertTrue(octen["decision"].startswith("HOLD"))

    def test_research_only_no_forged_authorization(self):
        self.assertEqual(self.approved["entries"], [])
        self.assertEqual(len(self.queue["priority_group"]), 4)
        self.assertEqual(self.queue["summary"]["fresh_priority_file_references"], 181)
        self.assertEqual(self.queue["summary"]["fresh_priority_publisher_source_bytes"], 1505197831)
        self.assertEqual(self.queue["summary"]["approved_file_scopes"], 0)
        self.assertFalse(self.queue["execution_controls"]["download_enabled"])
        self.assertFalse(self.source["rights_and_runtime"]["owner_signed_scope_authorization"])
        acquired = {r["repo_id"] for r in self.queue["reconciliation_99_to_112"]["exclude_from_new_download"]}
        proposed = {r["repo_id"] for r in self.queue["proposed_research_originals"]}
        self.assertFalse(proposed & acquired)
        self.assertFalse(any(r["download_enabled"] or r["download_approved"] for r in self.queue["proposed_research_originals"]))
        for r in self.queue["catalog_backfill_review_already_acquired_no_redownload"]:
            self.assertIn(r["repo_id"], acquired)

    def test_canonical_v64_unmodified_at_review(self):
        if self.current["revision_id"] != "v64-20261122":
            self.skipTest("R153 snapshot applies to the v64 canonical baseline")
        self.assertEqual(self.current["expected"]["tracked"], 236)
        self.assertEqual(self.current["expected"]["active"], 189)
        self.assertEqual(self.current["expected"]["by_decision"]["conditional"], 134)
        self.assertFalse(self.current["statuses"]["download_approved"])


if __name__ == "__main__":
    unittest.main()
