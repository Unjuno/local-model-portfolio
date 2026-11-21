"""R149: live-source adjudication of the post-99 queue, with zero implicit approvals.

Read-only regression test; it never downloads model weights or executes model code.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class R149Post99SourceAdjudication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = read_json("catalog/CURRENT.json")
        cls.catalog = read_json("catalog/effective-portfolio-2026-11-22-v63.json")
        cls.queue = read_json("queues/proposed-v63-r149-after99-11-research-only.json")
        cls.study = read_json("catalog/decisions/2026-11-22-r149-v63-next11-source-adjudication.json")
        cls.ledger = read_json("catalog/execution/2026-11-19-acquisition-ledger.json")
        cls.approvals = read_json("queues/approved.json")

    def test_v63_canonical_selection_remains_unchanged(self):
        self.assertEqual(self.current["revision_id"], "v63-20261122")
        self.assertEqual(self.study["current_catalog_revision"], "v63-20261122")
        self.assertFalse(self.study["canonical_catalog_changed"])
        self.assertEqual(self.catalog["counts"]["tracked"], 235)
        self.assertEqual(self.catalog["counts"]["active"], 188)
        self.assertEqual(self.catalog["counts"]["by_decision"]["select"], 55)
        self.assertEqual(self.catalog["counts"]["by_decision"]["conditional"], 133)
        self.assertEqual(len(self.approvals["entries"]), 0)

    def test_all_eleven_research_candidates_exact_and_not_downloadable(self):
        q = self.queue["candidate_research_only"]
        d = self.study["candidate_decisions"]
        self.assertEqual(len(q), 11)
        self.assertEqual(len(d), 11)
        self.assertEqual(len({x["repo_id"] for x in d}), 11)
        self.assertEqual([x["repo_id"] for x in d], [x["repo_id"] for x in q])
        acquired = {x["repo_id"] for x in self.ledger["models"] if x["status"] == "VERIFIED"}
        self.assertEqual(len(acquired), 99)
        for s, c in zip(q, d):
            self.assertNotIn(c["repo_id"], acquired)
            self.assertEqual(c["phase"], s["phase"])
            self.assertEqual(c["immutable_revision_sha"], s["publisher_revision_sha"])
            self.assertEqual(len(c["immutable_revision_sha"]), 40)
            self.assertEqual(c["selected_files"], s["selected_file_count"])
            self.assertEqual(c["publisher_reference_bytes"], s["publisher_reference_bytes"])
            self.assertEqual(c["existing_source_manifest"], s["source_manifest"])
            self.assertTrue((ROOT / c["existing_source_manifest"]).is_file())
            self.assertFalse(s["download_approved"])
            self.assertFalse(s["download_enabled"])
            self.assertFalse(c["download_approved"])
            self.assertFalse(c["download_enabled"])
            self.assertFalse(c["owner_explicit_per_source_approval_present"])
            self.assertFalse(c["owner_specific_license_acts_reviewed"])
            self.assertFalse(c["complete_offline_restore_verified"])
            self.assertFalse(c["user_owner_independent_local_hash_checked"])

    def test_byte_totals_held_large_and_dependencies_are_distinct(self):
        expected = {
            "P0_SMALL_ORIGINALS_AND_EDGE": 2234744280,
            "P1_SPECIALIZED_AND_UNCENSORED_PARENTS": 11871408047,
            "P2_MID_SPECIALIZED_ABI_REVIEW": 54438018606,
            "P3_LARGE_RESEARCH_HOLD": 129572889973,
        }
        candidates = self.study["candidate_decisions"]
        self.assertEqual(self.study["candidate_model_count"], 11)
        self.assertEqual(self.study["source_reference_bytes_by_phase"]["P0"], expected["P0_SMALL_ORIGINALS_AND_EDGE"])
        self.assertEqual(self.study["source_reference_bytes_by_phase"]["P1"], expected["P1_SPECIALIZED_AND_UNCENSORED_PARENTS"])
        self.assertEqual(self.study["source_reference_bytes_by_phase"]["P2"], expected["P2_MID_SPECIALIZED_ABI_REVIEW"])
        self.assertEqual(self.study["source_reference_bytes_by_phase"]["P3_HOLD"], expected["P3_LARGE_RESEARCH_HOLD"])
        for phase, amount in expected.items():
            self.assertEqual(sum(x["publisher_reference_bytes"] for x in candidates if x["phase"] == phase), amount)
        self.assertEqual(sum(x["publisher_reference_bytes"] for x in candidates if x["phase"] != "P3_LARGE_RESEARCH_HOLD"), 68544170933)
        self.assertEqual(self.study["additional_apple_parent_reference_bytes"], 17567235949)
        self.assertEqual(self.study["additional_cactus_runtime_reference_bytes"], 4137947)
        self.assertIsNone(self.study["actual_incremental_transfer_bytes_verified"])
        ripple = [x for x in candidates if x["repo_id"] == "ricursiveAI/Ripple-65B-Preview"]
        self.assertEqual(len(ripple), 1)
        self.assertIn("HOLD", ripple[0]["selection_reaffirmed"])
        self.assertEqual(self.study["additional_discovered_candidate_hold"]["repo_id"], "KittenML/kitten-tts-2-nano")
        self.assertNotIn("KittenML/kitten-tts-2-nano", {x["repo_id"] for x in self.catalog["items"]})

    def test_rights_hdd_and_execution_never_silently_pass(self):
        self.assertFalse(self.study["physical_owner_drive_rehashed_this_study"])
        self.assertEqual(self.study["new_model_selected"], 0)
        self.assertEqual(self.study["new_bytes_downloaded_by_this_work"], 0)
        self.assertEqual(self.study["owner_approval_entries_added"], 0)
        self.assertFalse(self.study["owner_D_files_modified"])
        for x in self.study["candidate_decisions"]:
            self.assertNotEqual(x["verification_level"], "OWNER_LOCAL_SHA_VERIFIED")

if __name__ == "__main__":
    unittest.main()
