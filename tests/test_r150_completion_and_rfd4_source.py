"""R150 verified ledger99 completion map and RFD4 root/auxiliary identity.

Offline standard library; never downloads weights, executes checkpoints or
reads the owner's external drive. All tests retain strict acquisition STOP.
"""
import copy
import json
import unittest
from pathlib import Path
from unittest import mock
from scripts.audit_completion_r150 import build
from scripts.check_parameter_cutoff import validate_model
from scripts.audit_selection_decisions import audit as decision_audit
from scripts.check_parameter_cutoff import audit as parameter_audit

ROOT=Path(__file__).resolve().parents[1]
def L(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))

class R150Completion(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=L('catalog/audits/2026-11-22-r150-all235-completion-status.json')
  cls.rfd4=L('catalog/research/2026-11-22-r150-rfd4-core-weight-same-auxiliary-diff.json')
  cls.v63=L('catalog/effective-portfolio-2026-11-22-v63.json')
  cls.current=L('catalog/CURRENT.json')
  cls.ledger=L('catalog/execution/2026-11-19-acquisition-ledger.json')
 def test_full_235_rows_and_existing_verified_status(self):
  r=self.report
  self.assertEqual(r['catalog_revision'],'v63-20261122')
  self.assertEqual(r['registered_assets'],235)
  self.assertEqual(r['active_assets'],188)
  self.assertEqual((r['registered_models'],r['registered_datasets']),(209,26))
  self.assertEqual(r['source_receipt_status_counts'],{
    'VERIFIED':99,'HOLD_GATED_OR_PRIVATE':1,'NO_ACQUISITION_REPORT_FOR_REPO':135})
  self.assertEqual(r['active_source_receipt_status_counts'],{
    'VERIFIED':99,'HOLD_GATED_OR_PRIVATE':1,'NO_ACQUISITION_REPORT_FOR_REPO':88})
  self.assertEqual(len(r['assets']),235)
  self.assertEqual(len({(x['asset_kind'],x['repo_id']) for x in r['assets']}),235)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in r['assets']},
                   {(x['asset_kind'],x['repo_id']) for x in self.v63['items']})
  self.assertEqual(r['active_unknown_total_parameter_count'],13)
  self.assertEqual(r['active_conditional_gated_count'],21)
  self.assertFalse(any(x['new_transfer_authorized'] for x in r['assets']))
  self.assertTrue(all(x['owner_HDD_full_SHA_independently_reverified_in_this_study'] is False for x in r['assets']))
  self.assertTrue(r['not_reported_acquired_does_not_mean_absent_from_user_disk'])
 def test_latest_builder_and_asof_snapshot_agree(self):
  if self.current['revision_id']=='v63-20261122':
   self.assertEqual(build(ROOT),self.report)
  else:
   self.assertIn('catalog/revisions/v63-2026-11-22.json',self.current['ordered_overlays'])
   self.assertEqual(len(self.v63['items']),self.report['registered_assets'])
 def test_rfd4_original_root_sha_same_and_auxiliary_differs(self):
  x=self.rfd4
  self.assertTrue(x['core_identity']['old_and_acquired_equal'])
  self.assertEqual(x['core_identity']['same_lfs_sha256'],
    '5b549dd61adb2f6c6b5cb95bda13f40f5e31556b4e6c755edc0ca6f011c68fb0')
  self.assertEqual(x['core_identity']['bytes'],1742660596)
  self.assertEqual(x['file_scope_conclusions']['core_reacquisition_decision'],'DO_NOT_REDOWNLOAD')
  self.assertTrue(x['distinct_runtime_or_learned_scope']['transformers_conversion_weight_differs'])
  self.assertNotEqual(x['distinct_runtime_or_learned_scope']['older_transformers_sha256'],
                      x['distinct_runtime_or_learned_scope']['acquired_transformers_sha256'])
  self.assertEqual(x['publisher_files_in_snapshots'],[51,78])
  self.assertEqual(x['historical_ledger_receipt']['status'],'VERIFIED')
  self.assertFalse(x['historical_ledger_receipt']['this_research_independently_rehashed_owner_disk'])
  self.assertFalse(x['file_scope_conclusions']['complete_offline_reconstruction_proven'])
  self.assertEqual(x['file_scope_conclusions']['approved_queue_entries_added'],0)
 def test_decision_and_parameter_auditors_support_later_revisions(self):
  self.assertEqual(decision_audit(ROOT),[])
  self.assertEqual(parameter_audit(ROOT),[])
 def test_unknown_total_bounded_lora_is_not_download_ready(self):
  v={x['repo_id']:x for x in self.v63['items']}
  for repo in ('harness-hub/Qwen3.8-27B-pi-adapted',
               'PhalaCloud/Qwen3.8-27B-Uncensored-LoRA'):
   base=v[repo]
   self.assertIsNone(base['parameter_gate']['total_parameters'])
   self.assertEqual(validate_model(base),[])
   x=copy.deepcopy(base)
   field=('conservative_parent_plus_adapter_upper_bound' if repo.startswith('harness-')
          else 'conservative_parent_plus_adapter_upper')
   x['parameter_gate'][field]=150000000000
   self.assertTrue(validate_model(x))
   x=copy.deepcopy(base);x['download_ready']=True
   self.assertTrue(validate_model(x))
 def test_kumo_unknown_requires_correlated_current_queue_stop(self):
  a={x['repo_id']:x for x in self.v63['items']}
  q={x['repo_id']:x for x in L('queues/proposed-v63-2026-11-22.json')['candidates']}
  m=a['nvidia/Kumo-Anomaly']
  self.assertTrue(validate_model(m))
  self.assertEqual(validate_model(m,queue_block=q[m['repo_id']]),[])
  y=copy.deepcopy(q[m['repo_id']]);y['can_enter_approved_queue']=True
  self.assertTrue(validate_model(m,queue_block=y))
  y=copy.deepcopy(q[m['repo_id']]);y['download_approved']=True
  self.assertTrue(validate_model(m,queue_block=y))
 def test_no_new_approval_and_no_payloads(self):
  self.assertEqual(L('queues/approved.json')['entries'],[])
  self.assertEqual(self.report['recorded_explicit_download_approvals'],0)
  self.assertEqual(self.report['active_ready_for_new_acquisition'],0)
  self.assertEqual(self.report['number_of_independently_verified_owner_offline_restores_this_study'],0)

if __name__=='__main__':unittest.main()
