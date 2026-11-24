"""R166/v72: corrected 5-source complete trees, 4 archival HOLDs, all210 fail-closed. No network."""
import json,re,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def ld(x):return json.loads((R/x).read_text(encoding='utf8'))
class R166V72(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=ld('manifests/drafts/r166-2026-11-25-inkling-small-five-complete-paginated-original-sources.candidate.json')
  cls.alt=ld('manifests/drafts/r166-2026-11-25-inkling2-small-three-gguf-format-alternatives-UNAPPROVED.candidate.json')
  cls.rev=ld('catalog/revisions/v72-2026-11-25.json')
  cls.old=ld('catalog/effective-portfolio-2026-11-25-v71.json')
  cls.new=ld('catalog/effective-portfolio-2026-11-25-v72.json')
  cls.cur=ld('catalog/CURRENT.json')
  cls.ready=ld('catalog/readiness/v72-2026-11-25-r166-all210-gates.json')
  cls.ac=ld('catalog/access/2026-11-25-v72-conditional-hub-gates.json')
  cls.q=ld('queues/proposed-v72-2026-11-25.json')
  cls.prep=ld('catalog/preparation/2026-11-25-insurance-bundles-v72.json')
  cls.qa=ld('queues/proposed-v72-r166-inkling-family-archive-HOLD-UNAPPROVED.json')

 def test_five_official_full_pagination_lengths_and_gated_missing_shas(self):
  exp={'thinkingmachines/Inkling-Small':(50,531944669421,35,0,2),
      'distributedcognition/Inkling-Small-abliterated':(48,698246151509,0,26,2),
      'thinkingmachines/Inkling-2-Small':(43,393510050371,27,0,1),
      'thinkingmachines/Inkling-2-Small-MXFP8':(61,622833459732,51,0,2),
      'OpenUncensored/Inkling-2-Small-Uncensored':(61,622833373184,52,0,2)}
  # Some author repositories contain LFS references on non-weight assets; all are counted.
  m={x['repo_id']:x for x in self.src['repositories']}
  self.assertEqual(set(m),set(exp))
  for rid,(n,b,sh,mask,pages) in exp.items():
   x=m[rid]
   self.assertEqual((x['publisher_reference_file_count'],x['publisher_reference_bytes'],x['publisher_lfs_masked'],x['pages_fetched']),(n,b,mask,pages))
   self.assertEqual(x['publisher_lfs_sha256_available'],sh)
   self.assertEqual(sum(f['bytes'] for f in x['complete_files']),b)
   self.assertEqual(len({f['path'] for f in x['complete_files']}),n)
   for f in x['complete_files']:
    sha=f['publisher_LFS_sha256']
    self.assertTrue(sha is None or re.fullmatch(r'[a-f0-9]{64}',sha))
    self.assertFalse(f['owner_local_sha256_verified'])
  self.assertEqual(self.src['totals']['publisher_reference_files'],263)
  self.assertEqual(self.src['totals']['publisher_reference_bytes'],2869367704217)
  self.assertEqual(self.src['totals']['publisher_lfs_sha256_available'],165)
  self.assertEqual(self.src['totals']['publisher_lfs_masked'],26)
  self.assertEqual(sum(len(x['additional_recovered_paths']) for x in m.values()),27)

 def test_original_mxfp8_and_edit_full_shard_dedup_metadata_only(self):
  shared=self.src['mxp8_parent_vs_uncensored']
  self.assertEqual(shared['publisher_sha_identical_same_path_file_count'],11)
  self.assertEqual(shared['publisher_sha_identical_same_path_bytes'],56755370428)
  self.assertEqual(shared['uncensored_full_repo_bytes_minus_sha_identical_publisher_refs'],566078002756)
  self.assertTrue(shared['not_actual_incremental_owner_disk_bytes'])
  edit=next(f for x in self.src['repositories'] if x['repo_id']=='OpenUncensored/Inkling-2-Small-Uncensored' for f in x['complete_files'] if f['path']=='edit.pt')
  self.assertEqual(edit['bytes'],39174)
  self.assertEqual(edit['publisher_LFS_sha256'],'58554a71aedb111f48cced364c035f102ccfd114e250dba6e165b929d356301a')

 def test_v71_all260_identical_and_four_independent_HOLD_state_ids(self):
  self.assertIn(self.cur['revision_id'],('v72-20261125','v73-20261125'))
  self.assertEqual(self.new['items'][:260],self.old['items'])
  self.assertEqual(self.new['items'][260:],self.rev['additions'])
  self.assertEqual((len(self.new['items']),self.new['counts']['active'],self.new['counts']['models'],self.new['counts']['datasets']),(264,210,238,26))
  self.assertEqual((self.new['counts']['by_decision']['select'],self.new['counts']['by_decision']['conditional'],self.new['counts']['by_decision']['hold']),(56,154,35))
  self.assertEqual(self.new['counts']['parameter_gate']['OVER_150B_QUANT_REVIEW_REQUIRED'],7)
  self.assertIn(self.cur['expected']['tracked'],(264,265))
  self.assertIn(self.cur['expected']['active'],(210,211))
  self.assertTrue(self.rev['all_previous_260_assets_preserved_identically'])
  self.assertTrue(all(x['portfolio_decision']=='hold' and not x['download_ready'] for x in self.rev['additions']))
  self.assertEqual(set(self.rev['added_assets']),{'thinkingmachines/Inkling-Small','distributedcognition/Inkling-Small-abliterated','thinkingmachines/Inkling-2-Small','OpenUncensored/Inkling-2-Small-Uncensored'})
  self.assertNotIn('thinkingmachines/Inkling-2-Small-MXFP8',set(x['repo_id'] for x in self.new['items']))

 def test_all210_stops_and_154_conditional_gates_without_approval(self):
  active={x['repo_id'] for x in self.new['items'] if x['portfolio_decision'] in ('select','conditional')}
  conditional={x['repo_id'] for x in self.new['items'] if x['portfolio_decision']=='conditional'}
  self.assertEqual(len(active),210);self.assertEqual(len(conditional),154)
  self.assertEqual({x['repo_id'] for x in self.q['candidates']},active)
  self.assertEqual({x['repo_id'] for x in self.prep['items']},active)
  self.assertEqual({x['repo_id'] for x in self.ready['records']},active)
  self.assertEqual({x['repo_id'] for x in self.ac['entries']},conditional)
  self.assertEqual(self.ready['summary']['blocked_any'],210)
  self.assertEqual(self.ready['summary']['ready_to_approve'],0)
  self.assertTrue(all(not x['download_approved'] and not x['ready_to_acquire'] for x in self.ready['records']))
  self.assertEqual(ld('queues/approved.json')['entries'],[])
  self.assertFalse(self.q['download_enabled'])
  self.assertFalse(self.prep['download_enabled'])
  self.assertFalse(self.ac['download_authorized'])
  self.assertEqual(ld('catalog/readiness/CURRENT.json')['catalog_revision'],self.cur['revision_id'])
  self.assertEqual(ld('catalog/estimates/CURRENT.json')['portfolio_revision'],self.cur['revision_id'])

 def test_three_formats_not_separate_trained_origins(self):
  exp={'UD-IQ2_XXS':(5,190584243104),'UD-Q3_K_XL':(7,285128587168),'UD-Q4_K_XL':(9,354150001600)}
  for row in self.alt['quantization_subfolder_scopes']:
   self.assertEqual((row['total_files'],row['publisher_bytes']),exp[row['variant']])
   self.assertFalse(row['independent_trained_outcome'])
   self.assertFalse(row['acquisition_approved'])
  self.assertEqual(self.alt['optional_single_vision_projector']['bytes'],658223328)
  self.assertFalse(self.alt['user_explicit_download_authorization'])
  self.assertEqual(self.qa['user_explicit_file_scope_authorization_added'],0)

if __name__=='__main__':unittest.main()
