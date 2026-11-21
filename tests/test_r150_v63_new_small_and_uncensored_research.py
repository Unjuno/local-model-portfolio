"""R150 source-and-decision consistency tests; offline, no downloads or code execution."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "manifests/drafts/r150-2026-11-22-wemm-timestral5m-publisher-fixed.candidate.json"
QUEUE = "queues/proposed-v63-r150-after99-13-research-only.json"
HIST = "queues/proposed-v63-r149-after99-11-research-only.json"
DECISION = "catalog/decisions/2026-11-22-r150-v63-four-originals-research-decisions.json"

def load(relpath):
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))

class R150NewSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load(MANIFEST)
        cls.q = load(QUEUE)
        cls.old = load(HIST)
        cls.d = load(DECISION)

    def test_exact_immutable_original_file_scopes(self):
        s = {x["repo_id"]: x for x in self.m["publisher_sources"]}
        self.assertEqual(set(s), {"mistralai/Timestral-5M", "tencent/WeMM-Video-2B"})
        self.assertEqual(self.m["full_repo_files"], 33)
        self.assertEqual(self.m["full_repo_bytes"], 6611554027)
        self.assertEqual(self.m["weight_only_bytes"], 6588239864)
        self.assertEqual(s["mistralai/Timestral-5M"]["full_repo_publisher_bytes"], 20854471)
        self.assertEqual(s["tencent/WeMM-Video-2B"]["full_repo_publisher_bytes"], 6590699556)
        for x in s.values():
            self.assertEqual(len(x["immutable_revision_sha"]), 40)
            self.assertEqual(len(x["files"]), x["total_file_count"])
            self.assertEqual(sum(f["bytes"] for f in x["files"]), x["full_repo_publisher_bytes"])
            self.assertEqual(len({f["path"] for f in x["files"]}), x["total_file_count"])
            self.assertEqual(x["weights_file_bytes"], sum(f["bytes"] for f in x["files"] if f["path"].endswith(".safetensors")))
            self.assertFalse(x["owner_licensed_acts_verified"])
            self.assertFalse(x["owner_manifest_approved"])
            self.assertFalse(x["offline_restore_verified"])
            for f in x["files"]:
                self.assertTrue(isinstance(f["bytes"], int) and f["bytes"] >= 0)
                self.assertEqual(len(f["git_blob_sha1"]), 40)
                if f["publisher_lfs_sha256"]:
                    self.assertEqual(len(f["publisher_lfs_sha256"]), 64)
                if f["publisher_sha256_from_checksums"]:
                    self.assertEqual(len(f["publisher_sha256_from_checksums"]), 64)
                if f["publisher_lfs_sha256"] and f["publisher_sha256_from_checksums"]:
                    self.assertEqual(f["publisher_lfs_sha256"], f["publisher_sha256_from_checksums"])
                self.assertFalse(f["owner_local_sha_verified"])

    def test_publisher_sha_and_package_metadata(self):
        s = {x["repo_id"]: x for x in self.m["publisher_sources"]}
        w = s["tencent/WeMM-Video-2B"]
        self.assertEqual((w["total_file_count"], w["publisher_lfs_sha256_refs"], w["publisher_checksum_file_refs"]), (27, 5, 25))
        self.assertEqual(w["weights_file_bytes"], 6567395904)
        self.assertEqual(len([f for f in w["files"] if f["path"].endswith(".py")]), 9)
        t = s["mistralai/Timestral-5M"]
        self.assertEqual((t["total_file_count"], t["publisher_lfs_sha256_refs"]), (6, 1))
        self.assertEqual(t["weights_file_bytes"], 20843960)
        self.assertEqual(len([f for f in t["files"] if f["path"] == "LICENSE"]), 1)

    def test_11_original_candidates_retained_and_zero_approval(self):
        now = {x["repo_id"]: x for x in self.q["candidate_research_only"]}
        self.assertEqual((self.old["candidate_repo_count"], self.q["candidate_repo_count"]), (11, 13))
        self.assertEqual(len(now), 13)
        for x in self.old["candidate_research_only"]:
            self.assertEqual(x, now[x["repo_id"]])
        self.assertEqual(set(now)-{x["repo_id"] for x in self.old["candidate_research_only"]},
                         {"mistralai/Timestral-5M", "tencent/WeMM-Video-2B"})
        self.assertEqual(self.q["nonhold_publisher_reference_bytes"], 75155724960)
        self.assertEqual(self.q["phase_summary"]["P0_SMALL_ORIGINALS_AND_EDGE"]["source_repos"], 5)
        self.assertEqual(self.q["phase_summary"]["P1_SPECIALIZED_AND_UNCENSORED_PARENTS"]["source_repos"], 5)
        self.assertFalse(self.q["approval_controls"]["approved"])
        self.assertFalse(self.q["approval_controls"]["download_enabled"])
        self.assertEqual(self.q["approval_controls"]["entries_approved"], 0)
        for id in ("mistralai/Timestral-5M", "tencent/WeMM-Video-2B"):
            self.assertFalse(now[id]["owner_manifest_approval_present"])
            self.assertFalse(now[id]["owner_licensed_act_reviewed"])
            self.assertFalse(now[id]["owner_local_SHA_reverified"])
            self.assertEqual(now[id]["canonical_selection_status"], "RESEARCH_CANDIDATE_NOT_YET_ADDED_TO_CURRENT")

    def test_no_unapproved_edited_model_or_false_canonical_claim(self):
        self.assertEqual(len(self.d["models"]), 4)
        self.assertEqual(self.d["canonical_new_assets_adopted"], 0)
        self.assertEqual(self.d["approved_manifest_count"], 0)
        self.assertEqual(self.d["payload_bytes_downloaded"], 0)
        self.assertFalse(self.d["user_D_direct_sha_verified"])
        self.assertFalse(self.m["owner_D_independent_sha_verified"])
        self.assertEqual([x["research_decision"].startswith("HOLD") for x in self.d["models"]],
                         [False, False, True, True])
        self.assertEqual(self.q["reported_acquired"]["models_verified"], 99)
        self.assertEqual(self.q["reported_acquired"]["files_verified"], 1478)

if __name__ == "__main__":
    unittest.main()
