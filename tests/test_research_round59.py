"""R59 static evidence and no-download integrity checks; stdlib, no model loading."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
    q=(ROOT/p).resolve()
    if not q.is_relative_to(ROOT.resolve()):raise ValueError("path escapes repository")
    return json.loads(q.read_text(encoding="utf-8"))
class R59(unittest.TestCase):
    def setUp(self):
        self.a=read("catalog/research/2026-11-14-r59-maya2-drama3-cross-repo-components.json")
        self.d=read("manifests/drafts/r59-maya2-drama3-four-repo-source-subsets.candidate.json")
        self.s={x["repo_id"]:x for x in self.a["source_scopes"]}
    def test_all_four_immutable_and_hash_evidence(self):
        self.assertEqual(len(self.s),4)
        self.assertEqual(len(self.d["source_subsets"]),4)
        self.assertEqual(self.d["total_source_file_refs"],48)
        self.assertEqual(self.d["total_source_subset_bytes"],sum(x["selected_bytes"] for x in self.s.values()))
        self.assertFalse(self.d["download_enabled"])
        self.assertFalse(self.d["approved"])
        for x in self.s.values():
            self.assertRegex(x["immutable_revision_sha"],r"^[a-f0-9]{40}$")
            self.assertEqual(x["selected_bytes"],sum(f["size_bytes"] for f in x["files"]))
            self.assertEqual(x["selected_path_count"],len(x["files"]))
            self.assertFalse(x["download_approved"])
            self.assertFalse(x["owner_access_authorized"])
            self.assertFalse(x["license_full_text_and_third_party_notices_signoff"])
            for f in x["files"]:
                self.assertRegex(f["publisher_git_blob_sha1"],r"^[a-f0-9]{40}$")
                if f["publisher_lfs_sha256"]: self.assertRegex(f["publisher_lfs_sha256"],r"^[a-f0-9]{64}$")
                self.assertFalse(f["local_payload_hash_verified"])
    def test_maya_mimi_ecapa_learned_dependencies(self):
        m=self.a["maya2_bundle"]
        self.assertEqual(m["three_repo_weight_bytes"],5478382531)
        self.assertEqual(m["external_mimi_parameter_count"],96151393)
        self.assertIsNone(m["ecapa_complete_learned_tensor_count"])
        self.assertIsNone(m["complete_pipeline_parameter_count"])
        self.assertEqual(self.s["maya-research/maya2-native"]["selected_weight_file_count"],2)
        self.assertEqual(self.s["kyutai/mimi"]["selected_weight_file_count"],1)
        self.assertEqual(self.s["speechbrain/spkrec-ecapa-voxceleb"]["selected_weight_file_count"],3)
    def test_drama_codec_not_ignored_or_loaded(self):
        f=self.a["drama3_bundle"]
        self.assertEqual(f["codec_file_bytes"],1871099728)
        self.assertEqual(f["codec_file_sha256"],"74fc41c5a7151c6f350af8bd7e5d6e3accfcc7f3dfbfac23afd35af07052bb2f")
        self.assertEqual(self.s["fishaudio/drama-3"]["selected_weight_file_count"],16)
        self.assertIsNone(f["codec_learned_parameter_count"])
        self.assertIn("pickle",f["codec_serialization_warning"].lower())
    def test_current_selection_unchanged(self):
        current=read("catalog/CURRENT.json")
        historical=read("catalog/effective-portfolio-2026-11-14-v32.json")
        self.assertEqual(len(historical["items"]),182)
        self.assertEqual(sum(x["portfolio_decision"] in ("select","conditional") for x in historical["items"]),135)
        self.assertEqual(read("queues/approved.json")["entries"],[])
        self.assertTrue(self.a["selected_assets_unchanged"])
        self.assertEqual(self.a["select_count_change"],0)
        self.assertEqual(self.a["model_downloads"],0)
        self.assertEqual(current.get("latest_multirepo_dependency_audit",{}).get("path"),"catalog/research/2026-11-14-r59-maya2-drama3-cross-repo-components.json")
if __name__=="__main__":unittest.main()
