"""Offline R119 archival source selection and acquisition authorization regression."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "download_r115_windows.py"
MANIFEST = ROOT / "queues" / "proposed-v49-r119-next7-public-source-entries.json"
SENSE = ROOT / "manifests" / "drafts" / "r117-2026-11-19-sensenova-loop9b-public-bf16-master-and-official-gated.json"

spec = importlib.util.spec_from_file_location("archive_windows", SCRIPT)
app = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(app)


class R119ResearchAndAuthorization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.sense = json.loads(SENSE.read_text(encoding="utf-8"))

    def test_seven_immutable_source_entries_are_valid(self):
        valid = app.validate_manifest(self.plan)
        self.assertEqual(len(valid), 7)
        self.assertEqual(self.plan["unique_model_outcomes"], 6)
        self.assertEqual(self.plan["supporting_code_bundles"], 1)
        self.assertEqual(self.plan["go_scope_bytes"], 258965078216)
        self.assertEqual(sum(x["source_bytes"] for x in valid), 258965078216)
        self.assertFalse(any(x["gated"] for x in valid))
        self.assertTrue(all(x["source_revision"] and len(x["source_revision"]) == 40
                            for x in valid))

    def test_not_saving_duplicate_quantization_variants(self):
        valid = app.validate_manifest(self.plan)
        s = next(e for e in valid if e["source_repo_id"] == "sensenova/SenseNova-Loop-9B-GGUF")
        files = {f["path"] for f in s["files"]}
        self.assertEqual({x for x in files if x.endswith(".gguf")},
                         {"SenseNova-Loop-9B-BF16.gguf", "mmproj-SenseNova-Loop-9B-F16.gguf"})
        self.assertEqual(self.sense["observed_official"]["gated"], "auto")
        self.assertIs(self.sense["public_release_fallback"]["gated"], False)

    def test_preview_code_only_when_identical_to_official(self):
        valid = app.validate_manifest(self.plan)
        p = next(e for e in valid if e["source_repo_id"].endswith("SenseNova-Loop-9B-Preview"))
        self.assertEqual({x["path"] for x in p["files"]},
                         {"modeling_sensenova_loop.py", "chat_template.jinja"})
        self.assertTrue(all(x["identical_to_official_current"] for x in
                            self.sense["cross_repo_publisher_code_support"]["source_files"]))
        self.assertEqual(len(self.sense["cross_repo_publisher_code_support"]
                             ["preview_specific_files_excluded"]), 2)

    def test_mit_computer_agent_and_apache_memory_writer_only(self):
        valid = app.validate_manifest(self.plan)
        by = {e["source_repo_id"]: e for e in valid}
        self.assertEqual(by["microsoft/Fara1.5-27B"]["license_metadata"], "mit")
        self.assertEqual(by["tencent/Hy-Memory-30B-A3B"]["license_metadata"], "apache-2.0")
        self.assertEqual(by["microsoft/Fara1.5-27B"]["source_file_count"], 22)
        self.assertEqual(by["tencent/Hy-Memory-30B-A3B"]["source_file_count"], 59)

    def test_no_unapproved_transfer(self):
        valid = app.validate_manifest(self.plan)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "approval.json"
            path.write_text('{"schema_version":1,"entries":[]}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "No explicitly approved"):
                app.assert_explicit_approved_sources(valid, path)

    def test_previously_verified_report_not_claimed_as_new_owner_checksum(self):
        self.assertTrue(self.plan["reported_prior_only_not_independent_disk_verified"])
        self.assertFalse(self.plan["owner_D_drive_hdd_independently_verified_here"])


if __name__ == "__main__":
    unittest.main()
