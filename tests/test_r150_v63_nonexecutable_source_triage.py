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
   self.assertIsInstance(item["exact_publisher_bytes"],int)
   self.assertGreater(item["exact_publisher_bytes"],0)
  self.assertFalse(p["download_approved"])
  self.assertFalse(p["download_enabled"])
  self.assertFalse(p["license_text_reviewed"])
  self.assertFalse(p["third_party_runtime_code_audited"])
  self.assertEqual(p["publisher_full_repo_bytes_exact"],6590699556)
  self.assertTrue(p["publisher_sums_crosschecked_against_independent_publisher_tree_25_of_25"])
  fixed=read("manifests/drafts/r150-2026-11-22-wemm-timestral5m-publisher-fixed.candidate.json")
  shared=next(x for x in fixed["publisher_sources"] if x["repo_id"]==p["repo_id"])
  self.assertEqual(shared["immutable_revision_sha"],p["publisher_revision_sha_observed"])
  self.assertEqual(sum(x["bytes"] for x in shared["files"]),6590699556)
  self.assertEqual(len(shared["files"]),27)
  for x in p["selected_source_files_with_publisher_declared_hashes"]:
   other=next(y for y in shared["files"] if y["path"]==x["path"])
   self.assertEqual(other["bytes"],x["exact_publisher_bytes"])
   self.assertEqual(other["publisher_sha256_from_checksums"],x["publisher_declared_sha256"])
 def test_baseline_unchanged_and_no_apparent_approval(self):
  current=read("catalog/CURRENT.json")
  self.assertIn(current["revision_id"],("v63-20261122","v64-20261122","v65-20261122", "v66-20261124", "v67-20261124"))
  historical=read("catalog/effective-portfolio-2026-11-22-v63.json"); self.assertEqual((historical["counts"]["tracked"],historical["counts"]["active"]),(235,188))
  self.assertEqual(read("queues/approved.json")["entries"],[])
  d=read("catalog/decisions/2026-11-22-r150-post99-new-multimodal-and-uncensored-triage.json")
  q=read("queues/proposed-v63-r150-after99-plus-wemm-research-only.json")
  self.assertEqual(d["approved_downloads_added"],0)
  self.assertEqual(q["reported_acquired_models"],99)
  self.assertEqual(q["existing_candidate_repos"],11)
  self.assertEqual(q["existing_nonhold_reference_bytes"],68544170933)
  fixed=read("manifests/drafts/r150-2026-11-22-wemm-timestral5m-publisher-fixed.candidate.json")
  extra=next(x for x in fixed["publisher_sources"] if x["repo_id"]=="mistralai/Timestral-5M")
  self.assertEqual(extra["full_repo_publisher_bytes"],20854471)
  self.assertEqual(len(extra["files"]),6)
  self.assertEqual(sum(f["bytes"] for f in extra["files"]),20854471)
  self.assertEqual(extra["immutable_revision_sha"],"bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f")
  self.assertEqual(q["newly_researched_source_repo_count"],2)
  self.assertEqual(q["new_source_repos_exact_full_bytes"],6611554027)
  self.assertEqual(q["nonhold_new_plus_existing_reference_bytes_not_incremental_owner"],75155724960)

  self.assertEqual(q["approval_controls"]["entries_approved"],0)
  self.assertFalse(q["approval_controls"]["download_enabled"])
  self.assertTrue(q["canonical_235_tracked_188_active_unchanged"])
  phases={x["phase"]:x for x in q["priority_phases"]}
  self.assertEqual(len(phases),6)
  self.assertEqual(phases["P0B_NEW_ULTRATINY_TIMESERIES"]["repo_ids"],
                   ["mistralai/Timestral-5M"])
  self.assertEqual(phases["P0B_NEW_ULTRATINY_TIMESERIES"]["publisher_reference_bytes_exact"],20854471)
  self.assertEqual(phases["P1_NEW_COMPACT_VIDEO_AUDIT_ONLY"]["repo_ids"],
                   ["tencent/WeMM-Video-2B"])
  self.assertEqual(phases["P1_NEW_COMPACT_VIDEO_AUDIT_ONLY"]["publisher_reference_bytes_exact"],6590699556)
  self.assertTrue(all(x["download_approved"] is False for x in phases.values()))
if __name__ == "__main__": unittest.main()
