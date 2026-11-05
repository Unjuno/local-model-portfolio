"""Synthetic metadata tests; no weight loading or network access."""
import copy
import json
from pathlib import Path
import unittest
from scripts.apply_selection_v21 import prepare


def fixture():
    items=[]
    for i in range(154):
        items.append({'asset_kind':'model','repo_id':f'old/asset-{i}',
          'portfolio_decision':'conditional' if i<108 else 'hold','risk_tier':'R1' if i<108 else 'HOLD',
          'forecast_priority':{'wave':'S1' if i<31 else 'S2','rank':i+1},
          'parameter_gate':{'total_parameters':1000,'status':'PASS_TOTAL_PARAMS_LT_150B'},'download_approved':False})
    c={'revision_id':'v20-20261106','expected':{'tracked':154,'active':108},'ordered_overlays':[],'notes':'','application_rule':''}
    v={'revision_id':'v20-20261106','items':items,'counts':{},'budget':{}}
    q={'source_revision':'v20-20261106','approved':False,'download_enabled':False,'candidates':[{'asset_kind':'model','repo_id':x['repo_id'],'not_authorized':True,'download_approved':False} for x in items[:108]]}
    entries=[]
    for i in range(5):
        entries.append({'asset_kind':'dataset' if i==3 else 'model','repo_id':f'new/item-{i}',
          'portfolio_decision':'conditional' if i<4 else 'hold','risk_tier':'R1' if i<4 else 'HOLD',
          'url':f'https://huggingface.co/new/item-{i}','reason_selected':'unique mechanism',
          'quality_negative':'not independently reproduced','evidence_date':'2026-11-06',
          'forecast_priority':{'wave':'S1'},'download_approved':False,
          'parameter_gate':{'status':'NOT_APPLICABLE_TO_DATASET' if i==3 else 'PASS_TOTAL_PARAMS_LT_150B','total_parameters':None if i==3 else 1000},
          'restriction_assessment':{'probability':None,'specific_stop_notice_verified':False,'observed':'publisher license','scenario':'conditional hypothesis'},
          'selection_budget_cap_bytes':10 if i<4 else None,
          'selected_file_bytes':None,'fully_pinned_revision_sha':None,'license_text_reviewed':False,'dependencies_reviewed':False})
    overlay={'revision_id':'v21-20261106','previous_revision_id':'v20-20261106','archive_target_bytes':4000000000000,
             'minimum_free_bytes':200000000000,'max_new_selection_budget_bytes':40,'additions':entries}
    return c,v,q,overlay

