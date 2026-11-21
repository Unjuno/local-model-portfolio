"""Offline guards for pinned Bison/Groundhog original source selection."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalog/research/2026-11-22-baselabs-bison-groundhog-immutable-source-selection.json"


class TestPublisherComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_exact_full_source_and_unique_file_ids(self):
        d = self.data
        self.assertEqual(d["approved_downloads_added"], 0)
        self.assertFalse(d["model_payload_downloaded"])
        self.assertFalse(d["runtime_code_execution"])
        self.assertEqual(d["new_canonical_additions"], 0)
        self.assertEqual(d["canonical_on_observation"], "v63-20261122")
        models = {m["repo_id"]: m for m in d["publisher_sources"]}
        self.assertEqual(set(models), {"baselabs/bison-1", "baselabs/groundhog-1"})
        expected = {
            "baselabs/bison-1": (65398108261, 31273086512, "bf8350b2c59eb6c36e95d02a2af870aec18724a7"),
            "baselabs/groundhog-1": (53120939617, 25805933872, "f4602c43599114a7af2c158472b59a4ff2d13663"),
        }
        for repo_id, (bytes_expected, parameters_expected, sha_expected) in expected.items():
            m = models[repo_id]
            self.assertEqual((m["all_repo_bytes"], m["total_parameters"], m["revision_sha"]),
                             (bytes_expected, parameters_expected, sha_expected))
            self.assertEqual(len(m["publisher_files"]), 16)
            self.assertEqual(len({f["path"] for f in m["publisher_files"]}), 16)
            self.assertEqual(sum(f["bytes"] for f in m["publisher_files"]), bytes_expected)
            self.assertEqual(m["lfs_sha_count"], 4)
            self.assertEqual(sum(f["publisher_lfs_sha256"] is not None for f in m["publisher_files"]), 4)
            self.assertTrue(m["public_ungated_observed"])
            self.assertFalse(m["owner_rights_approved"])
            self.assertFalse(m["download_approved"])
            for f in m["publisher_files"]:
                self.assertTrue(re.fullmatch(r"[a-f0-9]{40}", f["git_blob_sha1"]))
                if f["publisher_lfs_sha256"]:
                    self.assertTrue(re.fullmatch(r"[a-f0-9]{64}", f["publisher_lfs_sha256"]))
                self.assertFalse(f["owner_local_sha_verified"])

    def test_rank_one_avoid_parallel_65_and_53GB_downloads(self):
        d = self.data
        self.assertEqual(d["technical_decision"]["prioritize_for_next_formal_conditional_selection"],
                         "baselabs/bison-1")
        self.assertEqual(d["technical_decision"]["retained_research_alternative"], "baselabs/groundhog-1")
        self.assertTrue(d["technical_decision"]["do_not_acquire_both_without_paired_evidence"])
        self.assertEqual(d["source_total_bytes_before_cross_repo_dedup"], 118519047878)


if __name__ == "__main__":
    unittest.main()
