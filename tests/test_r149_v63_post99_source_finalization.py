"""R149 research-only: immutable publisher draft agreement and explicit STOP.

This test does not download a model, execute foreign code or authorize acquisition.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class R149Post99SourceFinalization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = read("catalog/snapshots/v73-2026-11-25-current.json")
        cls.report = read("catalog/decisions/2026-11-22-r149-v63-next-source-finalization.json")
        cls.queue = read("queues/proposed-v63-r149-after99-11-research-only.json")
        cls.by_id = {item["repo_id"]: item for item in cls.report["decisions"]}

    def test_canonical_stays_v63_and_no_implicit_approval(self):
        self.assertIn(self.current["revision_id"], ("v63-20261122", "v64-20261122","v65-20261122", "v66-20261124", "v67-20261124","v68-20261125","v69-20261125","v70-20261125", "v71-20261125", "v72-20261125", "v73-20261125"))
        self.assertEqual(read("catalog/effective-portfolio-2026-11-22-v63.json")["counts"]["tracked"], 235)
        self.assertEqual(read("catalog/effective-portfolio-2026-11-22-v63.json")["counts"]["active"], 188)
        self.assertEqual(read("catalog/effective-portfolio-2026-11-22-v63.json")["counts"]["by_decision"]["select"], 55)
        self.assertEqual(read("catalog/effective-portfolio-2026-11-22-v63.json")["counts"]["by_decision"]["conditional"], 133)
        pointer = self.current["latest_r149_post99_source_decision"]
        self.assertEqual(
            pointer["machine_readable_decisions"],
            "catalog/decisions/2026-11-22-r149-v63-next-source-finalization.json",
        )
        self.assertTrue((ROOT / pointer["report"]).is_file())
        self.assertTrue(pointer["canonical_v63_asset_decisions_unchanged"])
        self.assertFalse(pointer["owner_local_sha_runtime_and_rights_verified"])
        self.assertEqual(self.report["active_selection_changed"], 0)
        self.assertEqual(self.report["new_asset_ids_added"], 0)
        self.assertEqual(self.report["model_weight_downloads_performed_in_review"], 0)
        self.assertEqual(self.report["download_approvals_created"], 0)
        self.assertEqual(self.report["existing_payload_deleted"], 0)
        self.assertEqual(read("queues/approved.json")["entries"], [])
        self.assertEqual(len(self.report["decisions"]), 11)
        self.assertEqual(len(self.by_id), 11)
        self.assertEqual(set(self.by_id), {
            row["repo_id"] for row in self.queue["candidate_research_only"]
        })
        for row in self.report["decisions"]:
            for flag in (
                "owner_license_rights_verified",
                "owner_disk_free_floor_verified",
                "owner_local_sha_verified",
                "pinned_runtime_and_dependency_abi_verified",
                "full_offline_restore_verified",
                "explicit_source_acquisition_approval",
                "download_enabled",
                "reported_ledger99_duplicate",
            ):
                self.assertIs(row[flag], False, (row["repo_id"], flag))
        self.assertEqual(
            self.by_id["ricursiveAI/Ripple-65B-Preview"]["portfolio_decision"],
            "hold",
        )

    def test_all_eleven_static_manifests_match_pinned_paths_bytes_and_revisions(self):
        original = {row["repo_id"]: row for row in self.queue["candidate_research_only"]}
        checked = 0
        ref_bytes = 0
        for item in self.report["decisions"]:
            q = original[item["repo_id"]]
            manifest = read(item["source_manifest"])
            sources = (
                manifest.get("model_repos")
                or manifest.get("publisher_sources")
                or manifest.get("publisher_model_sources")
                or manifest.get("sources")
            )
            source = next(s for s in sources if s["repo_id"] == item["repo_id"])
            files = (
                source.get("selected_files")
                or source.get("publisher_selected_files")
                or source.get("files")
            )
            revision = source.get("immutable_revision_sha") or source.get("revision_sha")
            self.assertRegex(item["source_revision_sha"], r"^[0-9a-f]{40}$")
            self.assertEqual(revision, item["source_revision_sha"])
            self.assertEqual(revision, q["publisher_revision_sha"])
            self.assertEqual(len(files), item["publisher_selected_file_count"])
            self.assertEqual(len(files), q["selected_file_count"])
            self.assertEqual(
                sum(f["bytes"] for f in files), item["publisher_selected_bytes"]
            )
            self.assertEqual(item["publisher_selected_bytes"], q["publisher_reference_bytes"])
            self.assertEqual(
                sum(bool(f.get("publisher_lfs_sha256")) for f in files),
                item["publisher_selected_lfs_sha256_refs"],
            )
            for file in files:
                self.assertRegex(file["path"], r"^\S")
                self.assertRegex(
                    file.get("git_blob_sha1") or file.get("oid"),
                    r"^[0-9a-f]{40}$",
                )
                if file.get("publisher_lfs_sha256"):
                    self.assertRegex(file["publisher_lfs_sha256"], r"^[0-9a-f]{64}$")
            checked += len(files)
            ref_bytes += sum(f["bytes"] for f in files)
        s = self.report["selected_11_existing_source_scope_manifest_validation"]
        self.assertEqual((checked, ref_bytes), (
            s["all_11_publisher_file_refs"], s["all_11_publisher_file_bytes"]
        ))
        self.assertEqual((checked, ref_bytes), (219, 198117060906))
        self.assertTrue(s["validates_publisher_metadata_not_owner_local_files"])
        self.assertEqual(s["immutable_repo_revision_matched"], 11)
        self.assertEqual(s["publisher_selected_file_count_matched"], 11)
        self.assertEqual(s["publisher_selected_byte_sum_matched"], 11)

    def test_p0_certain_scope_not_software_or_user_permission(self):
        p0 = self.report["p0_ranked_for_later_per_source_owner_review"]
        self.assertEqual(p0, [
            "mistralai/Timestral-28M",
            "KittenML/kitten-tts-2-pico",
            "Cactus-Compute/mirage",
            "AuroraAI-Research/Aurora2-400M-A20M",
        ])
        self.assertEqual(
            sum(self.by_id[k]["publisher_selected_bytes"] for k in p0), 2234744280
        )
        self.assertEqual(
            self.report["archive_planning_reference_bytes"]["p0_to_p2_ten"],
            68544170933,
        )
        self.assertEqual(
            self.report["archive_planning_reference_bytes"]["p3_ripple_hold"],
            129572889973,
        )
        self.assertIsNone(
            self.report["archive_planning_reference_bytes"]["owner_incremental_transfer_bytes"]
        )
        self.assertFalse(
            self.report["archive_planning_reference_bytes"]["owner_cached_shared_sha_reuse_verified"]
        )
        self.assertTrue(self.report["critical_offline_restore_findings"][
            "kitten_int4_explicit_backend_required"
        ])
        kitten_manifest = read(
            "manifests/drafts/r143-2026-11-22-three-specialists-originals.candidate.json"
        )
        kitten = next(x for x in kitten_manifest["model_repos"]
                      if x["repo_id"] == "KittenML/kitten-tts-2-pico")
        paths = {f["path"] for f in kitten["selected_files"]}
        self.assertEqual(len([p for p in paths if p.endswith("_int4.onnx")]), 8)
        self.assertFalse(any(p.endswith("_int8.onnx") for p in paths))
        self.assertEqual(len([p for p in paths if p.startswith("voices_")]), 8)
        self.assertIn("g2p/g2p_bart_en_us/model.safetensors", paths)
        cactus_runtime = self.report["archive_planning_reference_bytes"][
            "separate_cactus_4_1_4_runtime_reference"
        ]
        self.assertEqual(cactus_runtime, 4137947)
        self.assertEqual(
            self.report["archive_planning_reference_bytes"][
                "separate_fastframes_CFpp_Wan_parent_reference"
            ],
            17567235949,
        )

    def test_bis_policy_and_rfd4_not_conflated_with_download_readiness(self):
        policy = self.report["regulatory_fact"]
        self.assertEqual(policy["us_export_rule_effective"], "2026-11-19")
        self.assertTrue(policy["eccn_4E091_model_weight_control_revoked"])
        self.assertFalse(policy["future_local_models_general_ban_verified"])
        self.assertTrue(policy["does_not_imply_all_cross_border_model_transfers_are_legal"])
        self.assertEqual(self.report["rfd4_weight_revision_sha_conflict"]["repo_id"],
                         "nvidia/RFD4-Proteina")
        self.assertTrue(
            self.report["rfd4_weight_revision_sha_conflict"][
                "reported_weight_revision_differs_from_old_catalog"
            ]
        )
        prior = read("catalog/research/2026-11-22-r148-ledger99-immutable-revision-drift.json")
        self.assertEqual(
            prior["one_weight_identity_and_dependency_scope_difference_repo"],
            "nvidia/RFD4-Proteina",
        )


if __name__ == "__main__":
    unittest.main()
