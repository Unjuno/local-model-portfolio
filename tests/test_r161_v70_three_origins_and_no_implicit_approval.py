"""Offline source/catalog/authorization regression for R161/v70. No model payload or network."""
import copy
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf8'))

MAN='manifests/drafts/r161-2026-11-25-three-novel-small-dspark-sala-origins.candidate.json'
OV='catalog/revisions/v70-2026-11-25.json'
OLD='catalog/effective-portfolio-2026-11-25-v69.json'
NEW='catalog/effective-portfolio-2026-11-25-v70.json'
Q='queues/proposed-v70-2026-11-25.json'
ACC='catalog/access/2026-11-25-v70-conditional-hub-gates.json'
PREP='catalog/preparation/2026-11-25-insurance-bundles-v70.json'
READY='catalog/readiness/v70-2026-11-25-r161-all208-gates.json'
DEC='catalog/decisions/2026-11-25-r161-v70-three-trained-origins-and-sala-hold.json'

class R161V70SourceAndGuards(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=load(MAN);cls.v=load(OV);cls.b=load(OLD);cls.e=load(NEW);cls.c=load('catalog/CURRENT.json')
  cls.q=load(Q);cls.acc=load(ACC);cls.prep=load(PREP);cls.ready=load(READY);cls.dec=load(DEC)
  cls.sources={x['repo_id']:x for x in cls.s['new_model_research_sources']}

 def test_exact_publisher_src_30files_7sha_all_oids_and_bytes(self):
  spec={
   'openbmb/MiniCPM5-1B':('ac83f813ba7da263c51a9f3ec37c2072597e54af',11,2171355218,1,1080632832),
   'openbmb/MiniCPM5-2B-DSpark':('a63eb96b9bba7e999639d3fe3b6d70a0ea38eabd',4,647565508,1,323776001),
   'openbmb/MiniCPM-SALA':('9180fe1db74f71fb81bc7105efe88f6b19c959b0',15,18959519287,5,9477203968)}
  self.assertEqual(set(self.sources),set(spec))
  for rid,(rev,fc,b,sha,params) in spec.items():
   src=self.sources[rid];self.assertEqual((src['publisher_revision_sha'],src['file_count'],src['publisher_all_file_bytes'],src['publisher_lfs_sha256_count'],src['publisher_safetensors_total_elements']),(rev,fc,b,sha,params))
   self.assertRegex(rev,r'^[a-f0-9]{40}$')
   fs=src['publisher_files'];self.assertEqual(len(fs),fc)
   self.assertEqual(len({f['path'].casefold() for f in fs}),fc)
   self.assertEqual(sum(f['publisher_reference_bytes'] for f in fs),b)
   self.assertEqual(sum(f['publisher_lfs_sha256'] is not None for f in fs),sha)
   for f in fs:
    self.assertRegex(f['publisher_git_blob_oid_sha1'],r'^[a-f0-9]{40}$')
    if f['publisher_lfs_sha256']:self.assertRegex(f['publisher_lfs_sha256'],r'^[a-f0-9]{64}$')
    self.assertFalse(f['owner_local_hash_checked']);self.assertIsNone(f['owner_local_file_present'])
   self.assertFalse(src['download_approved']);self.assertFalse(src['owner_SHA_verified']);self.assertFalse(src['offline_restore_verified'])
  self.assertEqual(self.s['source_reference_summary'],{'files':30,'publisher_reference_bytes':21778440013,'LFS_SHA256_refs':7})

 def test_previous_255_assets_preserved_and_selected_255_205(self):
  self.assertEqual((self.b['revision_id'],len(self.b['items'])),('v69-20261125',255))
  self.assertEqual(self.e['items'][:255],self.b['items'])
  self.assertEqual(self.e['items'][255:],self.v['additions'])
  self.assertEqual(self.e['revision_id'],'v70-20261125')
  self.assertIn(self.c['revision_id'],('v71-20261125','v72-20261125'))
  current_view=load(self.c['materialized_catalog_path'])
  self.assertEqual(current_view['items'][:258],self.e['items'])
  self.assertEqual((len(self.e['items']),self.e['counts']['tracked'],self.e['counts']['active']),(258,258,208))
  self.assertEqual((self.e['counts']['by_decision']['conditional'],self.e['counts']['by_decision']['select'],self.e['counts']['by_decision']['hold']),(152,56,31))
  self.assertEqual((self.e['counts']['models'],self.e['counts']['datasets']),(232,26))
  self.assertTrue(all(self.c['expected'][k]==v for k,v in current_view['counts'].items()))
  self.assertEqual(self.c['expected']['budget_scenario'],current_view['budget'])
  self.assertEqual(self.c['expected']['archive_limit_bytes'],4000000000000)
  self.assertEqual(self.c['expected']['minimum_free_bytes'],200000000000)
  self.assertIn(OV,self.c['ordered_overlays'])
  self.assertEqual([x['repo_id'] for x in self.v['additions']],['openbmb/MiniCPM5-1B','openbmb/MiniCPM5-2B-DSpark','openbmb/MiniCPM-SALA'])
  self.assertEqual([x['portfolio_decision'] for x in self.v['additions']],['conditional','conditional','hold'])
  self.assertFalse(any(x['download_approved'] or x['download_ready'] for x in self.v['additions']))

 def test_all_205_fail_closed_and_auxiliary_identity(self):
  active={x['repo_id'] for x in self.e['items'] if x['portfolio_decision'] in ('select','conditional')}
  self.assertEqual(len(active),208)
  self.assertEqual({x['repo_id'] for x in self.q['candidates']},active)
  self.assertEqual({x['repo_id'] for x in self.ready['records']},active)
  self.assertEqual({x['repo_id'] for x in self.prep['items']},active)
  self.assertEqual({x['repo_id'] for x in self.acc['entries']},{x['repo_id'] for x in self.e['items'] if x['portfolio_decision']=='conditional'})
  self.assertEqual((len(self.q['candidates']),len(self.ready['records']),len(self.prep['items']),len(self.acc['entries'])),(208,208,208,152))
  self.assertEqual(self.ready['summary']['blocked_any'],208)
  self.assertEqual(self.ready['summary']['ready_to_approve'],0)
  self.assertEqual(sum(bool(x['ready_to_acquire']) for x in self.ready['records']),0)
  self.assertEqual(sum(bool(x['download_approved']) for x in self.ready['records']),0)
  self.assertEqual(sum(bool(x['download_authorized']) for x in self.acc['entries']),0)
  self.assertFalse(self.q['approved']);self.assertFalse(self.q['download_enabled'])
  self.assertFalse(self.prep['download_enabled']);self.assertEqual(self.acc['gated_count'],21)
  self.assertEqual(load('queues/approved.json')['entries'],[])

 def test_no_double_download_parent_and_holds(self):
  ledger=load('catalog/execution/2026-11-19-acquisition-ledger.json')
  verified={x['repo_id'] for x in ledger['models'] if x['status']=='VERIFIED'}
  self.assertEqual((len(verified),ledger['summary']['files_verified_total']),(116,1758))
  self.assertTrue(set(self.sources).isdisjoint(verified))
  parent='openbmb/MiniCPM5-2B'
  self.assertNotIn(parent,verified)
  self.assertIn(parent,{x['repo_id'] for x in self.b['items']})
  drafter=self.v['additions'][1]
  self.assertEqual(drafter['fixed_parent_dependency']['repo_id'],parent)
  self.assertFalse(drafter['fixed_parent_dependency']['inference_target_owner_local_SHA_verified'])
  self.assertFalse(drafter['fixed_parent_dependency']['publisher_training_parent_exact_SHA_independently_verified'])
  self.assertTrue(drafter['personal_access_verified'] is False)
  self.assertFalse(self.s['approval_control']['untrusted_model_code_executed'])
  self.assertEqual(self.s['approval_control']['approved_queue_entries_added'],0)
  self.assertEqual(self.dec['model_weight_bytes_downloaded_now'],0)
  self.assertEqual(self.dec['user_download_authorizations_added'],0)
  self.assertEqual(self.v['approved_queue_entries_added'],0)
  self.assertEqual(self.s['known_training_and_runtime']['openbmb/MiniCPM-SALA']['runtime_code_branch'],'minicpm_sala')
  self.assertFalse(self.s['known_training_and_runtime']['openbmb/MiniCPM-SALA']['code_commit_pin_does_not_verify_build_or_license_closure'] is False)

if __name__=='__main__':unittest.main()
