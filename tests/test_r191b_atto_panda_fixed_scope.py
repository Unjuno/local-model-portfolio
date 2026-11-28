import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

class TestR191bFixedSource(unittest.TestCase):
    def test_scope_sums_and_hashes(self):
        m=load("manifests/drafts/r191b-2026-11-28-atto-three-fixed-publisher-scopes.candidate.json")
        self.assertFalse(m["approved"])
        self.assertFalse(m["download_enabled"])
        self.assertIsNone(m["complete_dependency_inclusive_bytes"])
        self.assertIsNone(m["actual_owner_incremental_bytes"])
        rows={r["repo_id"]:r for r in m["source_models"]}
        self.assertEqual(set(rows), {"NeuML/colbert-atto-170-8d","NeuML/colbert-atto-840-8d","NeuML/colbert-atto-90k-32d"})
        for r in rows.values():
            self.assertEqual(len(r["source_files"]),11)
            self.assertEqual(sum(x["bytes"] for x in r["source_files"]),r["source_total_bytes"])
            for f in r["source_files"]:
                self.assertRegex(f["publisher_git_blob_sha1"],r"^[0-9a-f]{40}$")
                if f["publisher_lfs_sha256"] is not None:
                    self.assertRegex(f["publisher_lfs_sha256"],r"^[0-9a-f]{64}$")
        self.assertEqual(rows["NeuML/colbert-atto-90k-32d"]["source_total_bytes"],468771)
        self.assertEqual(rows["NeuML/colbert-atto-90k-32d"]["safetensors_total"],90304)
        for id in ("NeuML/colbert-atto-170-8d","NeuML/colbert-atto-840-8d"):
            self.assertEqual(rows[id]["decision"],"HOLD")
            self.assertEqual(rows[id]["candidate_selected_file_bytes"],0)
    def test_no_formal_change(self):
        d=load("catalog/decisions/2026-11-28-r191b-atto-panda-concurrent-reconciliation.json")
        for k in ("formal_additions","formal_replacements","formal_exclusions"):
            self.assertEqual(d[k],[])
        self.assertEqual(d["download_approved_bytes"],0)
        self.assertEqual(d["physical_files_deleted"],0)
        e=load("catalog/research/2026-11-28-r191b-atto-panda-fixed-scope-evidence.json")
        self.assertEqual(e["base_commit"],d["base_commit"])
        self.assertEqual(e["decisions"],d["comparisons"])
        self.assertEqual(e["source_manifest"],"manifests/drafts/r191b-2026-11-28-atto-three-fixed-publisher-scopes.candidate.json")
        self.assertEqual(d["additional_reference_bytes_vs_prior_weight_pointer"],106051)
        for id in ("DeepLearnPhysics/panda-v2-instance.pilarnet-m","DeepLearnPhysics/panda-v2-instance.tpcpp-10m"):
            self.assertTrue(any(x["repo_id"]==id and x["decision"]=="HOLD" for x in d["comparisons"]))

if __name__=="__main__":
    unittest.main()
