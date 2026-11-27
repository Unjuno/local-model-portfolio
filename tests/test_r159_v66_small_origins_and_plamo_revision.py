"""R159 metadata-only offline source regression. Does not load weights or invoke remote network."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


from scripts.ledger_history_r168 import historical_117_ledger

class R159SourceAndRightsRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read("manifests/drafts/r159-2026-11-24-wemm-ecom-plamo-ernie-immutable-sources.candidate.json")
        cls.queue = read("queues/proposed-v66-r159-post116-edge-UNAPPROVED.json")
        cls.decision = read("catalog/decisions/2026-11-24-r159-compact-models-plamo-drift-and-ernie-hold.json")
        cls.current = read("catalog/CURRENT.json")
        cls.approved = read("queues/approved.json")
        cls.ledger = historical_117_ledger(read("catalog/execution/2026-11-19-acquisition-ledger.json"))

    def test_six_immutable_publisher_source_scopes(self):
        source = self.source
        self.assertEqual(len(source["publisher_sources"]), 6)
        self.assertEqual(source["statistics"]["full_file_count"], 229)
        self.assertEqual(source["statistics"]["full_publisher_reference_bytes"], 184714085822)
        self.assertEqual(source["statistics"]["full_lfs_sha256_references"], 159)
        expected = {
            "tencent/WeMM-Ecom-0.8B": (20, 1733044450, 8),
            "openbmb/MiniCPM5-2B": (11, 5043807977, 1),
            "pfnet/plamo-3-translate-0.8b": (16, 1785590177, 3),
            "tencent/WeMM-Ecom-2B": (22, 4453620451, 10),
            "pfnet/plamo-3-translate-2b": (18, 5762122137, 4),
            "baidu/ERNIE-5.5-Flash-Preview": (142, 165935900630, 133),
        }
        actual = {}
        for source_repo in source["publisher_sources"]:
            model_id = source_repo["id"]
            self.assertNotIn(model_id, actual)
            self.assertRegex(source_repo["rev"], r"^[a-f0-9]{40}$")
            paths = [f["path"] for f in source_repo["files"]]
            self.assertEqual(len(paths), len(set(paths)))
            files = source_repo["files"]
            self.assertEqual(sum(f["bytes"] for f in files), source_repo["publisher_full_bytes"])
            self.assertEqual(sum(bool(f["publisher_lfs_sha256"]) for f in files), source_repo["publisher_lfs_sha256_refs"])
            for f in files:
                self.assertGreaterEqual(f["bytes"], 0)
                self.assertRegex(f["git_blob_sha1"], r"^[a-f0-9]{40}$")
                if f["publisher_lfs_sha256"]:
                    self.assertRegex(f["publisher_lfs_sha256"], r"^[a-f0-9]{64}$")
                self.assertFalse(f["owner_SHA_verified"])
            actual[model_id] = (len(files), source_repo["publisher_full_bytes"], source_repo["publisher_lfs_sha256_refs"])
            self.assertFalse(source_repo["download_approved"])
            self.assertFalse(source_repo["owner_current_SHA_verified"])
            self.assertFalse(source_repo["owner_individual_license_acts_reviewed"])
            self.assertFalse(source_repo["complete_offline_reproduction_verified"])
        self.assertEqual(actual, expected)

    def test_next_two_not_duplicate_quantization_repos(self):
        self.assertEqual(self.source["statistics"]["new_originals_recommended_count"], 2)
        self.assertEqual(self.source["statistics"]["new_originals_recommended_full_files"], 31)
        self.assertEqual(self.source["statistics"]["new_originals_recommended_full_publisher_bytes"], 6776852427)
        expected = {"tencent/WeMM-Ecom-0.8B", "openbmb/MiniCPM5-2B"}
        self.assertEqual(set(self.source["statistics"]["new_originals_recommended"]), expected)
        selected = self.queue["proposed_new_originals"]
        self.assertEqual({r["repo_id"] for r in selected}, expected)
        self.assertFalse(any("-GGUF" in x["repo_id"] or "-FP8" in x["repo_id"] for x in selected))
        already_reported = {r["repo_id"] for r in self.ledger["models"] if r["status"] == "VERIFIED"}
        self.assertTrue(expected.isdisjoint(already_reported))
        for r in selected:
            self.assertFalse(r["download_approved"])
            self.assertFalse(r["download_enabled"])

    def test_plamo_is_existing_catalog_and_nonweight_revision_drift(self):
        p = self.source["existing_plamo_0p8b_revision_audit"]
        self.assertEqual(p["archived_frozen_revision"], "cc8e88169807d5a272e8ff06db12eb0129b67f81")
        self.assertEqual(p["new_public_revision"], "c5a33c561bc6a4fbac38c3460bbb384e15c0b231")
        self.assertEqual(p["archived_full_bytes"], 1785576024)
        self.assertEqual(p["current_full_bytes"], 1785590177)
        self.assertEqual(p["archived_full_file_count"], 16)
        self.assertEqual(p["current_full_file_count"], 16)
        self.assertEqual(len(p["modified_nonweight_files"]), 5)
        changes = {x["path"] for x in p["modified_nonweight_files"]}
        self.assertEqual(changes, {"LICENSE/en", "LICENSE/ja", "README.md", "README_ja.md", "chat_template.jinja"})
        self.assertNotIn("model.safetensors", changes)
        self.assertEqual(p["unchanged_learned_model_weight"]["sha256"],
                         "7c9f0066d166c075bdbe83ada3d444e08bd7a6ee3f345f47a1f3c442aa6898c5")
        r24 = read("catalog/revisions/v24-2026-11-06.json")
        self.assertIn("pfnet/plamo-3-translate-0.8b", [x["repo_id"] for x in r24["additions"]])
        self.assertFalse(p["user_license_review"])
        self.assertTrue(p["new_revision_change_conclusion"].startswith("WEIGHT_IDENTICAL"))
        self.assertEqual(self.decision["already_selected_no_new_asset"]["not_silent_repin"], True)

    def test_ernie_over150b_not_approved_as_ram_equivalent(self):
        e = self.decision["new_earnies_280b_constraints"]
        self.assertEqual(e["publisher_declared_total_parameters"], 280000000000)
        self.assertEqual(e["hub_safetensors_stored_elements"], 299559241286)
        self.assertGreater(e["publisher_declared_total_parameters"], 150000000000)
        self.assertTrue(e["exception_unverified"])
        self.assertEqual(e["required_matched_ram_trials_min"], 30)
        self.assertIs(e["estimated_usable_RAM_at_context_and_batch_unknown"], True)
        entry = next(x for x in self.queue["research_holds"] if x["repo_id"] == e["repo_id"])
        self.assertFalse(entry["download_enabled"])
        self.assertEqual(entry["frozen_full_source_file_count"], 142)

    def test_ledger_and_approval_gates_unchanged(self):
        self.assertEqual(self.approved["entries"], [])
        self.assertEqual(self.ledger["summary"]["models_verified"], 116)
        self.assertEqual(self.ledger["summary"]["files_verified_total"], 1758)
        self.assertEqual(self.ledger["summary"]["bytes_verified_total"], 2021784002725)
        self.assertEqual(self.decision["formal_catalog_additions"], 0)
        self.assertEqual(self.decision["download_authorizations"], 0)
        self.assertEqual(self.decision["new_weight_payload_transferred"], 0)
        self.assertFalse(self.queue["mandatory_gates"]["download_enabled"])
        self.assertFalse(self.queue["mandatory_gates"]["explicit_owner_file_scope_approval"])
        self.assertFalse(self.queue["mandatory_gates"]["owner_local_file_SHA_verified"])
        self.assertFalse(self.queue["mandatory_gates"]["legal_per_user_intended_act"])
        if self.current["revision_id"] == "v66-20261124":
            self.assertEqual(self.current["expected"]["tracked"], 246)
            self.assertEqual(self.current["expected"]["active"], 197)
            self.assertFalse(self.current["statuses"]["download_approved"])


if __name__ == "__main__":
    unittest.main()
