"""Offline regression for v57 publisher-original metadata only; no model payload is fetched."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class V57SparkHereticSourceTest(unittest.TestCase):
    def test_canonical_and_selection_counts(self):
        # Historical v57 assertion; CURRENT may move to v58 or later.
        x = load("catalog/effective-portfolio-2026-11-20-v57.json")
        self.assertEqual(x["revision_id"], "v57-20261120")
        self.assertEqual((x["counts"]["tracked"], x["counts"]["active"], x["counts"]["models"], x["counts"]["datasets"]), (213, 166, 187, 26))
        self.assertEqual(x["counts"]["by_decision"]["select"], 53)
        self.assertEqual(x["counts"]["by_decision"]["conditional"], 113)
        self.assertEqual(x["counts"]["parameter_gate"]["PASS_TOTAL_PARAMS_LT_150B"], 163)
        self.assertEqual(len(x["items"]), 213)
        self.assertEqual(len({(r["asset_kind"], r["repo_id"]) for r in x["items"]}), 213)
        self.assertEqual(len(load("queues/approved.json")["entries"]), 0)

    def test_source_manifest_immutable_and_complete(self):
        x = load("manifests/drafts/r133-2026-11-20-spark4b-and-heretic9b-bf16-mtp-originals.candidate.json")
        self.assertEqual((x["source_files"], x["publisher_lfs_sha256_count"], x["publisher_source_bytes"]), (41, 8, 27570829651))
        self.assertFalse(x["download_approved"])
        self.assertFalse(x["owner_hdd_current_verified"])
        self.assertEqual([r["publisher_source_file_count"] for r in x["sources"]], [22, 19])
        for repo in x["sources"]:
            self.assertEqual(len(repo["revision"]), 40)
            files = repo["all_selected_source_files"]
            self.assertEqual(sum(r["bytes"] for r in files), repo["publisher_selected_source_bytes"])
            self.assertEqual(len({r["path"] for r in files}), len(files))
            self.assertTrue(all(r.get("git_blob_sha1") or r.get("publisher_lfs_sha256") for r in files))
            self.assertTrue(all(not r["owner_local_hash_verified"] for r in files))
        names = [r["path"] for r in x["sources"][1]["all_selected_source_files"]]
        self.assertIn("model-mtp.safetensors", names)
        line = x["model_lineage"][1]
        self.assertEqual(line["mtptensors_in_index"], 15)
        self.assertEqual(line["hub_safetensors_total_including_mtp"] - line["main_index_total_excluding_mtp"], 243290624)

    def test_every_derived_scope_active_and_stopped(self):
        # Check immutable historical sidecars, not the moving CURRENT pointers.
        q = load("queues/proposed-v57-2026-11-20.json")
        a = load("catalog/access/2026-11-20-v57-conditional-hub-gates.json")
        b = load("catalog/preparation/2026-11-20-insurance-bundles-v57.json")
        r = load("catalog/readiness/v57-2026-11-20-r133-all166-gates.json")
        self.assertEqual((len(q["candidates"]), len(a["entries"]), len(b["items"]), len(r["records"])), (166, 113, 166, 166))
        self.assertEqual((r["summary"]["blocked_any"], r["summary"]["ready_to_approve"], r["summary"]["downloads_approved"]), (166, 0, 0))
        for repo_id in ("FrostWolfAI/Spark-X2.6-4B-abliterated", "xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic"):
            for rows in (q["candidates"], a["entries"], b["items"], r["records"]):
                found = [v for v in rows if v["repo_id"] == repo_id]
                self.assertEqual(len(found), 1)
                self.assertFalse(found[0]["download_approved"] if "download_approved" in found[0] else found[0]["download_authorized"])

if __name__ == "__main__":
    unittest.main()
