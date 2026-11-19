"""Offline regression checks for R117 v48 selected source files (no downloads)."""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "queues/proposed-v48-r117-next-wave-eight-source-pinned.json"
CATALOG = ROOT / "catalog/effective-portfolio-2026-11-18-v48.json"
LEDGER = ROOT / "catalog/execution/2026-11-19-acquisition-ledger.json"
RECON = ROOT / "catalog/decisions/2026-11-19-r117-all154-acquisition-gap-and-next-wave.json"
EXPECTED_IDS = {
    "GSAI-ML/iLLaDA-8B-Base",
    "RWKV/RWKV7-7.2B-20260805",
    "microsoft/TRELLIS.2-4B",
    "microsoft/Fara1.5-27B",
    "Tongyi-MAI/Z-Image-Turbo",
    "Wan-AI/Wan2.2-TI2V-5B",
    "elyza/ELYZA-tasks-100",
    "CohereLabs/aya_dataset",
}
BINARY_SUFFIXES = (".safetensors", ".pth", ".pt", ".bin", ".onnx", ".parquet", ".gguf")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class SourceLockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = read(MANIFEST)
        cls.catalog = read(CATALOG)
        cls.ledger = read(LEDGER)
        cls.recon = read(RECON)
        cls.models = {row["repo_id"]: row for row in cls.m["models"]}

    def test_exact_eight_targets_no_duplicate_ids(self):
        self.assertEqual(set(self.models), EXPECTED_IDS)
        self.assertEqual(len(self.m["models"]), len(EXPECTED_IDS))
        self.assertEqual(self.m["repo_count"], 8)
        self.assertEqual(self.m["model_count"], 6)
        self.assertEqual(self.m["dataset_count"], 2)

    def test_total_files_and_immutable_publisher_bytes(self):
        m = self.m
        self.assertEqual(m["selected_file_refs"], 188)
        self.assertEqual(m["sha256_refs"], 48)
        self.assertEqual(m["selected_bytes"], 169094028046)
        self.assertEqual(sum(e["selected_source_bytes"] for e in m["models"]), m["selected_bytes"])
        self.assertEqual(sum(e["selected_file_count"] for e in m["models"]), m["selected_file_refs"])
        self.assertEqual(sum(e["publisher_sha256_count"] for e in m["models"]), m["sha256_refs"])

    def test_source_revisions_paths_and_bytes_are_valid(self):
        for e in self.m["models"]:
            self.assertRegex(e["revision"], r"^[0-9a-f]{40}$")
            self.assertFalse(e["gated"])
            self.assertTrue(e["license_metadata"])
            self.assertEqual(sum(f["bytes"] for f in e["selected_files"]), e["selected_source_bytes"])
            self.assertEqual(len(e["selected_files"]), e["selected_file_count"])
            self.assertEqual(len({f["path"] for f in e["selected_files"]}), e["selected_file_count"])
            for f in e["selected_files"]:
                path = f["path"]
                self.assertTrue(path)
                self.assertNotIn("\\", path)
                self.assertNotIn("..", path.split("/"))
                self.assertFalse(path.startswith("/"))
                self.assertIs(type(f["bytes"]), int)
                self.assertGreater(f["bytes"], 0)
                self.assertRegex(f["git_blob_sha1"], r"^[0-9a-f]{40}$")
                if f["sha256"] is not None:
                    self.assertRegex(f["sha256"], r"^[0-9a-f]{64}$")
                if path.lower().endswith(BINARY_SUFFIXES):
                    self.assertIsNotNone(f["sha256"], f"Binary requires LFS SHA256: {e['repo_id']}/{path}")

    def test_active_and_not_in_verified_ledger(self):
        active = {x["repo_id"]: x for x in self.catalog["items"]
                  if x["portfolio_decision"] in ("select", "conditional")}
        recorded = {x["repo_id"] for x in self.ledger["models"]}
        self.assertEqual(len(active), 154)
        for rid, item in self.models.items():
            self.assertIn(rid, active)
            self.assertEqual(active[rid]["asset_kind"], item["repo_type"])
            self.assertNotIn(rid, recorded)

    def test_only_original_binary_formats_selected(self):
        i = self.models["GSAI-ML/iLLaDA-8B-Base"]
        self.assertEqual(sum(f["path"].endswith(".safetensors") for f in i["selected_files"]), 4)
        r = self.models["RWKV/RWKV7-7.2B-20260805"]
        self.assertEqual(sum(f["path"].endswith(".safetensors") for f in r["selected_files"]), 3)
        f = self.models["microsoft/Fara1.5-27B"]
        self.assertEqual(sum(fx["path"].endswith(".safetensors") for fx in f["selected_files"]), 10)
        self.assertTrue(any(x["path"] == "model.safetensors.index.json" for x in f["selected_files"]))

    def test_3d_material_and_video_dependency_components_present(self):
        tr = {f["path"] for f in self.models["microsoft/TRELLIS.2-4B"]["selected_files"]}
        self.assertTrue(any("shape_enc" in f for f in tr))
        self.assertTrue(any("tex_dec" in f for f in tr))
        wan = {f["path"] for f in self.models["Wan-AI/Wan2.2-TI2V-5B"]["selected_files"]}
        self.assertIn("Wan2.2_VAE.pth", wan)
        self.assertIn("models_t5_umt5-xxl-enc-bf16.pth", wan)

    def test_demonstration_assets_excluded_from_image_video(self):
        for rid in ("Tongyi-MAI/Z-Image-Turbo", "Wan-AI/Wan2.2-TI2V-5B"):
            item = self.models[rid]
            self.assertTrue(item["excluded_files"])
            self.assertTrue(all(not f["path"].startswith(("assets/", "examples/"))
                                for f in item["selected_files"]))

    def test_datasets_have_origins_and_licenses(self):
        self.assertEqual(self.models["elyza/ELYZA-tasks-100"]["license_metadata"], "cc-by-sa-4.0")
        self.assertEqual(self.models["CohereLabs/aya_dataset"]["license_metadata"], "apache-2.0")
        self.assertTrue(any(f["path"].endswith(".parquet")
                            for f in self.models["CohereLabs/aya_dataset"]["selected_files"]))

    def test_no_downloading_or_rights_claim(self):
        self.assertFalse(self.m["approval"]["download_authorized"])
        self.assertFalse(self.m["approval"]["current_owner_D_drive_rehashed_this_round"])
        self.assertFalse(self.m["approval"]["licensed_acts_confirmed"])
        for row in self.m["models"]:
            self.assertFalse(row["actual_downloaded"])
            self.assertFalse(row["owner_file_hash_verified"])
            self.assertFalse(row["download_approved"])

    def test_reconciliation_all_154(self):
        rows = self.recon["per_active_asset"]
        self.assertEqual(len(rows), 154)
        self.assertEqual(len({x["repo_id"] for x in rows}), 154)
        statuses = [x["acquisition_evidence_status"] for x in rows]
        self.assertEqual(sum(x.startswith("REPORTED_PUBLISHER_HASH_VERIFIED") for x in statuses), 53)
        self.assertEqual(statuses.count("REPORTED_HOLD_GATED"), 1)
        self.assertEqual(statuses.count("NOT_REPORTED_AS_ACQUIRED"), 100)
        self.assertEqual(sum(x["next_wave_selected"] for x in rows), 8)


if __name__ == "__main__":
    unittest.main()
