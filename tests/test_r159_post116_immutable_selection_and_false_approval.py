"""R159 publisher metadata only. Never execute model code or transfer weights."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
def L(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))

from scripts.ledger_history_r168 import historical_117_ledger

class R159Post116SourceAndApproval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current=L("catalog/snapshots/v73-2026-11-25-current.json")
        cls.catalog=L("catalog/effective-portfolio-2026-11-24-v66.json")
        cls.ledger=historical_117_ledger(L("catalog/execution/2026-11-19-acquisition-ledger.json"))
        cls.src=L("manifests/drafts/r159-2026-11-24-ive-ivonnet-ccore-immutable-publisher-source.candidate.json")
        cls.q=L("queues/proposed-v66-r159-after116-novel-decision-models-UNAPPROVED.json")
        cls.audit=L("catalog/research/2026-11-24-r159-ledger116-reconciliation.json")
        cls.dec=L("catalog/decisions/2026-11-24-r159-v66-novel-decision-models-and-ledger116.json")
    def test_catalog_unmodified_and_acquisition116_not_owner_SHA(self):
        self.assertIn(self.current["revision_id"],("v66-20261124","v67-20261124","v68-20261125","v69-20261125","v70-20261125", "v71-20261125", "v72-20261125", "v73-20261125"))
        self.assertEqual((len(L("catalog/effective-portfolio-2026-11-24-v66.json")["items"]),L("catalog/effective-portfolio-2026-11-24-v66.json")["counts"]["active"]),(246,197))
        self.assertEqual((self.ledger["summary"]["models_verified"],self.ledger["summary"]["files_verified_total"],self.ledger["summary"]["bytes_verified_total"]),(116,1758,2021784002725))
        self.assertFalse(self.audit["owner_windows_D_physically_rehashed_by_this_audit"])
        self.assertEqual(len(self.audit["newly_reported_four_repos"]),4)
        self.assertEqual((self.audit["new_reported_files"],self.audit["new_reported_bytes"]),(44,1235859638))
        self.assertEqual(L("queues/approved.json")["entries"],[])
    def test_exact_three_ledger116_gaps_never_redownload(self):
        verified={x["repo_id"] for x in self.ledger["models"] if x["status"]=="VERIFIED"}
        selected={x["repo_id"] for x in self.catalog["items"]}
        gaps=verified-selected
        self.assertEqual(gaps,set())
        historic={"Datadog/Toto-2.0-4m","inclusionAI/LingSante-Pulse-1.0","ostris/primal_vae"}
        self.assertEqual({x["repo_id"] for x in self.audit["historical_v65_missing_before_v66_backfill"]},historic)
        self.assertEqual(set(self.q["preexisting_reported_VERIFIED_but_uncatalogued"]),set())
        self.assertTrue(self.q["preexisting_reported_not_to_redownload"])
    def test_new_IVE_Ivonnet_first_party_source_byte_sha_and_release_manifest(self):
        chosen=self.src["publisher_sources"][:2]
        self.assertEqual([x["repo_id"] for x in chosen],["illuin/Ivonnet-0.8B","illuin/IVE-4B"])
        self.assertEqual([x["publisher_revision_sha"] for x in chosen],["6a6a979489d262861ad3c34faaa1a763d1ce4baf","1e65613dfd83ba6949883325fc5f4791dae56a46"])
        self.assertEqual([x["publisher_full_file_count"] for x in chosen],[21,23])
        self.assertEqual([x["publisher_full_bytes"] for x in chosen],[1728496331,9102712961])
        self.assertEqual([x["trained_parameter_count_from_metadata"] for x in chosen],[852985920,4539265536])
        self.assertEqual(self.src["new_research_conditional_file_count"],44)
        self.assertEqual(self.src["new_research_conditional_source_bytes"],10831209292)
        for x in chosen:
            self.assertFalse(x["download_approved"])
            self.assertFalse(x["owner_source_local_sha_verified"])
            self.assertEqual(x["model_card_license_tag"],"apache-2.0")
            self.assertEqual(x["publisher_full_bytes"],sum(f["bytes"] for f in x["publisher_source_files"]))
            self.assertEqual(len({f["path"] for f in x["publisher_source_files"]}),x["publisher_full_file_count"])
            self.assertTrue(x["publisher_release_manifest_weight_SHA_crosscheck_pass"])
            self.assertTrue(x["publisher_release_verification_flag"])
            self.assertEqual(x["torch_dependency_from_publisher"],">=2.6")
            self.assertEqual(x["transformers_dependency_from_publisher"],">=5.7,<6")
            self.assertTrue({"readout.safetensors","source/pyproject.toml","decision_config.json","tokenizer.json"}.issubset({f["path"] for f in x["publisher_source_files"]}))
            for f in x["publisher_source_files"]:
                self.assertEqual(len(f["git_blob_sha1"]),40)
                if f["publisher_lfs_sha256"]:self.assertEqual(len(f["publisher_lfs_sha256"]),64)
                self.assertFalse(f["owner_local_sha256_verified"])
        a={f["path"]:f for f in chosen[0]["publisher_source_files"]}
        b={f["path"]:f for f in chosen[1]["publisher_source_files"]}
        self.assertEqual(a["tokenizer.json"]["publisher_lfs_sha256"],b["tokenizer.json"]["publisher_lfs_sha256"])
        self.assertEqual(self.src["overlap_independent_trained_weight_digests"],0)
        self.assertNotEqual(a["readout.safetensors"]["publisher_lfs_sha256"],b["readout.safetensors"]["publisher_lfs_sha256"])
    def test_coder_alternative_hold_and_format_aware_no_duplicate(self):
        h=self.src["publisher_sources"][2]
        self.assertEqual(h["repo_id"],"ccore/CCORE-Web-Coder-4B")
        self.assertEqual((h["publisher_full_file_count"],h["publisher_full_bytes"]),(30,33809262632))
        self.assertEqual(h["competing_full_weight_format_files"],5)
        self.assertEqual(h["candidate_native_safetensors_bytes"],17490122528)
        self.assertEqual(h["already_in_source_alternative_gguf_count"],4)  # 3 GGUF + one mmproj
        self.assertEqual(h["research_selection"],"HOLD_NO_ADDITIONAL_FULL_MODEL")
        self.assertFalse(h["download_approved"])
        self.assertNotIn(h["repo_id"],{x["repo_id"] for x in self.q["research_selection_rows"]})
    def test_unapproved_queue_and_decision_separation(self):
        self.assertEqual(self.q["research_selection_repo_count"],2)
        self.assertEqual(self.q["research_selection_source_file_count"],44)
        self.assertEqual(self.q["research_selection_publisher_reference_bytes"],10831209292)
        self.assertTrue(self.q["auto_approval_prohibited"])
        self.assertFalse(self.q["download_enabled"])
        self.assertFalse(self.q["approved_by_user"])
        self.assertEqual(self.q["approved_entries"],0)
        self.assertFalse(self.dec["formal_catalogue_changed"])
        self.assertEqual(self.dec["download_approvals_added"],0)
        self.assertEqual(self.dec["model_payloads_downloaded"],0)
        self.assertEqual(len(self.dec["new_research_candidates"]),2)
        for c in self.dec["new_research_candidates"]:
            self.assertFalse(c["source_download_approved"])
    def test_new_v65_plan_generator_creates_owner_review_not_approval(self):
        spec=importlib.util.spec_from_file_location("read_only_r159",ROOT/"scripts/build_v65_plan.py")
        plan=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plan)
        with tempfile.TemporaryDirectory() as td:
            scratch=Path(td)
            # Historical planner tested against its fixed v66 selection header;
            # do not weaken production fail-closed check for later v67 current.
            current = L("catalog/snapshots/v73-2026-11-25-current.json")
            current["revision_id"] = "v66-20261124"
            current["expected"]["tracked"] = 246
            current["expected"]["active"] = 197
            (scratch/"current-v66.json").write_text(json.dumps(current))
            # Replay the audited original v66/116 receipts; production 133 must fail closed.
            (scratch/"ledger-historical-116.json").write_text(json.dumps(self.ledger))
            with mock.patch.object(plan,"QUEUE",ROOT/"queues/proposed-v66-r159-after116-novel-decision-models-UNAPPROVED.json"),\
                 mock.patch.object(plan,"SOURCE",ROOT/"manifests/drafts/r159-2026-11-24-ive-ivonnet-ccore-immutable-publisher-source.candidate.json"),\
                 mock.patch.object(plan,"LEDGER",scratch/"ledger-historical-116.json"),\
                 mock.patch.object(plan,"CURRENT",scratch/"current-v66.json"),\
                 mock.patch.object(plan,"DISC",scratch),\
                 mock.patch.object(plan,"PLAN",scratch/"plan.json"),\
                 mock.patch.object(plan,"APPROVAL",scratch/"review-UNAPPROVED.json"):
                plan.main()
            a=json.loads((scratch/"plan.json").read_text())
            b=json.loads((scratch/"review-UNAPPROVED.json").read_text())
            self.assertEqual(len(a["candidates"]),2)
            self.assertEqual(a["publisher_reference_bytes"],10831209292)
            self.assertEqual(len(b["entries"]),2)
            self.assertFalse(a["download_enabled"])
            self.assertFalse((scratch/"approved-v65.json").exists())
            for x in b["entries"]:
                self.assertIsNone(x["approval_ref"])
                for k in ("approved","approved_by_user","download_enabled","license_text_reviewed","parent_dependency_rights_reviewed","nonstandard_license_permission_verified"):
                    self.assertFalse(x[k])
    def test_old_v65_generated_approval_reference_cannot_pass_executor(self):
        spec=importlib.util.spec_from_file_location("p159",ROOT/"scripts/preserve_execute.py")
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        task={"repo_id":"example/sample","rev":"a"*40,"files":[{"path":"model.safetensors","bytes":100,"sha256":"b"*64}]}
        test={"repo_id":task["repo_id"],"revision_sha":task["rev"],"files":task["files"],
              "approved":True,"approved_by_user":True,"download_enabled":True,
              "license_text_reviewed":True,"parent_dependency_rights_reviewed":True,
              "nonstandard_license_permission_verified":True,
              "approval_ref":"v65-post112-exact-source-files-example-sample"}
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"approved-v65-synthetic.json"
            path.write_text(json.dumps({"entries":[test]}))
            self.assertIsNone(module.approval_for(task,approval_path=path))
            test["approval_ref"]="owner-explicit-individual-license-scope-review-2026-11-24"
            path.write_text(json.dumps({"entries":[test]}))
            self.assertIsNotNone(module.approval_for(task,approval_path=path))
if __name__=="__main__":
    unittest.main()
