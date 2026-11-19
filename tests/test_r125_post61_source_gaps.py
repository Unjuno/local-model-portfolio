# R125 deterministic source metadata tests. No network, weights or dynamic code execution.
import json
import pathlib
import unittest
import itertools
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
class Post61ScopeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.plan=load("queues/proposed-v52-r125-post61-gap66plus-2026-11-20.json")
  cls.eff=load("catalog/effective-portfolio-2026-11-19-v52.json")
  cls.approved=load("queues/approved.json")
 def test_counts_hashes_and_file_uniqueness(self):
  p=self.plan
  self.assertEqual(p['evaluated_model_originals'],6)
  self.assertEqual(p['source_gap_candidate_files'],67)
  self.assertEqual(p['source_gap_candidate_lfs_sha256_refs'],25)
  self.assertEqual(sum(x['research_candidate_bytes'] for x in p['entries']),p['source_gap_candidate_bytes'])
  self.assertEqual(len({x['repo_id'] for x in p['entries']}),6)
  active={x['repo_id'] for x in self.eff['items'] if x['portfolio_decision'] in ('select','conditional')}
  for x in p['entries']:
   self.assertIn(x['repo_id'],active)
   self.assertEqual(len(x['all_publisher_files']),x['publisher_full_source_file_count'])
   self.assertEqual(sum(f['bytes'] for f in x['all_publisher_files']),x['publisher_full_source_bytes'])
   self.assertEqual(len(x['research_candidate_files']),x['research_candidate_file_count'])
   self.assertEqual(sum(f['bytes'] for f in x['research_candidate_files']),x['research_candidate_bytes'])
   self.assertEqual(len({f['path'] for f in x['all_publisher_files']}),len(x['all_publisher_files']))
   for f in x['research_candidate_files']:
    self.assertRegex(f['publisher_git_blob_sha1'],r'^[0-9a-f]{40}$')
    if f['publisher_lfs_sha256'] is not None:self.assertRegex(f['publisher_lfs_sha256'],r'^[0-9a-f]{64}$')
 def test_four_missing_subsets_unique(self):
  for x in self.plan['entries']:
   if x['reported_ledger_files'] is None:continue
   items=x['all_publisher_files']
   cnt=x['publisher_full_source_file_count']-x['reported_ledger_files']
   difference=x['publisher_full_source_bytes']-x['reported_ledger_bytes']
   actual=[f['path'] for f in x['research_candidate_files']]
   found=[]
   for c in itertools.combinations(items,cnt):
    if sum(z['bytes'] for z in c)==difference:
     found.append([z['path'] for z in c])
     if len(found)>1:break
   self.assertEqual(found,[actual],msg=x['repo_id'])
 def test_dependency_code_and_license_cautions(self):
  by={x['repo_id']:x for x in self.plan['entries']}
  self.assertIn('modeling_illada.py',[f['path'] for f in by['GSAI-ML/iLLaDA-8B-Base']['research_candidate_files']])
  self.assertIn('silence_latent.pt',[f['path'] for f in by['ACE-Step/acestep-v15-xl-turbo']['research_candidate_files']])
  self.assertIn('tokenizer.py',[f['path'] for f in by['HuggingFaceBio/Carbon-X']['research_candidate_files']])
  self.assertFalse(by['HuggingFaceBio/Carbon-X']['standalone_license_file_on_model_repo'])
  self.assertFalse(by['ACE-Step/acestep-v15-xl-turbo']['standalone_license_file_on_model_repo'])
 def test_no_acquisition_authorization_or_replacement(self):
  self.assertEqual(self.approved.get('entries',[]),[])
  self.assertFalse(self.plan['download_enabled'])
  self.assertFalse(self.plan['approved'])
  for x in self.plan['entries']:
   self.assertFalse(x['download_approved'])
   self.assertFalse(x['eligible_for_direct_download'])
if __name__=="__main__":unittest.main()
