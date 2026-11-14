"""R64 asset/source integration is static and never downloads model payloads."""
import json
import unittest
from pathlib import Path
from scripts.archive_preflight import audit_source_manifest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "catalog/readiness/v32-2026-11-15-r64-all-active.json"
PILOT = ROOT / "manifests/drafts/r64-eight-source-scopes.candidate.json"
APPROVED = ROOT / "queues/approved.json"

class R64ReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.pilot = json.loads(PILOT.read_text(encoding="utf-8"))

    def test_catalog_is_unique_and_fail_closed(self):
        rows = self.ledger["records"]
        self.assertEqual(135, len(rows))
        self.assertEqual(135, len({(r["asset_kind"], r["repo_id"]) for r in rows}))
        self.assertEqual(53, sum(x["decision"] == "select" for x in rows))
        self.assertEqual(82, sum(x["decision"] == "conditional" for x in rows))
        self.assertEqual(9, sum(x["source_evidence"]["classification"] != "HISTORICAL_V27_SOURCE_CENSUS_ONLY" for x in rows))
        self.assertEqual(7, sum(x["total_parameters_gate"] == "UNVERIFIED_BLOCK_FINAL_LOCK" for x in rows))
        self.assertTrue(all(not r["acquisition_ready"] and not r["download_authorized"] for r in rows))

    def test_source_pilot_matches_existing_read_only_preflight_contract(self):
        p = self.pilot
        self.assertEqual([], audit_source_manifest(p))
        self.assertEqual(9, len(p["repositories"]))
        self.assertEqual(8, len(p["packages"]))
        self.assertEqual(91, sum(x["file_count"] for x in p["repositories"]))
        self.assertEqual(38_519_866_446, sum(x["selected_bytes"] for x in p["repositories"]))
        self.assertTrue(all(not x["local_hash_verified"] and not x["body_downloaded"]
                            for repo in p["repositories"] for x in repo["files"]))
        self.assertTrue(all(not p[k] for k in ("executable", "approved_manifest", "download_authorized", "auto_execute", "auto_seed")))

    def test_no_implicit_duplicate_original_or_auto_download(self):
        repos = {x["repo_id"]: x for x in self.pilot["repositories"]}
        self.assertEqual(7, repos["nvidia/RFD4-Proteina"]["file_count"])
        self.assertNotIn("Qwen/Qwen3.8-27B", repos)
        self.assertTrue(all(not f["path"].startswith("acestep-v15-turbo/")
                            for f in repos["ACE-Step/Ace-Step1.5"]["files"]))
        self.assertTrue(all(not p["download_approved"] for p in self.pilot["packages"]))
        self.assertEqual([], json.loads(APPROVED.read_text(encoding="utf-8"))["entries"])

if __name__ == "__main__":
    unittest.main()
