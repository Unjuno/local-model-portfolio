import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class DBSSourceResearch(unittest.TestCase):
 def test_scopes(self):
  m=json.loads((R/"manifests/drafts/2026-11-28-dbs-three-stem-source.candidate.json").read_text());s,h=m["source_models"];self.assertEqual(sum(f["bytes"] for f in s["source_files"]),4116715);self.assertEqual(sum(f["bytes"] for f in h["source_files"]),18891321);self.assertEqual(sum(f["bytes"] for f in m["runtime_source"]["source_files"]),206489);self.assertEqual(m["combined_selected_model_plus_code_reference_bytes"],4323204);self.assertFalse(m["download_enabled"]);self.assertFalse(m["approved_by_user"]);self.assertFalse(m["formal_catalog_promotion_performed"]);self.assertIsNone(m["complete_dependency_inclusive_bytes"])
 def test_decisions(self):
  e=json.loads((R/"catalog/research/2026-11-28-dbs-three-stem-separation-evidence.json").read_text());self.assertFalse(e["formal_catalog_promotion_performed"]);self.assertTrue(e["formal_add_proposal_pending"]);self.assertEqual(e["approved_downloads"],0);self.assertEqual(e["physical_deletions"],0);self.assertEqual(e["capacity"]["combined_reference_bytes"],4323204)
