"""R164 missing Inkling Small family research-only; no network, payload, or model execution."""
import json,re,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
class R164(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=read('manifests/drafts/r164-2026-11-25-inkling-small-uncensored-missing-family-publisher-research.candidate.json')
  cls.dec=read('catalog/decisions/2026-11-25-r164-missed-inkling-uncensored-family-archive-audit.json')
  cls.q=read('queues/proposed-v71-r164-missed-inkling-small-and-uncensored-UNAPPROVED.json')
 def test_source_locked_and_gated_hash_mask_protected(self):
  rows=self.src['source_repos'];self.assertEqual(len(rows),5)
  spec={'thinkingmachines/Inkling-Small':(48,531916781513,False),
        'distributedcognition/Inkling-Small-abliterated':(47,698246149596,'auto'),
        'thinkingmachines/Inkling-2-Small':(43,393510050371,False),
        'thinkingmachines/Inkling-2-Small-MXFP8':(49,553004791314,False),
        'OpenUncensored/Inkling-2-Small-Uncensored':(49,553004704928,False)}
  self.assertEqual({x['repo_id'] for x in rows},set(spec))
  for x in rows:
   self.assertRegex(x['revision_sha'],r'^[a-f0-9]{40}$')
   self.assertEqual((x['source_file_count'],x['source_reference_bytes'],x['publisher_gated']),spec[x['repo_id']])
   self.assertEqual(len(x['files']),x['source_file_count'])
   self.assertEqual(sum(f['reference_bytes'] for f in x['files']),x['source_reference_bytes'])
   self.assertTrue(all(not f['owner_local_sha256_verified'] for f in x['files']))
   self.assertTrue(all(f['publisher_lfs_sha256'] is None or re.fullmatch(r'[a-f0-9]{64}',f['publisher_lfs_sha256']) for f in x['files']))
  gate=next(x for x in rows if x['publisher_gated']=='auto')
  self.assertEqual(gate['masked_publisher_lfs_count'],26)
  self.assertEqual(gate['available_publisher_lfs_sha_count'],0)
 def test_edit_is_not_complete_model_and_parent_mxfp8_required(self):
  d=self.src['small_2_MXFP8_base_versus_uncensored_hash_overlap']
  self.assertEqual(d['same_path_and_git_blob_sha1_file_count'],3)
  self.assertEqual(d['same_publisher_content_bytes'],14863943654)
  self.assertEqual(d['edit_file']['reference_bytes'],39174)
  self.assertEqual(d['edit_file']['publisher_lfs_sha256'],'58554a71aedb111f48cced364c035f102ccfd114e250dba6e165b929d356301a')
  self.assertFalse(d['edit_file_can_be_reapplied_without_code_and_exact_parent'])
  self.assertEqual(self.src['parameter_screen']['inkling_2_small_total_params_author'],594000000000)
 def test_current_selection_and_acquisition_not_changed(self):
  C=read('catalog/CURRENT.json');E=read('catalog/effective-portfolio-2026-11-25-v71.json');L=read('catalog/execution/2026-11-19-acquisition-ledger.json')
  ids={x['repo_id'] for x in E['items']};acq={x['repo_id'] for x in L['models'] if x['status']=='VERIFIED'}
  self.assertTrue({x['repo_id'] for x in self.src['source_repos']}.isdisjoint(ids|acq))
  self.assertEqual(len(ids),260)
  self.assertGreaterEqual(C['expected']['tracked'],260)
  self.assertEqual(L['summary']['models_verified'],116)
  self.assertEqual(read('queues/approved.json')['entries'],[])
  self.assertFalse(self.q['actual_weight_download_enabled'])
  self.assertFalse(self.q['explicit_user_approval_granted'])
  self.assertTrue(self.dec['no_new_formal_selected_models'])
  self.assertFalse(self.src['status']['model_licenses_for_owner_acts_verified'])
if __name__=='__main__':unittest.main()
