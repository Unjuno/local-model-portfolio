"""Offline metadata-only regression for v58 original model archive selection."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

class V58SourceAndCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.curr = load("catalog/CURRENT.json")
        cls.eff = load("catalog/effective-portfolio-2026-11-21-v58.json")
        cls.old = load("catalog/effective-portfolio-2026-11-20-v57.json")
        cls.overlay = load("catalog/revisions/v58-2026-11-21.json")
        cls.src = load("manifests/drafts/r137-2026-11-21-inkling2mini-and-dettato-four-publisher-sources.candidate.json")
        cls.queue = load("queues/proposed-v58-2026-11-21.json")
        cls.access = load("catalog/access/2026-11-21-v58-conditional-hub-gates.json")
        cls.dep = load("catalog/preparation/2026-11-21-insurance-bundles-v58.json")
        cls.ready = load("catalog/readiness/v58-2026-11-21-r137-all171-gates.json")

    def test_current_and_five_added_immutable(self):
        self.assertIn(self.curr["revision_id"], ("v58-20261121", "v59-20261121", "v60-20261122", "v61-20261122", "v62-20261122", "v63-20261122", "v64-20261122","v65-20261122", "v66-20261124", "v67-20261124","v68-20261125","v69-20261125","v70-20261125"))
        self.assertIn(self.curr["materialized_catalog_path"],
                         ("catalog/effective-portfolio-2026-11-21-v58.json",
                          "catalog/effective-portfolio-2026-11-21-v59.json",
                          "catalog/effective-portfolio-2026-11-22-v60.json",
                          "catalog/effective-portfolio-2026-11-22-v61.json",
                          "catalog/effective-portfolio-2026-11-22-v62.json",
                          "catalog/effective-portfolio-2026-11-22-v63.json","catalog/effective-portfolio-2026-11-22-v64.json", "catalog/effective-portfolio-2026-11-22-v65.json", "catalog/effective-portfolio-2026-11-24-v66.json", "catalog/effective-portfolio-2026-11-24-v67.json","catalog/effective-portfolio-2026-11-25-v68.json","catalog/effective-portfolio-2026-11-25-v69.json","catalog/effective-portfolio-2026-11-25-v70.json"))
        self.assertGreaterEqual(self.curr["expected"]["tracked"], 218)
        self.assertGreaterEqual(self.curr["expected"]["active"], 171)
        self.assertEqual(self.eff["counts"]["tracked"], 218)
        self.assertEqual(self.eff["counts"]["active"], 171)
        self.assertEqual(self.eff["counts"]["models"], 192)
        self.assertEqual(self.eff["counts"]["datasets"], 26)
        self.assertEqual(len(self.overlay["additions"]), 5)
        self.assertEqual(len(self.old["items"]), 213)
        for old, new in zip(self.old["items"], self.eff["items"]):
            self.assertEqual(old, new)
        self.assertEqual(len({(x["asset_kind"], x["repo_id"])
                              for x in self.eff["items"]}), 218)

    def test_publisher_frozen_source_all_components(self):
        src = self.src
        self.assertEqual(src["source_repos"], 5)
        self.assertEqual(src["source_files"], 39)
        self.assertEqual(src["publisher_source_bytes"], 20_312_109_868)
        self.assertEqual(src["publisher_lfs_sha256_refs"], 17)
        self.assertEqual(src["dettato"]["all_four_repo_source_bytes"], 120_466_597)
        self.assertEqual(src["dettato"]["all_four_repo_source_file_count"], 25)
        self.assertEqual(src["dettato"]["original_model_weight_bytes"], 112_758_556)
        self.assertEqual(src["dettato"]["source_code"]["commit"],
                         "9b724251794f2bbd5eaa43e54734e5a251829130")
        observed = set()
        count_files = count_sha = count_bytes = 0
        for x in src["publisher_original_sources"]:
            self.assertNotIn(x["repo_id"], observed)
            observed.add(x["repo_id"])
            self.assertEqual(len(x["immutable_revision_sha"]), 40)
            self.assertFalse(x["source_access"]["private"])
            self.assertFalse(x["source_access"]["gated"])
            self.assertEqual(len(x["files"]), x["source_file_count"])
            count_files += x["source_file_count"]
            count_bytes += x["publisher_total_source_bytes"]
            count_sha += x["lfs_sha256_ref_count"]
            self.assertEqual(sum(f["bytes"] for f in x["files"]),
                             x["publisher_total_source_bytes"])
            for f in x["files"]:
                self.assertEqual(len(f["git_blob_sha1"]), 40)
                if f["publisher_lfs_sha256"] is not None:
                    self.assertEqual(len(f["publisher_lfs_sha256"]), 64)
                self.assertFalse(f["local_sha256_verified"])
                self.assertFalse(x["download_approved"])
        self.assertEqual((count_files, count_bytes, count_sha),
                         (39, 20_312_109_868, 17))

    def test_dettato_learned_components_and_inkling_mtp(self):
        m = self.src
        stages = m["dettato"]["stage_models"]
        self.assertEqual(len(stages), 4)
        self.assertEqual(sum(x["hub_float_parameters"] for x in stages), 28_144_065)
        self.assertEqual(m["inkling"]["mtp_header_tensor_count"], 54)
        self.assertEqual(m["inkling"]["mtp_header_exact_BF16_serialized_elements"],
                         317_897_872)
        self.assertEqual(m["inkling"]["main_publisher_safetensors_logical_total"],
                         26_388_646_440)
        self.assertEqual(m["inkling"]["reported_total_plus_additional_MTP"],
                         26_706_544_312)
        for x in self.overlay["additions"]:
            self.assertEqual(x["parameter_gate"]["status"],
                             "PASS_TOTAL_PARAMS_LT_150B")
            self.assertLess(x["parameter_gate"]["total_parameters"],
                            150_000_000_000)
            self.assertEqual(x["candidate_selected_source_file_count"],
                             len(x["candidate_selected_source_files"]))
            self.assertFalse(x["download_approved"])
            self.assertFalse(x["download_ready"])
        self.assertNotIn(m["varloop_research_alternative"]["repo_id"],
                         {x["repo_id"] for x in self.eff["items"]})

    def test_sidecar_coverage_fail_closed(self):
        self.assertEqual(len(self.queue["candidates"]), 171)
        self.assertEqual(len(self.access["entries"]), 118)
        self.assertEqual(len(self.dep["items"]), 171)
        self.assertEqual(len(self.ready["records"]), 171)
        self.assertEqual(self.ready["summary"]["blocked_any"], 171)
        self.assertEqual(self.ready["summary"]["ready_to_approve"], 0)
        self.assertEqual(self.ready["summary"]["downloads_approved"], 0)
        self.assertFalse(self.queue["approved"])
        self.assertFalse(self.queue["download_enabled"])
        self.assertFalse(self.dep["download_enabled"])
        self.assertFalse(self.ready["download_approved"])
        self.assertFalse(self.ready["ready_to_acquire"])
        self.assertEqual(load("queues/approved.json")["entries"], [])
        for asset in self.overlay["additions"]:
            record = next(x for x in self.ready["records"]
                          if x["repo_id"] == asset["repo_id"])
            self.assertFalse(record["ready_to_acquire"])
            self.assertFalse(record["download_approved"])
            self.assertFalse(record["offline_restore_verified"])

if __name__ == "__main__":
    unittest.main()
