"""v41 two primary source and territorial-license updates, no selection changes."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def get(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class TestV41(unittest.TestCase):
 def test_unchanged_selections(self):
  a=get("catalog/effective-portfolio-2026-11-15-v40.json")["items"]
  b=get("catalog/effective-portfolio-2026-11-15-v41.json")["items"]
  self.assertEqual(len(a),195);self.assertEqual(len(b),195)
  self.assertEqual([(x["repo_id"],x["portfolio_decision"]) for x in a],[(x["repo_id"],x["portfolio_decision"]) for x in b])
  self.assertEqual({x["repo_id"] for x,y in zip(a,b) if x!=y},{"ausboss/Qwen-Image-2.1-Consistency-LoRA","PrunaAI/P-H3-Image"})
 def test_source_rights_and_fail_closed(self):
  m=get("manifests/drafts/v40-qwen-image21-step1500.candidate.json")
  self.assertEqual(len(m["selected_source_files"]),5)
  self.assertEqual(m["selected_publisher_source_bytes"],159544753)
  v=get("catalog/effective-portfolio-2026-11-15-v41.json")
  p=next(x for x in v["items"] if x["repo_id"]=="PrunaAI/P-H3-Image")
  self.assertEqual(p["parameter_gate"]["known_three_component_subtotal"],46970622448)
  self.assertIsNone(p["parameter_gate"]["total_parameters"])
  self.assertEqual(p["license_detail"]["excluded_territories"],["EU","UK","Republic of Korea","USA"])
  self.assertEqual(get("queues/approved.json")["entries"],[])
 def test_current(self):
  c=get("catalog/CURRENT.json");self.assertEqual(get("catalog/effective-portfolio-2026-11-15-v41.json")["revision_id"],"v41-20261115")
  self.assertEqual(get(c["latest_active_readiness_audit"]["summary_path"])["summary"]["ready_to_approve"],0)
if __name__=="__main__":unittest.main()
