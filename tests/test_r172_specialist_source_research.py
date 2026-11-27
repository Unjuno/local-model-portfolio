import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

class R172Research(unittest.TestCase):
    def test_sources_and_no_approval(self):
        m = read("manifests/drafts/r172-2026-11-28-indra-depthpro2-source-evidence-RESEARCH.candidate.json")
        self.assertTrue(m["research_only_nonexecutable"])
        self.assertFalse(m["download_approved"])
        self.assertFalse(m["model_payload_fetched"])
        self.assertEqual(len(m["source_repos"]), 4)
        self.assertEqual(sum(len(r["files"]) for r in m["source_repos"]), 56)
        self.assertEqual(sum(r["publisher_source_bytes"] for r in m["source_repos"]), 706047475)
        for r in m["source_repos"]:
            self.assertRegex(r["revision"], r"^[0-9a-f]{40}$")
            self.assertFalse(r["gated"])
            self.assertEqual(len({f["path"] for f in r["files"]}), r["file_count"])
            self.assertEqual(sum(f["bytes"] for f in r["files"]), r["publisher_source_bytes"])
            for f in r["files"]:
                self.assertRegex(f["git_oid"], r"^[0-9a-f]{40}$")
                if f["lfs_sha256"] is not None:
                    self.assertRegex(f["lfs_sha256"], r"^[0-9a-f]{64}$")
        self.assertIsNone(m["totals"]["exact_owner_incremental_bytes"])
        q = read("queues/proposed-v75-r172-cpu-ocr-and-metric-depth-UNAPPROVED.json")
        self.assertTrue(q["research_only_nonexecutable"])
        self.assertTrue(all(not e["download_approved"] and not e["ready_to_acquire"] for e in q["entries"]))
        self.assertEqual(read("queues/approved.json")["entries"], [])

    def test_baseline_novelty_and_selection_unchanged(self):
        a = read("catalog/effective-portfolio-2026-11-28-v75.json")["items"]
        self.assertEqual(len(a), 266)
        ids = {r["repo_id"] for r in a}
        self.assertFalse(ids & {"datalab-to/indra-ocr", "apple/DepthPro2-S", "apple/DepthPro2-focal", "apple/DepthPro2-B"})
        self.assertEqual(sum(r["portfolio_decision"] in ("select", "conditional") for r in a), 210)
        d = read("catalog/decisions/2026-11-28-r172-cpu-ocr-and-metric-depth-research.json")
        self.assertEqual(d["formal_model_additions"], 0)
        self.assertEqual(d["approved_downloads"], 0)
        self.assertEqual(d["physical_deletions"], 0)
