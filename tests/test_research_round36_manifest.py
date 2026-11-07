"""R36 non-executable pinned source files: tests do not download or execute AI weights."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts.archive_preflight import audit_source_manifest, inspect_archive

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manifests/drafts/r36-22-source-closure-weight-only.candidate.json"

class R36NonExecutableDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.repos = {r["key"]: r for r in cls.plan["repositories"]}
        cls.packages = {p["key"]: p for p in cls.plan["packages"]}

    def test_structural_preflight_has_no_errors(self):
        self.assertEqual(audit_source_manifest(self.plan), [])
        self.assertEqual(len(self.repos), 6)
        self.assertEqual(len(self.packages), 4)
        self.assertEqual(sum(r["file_count"] for r in self.repos.values()), 20)

    def test_source_bytes_sum_to_exact_pinned_components(self):
        for row in self.repos.values():
            self.assertEqual(row["selected_bytes"], sum(f["bytes"] for f in row["files"]))
            self.assertEqual(row["file_count"], len(row["files"]))
            self.assertEqual(len(row["revision"]), 40)
            self.assertTrue(all(len(f["source_sha256"]) == 64 for f in row["files"]))
        expected = 52_879_817_929
        self.assertEqual(self.plan["potential_incremental_bytes_without_existing_hash_reuse"], expected)
        self.assertEqual(sum(p["selected_model_and_support_bytes"] for p in self.packages.values()), expected)

    def test_distinct_learned_pairs_are_not_dropped(self):
        self.assertEqual(self.packages["liquid-vl-with-dspark"]["repository_keys"],
                         ["lfm25-vl-target", "lfm25-vl-dspark"])
        self.assertEqual(self.packages["lilavati-and-checker"]["repository_keys"],
                         ["lilavati-generator", "lilavati-checker"])
        gen = self.repos["lilavati-generator"]["files"][0]
        chk = self.repos["lilavati-checker"]["files"][0]
        self.assertEqual(gen["bytes"], chk["bytes"])
        self.assertNotEqual(gen["source_sha256"], chk["source_sha256"])

    def test_heretic_and_fineweb_are_selected_not_full_mirrors(self):
        self.assertEqual(self.packages["rvn-heretic-q4"]["selected_model_and_support_bytes"], 17_176_647_232)
        ds = self.repos["fineweb-edu-10bt"]
        self.assertEqual(ds["repo_type"], "dataset")
        self.assertEqual(ds["file_count"], 14)
        self.assertTrue(all(x["path"].startswith("sample/10BT/") for x in ds["files"]))
        self.assertEqual(ds["selected_bytes"], 28_518_193_415)

    def test_no_download_or_owner_approval_in_source_lock(self):
        for key in ("executable", "approved_manifest", "download_authorized", "auto_execute", "auto_seed"):
            self.assertIs(self.plan[key], False)
        for row in self.repos.values():
            self.assertFalse(row["dependencies_complete"])
            self.assertFalse(row["rights_reviewed"])
            self.assertTrue(all(not f["local_hash_verified"] and not f["body_downloaded"] for f in row["files"]))
        self.assertEqual(self.plan["owner_approval_gate"], "BLOCKED")
        self.assertEqual(self.plan["license_gate"], "UNREVIEWED")

    def test_local_probe_cannot_convert_metadata_to_download_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = inspect_archive(self.plan, Path(tmp), {},
                                     hash_existing=False,
                                     staging_reserve_bytes=None,
                                     existing_archive_bytes=None)
            self.assertEqual(result["capacity"]["overall_gate"], "UNCERTAIN")
            self.assertEqual(result["capacity"]["confirmed_reused_bytes"], 0)
            self.assertIs(result["download_authorized"], False)
            self.assertIs(result["capacity"]["real_download_permitted"], False)

    def test_illicit_flag_mutation_is_detected(self):
        plan = dict(self.plan)
        plan["download_authorized"] = True
        self.assertTrue(any("non-executable flag violated" in x
                            for x in audit_source_manifest(plan)))

if __name__ == "__main__":
    unittest.main()
