"""R150 research-only checks; no network, weights, model code or approvals."""
import json, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def read(path): return json.loads((ROOT / path).read_text(encoding="utf-8"))
class R150SourceSafety(unittest.TestCase):
 def test_publisher_digest_manifest_does_not_authorize_download(self):
  p=read("manifests/drafts/r150-2026-11-22-wemm-video2b-publisher-sha256.candidate.json")
  self.assertEqual(p["publisher_revision_sha_observed"], "821690998399cac0f55bb7f7f805ebafa650c3a4")
  self.assertEqual(p["published_file_tree_count_observed"],27)
  self.assertEqual(len(p["selected_source_files_with_publisher_declared_hashes"]),25)
  self.assertEqual(len({x["path"] for x in p["selected_source_files_with_publisher_declared_hashes"]}),25)
  self.assertEqual(sorted(p["missing_publisher_SHA256_entries"]),[".gitattributes","SHA256SUMS"])
  for item in p["selected_source_files_with_publisher_declared_hashes"]:
   self.assertEqual(len(item["publisher_declared_sha256"]),64)
   int(item["publisher_declared_sha256"],16)
   self.assertFalse(item["owner_local_sha256_verified"])
   self.assertIsNone(item["exact_publisher_bytes"])
  self.assertFalse(p["download_approved"])
  self.assertFalse(p["download_enabled"])
  self.assertFalse(p["license_text_reviewed"])
  self.assertFalse(p["third_party_runtime_code_audited"])
  self.assertIsNone(p["publisher_full_repo_bytes_exact"])
 def test_baseline_unchanged_and_no_apparent_approval(self):
  current=read("catalog/CURRENT.json")
  self.assertEqual(current["revision_id"],"v63-20261122")
  self.assertEqual((current["expected"]["tracked"],current["expected"]["active"]),(235,188))
  self.assertEqual(read("queues/approved.json")["entries"],[])
  d=read("catalog/decisions/2026-11-22-r150-post99-new-multimodal-and-uncensored-triage.json")
  q=read("queues/proposed-v63-r150-after99-plus-wemm-research-only.json")
  self.assertEqual(d["approved_downloads_added"],0)
  self.assertEqual(q["reported_acquired_models"],99)
  self.assertEqual(q["existing_candidate_repos"],11)
  self.assertEqual(q["existing_nonhold_reference_bytes"],68544170933)
  self.assertEqual(q["approval_controls"]["entries_approved"],0)
  self.assertFalse(q["approval_controls"]["download_enabled"])
  self.assertTrue(q["canonical_235_tracked_188_active_unchanged"])
  self.assertEqual(len(q["priority_phases"]),5)
  self.assertEqual(q["priority_phases"][1]["repo_ids"],["tencent/WeMM-Video-2B"])
  self.assertIsNone(q["priority_phases"][1]["publisher_reference_bytes_exact"])
if __name__ == "__main__": unittest.main()
