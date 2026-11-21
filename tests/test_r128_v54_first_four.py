"""Offline safety, provenance and staging checks for v54 R128 four-source pilot."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "download_r115_windows.py"
SOURCE = ROOT / "queues" / "proposed-v54-r128-first-four-delta-source.json"
R125 = ROOT / "queues" / "proposed-v52-r125-ledger61-delta-next15.json"
R126 = ROOT / "queues" / "proposed-v53-r126-aion-bf16-first-public-source.json"
LEDGER = ROOT / "catalog" / "execution" / "2026-11-19-acquisition-ledger.json"
CATALOG = ROOT / "catalog" / "effective-portfolio-2026-11-20-v54.json"
DECISION = ROOT / "catalog" / "decisions" / "2026-11-20-r128-v54-live-ledger61-and-parent-gap.json"

spec = importlib.util.spec_from_file_location("r128_downloader", SCRIPT)
engine = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(engine)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class R128OriginalsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load(SOURCE)
        cls.original = load(R125)
        cls.aion = load(R126)
        cls.ledger = load(LEDGER)
        cls.cat = load(CATALOG)
        cls.recon = load(DECISION)

    def test_exact_four_101_file_and_size(self):
        selected = engine.validate_manifest(self.m)
        self.assertEqual(len(selected), 4)
        self.assertEqual(sum(len(x["files"]) for x in selected), 101)
        self.assertEqual(sum(x["source_bytes"] for x in selected), 6_127_042_272)
        self.assertEqual(sum(sum(x.get("sha256") is not None for x in e["files"])
                             for e in selected), 9)

    def test_namespaces_and_selected_order(self):
        selected = engine.validate_manifest(self.m)
        self.assertEqual([x["source_repo_id"] for x in selected], [
            "elyza/ELYZA-tasks-100", "CohereLabs/aya_dataset",
            "Reson8/Rumble-2-Flash", "microsoft/Aion-1.0-Instruct-2.3B"])
        self.assertEqual([x["repository_type"] for x in selected],
                         ["dataset", "dataset", "model", "model"])

    def test_exact_source_matches_previously_pinned_versions(self):
        r125 = {e["source_repo_id"]: e for e in self.original["entries"]}
        for x in self.m["entries"]:
            base = (self.aion["entries"][0] if x["source_repo_id"].startswith("microsoft/")
                    else r125[x["source_repo_id"]])
            for field in ("source_repo_id", "source_revision", "source_bytes",
                          "repository_type", "license_metadata"):
                self.assertEqual(x[field], base[field])
            self.assertEqual(x["files"], base["files"])

    def test_no_ledger_download_claim_for_four_sources(self):
        recorded = {x["repo_id"]: x for x in self.ledger["models"]}
        for e in self.m["entries"]:
            if e["catalog_repo_id"] in recorded:
                self.assertEqual(recorded[e["catalog_repo_id"]]["status"],"VERIFIED")
            self.assertFalse(e["download_approved"])
        self.assertGreaterEqual(self.ledger["summary"]["models_verified"],61)
        self.assertFalse(self.m["owner_disk_independently_rehashed_this_turn"])

    def test_owner_specific_approval_has_not_been_inferred(self):
        self.assertFalse(self.m["user_exact_source_scope_consent"])
        self.assertFalse(self.m["license_and_parent_rights_act_review_complete"])
        for e in self.m["entries"]:
            self.assertFalse(e["download_approved"])
            self.assertFalse(e["license_rights_act_scope_verified"])
            self.assertFalse(e["owner_D_volume_current_verified"])

    def test_empty_approval_blocks_before_network(self):
        selected = engine.validate_manifest(self.m)
        with tempfile.TemporaryDirectory() as folder:
            approvals = Path(folder) / "approval.json"
            approvals.write_text('{"schema_version":1,"entries":[]}', encoding="utf-8")
            with self.assertRaises(ValueError):
                engine.assert_explicit_approved_sources(selected, approvals)

    def test_model_and_dataset_hf_downloader_calls_different_repo_type(self):
        selected = engine.validate_manifest(self.m)
        for e in (selected[0], selected[2]):
            hub = Mock(return_value="does-not-run-network")
            with tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                engine.hub_download_selected(hub, e, e["files"][0]["path"], target)
                hub.assert_called_once_with(repo_id=e["source_repo_id"],
                                            filename=e["files"][0]["path"],
                                            revision=e["source_revision"],
                                            local_dir=str(target),
                                            repo_type=e["repository_type"])

    def test_tampering_source_bytes_or_revision_rejected(self):
        alt = copy.deepcopy(self.m)
        alt["entries"][0]["files"][0]["bytes"] += 1
        with self.assertRaises(ValueError):
            engine.validate_manifest(alt)
        alt = copy.deepcopy(self.m)
        alt["entries"][2]["source_revision"] = "f" * 40
        # Revision alone has valid shape, but any new signed scope must be re-approved.
        self.assertNotEqual(engine.source_fingerprint(alt["entries"][2]),
                            engine.source_fingerprint(self.m["entries"][2]))

    def test_gated_and_license_invalid_fail(self):
        for field, value in (("gated", True), ("license_metadata", "not-a-license")):
            alt = copy.deepcopy(self.m)
            alt["entries"][2][field] = value
            with self.assertRaises(ValueError):
                engine.validate_manifest(alt)

    def test_portable_dataset_scope_with_upstream_exclusion_provenance(self):
        elyza = self.m["entries"][0]
        files = {x["path"] for x in elyza["files"]}
        self.assertIn("test.csv", files)
        self.assertNotIn("baseline/preds/anthropic.claude-v2:1.csv", files)
        self.assertEqual(len(files), 65)
        for item in elyza["files"]:
            engine.validate_relpath(item["path"])

    def test_full_160_reconcile_and_remory_parent_absence(self):
        self.assertEqual(self.cat["counts"]["tracked"], 207)
        self.assertEqual(self.cat["counts"]["active"], 160)
        self.assertEqual(len(self.recon["per_active_asset"]), 160)
        self.assertEqual(self.recon["summary"], {
            "REPORTED_VERIFIED_NOT_THIS_TURN_REHASH": 61,
            "REPORTED_HOLD_GATED_OR_PRIVATE": 1,
            "NO_ACQUISITION_REPORT": 98
        })
        dependency = self.recon["parent_dependency_audit"]
        self.assertFalse(dependency["original_parent_weights_are_in_61_model_verified_report"])
        self.assertEqual(dependency["parent_config_delta_source_bytes"], 91_892)
        self.assertFalse(dependency["owner_archive_parent_weights_present_and_sha_verified"])


if __name__ == "__main__":
    unittest.main()
