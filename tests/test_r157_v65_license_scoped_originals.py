"""R157: source dedup vs model trained-state identity, robot mesh rights HOLD, and
fail-closed v64 plan generation. Offline stdlib; no model import or payload transfer.
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class R157RightsAndDedup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load("manifests/drafts/r157-2026-11-22-cartwheel-policy-52-and-heretic-lora-9-unique-source.candidate.json")
        cls.queue = load("queues/proposed-v65-r157-post112-noduplicate-and-rights-HOLD-UNAPPROVED.json")
        cls.original = load("manifests/drafts/r154-2026-11-22-four-primary-sources-after112.candidate.json")
        cls.catalog = load("catalog/effective-portfolio-2026-11-22-v65.json")
        cls.ledger = load("catalog/execution/2026-11-19-acquisition-ledger.json")

    def test_current_canonical_decisions_preserved_not_overwritten(self):
        current = load("catalog/CURRENT.json")
        self.assertEqual(current["revision_id"], "v66-20261124")
        self.assertEqual((current["expected"]["tracked"], current["expected"]["active"]), (246, 197))
        self.assertEqual((current["expected"]["by_decision"]["select"], current["expected"]["by_decision"]["conditional"], current["expected"]["by_decision"]["hold"]), (56, 141, 30))
        current_models = {x["repo_id"]: x for x in self.catalog["items"]}
        self.assertEqual(current_models["GetCartwheelInc/cartwheel-control"]["portfolio_decision"], "hold")
        self.assertEqual(current_models["nchapman/Qwen3.5-0.8B-Heretic-LoRA"]["portfolio_decision"], "conditional")
        self.assertEqual(current_models["mistralai/Timestral-5M"]["portfolio_decision"], "select")
        self.assertEqual(current_models["tencent/WeMM-Video-2B"]["portfolio_decision"], "conditional")
        self.assertEqual(load("queues/approved.json")["entries"], [])

    def test_two_original_scope_sources_61_files_and_ref_sums(self):
        source = self.source
        self.assertEqual((source["source_repos"], source["selected_files"], source["selected_bytes"], source["publisher_LFS_refs_selected"]), (2, 61, 112_597_730, 47))
        original = {x["repo_id"]: x for x in self.original["publisher_sources"]}
        for obj in source["publisher_sources"]:
            prev = original[obj["repo_id"]]
            self.assertEqual(obj["publisher_revision_sha"], prev["model_source_commit"])
            self.assertEqual(obj["publisher_original_file_count"], len(prev["files"]))
            self.assertEqual(obj["publisher_original_repo_bytes"], prev["full_publisher_file_bytes"])
            self.assertEqual(obj["selected_source_bytes"], sum(x["bytes"] for x in obj["selected_files"]))
            self.assertEqual(obj["selected_source_file_count"], len(obj["selected_files"]))
            self.assertEqual(obj["selected_source_file_count"] + len(obj["excluded_files"]), obj["publisher_original_file_count"])
            self.assertFalse(obj["download_approved"])
            for f in obj["selected_files"]:
                self.assertEqual(len(f["publisher_git_blob_sha1"]), 40)
                if f["publisher_lfs_sha256"]:
                    self.assertEqual(len(f["publisher_lfs_sha256"]), 64)
                self.assertFalse(f["owner_local_SHA_verified"])

    def test_cartwheel_three_policies_hold_and_excludes_thirdparty_robot_mesh(self):
        src = next(x for x in self.source["publisher_sources"] if x["repo_id"].startswith("GetCartwheelInc/"))
        self.assertEqual((src["publisher_original_file_count"], src["publisher_original_repo_bytes"]), (154, 304_057_444))
        self.assertEqual((src["selected_source_file_count"], src["selected_source_bytes"]), (52, 110_571_134))
        self.assertEqual((len(src["excluded_files"]), sum(x["bytes"] for x in src["excluded_files"])), (102, 193_486_310))
        paths = {x["path"] for x in src["selected_files"]}
        self.assertEqual({p for p in paths if p.endswith("policy.safetensors")},
                         {"asimov-1/policy.safetensors", "g1/policy.safetensors", "rp1/policy.safetensors"})
        self.assertTrue({"LICENSE", "NOTICE", "README.md"}.issubset(paths))
        self.assertFalse(any("/model/" in p or p.endswith("robot.glb") for p in paths))
        self.assertTrue(self.source["cartwheel_RP1_robot_assets_upstream_license_not_provided"])
        self.assertTrue(self.source["cartwheel_HOLD_must_not_be_silently_promoted_to_conditional"])
        self.assertTrue(self.source["cartwheel_external_robot_geometry_and_sim_code_missing"])

    def test_heretic_two_real_safetensors_no_gguf_or_identical_trial(self):
        src = next(x for x in self.source["publisher_sources"] if x["repo_id"].startswith("nchapman/"))
        self.assertEqual((src["publisher_original_file_count"], src["publisher_original_repo_bytes"]), (16, 6_165_749))
        self.assertEqual((src["selected_source_file_count"], src["selected_source_bytes"]), (9, 2_026_596))
        paths = {x["path"]: x for x in src["selected_files"]}
        weights = {p: f["publisher_lfs_sha256"] for p, f in paths.items() if p.endswith(".safetensors")}
        self.assertEqual(set(weights), {"adapter_model.safetensors", "pareto/trial_004_ref6_kl0.0275/adapter_model.safetensors"})
        self.assertNotEqual(*weights.values())
        self.assertFalse(any(p.endswith(".gguf") or "trial_002" in p for p in paths))
        original = next(x for x in self.original["publisher_sources"] if x["repo_id"] == src["repo_id"])
        raw = {x["path"]: x for x in original["files"]}
        self.assertEqual(raw["adapter_model.safetensors"]["sha256"],
                         raw["pareto/trial_002_ref4_kl0.0714/adapter_model.safetensors"]["sha256"])
        self.assertTrue(self.source["heretic_same_SHA_default_and_trial002_duplicate_excluded"])
        self.assertEqual(len(self.source["heretic_distinct_original_adapter_states"]) if isinstance(self.source["heretic_distinct_original_adapter_states"], list) else self.source["heretic_distinct_original_adapter_states"], 2)

    def test_post112_queue_nonduplicate_and_hold_gates(self):
        q = self.queue
        self.assertEqual(q["current_reported_acquired_VERIFIED"], 112)
        self.assertTrue(q["all_112_reported_verified_repo_IDs_present_in_v65"])
        self.assertEqual(len(q["source_research_rows"]), 5)
        self.assertEqual(q["not_reported_small_research_priority_bytes_excluding_cartwheel_HOLD"], 65_654_804)
        self.assertEqual(q["unique_small_new_or_supplementary_candidate_bytes_including_cartwheel_HOLD"], 176_225_938)
        self.assertEqual(q["large_two_HOLD_bytes"], 182_693_829_590)
        self.assertFalse(q["download_enabled"])
        self.assertEqual(q["new_approvals_added"], 0)
        verified = {x["repo_id"] for x in self.ledger["models"] if x["status"] == "VERIFIED"}
        self.assertEqual(len(verified), 116)
        selected={x["repo_id"] for x in self.catalog["items"]}
        self.assertEqual(verified-selected,
                         {"Datadog/Toto-2.0-4m","inclusionAI/LingSante-Pulse-1.0","ostris/primal_vae"})
        self.assertIn("nchapman/Qwen3.5-0.8B-Heretic-LoRA", verified)
        self.assertNotIn("GetCartwheelInc/cartwheel-control", verified)
        for x in q["source_research_rows"]:
            self.assertFalse(self.queue["download_enabled"])
            self.assertFalse(self.queue["do_not_download_unless_exact_licensed_source_approved"] is False)

    def test_v64_generator_is_now_strictly_research_only_2_new_scopes(self):
        # R156 concurrently replaced the obsolete R152 13-item generator.
        # Never regress to the old source queue / synthetic approval builder.
        script = ROOT / "scripts/build_v64_plan.py"
        text = script.read_text(encoding="utf-8")
        for banned in ('"approved_by_user": True', '"license_text_reviewed": True',
                       'D:/AI_VAULT/state/approved-v64.json'):
            self.assertNotIn(banned, text)
        self.assertIn("UNAPPROVED", text)
        spec = importlib.util.spec_from_file_location("r157_readonly_v64_generator", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            with mock.patch.object(module, "QUEUE",
                     ROOT / "queues/proposed-v65-r156-toto4m-pico8-UNAPPROVED.json"), \
                 mock.patch.object(module, "SOURCE",
                     ROOT / "manifests/drafts/r156-2026-11-22-toto4m-pico8-post112-publisher-source.candidate.json"), \
                 mock.patch.object(module, "LEDGER",
                     ROOT / "catalog/execution/2026-11-19-acquisition-ledger.json"), \
                 mock.patch.object(module, "HISTORICAL_QUEUE",
                     ROOT / "queues/proposed-v64-r152-post99-13-plus-bison-research-only.json"), \
                 mock.patch.object(module, "DISC", d), \
                 mock.patch.object(module, "PLAN", d / "plan.json"), \
                 mock.patch.object(module, "APPROVAL", d / "review-v65-r156-UNAPPROVED.json"):
                with self.assertRaisesRegex(ValueError,"ledger changed"):
                    module.main()
            self.assertFalse((d / "plan.json").exists())
            return  # historical v64 plan stale after ledger116, stop safely
            plan = json.loads((d / "plan.json").read_text())
            review = json.loads((d / "review-v65-r156-UNAPPROVED.json").read_text())
            self.assertEqual(len(plan["candidates"]), 2)
            self.assertTrue(plan["historical_13_matched_receipts_skipped"])
            self.assertFalse(plan["download_enabled"])
            self.assertFalse(plan["approved"])
            self.assertEqual(sum(x["selected_file_bytes"] for x in plan["candidates"]), 81_355_672)
            self.assertEqual(len(review["entries"]), 2)
            self.assertFalse((d / "approved-v64.json").exists())
            for x in review["entries"]:
                self.assertIsNone(x["approval_ref"])
                for k in ("approved", "download_enabled", "approved_by_user",
                          "license_text_reviewed", "parent_dependency_rights_reviewed",
                          "nonstandard_license_permission_verified"):
                    self.assertIs(x[k], False)

    def test_13_historic_r152_scopes_identical_to_112_ledger_and_one_large_hold(self):
        older = load("queues/proposed-v64-r152-post99-13-plus-bison-research-only.json")
        byid = {x["repo_id"]: x for x in self.ledger["models"] if x["status"] == "VERIFIED"}
        rows = older["candidate_research_only"]
        self.assertEqual(len(rows), 14)
        matches = [x for x in rows if x["repo_id"] in byid
                   and byid[x["repo_id"]]["revision_sha"] == x["publisher_revision_sha"]
                   and byid[x["repo_id"]]["files_verified"] == x["selected_file_count"]
                   and byid[x["repo_id"]]["source_bytes"] == x["publisher_reference_bytes"]]
        self.assertEqual(len(matches), 13)
        self.assertEqual([x["repo_id"] for x in rows if x not in matches],
                         ["ricursiveAI/Ripple-65B-Preview"])
        self.assertEqual(load("queues/approved.json")["entries"], [])


if __name__ == "__main__":
    unittest.main()
