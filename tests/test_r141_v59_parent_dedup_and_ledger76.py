"""Offline invariant tests; never fetch model weights or execute remote inference code."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class V59ArchiveSourceIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = load("catalog/CURRENT.json")
        cls.old = load("catalog/effective-portfolio-2026-11-21-v58.json")
        cls.eff = load("catalog/effective-portfolio-2026-11-21-v59.json")
        cls.ov = load("catalog/revisions/v59-2026-11-21.json")
        cls.src = load("manifests/drafts/r139-2026-11-21-inkling-micro-edits-and-deepseek4b-varloop.candidate.json")
        cls.base = load("manifests/drafts/r137-2026-11-21-inkling2mini-and-dettato-four-publisher-sources.candidate.json")
        cls.phases = load("queues/proposed-v59-r140-ledger76-next-21-deduplicated-sources.json")
        cls.q = load("queues/proposed-v59-2026-11-21.json")
        cls.acc = load("catalog/access/2026-11-21-v59-conditional-hub-gates.json")
        cls.prep = load("catalog/preparation/2026-11-21-insurance-bundles-v59.json")
        cls.readiness = load("catalog/readiness/v59-2026-11-21-r139-all174-gates.json")

    def test_historical_v58_all_inherited_without_change(self):
        self.assertIn("catalog/revisions/v59-2026-11-21.json", self.c["ordered_overlays"])
        self.assertEqual(self.eff["revision_id"], "v59-20261121")
        self.assertEqual(self.eff["counts"]["tracked"], 221)
        self.assertEqual(self.eff["counts"]["active"], 174)
        self.assertEqual(self.eff["counts"]["models"], 195)
        self.assertEqual(self.eff["counts"]["datasets"], 26)
        self.assertEqual(self.eff["counts"]["by_decision"]["conditional"], 121)
        self.assertEqual(self.old["counts"]["tracked"], 218)
        self.assertEqual(self.old["counts"]["active"], 171)
        self.assertEqual(self.old["items"], self.eff["items"][:218])
        self.assertEqual(len({(x["asset_kind"], x["repo_id"]) for x in self.eff["items"]}), 221)
        self.assertEqual([x["repo_id"] for x in self.eff["items"][218:]], self.ov["added_assets"])
        latest = load(self.c["materialized_catalog_path"])
        self.assertEqual(latest["revision_id"], self.c["revision_id"])
        self.assertEqual(latest["counts"]["tracked"], self.c["expected"]["tracked"])
        self.assertEqual(latest["counts"]["active"], self.c["expected"]["active"])

    def test_source_scope_42_files_nontampered(self):
        m = self.src
        self.assertEqual(len(m["formal_conditional_proposed"]), 3)
        self.assertEqual(m["selected_active_files"], 42)
        self.assertEqual(m["selected_active_source_bytes"], 9_347_231_341)
        self.assertEqual(m["selected_research_hold_files"], 14)
        self.assertEqual(m["selected_research_hold_source_bytes"], 20_191_620_855)
        self.assertFalse(m["approvals"]["download_approved"])
        self.assertFalse(m["approvals"]["model_weights_transferred_this_review"])
        r = m["external_publisher_sources"]
        self.assertEqual(len(r), 4)
        for x in r:
            self.assertEqual(len(x["immutable_revision_sha"]), 40)
            self.assertFalse(x["source_access"]["gated"])
            self.assertFalse(x["source_access"]["private"])
            self.assertEqual(sum(f["bytes"] for f in x["selected_files"]), x["selected_source_bytes"])
            self.assertEqual(len(x["selected_files"]), x["selected_file_count"])
            self.assertEqual(len({f["path"] for f in x["selected_files"]}), len(x["selected_files"]))
            for f in x["selected_files"]:
                self.assertEqual(len(f["git_blob_sha1"]), 40)
                if f["publisher_lfs_sha256"]:
                    self.assertEqual(len(f["publisher_lfs_sha256"]), 64)
                self.assertFalse(f["owner_local_sha_verified"])

    def test_duplicate_main_inkling_files_excluded_without_unsafe_rewrite(self):
        m = self.src["parent_shared_exact_dedup"]
        self.assertEqual(m["excluded_matching_file_count"], 13)
        self.assertEqual(m["excluded_source_bytes"], 20_191_588_440)
        self.assertEqual(m["selected_unique_file_count"], 20)
        self.assertEqual(m["selected_unique_source_bytes"], 1_190_518)
        self.assertFalse(m["physical_owner_parent_sha_reverified"])
        base = next(x for x in self.base["publisher_original_sources"]
                    if x["repo_id"] == "thinkingmachines/Inkling-2-Mini")
        seen = {f["path"]: f for f in base["files"]}
        for f in m["excluded_matching_upstream_files"]:
            old = seen[f["path"]]
            self.assertEqual(old["bytes"], f["bytes"])
            self.assertEqual(old["git_blob_sha1"], f["git_blob_sha1"])
            self.assertEqual(old["publisher_lfs_sha256"], f["publisher_lfs_sha256"])
        self.assertEqual(m["parent_revision"], base["immutable_revision_sha"])
        for x in self.ov["additions"]:
            self.assertFalse(x["download_approved"])
            self.assertLess(x["parameter_gate"]["total_parameters"], 150_000_000_000)
        self.assertNotIn(self.src["research_hold_proposed"],
                         {x["repo_id"] for x in self.eff["items"]})

    def test_four_b_mtp_and_tiny_edit_tensor_counts(self):
        x = self.src["conservative_parameter_evidence"]
        self.assertEqual(x["standalone_4B_parameters_including_MTP"], 4_539_265_536)
        self.assertEqual(x["standalone_4B_MTP_elements"], 120_599_552)
        self.assertEqual(x["standalone_4B_MTP_tensors"], 15)
        self.assertEqual(x["inkling_ingine_edit_F32_elements"], 221_280)
        self.assertEqual(x["inkling_openuncensored_LORA_F32_elements"], 215_040)
        src = {r["repo_id"]: r for r in self.src["external_publisher_sources"]}
        self.assertEqual(src["aaaaygd/DeepSeek-V4-Pro-Qwen3.5-4B-UNCENSORED-heretic"]["selected_source_bytes"], 9_345_162_884)
        self.assertEqual(src["OpenUncensored/Inkling-2-Mini-Uncensored-LoRA"]["selected_source_bytes"], 877_939)

    def test_updated_source_ledger76_and_sha_reuse(self):
        q = self.phases
        self.assertEqual(q["total_source_repos"], 21)
        self.assertEqual(q["total_source_file_references"], 324)
        self.assertEqual(q["total_publisher_reference_bytes"], 223_837_135_371)
        self.assertEqual(q["publisher_distinct_LFS_sha256_files"], 70)
        self.assertEqual(q["publisher_duplicate_LFS_sha256_file_instances"], 1)
        self.assertEqual(q["potential_dedup_by_byte_after_owner_local_hash_check"], 19_989_339)
        self.assertEqual(q["near_term_without_P3_large_hold_bytes"], 94_264_245_398)
        self.assertEqual(q["reported_existing"]["model_count"], 76)
        self.assertEqual(len({x["repo_id"] for x in q["source_entries"]}), 21)
        self.assertEqual(sum(x["publisher_source_selected_files"] for x in q["source_entries"]), 324)
        self.assertEqual(sum(x["publisher_source_selected_bytes"] for x in q["source_entries"]), 223_837_135_371)
        self.assertFalse(q["download_controls"]["approved"])
        self.assertFalse(q["download_controls"]["download_enabled"])
        self.assertEqual(q["download_controls"]["approved_queue_entries"], 0)

    def test_readiness_and_legal_stops_still_fail_closed(self):
        self.assertEqual(len(self.q["candidates"]), 174)
        self.assertEqual(len(self.acc["entries"]), 121)
        self.assertEqual(len(self.prep["items"]), 174)
        self.assertEqual(len(self.readiness["records"]), 174)
        self.assertEqual(self.readiness["summary"]["ready_to_approve"], 0)
        self.assertEqual(self.readiness["summary"]["blocked_any"], 174)
        self.assertEqual(self.readiness["summary"]["downloads_approved"], 0)
        self.assertFalse(self.q["approved"])
        self.assertFalse(self.q["download_enabled"])
        self.assertFalse(self.readiness["download_approved"])
        self.assertFalse(self.readiness["ready_to_acquire"])
        self.assertEqual(load("queues/approved.json")["entries"], [])
        for item in self.ov["additions"]:
            row = next(z for z in self.readiness["records"] if z["repo_id"] == item["repo_id"])
            self.assertFalse(row["download_approved"])
            self.assertFalse(row["ready_to_acquire"])
            self.assertFalse(row["local_sha_verified"])
            self.assertFalse(row["offline_restore_verified"])


if __name__ == "__main__":
    unittest.main()
