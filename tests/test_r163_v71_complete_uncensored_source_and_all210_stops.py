"""R163 v71: offline JSON-only publisher provenance and zero-authority regression.

Run: python -m unittest discover -s tests -p 'test_r163_v71_complete_uncensored_source_and_all210_stops.py'
This test never imports model-distributed source code, touches a user HDD, or downloads weights.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class R163V71FullSourceAndStop(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cur = read("catalog/CURRENT.json")
        cls.before = read("catalog/effective-portfolio-2026-11-25-v70.json")
        cls.after = read("catalog/effective-portfolio-2026-11-25-v71.json")
        cls.overlay = read("catalog/revisions/v71-2026-11-25.json")
        cls.freeze = read("manifests/drafts/r163-2026-11-25-five-uncensored-source-complete-publisher-OID-SHA.candidate.json")
        cls.partial = read("manifests/drafts/r162-2026-11-25-new-uncensored-and-decision-partial-publisher-sha-RESEARCH.candidate.json")
        cls.old_queue = read("queues/proposed-v70-2026-11-25.json")
        cls.queue = read("queues/proposed-v71-2026-11-25.json")
        cls.old_prep = read("catalog/preparation/2026-11-25-insurance-bundles-v70.json")
        cls.prep = read("catalog/preparation/2026-11-25-insurance-bundles-v71.json")
        cls.old_access = read("catalog/access/2026-11-25-v70-conditional-hub-gates.json")
        cls.access = read("catalog/access/2026-11-25-v71-conditional-hub-gates.json")
        cls.old_readiness = read("catalog/readiness/v70-2026-11-25-r161-all208-gates.json")
        cls.readiness = read("catalog/readiness/v71-2026-11-25-r163-all210-gates.json")
        cls.approved = read("queues/approved.json")
        cls.ledger = read("catalog/execution/2026-11-19-acquisition-ledger.json")
        cls.r163queue = read("queues/proposed-v71-r163-next2-uncensored-full-source-UNAPPROVED.json")

    def test_v70_all258_records_preserved_and_current_v71(self) -> None:
        self.assertEqual(self.before["revision_id"], "v70-20261125")
        self.assertEqual(self.after["revision_id"], "v71-20261125")
        self.assertEqual(len(self.before["items"]), 258)
        self.assertEqual(len(self.after["items"]), 260)
        self.assertEqual(self.before["items"], self.after["items"][:258])
        self.assertEqual(self.overlay["previous_asset_count"], 258)
        self.assertEqual(self.overlay["additions"], self.after["items"][-2:])
        self.assertEqual(self.overlay["added_assets"], ["2Beyes/Aurum-2B-Uncensored",
                                                        "AnkitNayak-dev/QJev-1.5B-Abliterated"])
        self.assertEqual(self.overlay["removed_assets"], [])
        self.assertEqual(self.overlay["changed_prior_decisions"], [])
        ids = [(x["asset_kind"], x["repo_id"]) for x in self.after["items"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.after["counts"]["tracked"], 260)
        self.assertEqual(self.after["counts"]["active"], 210)
        self.assertEqual(self.after["counts"]["models"], 234)
        self.assertEqual(self.after["counts"]["datasets"], 26)
        self.assertEqual(self.after["counts"]["by_decision"]["select"], 56)
        self.assertEqual(self.after["counts"]["by_decision"]["conditional"], 154)
        self.assertIn(self.cur["revision_id"], ("v71-20261125","v72-20261125"))
        self.assertIn(self.cur["expected"]["tracked"], (260,264))
        self.assertEqual(self.cur["expected"]["active"], 210)
        self.assertFalse(self.cur["statuses"]["download_approved"])

    def test_complete_publisher_trees_compare_with_prior_partial_refs(self) -> None:
        freeze = self.freeze
        totals = freeze["totals"]
        self.assertTrue(freeze["publisher_file_path_bytes_oid_lfs_complete"])
        self.assertEqual(totals, {
            "repos": 5, "files": 66, "bytes": 20236001980,
            "lfsRefs": 14, "priorityRepoCount": 2, "priorityFiles": 38,
            "priorityBytes": 7674695120, "priorityLfsRefs": 9,
        })
        older = {x["repo_id"]: x for x in self.partial["publisher_model_source_meta"]}
        self.assertEqual(len(older), 5)
        found = set()
        for repo in freeze["publisher_sources"]:
            name = repo["repo_id"]
            self.assertNotIn(name, found)
            found.add(name)
            old = older[name]
            self.assertRegex(repo["immutable_revision_sha"], r"^[0-9a-f]{40}$")
            self.assertEqual(repo["immutable_revision_sha"], old["publisher_revision_sha"])
            self.assertEqual(repo["publisher_repo_bytes"], old["publisher_source_bytes"])
            self.assertEqual(repo["publisher_repo_file_count"], old["publisher_file_count"])
            files = repo["publisher_exact_files"]
            self.assertEqual(len(files), repo["publisher_repo_file_count"])
            self.assertEqual(sum(f["bytes"] for f in files), repo["publisher_repo_bytes"])
            self.assertEqual(sum(bool(f["publisher_lfs_sha256"]) for f in files), repo["publisher_lfs_count"])
            self.assertEqual([f["path"] for f in files], old["paths"])
            self.assertEqual(len({f["path"] for f in files}), len(files))
            for f in files:
                self.assertRegex(f["git_blob_sha1"], r"^[0-9a-f]{40}$")
                self.assertGreaterEqual(f["bytes"], 0)
                if f["publisher_lfs_sha256"] is not None:
                    self.assertRegex(f["publisher_lfs_sha256"], r"^[0-9a-f]{64}$")
            for trained in old["trained"]:
                f = next((z for z in files if z["path"] == trained["path"]), None)
                self.assertIsNotNone(f)
                self.assertEqual(f["bytes"], trained["bytes"])
                self.assertEqual(f["publisher_lfs_sha256"], trained["publisher_lfs_sha256"])
            self.assertFalse(repo["download_approved"])
            self.assertFalse(repo["owner_local_file_SHA_verified"])
            self.assertFalse(repo["personal_legal_use_rights_verified"])
            self.assertFalse(repo["dependencies_offline_restore_verified"])
        self.assertEqual(len(found), 5)

    def test_new_two_originals_keep_head_and_unfounded_benchmark_claims_blocked(self) -> None:
        self.assertEqual(self.overlay["new_total_publisher_source_file_refs"], 38)
        self.assertEqual(self.overlay["new_total_publisher_bytes"], 7674695120)
        self.assertEqual(self.overlay["new_publisher_lfs_sha256_refs"], 9)
        aurum = next(x for x in self.overlay["additions"] if x["repo_id"].startswith("2Beyes/"))
        qjev = next(x for x in self.overlay["additions"] if x["repo_id"].startswith("Ankit"))
        self.assertEqual(aurum["candidate_selected_source_file_count"], 23)
        self.assertEqual(qjev["candidate_selected_source_file_count"], 15)
        self.assertEqual(aurum["candidate_selected_source_file_bytes"], 4572557909)
        self.assertEqual(qjev["candidate_selected_source_file_bytes"], 3102137211)
        self.assertIn("62.5", aurum["quality_negative"])
        self.assertIn("87.9", aurum["quality_negative"])
        self.assertIn("decision_head.safetensors", qjev["preservation_bundle"]["must_preserve"])
        self.assertIn("calibration", qjev["quality_negative"])
        self.assertEqual(aurum["parameter_gate"]["status"], "PASS_TOTAL_PARAMS_LT_150B")
        self.assertEqual(qjev["parameter_gate"]["status"], "PASS_TOTAL_PARAMS_LT_150B")
        self.assertTrue(all(x["portfolio_decision"] == "conditional" and
                            not x["download_approved"] and not x["download_ready"]
                            for x in self.overlay["additions"]))

    def test_prep_access_queue_and_all210_readiness_fail_closed(self) -> None:
        comparisons = [
            (self.old_queue["candidates"], self.queue["candidates"], 210),
            (self.old_access["entries"], self.access["entries"], 154),
            (self.old_prep["items"], self.prep["items"], 210),
            (self.old_readiness["records"], self.readiness["records"], 210),
        ]
        for before, after, n in comparisons:
            self.assertEqual(len(after), n)
            self.assertEqual(after[:len(before)], before)
        self.assertEqual(self.readiness["summary"]["blocked_any"], 210)
        self.assertEqual(self.readiness["summary"]["ready_to_approve"], 0)
        self.assertEqual(self.readiness["summary"]["downloads_approved"], 0)
        self.assertFalse(self.queue["approved"])
        self.assertFalse(self.queue["download_enabled"])
        self.assertFalse(self.prep["download_enabled"])
        self.assertFalse(self.access["download_authorized"])
        self.assertFalse(self.readiness["download_approved"])
        self.assertEqual(self.approved["entries"], [])
        self.assertTrue(all(x["download_approved"] is False and x["ready_to_acquire"] is False
                            for x in self.readiness["records"]))
        self.assertTrue(all(x["download_approved"] is False for x in self.prep["items"]))
        self.assertTrue(all(x["download_authorized"] is False for x in self.access["entries"]))
        self.assertTrue(all(x["download_approved"] is False for x in self.queue["candidates"]))
        actual = {x["repo_id"] for x in self.readiness["records"]}
        expected = {x["repo_id"] for x in self.after["items"] if x["portfolio_decision"] in ("conditional", "select")}
        self.assertEqual(actual, expected)
        for r in self.readiness["records"][-2:]:
            self.assertIn("EXPLICIT_ACQUISITION_AUTHORIZATION", r["blocking_gates"])
            self.assertIn("OWNER_LOCAL_HASH_AND_OFFLINE_RESTORE", r["blocking_gates"])
            self.assertFalse(r["offline_restore_verified"])

    def test_exclusions_prior116_and_nonexecutable_research(self) -> None:
        self.assertEqual(self.ledger["summary"]["models_verified"], 116)
        self.assertEqual(self.ledger["summary"]["files_verified_total"], 1758)
        self.assertEqual(self.ledger["summary"]["bytes_verified_total"], 2021784002725)
        reported = {x["repo_id"] for x in self.ledger["models"] if x["status"] == "VERIFIED"}
        self.assertFalse(set(self.overlay["added_assets"]) & reported)
        self.assertEqual(len(self.r163queue["new_conditional_review_order"]), 2)
        self.assertEqual(len(self.r163queue["held_sources"]), 2)
        self.assertEqual(len(self.r163queue["rejected_sources"]), 1)
        self.assertEqual(self.r163queue["rejected_sources"][0]["repo_id"],
                         "electroglyph/Spark-X2.6-4B-uncensored-experimental-LoRA")
        self.assertEqual(self.cur["expected"]["budget_scenario"]["v71_new_download_approval_bytes"], 0)
        self.assertFalse(self.cur["latest_v71_uncensored_originals"]["owner_HDD_independent_SHA_verified"])
        self.assertEqual(self.cur["latest_v71_uncensored_originals"]["owner_download_approval_count"], 0)


if __name__ == "__main__":
    unittest.main()
