"""R74: fail-closed regression tests for the read-only v32 source-capacity verifier."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import verify_v32_primary_source_capacity as audit


class V32PrimaryCapacityTests(unittest.TestCase):
    def test_reconcile_complete_v32_real_metadata(self):
        result = audit.verify()
        self.assertEqual("PASS_SOURCE_SCOPE_ONLY", result["status"])
        self.assertEqual((135, 126, 9), (result["active"], result["old"], result["new"]))
        self.assertEqual(3_457_908_837_505, result["primary_bytes"])
        self.assertEqual(1_211_907_493, result["publisher_SHA_reused_bytes"])
        self.assertEqual(3_466_070_232_173, result["adjusted_source_scenario_bytes"])
        self.assertFalse(result["physical_capacity_verified"])
        self.assertFalse(result["download_approved"])

    def test_duplicate_v27_repo_refuses_unsafe_reconciliation(self):
        report = (audit.ROOT / audit.j.__globals__.get("ROOT", audit.ROOT) / "catalog/capacity/2026-11-07/v27/capacity-report.md") if False else (
            audit.ROOT / "catalog/capacity/2026-11-07/v27/capacity-report.md")
        data = report.read_text(encoding="utf-8")
        source_line = next(x for x in data.splitlines() if x.startswith("| orcarouter/"))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "catalog/capacity/2026-11-07/v27/capacity-report.md"
            target.parent.mkdir(parents=True)
            target.write_text(data + source_line + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate old ID"):
                audit.verify(root)

    def test_source_sha_mismatch_refuses_dedup(self):
        real_j = audit.j

        def changed(path):
            out = real_j(path)
            if path.endswith("2026-11-14-r62-ace-exact-source-scope-and-kumo-tag.json"):
                out = copy.deepcopy(out)
                out["QWEN_REUSE"]["reused_occurrences"][0]["bytes"] += 1
            return out

        with patch.object(audit, "j", changed):
            with self.assertRaisesRegex(ValueError, "Qwen SHA reuse mismatch"):
                audit.verify()

    def test_approved_queue_change_refuses_report(self):
        real_j = audit.j

        def changed(path):
            out = real_j(path)
            if path == "queues/approved.json":
                out = {"entries": [{"not_authorized": True}]}
            return out

        with patch.object(audit, "j", changed):
            with self.assertRaisesRegex(ValueError, "approval/physical disk"):
                audit.verify()


if __name__ == "__main__":
    unittest.main()
