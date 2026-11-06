"""v24: preserve three learned results while keeping authorization closed."""
import copy
import json
import unittest
from pathlib import Path
from scripts.apply_selection_v24 import prepare
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def fixture():
    items=[]
    for i in range(165):
        items.append({'asset_kind':'model','repo_id':f'fixture/m{i}',
            'portfolio_decision':'conditional' if i<118 else 'hold',
            'risk_tier':'R1' if i<118 else 'HOLD',
            'parameter_gate':{'status':'PASS_TOTAL_PARAMS_LT_150B','total_parameters':1_000_000},
            'forecast_priority':{'wave':['S1','S2','S3'][i%3],'rank':i+1},
            'download_approved':False,'selected_file_bytes':None})
    c={'revision_id':'v23-20261106','expected':{'tracked':165,'active':118,'budget_scenario':{}},
       'ordered_overlays':[],'notes':'','application_rule':'',
       'capacity_audit':{'source_revision':'v23-20261106','status':'ALL_118_PRIMARY_SCOPES_EXACT'}}
    v={'revision_id':'v23-20261106','items':items,'budget':{},'counts':{}}
    q={'source_revision':'v23-20261106','approved':False,'download_enabled':False,
       'candidates':[{'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],
           'not_authorized':True,'download_approved':False} for x in items[:118]]}
    return c,v,q,load('catalog/revisions/v24-2026-11-06.json')
class V24SelectionTests(unittest.TestCase):
    def test_three_additions_are_independent_and_cheap(self):
        a=load('catalog/revisions/v24-2026-11-06.json')
        self.assertEqual(a['previous_revision_id'],'v23-20261106')
        self.assertEqual(len(a['additions']),3)
        self.assertEqual(len({x['repo_id'].lower() for x in a['additions']}),3)
        self.assertEqual(sum(x['selection_budget_cap_bytes'] for x in a['additions']),102_000_000_000)
        self.assertEqual(a['previous_verified_capacity']['known_logical_dedup_bytes'],3_175_147_816_831)
        ids={x['repo_id'] for x in a['additions']}
        self.assertEqual(ids,{'pfnet/plamo-3-translate-31b',
                              'pfnet/plamo-3-translate-0.8b',
                              'nvidia/Cosmos3-Nano-Sim-Bimanual'})
        for item in a['additions']:
            self.assertFalse(item['download_approved'])
            self.assertFalse(item['license_text_reviewed'])
            self.assertIsNone(item['fully_pinned_revision_sha'])
            self.assertIsNone(item['selected_file_bytes'])
            self.assertEqual(len(item['upstream_revision_sha_observed']),40)
            self.assertTrue(item['reason_selected'] and item['quality_negative'])
            self.assertTrue(item['falsification_condition'])
            self.assertIsNone(item['restriction_assessment']['probability'])
            self.assertTrue(item['preservation_bundle']['scope_reference_only_no_download_manifest'])
    def test_transition_keeps_prior_165_exact(self):
        args=fixture();previous=copy.deepcopy(args)
        r=prepare(*args)
        self.assertEqual(args,previous)
        self.assertEqual(r['view']['items'][:165],args[1]['items'])
        self.assertEqual(len(r['view']['items']),168)
        self.assertEqual(r['current']['expected']['active'],121)
        self.assertEqual(len(r['queue']['candidates']),121)
        self.assertEqual(len(r['plan']['items']),121)
        self.assertFalse(r['queue']['approved'])
        self.assertFalse(r['queue']['download_enabled'])
        self.assertFalse(r['plan']['download_enabled'])
        self.assertEqual(r['current']['capacity_audit']['latest_revision_scope_coverage'],118)
        self.assertEqual(r['current']['capacity_audit']['v24_new_assets_unmeasured_count'],3)
        self.assertEqual(r['view']['budget']['new_active_reservation_cap_bytes'],102_000_000_000)
        self.assertIsNone(r['view']['budget']['final_selected_total_bytes'])
    def test_unauthorized_shortcuts_fail_closed(self):
        for field,v in (('download_approved',True),('fully_pinned_revision_sha','a'*40),
                        ('selected_file_bytes',0)):
            args=list(fixture());args[3]['additions'][0][field]=v
            with self.subTest(field=field),self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][1]['repo_id']='FIXTURE/M1'
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][0]['restriction_assessment']['probability']=0.5
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['max_new_selection_budget_bytes']=100
        with self.assertRaises(ValueError):prepare(*args)
    def test_previous_regulatory_ram_rule_preserved(self):
        args=list(fixture());args[3]['additions'][0]['parameter_gate']['total_parameters']=321_000_000_000
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[0]['revision_id']='v22-20261106'
        with self.assertRaises(ValueError):prepare(*args)
if __name__=='__main__':unittest.main()
