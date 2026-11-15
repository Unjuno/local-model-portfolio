"""V39 primary publisher original, outside VQ dependency, coherent nonexecutable queue."""
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(p):return json.loads((R/p).read_text(encoding="utf-8"))
def k(x):return x["asset_kind"],x["repo_id"].lower()
class V39(unittest.TestCase):
 def test_append_exact_original_no_approved_weights(self):
  old=J("catalog/effective-portfolio-2026-11-15-v38.json")
  new=J("catalog/effective-portfolio-2026-11-15-v39.json")
  overlay=J("catalog/revisions/v39-2026-11-15.json")
  self.assertEqual(new["items"][:193],old["items"])
  self.assertEqual(new["items"][193:],overlay["additions"])
  self.assertEqual(len({k(x) for x in new["items"]}),194)
  self.assertEqual(new["counts"]["active"],147)
  self.assertEqual(new["counts"]["models"],168)
  self.assertEqual(new["counts"]["datasets"],26)
  self.assertEqual(overlay["additions"][0]["repo_id"],"XiaomiRobotics/Xiaomi-Robotics-U0-4B")
  self.assertFalse(any(x["download_approved"] for x in new["items"]))
 def test_external_vq_original_with_no_pickle_alternate(self):
  s=J("catalog/research/2026-11-15-r89-xiaomi-u0-4b-immutable-selected-source.json")
  self.assertEqual(s["total_source_selected_file_count"],18)
  self.assertEqual(s["total_source_selected_bytes"],11991440188)
  self.assertEqual([len(r["selected_files"]) for r in s["repos"]],[12,6])
  self.assertEqual([r["selected_bytes"] for r in s["repos"]],[10170001048,1821439140])
  self.assertTrue(all(not f["weight_payload_fetched"] and not f["owner_local_sha_verified"] for r in s["repos"] for f in r["selected_files"]))
  self.assertNotIn("model.ckpt",{f["path"] for f in s["repos"][1]["selected_files"]})
  self.assertNotIn("config.yaml",{f["path"] for f in s["repos"][1]["selected_files"]})
  self.assertFalse(s["download_authorized"])
if __name__=="__main__":unittest.main()
