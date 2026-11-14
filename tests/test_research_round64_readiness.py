"""R64 current v32 complete 135-asset readiness: integrity and stop-gates."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path):
 q=(ROOT/path).resolve()
 if not q.is_relative_to(ROOT.resolve()):raise ValueError("unsafe source")
 return json.loads(q.read_text(encoding="utf-8"))
def key(x):return x["asset_kind"],x["repo_id"]
class R64(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ledger=load("catalog/audits/2026-11-15-v32-135-completion-readiness.json")
  cls.current=load("catalog/CURRENT.json")
  cls.portfolio=load("catalog/effective-portfolio-2026-11-14-v32.json")
 def test_all_135_exact_ids(self):
  rows=self.ledger["rows"]
  active=[x for x in self.portfolio["items"] if x["portfolio_decision"] in ("select","conditional")]
  self.assertEqual(len(active),135)
  self.assertEqual(len(rows),135)
  self.assertEqual(len(set(map(key,rows))),135)
  self.assertEqual(set(map(key,rows)),set(map(key,active)))
  self.assertEqual(self.ledger["summary"]["v27_primary_historical"],126)
  self.assertEqual(self.ledger["summary"]["post_v27_research"],9)
 def test_missing_final_locks_are_not_false_approvals(self):
  x=self.ledger
  self.assertEqual(x["summary"]["final_revision_and_bytes_both"],2)
  self.assertEqual(x["summary"]["missing_canonical_revision"],133)
  self.assertEqual(x["summary"]["missing_selected_bytes"],133)
  self.assertEqual(x["summary"]["unknown_parameters_active"],7)
  self.assertEqual(x["summary"]["conditional_gated"],17)
  self.assertEqual(x["summary"]["access_not_covered"],53)
  self.assertTrue(all(y["archival_final_lock"]=="BLOCKED"
       and not y["download_approved"]
       and not y["owner_permission_verified"]
       and "EXPLICIT_ACQUISITION_APPROVAL_NOT_GRANTED" in y["missing_gates"] for y in x["rows"]))
  self.assertEqual(load("queues/approved.json")["entries"],[])
 def test_budget_is_only_source_arithmetic(self):
  c=self.ledger["capacity"]
  self.assertEqual(c["v27_sha_union_bytes"],3417685712585)
  self.assertEqual(c["new_8_source_scopes_bytes"],24342724173)
  self.assertEqual(c["ACE_XL_shared_sha_aware_increment_bytes"],24041795415)
  self.assertEqual(c["known_source_scope_arithmetic_bytes"],3466070232173)
  self.assertEqual(c["nominal_empty_4tb_after_floor_arithmetic_margin_bytes"],333929767827)
  self.assertIsNone(c["full_135_archive_bytes"])
  self.assertIsNone(c["actual_owner_disk_bytes"])
 def test_pruna_header_scope_not_final_gate(self):
  r=next(x for x in self.ledger["rows"] if x["repo_id"]=="PrunaAI/P-H3-Image")
  self.assertEqual(r["parameter_gate"],"UNVERIFIED_BLOCK_FINAL_LOCK")
  self.assertEqual(r["specialized_source_research"]["stored_elements"],49635347496)
  self.assertTrue(r["specialized_source_research"]["not_unique_trainable_count"])
 def test_current_summary_link(self):
  self.assertEqual(self.current["revision_id"],"v32-20261114")
  self.assertEqual(self.current["latest_active_readiness_audit"]["summary_path"],"catalog/audits/2026-11-15-v32-135-completion-readiness.json")
  self.assertEqual(self.current["latest_active_readiness_audit"]["ready_to_approve"],0)
if __name__=="__main__":unittest.main()
