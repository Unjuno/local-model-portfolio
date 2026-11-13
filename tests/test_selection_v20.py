"""Synthetic-fixture tests of the deterministic catalog transition, not model tests."""
import copy
import unittest
from scripts.apply_selection_v20 import prepare


def fixture():
    items = []
    for i in range(150):
        kind = 'model' if i < 127 else 'dataset'
        items.append({'asset_kind': kind, 'repo_id': f'fixture/item-{i}',
                      'portfolio_decision': 'conditional' if i < 105 else 'hold',
                      'risk_tier': 'R1' if i < 105 else 'HOLD',
                      'forecast_priority': {'rank': i+1, 'wave': 'S2'},
                      'parameter_gate': {'status': 'PASS_TOTAL_PARAMS_LT_150B' if kind == 'model' else 'NOT_APPLICABLE_TO_DATASET', 'total_parameters': 1000000 if kind == 'model' else None},
                      'download_approved': False, 'selected_file_bytes': None})
    current = {'revision_id': 'v19-20261106', 'materialized_catalog_path': 'catalog/base.json',
               'priority_worklist_path': 'queues/base.json', 'ordered_overlays': [],
               'expected': {'tracked': 150, 'active': 105}, 'notes': '', 'application_rule': ''}
    view = {'revision_id': 'v19-20261106', 'items': items, 'budget': {}, 'counts': {}}
    queue = {'source_revision': 'v19-20261106', 'approved': False, 'download_enabled': False,
             'candidates': [{'asset_kind':x['asset_kind'], 'repo_id':x['repo_id'], 'not_authorized':True, 'download_approved':False} for x in items[:105]]}
    limits = {'archive_target_bytes':3800000000000, 'minimum_free_bytes':200000000000,
              'storage_allocation_policy':{'permitted_archive_budget_bytes':3800000000000}}
    rules = {'hard_boundaries': {'archive_target_bytes':3800000000000}}
    additions = []
    for i, kind in enumerate(['model','dataset','dataset','model']):
        additions.append({'asset_kind':kind,'repo_id':f'new/item-{i}', 'portfolio_decision':'conditional' if i<3 else 'deferred',
                          'risk_tier':'R1' if i<3 else 'BACKLOG', 'url':f'https://huggingface.co/new/item-{i}',
                          'reason_selected':'independent mechanism', 'quality_negative':'not independently evaluated',
                          'evidence_date':'2026-11-06', 'forecast_priority':{'wave':'S2'},
                          'parameter_gate':{'status':'PASS_TOTAL_PARAMS_LT_150B' if kind=='model' else 'NOT_APPLICABLE_TO_DATASET', 'total_parameters':31577900000 if kind=='model' else None},
                          'download_approved':False, 'selected_file_bytes':None,
                          'selection_budget_cap_bytes':80000000000 if i<3 else None})
    overlay = {'revision_id':'v20-20261106','previous_revision_id':'v19-20261106',
               'archive_target_bytes':4000000000000,'minimum_free_bytes':200000000000,
               'additions':additions, 'max_new_selection_budget_bytes':240000000000}
    return current, view, queue, limits, rules, overlay

class SelectionTests(unittest.TestCase):
    def test_adds_four_identities_and_three_active_without_mutating_source(self):
        args=fixture(); before=copy.deepcopy(args)
        result=prepare(*args)
        self.assertIn('view',result)
        self.assertEqual(len(result['view']['items']),154)
        self.assertEqual(result['current']['expected']['active'],108)
        self.assertEqual(args,before)
    def test_budget_is_four_decimal_tb_and_free_space_floor_is_preserved(self):
        result=prepare(*fixture())
        self.assertIn('limits',result)
        self.assertEqual(result['limits']['archive_target_bytes'],4000000000000)
        self.assertEqual(result['limits']['minimum_free_bytes'],200000000000)
        self.assertIsNone(result['view']['budget']['final_selected_total_bytes'])
    def test_queue_remains_unapproved_and_exactly_matches_active(self):
        result=prepare(*fixture())
        self.assertIn('queue',result)
        q=result['queue']
        self.assertFalse(q['approved']); self.assertFalse(q['download_enabled'])
        self.assertEqual(len(q['candidates']),108)
        self.assertTrue(all(x['not_authorized'] and not x['download_approved'] for x in q['candidates']))
    def test_rejects_duplicate_identity_case_insensitively(self):
        args=fixture(); args[-1]['additions'][0]['repo_id']='FIXTURE/ITEM-0'
        with self.assertRaises(ValueError): prepare(*args)
    def test_rejects_new_model_at_150b(self):
        args=fixture(); args[-1]['additions'][0]['parameter_gate']['total_parameters']=150000000000
        with self.assertRaises(ValueError): prepare(*args)
    def test_rejects_new_model_unknown_total(self):
        args=fixture(); args[-1]['additions'][0]['parameter_gate']['total_parameters']=None
        with self.assertRaises(ValueError): prepare(*args)
    def test_rejects_download_authorization(self):
        args=fixture(); args[-1]['additions'][0]['download_approved']=True
        with self.assertRaises(ValueError): prepare(*args)
    def test_rejects_unexpected_baseline(self):
        args=fixture(); args[0]['revision_id']='v21'
        with self.assertRaises(ValueError): prepare(*args)
    def test_rejects_new_reservations_above_explicit_cap(self):
        args=fixture(); args[-1]['max_new_selection_budget_bytes']=1
        with self.assertRaises(ValueError): prepare(*args)
    def test_does_not_promote_existing_held_items(self):
        args=fixture(); result=prepare(*args)
        self.assertIn('view',result)
        self.assertEqual(result['view']['items'][:150], args[1]['items'])

if __name__=='__main__': unittest.main()