class SelectionV21Tests(unittest.TestCase):
    def test_counts_preserve_records_without_mutating_input(self):
        args=fixture(); old=copy.deepcopy(args); r=prepare(*args)
        self.assertEqual(args,old)
        self.assertEqual(len(r['view']['items']),159)
        self.assertEqual(r['current']['expected']['active'],112)
        self.assertEqual(r['view']['items'][:154],old[1]['items'])
    def test_queue_is_nonexecutable_and_exact(self):
        r=prepare(*fixture()); q=r['queue']; self.assertEqual(len(q['candidates']),112)
        self.assertFalse(q['approved']); self.assertFalse(q['download_enabled'])
        self.assertTrue(all(x['not_authorized'] and not x['download_approved'] for x in q['candidates']))
        self.assertEqual({(x['asset_kind'],x['repo_id']) for x in q['candidates']},
                         {(x['asset_kind'],x['repo_id']) for x in r['view']['items'] if x['portfolio_decision'] in ('select','conditional')})
    def test_unknown_total_conditional_remains_blocked(self):
        a=fixture(); x=a[-1]['additions'][0]; x['parameter_gate']={'total_parameters':None,'status':'UNVERIFIED_BLOCK_FINAL_LOCK','research_screening_exception':'CONDITIONAL_RESEARCH_ONLY_NON_EXECUTABLE'}
        x['research_only_unknown_total_allow_conditional']=True
        r=prepare(*a); z=next(y for y in r['queue']['candidates'] if y['repo_id']==x['repo_id'])
        self.assertTrue(z['research_only']); self.assertFalse(z['can_enter_approved_queue'])
        x.pop('research_only_unknown_total_allow_conditional')
        with self.assertRaises(ValueError): prepare(*a)
    def test_duplicate_identity_rejected(self):
        a=fixture(); a[-1]['additions'][0]['repo_id']='OLD/ASSET-0'
        with self.assertRaises(ValueError): prepare(*a)
    def test_authorization_and_fabricated_risk_rejected(self):
        for k,value in [('download_approved',True),('fully_pinned_revision_sha','a'*40)]:
            a=fixture(); a[-1]['additions'][0][k]=value
            with self.assertRaises(ValueError): prepare(*a)
        a=fixture(); a[-1]['additions'][0]['restriction_assessment']['probability']=0.8
        with self.assertRaises(ValueError): prepare(*a)
    def test_oversized_not_automatically_excluded_or_promoted(self):
        a=fixture(); x=a[-1]['additions'][-1]; x['parameter_gate']={'total_parameters':180000000000,'status':'OVER_150B_QUANT_REVIEW_REQUIRED'}
        self.assertEqual(prepare(*a)['view']['items'][-1]['portfolio_decision'],'hold')
        a=fixture(); x=a[-1]['additions'][0]; x['parameter_gate']={'total_parameters':180000000000,'status':'OVER_150B_QUANT_REVIEW_REQUIRED'}
        with self.assertRaises(ValueError): prepare(*a)
    def test_unknown_bytes_not_zero_and_budget_ceiling_unchanged(self):
        r=prepare(*fixture()); self.assertIsNone(r['view']['budget']['final_selected_total_bytes'])
        self.assertEqual(r['view']['budget']['archive_limit_bytes'],4000000000000)
        self.assertEqual(r['view']['budget']['minimum_free_bytes'],200000000000)
        a=fixture(); a[-1]['max_new_selection_budget_bytes']=39
        with self.assertRaises(ValueError): prepare(*a)
    def test_stale_baseline_stops(self):
        a=fixture(); a[0]['revision_id']='v22'
        with self.assertRaises(ValueError): prepare(*a)

    def test_actual_overlay_has_five_evidence_scoped_records(self):
        path=Path(__file__).resolve().parents[1]/'catalog/revisions/v21-2026-11-06.json'
        o=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(len(o['additions']),5)
        self.assertEqual(sum(x['portfolio_decision']=='conditional' for x in o['additions']),4)
        self.assertEqual(sum(x['selection_budget_cap_bytes'] or 0 for x in o['additions']),92_000_000_000)
        m={x['repo_id']:x for x in o['additions']}
        self.assertEqual(m['Louis0324/StyleStream']['portfolio_decision'],'hold')
        for rid in ('WhissleAI/steer-tts','maya-research/maya2-native'):
            self.assertIsNone(m[rid]['parameter_gate']['total_parameters'])
            self.assertTrue(m[rid]['research_only_unknown_total_allow_conditional'])
        self.assertTrue(all(x['restriction_assessment']['probability'] is None for x in o['additions']))
    def test_actual_overlay_transforms_synthetic_source_with_correct_gates(self):
        a=list(fixture()); a[-1]=json.loads((Path(__file__).resolve().parents[1]/'catalog/revisions/v21-2026-11-06.json').read_text(encoding='utf-8'))
        r=prepare(*a)
        self.assertEqual(r['current']['expected']['active'],112)
        for rid in ('WhissleAI/steer-tts','maya-research/maya2-native'):
            e=next(x for x in r['queue']['candidates'] if x['repo_id']==rid)
            self.assertFalse(e['can_enter_approved_queue'])
            self.assertTrue(e['research_only'])

if __name__=='__main__':unittest.main()
