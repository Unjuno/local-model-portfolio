import ast, json, unittest
from collections import Counter
from pathlib import Path
R = Path(__file__).resolve().parents[1]
def load(p): return json.loads((R / p).read_text(encoding="utf-8"))
def key(x): return x["asset_kind"], x["repo_id"]
class IBEMFormal(unittest.TestCase):
    def test_unchanged_and_overlay(self):
        old=load("catalog/effective-portfolio-2026-11-28-v99.json")["items"]
        new=load("catalog/effective-portfolio-2026-11-28-v100.json")["items"]
        self.assertEqual(new[:-1],old)
        self.assertEqual(len(set(map(key,new))),294)
        self.assertEqual(new[-1],load("catalog/revisions/v100-2026-11-28.json")["additions"][0])
        self.assertTrue(new[-1]["research_only_nonexecutable"])
        self.assertIsNone(new[-1]["selected_file_bytes"])
        self.assertEqual(new[-1]["parameter_gate"]["total_parameters"],14157152)
    def test_source_scope(self):
        m=load("manifests/drafts/r190-2026-11-28-ibem-im2typst-original.candidate.json")
        self.assertEqual(sum(x["bytes"] for x in m["runtime_source"]["source_files"]),2417253)
        self.assertEqual(len(m["runtime_source"]["source_files"]),182)
        self.assertEqual(m["known_partial_source_bytes"],56693087+2417253)
        self.assertIsNone(m["complete_dependency_inclusive_bytes"])
        self.assertFalse(m["download_enabled"])
        self.assertEqual(m["source_models"][0]["source_files"][0]["publisher_lfs_sha256"],"8b7972f440556f328828f9e90247f266d9fbc59266f5ff8b23f7bce21f717924")
    def test_join_and_gate(self):
        c=load("catalog/effective-portfolio-2026-11-28-v100.json")
        active={key(x) for x in c["items"] if x["portfolio_decision"] in ("select","conditional")}
        conditional={key(x) for x in c["items"] if x["portfolio_decision"]=="conditional"}
        self.assertEqual(len(active),238)
        self.assertEqual(len(conditional),182)
        for p,k,expect in [("queues/proposed-v100-2026-11-28.json","candidates",active),("catalog/preparation/2026-11-28-insurance-bundles-v100.json","items",active),("catalog/readiness/v100-2026-11-28-r196-all238-gates.json","records",active),("catalog/access/2026-11-28-v100-conditional-hub-gates.json","entries",conditional)]:
            rows=load(p)[k]
            self.assertEqual(set(map(key,rows)),expect)
            self.assertEqual(len(rows),len(expect))
        rd=load("catalog/readiness/v100-2026-11-28-r196-all238-gates.json")
        self.assertTrue(all(not x["download_approved"] and not x["ready_to_acquire"] for x in rd["records"]))
        self.assertEqual(rd["summary"]["blocking_gate_counts"],dict(Counter(g for x in rd["records"] for g in x["blocking_gates"])))
        self.assertEqual(load("queues/approved.json")["entries"],[])
        self.assertEqual(load("catalog/execution/2026-11-19-acquisition-ledger.json")["summary"]["models_verified"],133)
        current=load("catalog/CURRENT.json")
        if current["revision_id"]=="v100-20261128":
            self.assertEqual(current["materialized_catalog_path"],"catalog/effective-portfolio-2026-11-28-v100.json")
            self.assertEqual(current["expected"]["active"],238)
    def test_no_synthetic_v93_approval(self):
        source=(R/"scripts/build_v93_plan.py").read_text(encoding="utf-8")
        ast.parse(source)
        self.assertNotIn("APPROVAL.write_text",source)
        self.assertNotIn('"approved_by_user": True',source)
        self.assertNotIn('"download_enabled": True',source)
if __name__=="__main__": unittest.main()
