"""Offline invariant checks for R134/R135 research-only publisher sources.

This test never contacts Hugging Face, opens weights, or executes model code.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class R135SourceAndLedgerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = load("queues/proposed-v57-r135-ledger66-next-deduplicated-sources.json")
        cls.manifest = load("manifests/drafts/r134-2026-11-20-rikiya08b-mellum-mtp-ripple65b.candidate.json")
        cls.ledger = load("catalog/execution/2026-11-19-acquisition-ledger.json")
        cls.approvals = load("queues/approved.json")
        cls.old = load("catalog/effective-portfolio-2026-11-20-v57.json")

    def test_frozen_three_sources_exact(self):
        m = self.manifest
        self.assertEqual(m["source_repository_count"], 3)
        self.assertEqual(m["publisher_source_file_count"], 66)
        self.assertEqual(m["publisher_source_bytes"], 156_517_459_653)
        self.assertEqual(m["publisher_LFS_SHA256_file_count"], 25)
        self.assertFalse(m["policy"]["approved"])
        self.assertFalse(m["policy"]["download_enabled"])
        for rec in m["sources"]:
            self.assertEqual(len(rec["revision_sha"]), 40)
            self.assertEqual(len(rec["files"]), rec["source_file_count"])
            self.assertEqual(sum(f["bytes"] for f in rec["files"]), rec["source_selected_bytes"])
            self.assertEqual(len({f["path"] for f in rec["files"]}), len(rec["files"]))
            self.assertTrue(all(not f["local_sha256_verified"] for f in rec["files"]))
            self.assertFalse(rec["download_approved"])

    def test_mellum_mtp_only_no_second_main(self):
        m = self.manifest["cross_revision_deduplication"]["JetBrains_Mellum2_1"]
        self.assertTrue(m["five_main_weight_shards_identical_SHA256"])
        self.assertEqual(m["base_main_safetensors_parameters"], 12_149_923_072)
        self.assertEqual(m["mtp_header_BF16_elements"], 428_371_456)
        self.assertEqual(m["mtp_header_tensor_count"], 205)
        self.assertEqual(m["total_model_parameters_including_mtp"], 12_578_294_528)
        self.assertLess(m["total_model_parameters_including_mtp"], 150_000_000_000)
        ids = [x["repo_id"] for x in self.queue["entries"]]
        self.assertIn("JetBrains/Mellum2.1-12B-A2.5B-Thinking-MTP", ids)
        self.assertNotIn(m["original_non_mtp_repo"], ids)

    def test_66_report_and_qwen_parent_not_retransferred(self):
        ledger = {x["repo_id"]: x for x in self.ledger["models"]}
        self.assertGreaterEqual(self.ledger["summary"]["models_verified"], 66)
        parent = ledger["Qwen/Qwen3.8-27B"]
        self.assertEqual(parent["revision_sha"], "37561816e66b5b9153b1b64c10968c18c1e6f4a0")
        self.assertEqual(parent["status"], "VERIFIED")
        self.assertEqual(len([f for f in parent["weight_files_sha256"]
                              if f["path"].endswith(".safetensors")]), 18)
        self.assertEqual(ledger["maya-research/maya2-native"]["status"], "VERIFIED")
        all_ids = {x["repo_id"] for x in self.queue["entries"]}
        for old in self.ledger["models"]:
            if old["status"] == "VERIFIED":
                self.assertNotIn(old["repo_id"], all_ids)
        self.assertEqual(self.queue["report66"]["already_reported_Qwen_parent"]["revision_sha"],
                         parent["revision_sha"])

    def test_phased_source_and_legal_stops(self):
        q = self.queue
        self.assertEqual(q["selected_source_repo_count"], 13)
        self.assertEqual(q["selected_source_files"], 243)
        self.assertEqual(q["selected_source_bytes_upper_if_every_source_absent"], 194_177_794_162)
        self.assertEqual(q["phase_summary"]["P0_PARENT_REUSE"]["bytes"], 486_825_520)
        self.assertEqual(q["phase_summary"]["P3_LARGE_DEFER"]["bytes"], 129_572_889_973)
        self.assertEqual(q["distinct_publisher_lfs_sha256_refs"], 48)
        self.assertFalse(q["approved"])
        self.assertFalse(q["download_enabled"])
        self.assertEqual(self.approvals["entries"], [])
        self.assertEqual(len({r["repo_id"] for r in q["entries"]}), 13)
        self.assertEqual(sum(r["publisher_selected_file_count"] for r in q["entries"]), 243)
        self.assertEqual(sum(r["publisher_selected_source_bytes"] for r in q["entries"]), 194_177_794_162)
        for rec in q["entries"]:
            self.assertFalse(rec["download_approved"])
            self.assertFalse(rec["download_enabled"])
            self.assertFalse(rec["individual_rights_approved"])
            self.assertFalse(rec["owner_HDD_SHA_checked"])
            self.assertEqual(sum(f["bytes"] for f in rec["selected_source_files"]),
                             rec["publisher_selected_source_bytes"])

    def test_v57_not_mutated_by_source_only_research(self):
        self.assertEqual(self.old["counts"]["tracked"], 213)
        self.assertEqual(self.old["counts"]["active"], 166)
        original = {x["repo_id"] for x in self.old["items"]}
        for x in self.manifest["sources"]:
            self.assertNotIn(x["repo_id"], original)

if __name__ == "__main__":
    unittest.main()
