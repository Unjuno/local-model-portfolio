"""V74 R170 metadata repair regression; no acquisition authorization."""
import collections
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class V74MetadataIntegrity(unittest.TestCase):
    def test_source_reference_summary(self):
        c = read("catalog/effective-portfolio-2026-11-27-v74.json")
        a = [i for i in c["items"] if i["portfolio_decision"] in ("select", "conditional")]
        def proxy(i):
            v = i.get("resource_screen", {}).get("source_all_repo_bytes")
            return v if v is not None else i.get("upstream_all_files_bytes_observed")
        s = c["screening_status"]
        self.assertEqual(s["count"], len(c["items"]))
        self.assertEqual(s["unknown_repo_bytes"], sum(proxy(i) is None for i in c["items"]))
        self.assertEqual(s["active_unknown_repo_bytes"], sum(proxy(i) is None for i in a))
        self.assertEqual(s["large_active_100gb_or_more"], sum(proxy(i) is not None and proxy(i) >= 100_000_000_000 for i in a))
        self.assertFalse(c["budget"]["physical_capacity_verified"])
    def test_blocker_summary_and_no_approval(self):
        r = read("catalog/readiness/v74-2026-11-27-r169-all210-gates.json")
        records = r["records"]
        self.assertEqual(len(records), 210)
        self.assertTrue(all(i["first_blocker"] in i["blocking_gates"] for i in records))
        self.assertEqual(collections.Counter(i["first_blocker"] for i in records), r["summary"]["first_blocker_counts"])
        self.assertEqual(collections.Counter(g for i in records for g in set(i["blocking_gates"])), r["summary"]["blocking_gate_counts"])
        self.assertTrue(all(not i["download_approved"] and not i["ready_to_acquire"] and i["final_selected_file_bytes"] is None for i in records))
        self.assertEqual(read("queues/approved.json")["entries"], [])
