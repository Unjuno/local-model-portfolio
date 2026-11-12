"""R49 pinned source file list validation (no network / no payload download)."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
class R49Test(unittest.TestCase):
 def test_revisions_lengths_and_sums(self):
  r=load('catalog/research/2026-11-12-r49-botpsy-ttm-immutable-census.json')
  q=load('manifests/drafts/r49-two-compact-immutable.candidate.json')
  self.assertEqual(len(r['packages']),2)
  self.assertEqual([x['known_source_scope_file_count'] for x in r['packages']],[11,6])
  self.assertEqual([x['known_source_scope_bytes'] for x in r['packages']],[1726201481,6126375])
  self.assertEqual(r['scope_counts']['full_snapshot_bytes'],1732327856)
  self.assertEqual(r['scope_counts']['lfs_sha256_rows'],4)
  self.assertEqual(r['scope_counts']['git_blob_sha1_rows'],13)
  self.assertFalse(q['executable']);self.assertFalse(q['approved_manifest']);self.assertFalse(q['download_authorized'])
  rows=[(p['repo_id'],f) for p in r['packages'] for f in p['files']]
  self.assertEqual(len(rows),17)
  self.assertEqual(len(set((repo,f['path']) for repo,f in rows)),17)
  self.assertEqual(sum(f['bytes'] for _,f in rows),1732327856)
  self.assertTrue(all(re.fullmatch('[0-9a-f]{64}' if f['hash_kind']=='HF_LFS_SHA256' else '[0-9a-f]{40}',f['source_hash']) for _,f in rows))
  self.assertTrue(all(not f['sha256_of_actual_user_file_verified'] for _,f in rows))
 def test_signature_and_rights_not_claimed_verified(self):
  q=load('catalog/research/2026-11-12-r49-botpsy-ttm-immutable-census.json')
  b,t=q['packages'];self.assertEqual(b['published_safetensors_total_parameters'],852985920)
  self.assertEqual(t['published_safetensors_total_parameters'],1414514)
  self.assertFalse(t['source_has_license_file'])
  self.assertFalse(t['sigstore']['cryptographically_verified'])
  self.assertEqual(t['inference_spec']['context_length'],512)
  self.assertEqual(t['inference_spec']['prediction_length'],30)
  self.assertEqual(load('queues/approved.json')['entries'],[])
if __name__=='__main__':unittest.main()
