"""R151: immutable Publisher scope consistency, never a transfer or owner approval.

Offline, stdlib-only tests: no model weights, network calls, custom model imports,
GPU work, third-party executable launch, or mutation of the owner archive.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class R151UnifiedSourceReadOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = load("queues/proposed-v63-r151-unified-15-research-scopes-UNAPPROVED.json")
        cls.d = load("catalog/decisions/2026-11-22-r151-v63-unified-source-and-license-adjudication.json")

    def test_canonical_v63_unchanged_and_no_synthetic_authorization(self):
        current = load("catalog/CURRENT.json")
        self.assertIn(current["revision_id"], ("v63-20261122", "v64-20261122","v65-20261122", "v66-20261124", "v67-20261124","v68-20261125","v69-20261125","v70-20261125", "v71-20261125"))
        historical=load("catalog/effective-portfolio-2026-11-22-v63.json"); self.assertEqual((historical["counts"]["tracked"], historical["counts"]["active"]), (235, 188))
        self.assertEqual(load("queues/approved.json")["entries"], [])
        self.assertEqual(self.q["source_scope_count"], 15)
        self.assertEqual(self.q["new_provisional_research_source_scopes_not_in_catalog"], 4)
        self.assertEqual(self.q["nonhold_research_source_scopes"], 14)
        self.assertEqual(self.q["nonhold_publisher_source_reference_bytes"], 128580722021)
        self.assertFalse(self.q["approval_controls"]["download_enabled"])
        self.assertEqual(self.q["approval_controls"]["approved_downloads"], 0)
        self.assertEqual(self.d["approved_queue_entries_remain"], 0)
        self.assertEqual(self.d["formal_additions_executed"], 0)
        self.assertFalse(self.d["owner_hdd_sha_verified"])

    def test_six_first_exact_file_scopes_agree_with_immutable_manifests(self):
        q = self.q["first_six_frozen_source_owner_review"]
        self.assertEqual(q["repos"], 6)
        self.assertEqual((q["selected_files"], q["publisher_reference_bytes"], q["lfs_sha_refs"]),
                         (214, 2559656195, 160))
        items = q["selected_models"]
        self.assertEqual(len(items), 6)
        self.assertEqual(len({e["repo_id"] for e in items}), 6)
        total_files = total_bytes = total_lfs = 0
        for e in items:
            manifest = load(e["src"])
            sections = (manifest.get("model_repos")
                        or manifest.get("publisher_sources")
                        or manifest.get("source_repos"))
            src = next(x for x in sections if x["repo_id"] == e["repo_id"])
            rev = (src.get("revision_sha") or src.get("immutable_revision_sha") or src.get("sha"))
            files = (src.get("selected_files") or src.get("publisher_selected_files")
                     or src.get("files"))
            self.assertRegex(rev, r"^[0-9a-f]{40}$")
            self.assertEqual(rev, e["revision"])
            self.assertEqual(len(files), e["n"])
            self.assertEqual(len({f["path"] for f in files}), len(files))
            self.assertEqual(sum(f["bytes"] for f in files), e["bytes"])
            self.assertEqual(sum(bool(f.get("publisher_lfs_sha256")) for f in files), e["lfs"])
            for f in files:
                self.assertRegex(f["git_blob_sha1"], r"^[0-9a-f]{40}$")
                if f.get("publisher_lfs_sha256"):
                    self.assertRegex(f["publisher_lfs_sha256"], r"^[0-9a-f]{64}$")
            for flag in ("owner_license_act_reviewed", "local_SHA_checked", "download_approved",
                         "download_enabled", "full_offline_restore_verified"):
                self.assertIs(e[flag], False, (e["repo_id"], flag))
            total_files += len(files)
            total_bytes += sum(f["bytes"] for f in files)
            total_lfs += sum(bool(f.get("publisher_lfs_sha256")) for f in files)
        self.assertEqual((total_files, total_bytes, total_lfs), (214, 2559656195, 160))
        self.assertEqual(self.d["first_six_source_metadata_validation"]["files"], 214)

    def test_fifteen_sources_one_repo_id_each_and_four_new_not_in_canonical(self):
        rows = self.q["first_six_frozen_source_owner_review"]["selected_models"] + (
            self.q["remaining_frozen_research_source_scopes"])
        self.assertEqual(len(rows), 15)
        self.assertEqual(len({x["repo_id"] for x in rows}), 15)
        self.assertEqual(len(self.d["source_pinned_new_four"]), 4)
        self.assertEqual(
            sum(x["source_bytes"] for x in self.d["source_pinned_new_four"]), 60036551088)
        for r in self.d["source_pinned_new_four"]:
            self.assertFalse(r["owner_license_verified"])
            self.assertRegex(r["pinned_sha"], r"^[0-9a-f]{40}$")
        self.assertEqual(self.d["large_Ripple_65B_research_hold_bytes"], 129572889973)

    def test_pico_qad_corrected_and_quantization_not_autoclassified(self):
        scope = load("manifests/drafts/r150-2026-11-22-kitten-pico-int8-qad-source-delta.candidate.json")
        self.assertEqual(len(scope["additional_int8_files"]), 8)
        self.assertEqual(scope["additional_publisher_reference_bytes"], 63628208)
        self.assertEqual(scope["proposed_selected_publisher_reference_bytes"], 349508085)
        self.assertTrue(all(not f["final_source_lock_ready"] for f in scope["additional_int8_files"]))
        self.assertEqual(scope["publisher_int8_weight_sha256_refs_observed"], 0)
        self.assertEqual(self.d["corrections_to_older_R150_first_four"]["additional_bytes"], 63628208)
        first_four = load("queues/proposed-v63-r150-first-four-UNAPPROVED.json")
        self.assertEqual(first_four["review_scope"]["publisher_reference_bytes"], 2234744280)
        self.assertFalse(first_four["review_scope"]["is_complete_training_outcome_archive"])
        self.assertEqual(first_four["review_scope"]["Pico_INT8_QAD_source_bytes_outside_locked_scope"], 63628208)

    def test_small_heretic_lo_ra_and_licensed_large_tts_remain_research_only(self):
        source = load("manifests/drafts/r150-2026-11-22-qwen0p8b-heretic-lora-two-unique-weights.candidate.json")
        self.assertEqual(len(source["unique_trained_source_weights"]), 2)
        self.assertEqual(source["raw_unique_safetensors_bytes"], 2006488)
        self.assertFalse(source["candidate_selected_source_bundle_ready"])
        self.assertFalse(source["download_approved"])
        self.assertFalse(self.d["next_frozen_source_task"]["entire_immutable_tree_frozen"])
        self.assertEqual(self.d["Kitten_1_7B_tts_hold"]["model_weights_license"],
                         "Stellon Labs Community License")
        self.assertTrue(self.d["Kitten_1_7B_tts_hold"]["code_license_not_equal_to_weight_license"])
        self.assertFalse(self.d["Kitten_1_7B_tts_hold"]["download_approved"])


if __name__ == "__main__":
    unittest.main()
